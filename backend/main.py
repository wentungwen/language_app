from flask import Flask, jsonify, request, session
from flask_cors import CORS
import googletrans
from google.cloud import translate_v2 as translate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
import secrets
import jwt
from datetime import datetime
import requests, os
from datetime import datetime

# import psycopg2


## GPT & google translate
GPT_APIKEY = os.environ.get("GPT_APIKEY")
GPT_API_ENDPOINT = "https://api.openai.com/v1/completions"
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

## app and database config
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///language_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(32)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(100))
    conversations = relationship("Conversation", back_populates="user")


class Conversation(db.Model):
    __tablename__ = "conversations"
    conversation_id = Column(Integer, primary_key=True)
    date = Column(String(100))
    topic = Column(String(100))
    lan_code = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    user = relationship("User", back_populates="conversations")
    contents = relationship("Content", back_populates="conversation")


class Content(db.Model):
    __tablename__ = "contents"
    content_id = Column(Integer, primary_key=True)
    content = Column(String(100), nullable=False)
    sender = Column(String(100), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.conversation_id"))
    conversation = relationship("Conversation", back_populates="contents")


# mock data
mock_conversations = [
    {
        "date": "2019-05-04",
        "topic": "te laat",
        "lan_code": "nl",
        "conversations": [
            {
                "sender": "A",
                "content": "(backend)Ik heb de treinkaarten. Twee retourtjes naar Den Haag.",
            },
            {
                "sender": "B",
                "content": "Volgens de man achter het loket, vertrekt de trein over een kwartier van spoor vijf.",
            },
            {
                "sender": "A",
                "content": "Goed zo. Ik ga even naar de wc. Weet jij waar die is?",
            },
            {
                "sender": "B",
                "content": "Ja. Daar bij de ingang. Ik blijf hier bij de koffers.",
            },
        ],
    },
    {
        "date": "2019-05-05",
        "topic": "de lein tiran ",
        "lan_code": "nl",
        "conversations": [
            {"sender": "A", "content": "(backend)Mamma, waar is pappa?"},
            {
                "sender": "B",
                "content": "Op kantoor, natuurlijk. Ga maar even naar buiten.",
            },
            {"sender": "A", "content": "Speel met poesje in de tuin. "},
            {
                "sender": "B",
                "content": "Maar waarom niet op straat? Met de jongens.",
            },
        ],
    },
]


@app.route("/login", methods=["POST"])
def login():
    posted_data = request.get_json()
    email = posted_data["email"]
    password = posted_data["password"]
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        username = user.username
        user_id = user.user_id
        token = generate_token(user.user_id)
        return jsonify({"user_id": user_id, "username": username, "token": token}), 200
    else:
        return jsonify({"status": "Not found"}), 404


@app.route("/signup", methods=["POST"])
def signup():
    posted_data = request.get_json()
    token = secrets.token_hex(16)
    user = User(
        username=posted_data["username"],
        email=posted_data["email"],
        password=posted_data["password"],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "token": token})


@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully"})


@app.route("/delete-conversation", methods=["DELETE"])
def delete_conversation():
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Missing token"}), 401

        data = request.get_json()
        conversation_id = data.get("conversation_id")
        if not conversation_id:
            return jsonify({"message": "Missing conversation."}), 400
        deleted_conversation = Conversation.query.filter_by(
            conversation_id=conversation_id
        ).first()
        db.session.delete(deleted_conversation)
        db.session.commit()
        return jsonify({"message": "Deleted successfully"}), 200
    except:
        return jsonify({"message": "Something went wrong"}), 500


@app.route("/save", methods=["POST"])
def save():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Missing token"}), 401
    user_id = decode_token(token)
    saved_conversations = request.get_json()["data"]
    new_conversation = Conversation(
        date=str(datetime.now()),
        topic=saved_conversations["topic"],
        lan_code=saved_conversations["lan_code"],
        user_id=user_id,
    )
    for conversation in saved_conversations["conversations"]:
        content = conversation["content"]
        sender = conversation["sender"]
        new_conversation.contents.append(Content(content=content, sender=sender))
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({"message": "Saved successfully"}), 200


@app.route("/translate", methods=["GET", "POST"])
def translate_to_en():
    if request.method == "POST":
        posted_data = request.get_json()
        print("posted_data:.....", posted_data)
        conversations = posted_data["conversations"]
        lan_code = posted_data["lan_code"]
        translated_conversations = conversations
        for conversation in translated_conversations:
            content = conversation.get("content")
            translated_text = translate_text(
                text=content, source_language=lan_code, target_language="en"
            )
            conversation["content"] = translated_text
        return jsonify({"conversations": translated_conversations})


@app.route("/get-conversations", methods=["GET"])
def get_conversations():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Missing token"}), 401
    else:
        user_id = decode_token(token)
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        conversations = Conversation.query.filter_by(user=user).all()
        if conversations:
            data = []
            for conversation in conversations:
                contents = Content.query.filter_by(conversation=conversation).all()
                conversation_content = [
                    {"sender": content.sender, "content": content.content}
                    for content in contents
                ]
                conversation_data = {
                    "conversation_id": conversation.conversation_id,
                    "date": conversation.date,
                    "topic": conversation.topic,
                    "lan_code": conversation.lan_code,
                    "conversations": conversation_content,
                }
                data.append(conversation_data)
            print("data:.....", data)
            return jsonify({"data": data}), 200
        else:
            return jsonify({"data": []})


@app.route("/get-all-conversations", methods=["GET"])
def get_all_conversations():
    conversations = Conversation.query.all()
    if conversations:
        data = []
        for conversation in conversations:
            contents = Content.query.filter_by(conversation=conversation).all()
            conversation_content = [
                {"sender": content.sender, "content": content.content}
                for content in contents
            ]

            datatime_obg = datetime.strptime(conversation.date, "%Y-%m-%d %H:%M:%S.%f")
            conversation_data = {
                "conversation_id": conversation.conversation_id,
                "date": datetime.strftime(datatime_obg, "%d-%m-%Y"),
                "topic": conversation.topic,
                "lan_code": conversation.lan_code,
                "conversations": conversation_content,
            }
            data.append(conversation_data)
        return jsonify({"data": data}), 200
    else:
        return jsonify({"data": []}), 200


@app.route("/generate-conversation", methods=["POST"])
def generate_conversation():
    posted_data = request.get_json()
    lan_code = posted_data["lan_code"]
    topic = posted_data["topic"]
    sentence_num = posted_data["sentence_num"]
    level = posted_data["level"]
    response = generate_gpt_conversation(lan_code, topic, sentence_num, level)
    return jsonify(response)


def add_content_to_conversation(conversation_id, content, sender):
    """Testing: Adds a content to a conversation table"""
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return False
    new_content = Content(content=content, sender=sender, conversation=conversation)
    db.session.add(new_content)
    db.session.commit()
    return True


@app.route("/add_content")
def add_content_route():
    # with app.app_context():
    #     add_content_to_conversation(2, "How are you?", "A")
    #     add_content_to_conversation(2, "How are you?", "A")
    return "Content added successfully"


def generate_token(user_id):
    payload = {"user_id": user_id}
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        user_id = payload["user_id"]
        print("Decoded payload:", payload)
        return user_id
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.PyJWTError as e:
        print("JWT decoding error:", str(e))
        return None


def translate_text(text, source_language, target_language):
    translate_client = translate.Client.from_service_account_json(
        GOOGLE_APPLICATION_CREDENTIALS
    )
    result = translate_client.translate(
        text, source_language=source_language, target_language=target_language
    )
    return result["translatedText"]


def generate_gpt_conversation(lan_code, topic, sentence_num, level):
    language = googletrans.LANGUAGES[lan_code]
    prompt = f'Generate a  {language} conversation. Difficulty levels: {level}. Total {str(sentence_num)} sentences. About {topic}. In Json format, ex:[{{"sender": "A","content": "...",}},]'
    request_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_APIKEY}",
    }
    request_data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    response = requests.post(
        GPT_API_ENDPOINT, headers=request_headers, json=request_data
    )
    if response.status_code == 200:
        generated_conversations = response.json()["choices"][0]["text"]
        stripped_res = generated_conversations.strip()
        return stripped_res
    else:
        print(
            f"Request failed with status code: {str(response.status_code), response.text}"
        )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
