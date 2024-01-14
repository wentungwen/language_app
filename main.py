from flask import Flask, jsonify, request, session
from flask_cors import CORS
from google.cloud import translate_v2 as translate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from openai import OpenAI
import secrets
import jwt
from datetime import datetime
import requests, os, json
from datetime import datetime


## GPT & google translate
GPT_APIKEY = os.environ.get("GPT_APIKEY")
GPT_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

## app and database config
app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://tmdadm:tmd+123@127.0.0.1:5432/tmd67"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(32)
db = SQLAlchemy(app)

# openai object
ai_client = OpenAI(api_key=GPT_APIKEY)


class User(db.Model):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(100))
    conversations = relationship("Conversation", back_populates="user")

    def check_password(self, password):
        return self.password == password

    def set_password(self, new_password):
        self.password = new_password
        return True


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


# methods


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


def add_content_to_conversation(conversation_id, content, sender):
    """Testing: Adds a content to a conversation table"""
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return False
    new_content = Content(content=content, sender=sender, conversation=conversation)
    db.session.add(new_content)
    db.session.commit()
    return True


# def check_password(email, password):
#     user = User.query.filter_by(email=email).first()
#     if user and user.password == password:
#         return user
#     else:
#         return False


# routes
@app.route("/login", methods=["POST"])
def login():
    posted_data = request.get_json()
    email = posted_data["email"]
    password = posted_data["password"]
    try:
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            token = generate_token(user.user_id)
            return (
                jsonify(
                    {
                        "user_id": user.user_id,
                        "email": user.email,
                        "username": user.username,
                        "token": token,
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "Incorrect email or password"}), 401
    except:
        return jsonify({"message": "Not found"}), 404


@app.route("/signup", methods=["POST"])
def signup():
    posted_data = request.get_json()
    token = secrets.token_hex(16)
    username = posted_data["username"]
    email = posted_data["email"]
    password = posted_data["password"]
    user = User(
        username=username,
        email=email,
        password=password,
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(
        {
            "message": "User created successfully",
            "token": token,
            "username": user.username,
            "email": email,
        }
    )


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
    # TODO: check if no conversation_id then saved as a new one
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Missing token"}), 401
    user_id = decode_token(token)
    saved_conversations = request.get_json()["data"]

    if "conversation_id" in saved_conversations:
        conversation_id = saved_conversations["conversation_id"]
        original_conversation = Conversation.query.filter_by(
            conversation_id=conversation_id
        ).first()
        if original_conversation:
            original_conversation.contents = []
            for conversation in saved_conversations["conversations"]:
                content = conversation["content"]
                sender = conversation["sender"]
                original_conversation.contents.append(
                    Content(content=content, sender=sender)
                )
            db.session.commit()
            return jsonify({"message": "Saved successfully"}), 200
        else:
            return jsonify({"message": "Conversation not found"}), 404

    else:
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


@app.route("/update-user-data", methods=["GET", "POST"])
def update_user_data():
    if request.method == "POST":
        posted_data = request.get_json()
        print(type(posted_data))
        user_id = posted_data["user_id"]
        old_data = posted_data["origin_data"]
        new_data = posted_data["new_data"]
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"message": "User not found"}), 404

        # if password is empty, then change the username and email
        if new_data["password"] == "" or old_data["password"] == "":
            user.username = new_data.get("username", user.username)
            user.email = new_data.get("email", user.email)

        # else verify the user is exist, and change the password
        else:
            if user.check_password(old_data.get("password")):
                user.set_password(new_data.get("password"))
            else:
                return jsonify({"message": "Incorrect password"}), 400

        # Commit the changes to the database
        db.session.commit()

        return (
            jsonify(
                message="User data changed successfully",
                username=user.username,
                email=user.email,
                user_id=user.user_id,
            ),
            200,
        )
    else:
        return jsonify({"message": "Conversation not found"}), 404


@app.route("/translate", methods=["GET", "POST"])
def translate_to_en():
    if request.method == "POST":
        posted_data = request.get_json()
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
    print("token:", token)
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


def generate_gpt_conversation(lan_code, topic, sentence_num, level, note):
    
    prompt = f"Language code: {lan_code}. Difficulty levels: {level}. Total sentences: {str(sentence_num)}. Topics: {topic}. Note: {note}."
    
    example = "[{\"sender\": \"A\", \"content\": \"...\"}, {\"sender\": \"B\", \"content\": \"...\"}]"

    response = ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a multi-language generator which generates creative open conversations of A and B senders. The response format must follow valid and complete JSON format, which enclosed in double quotes, for example: {example}",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=1,
        max_tokens=2000,
        top_p=1,
    )
    completion = response.choices[0].message.content
    print(completion)
    conversations_array = json.loads(completion)
    print(conversations_array)
    try:
        return conversations_array
    except Exception as e:
        print(e)
        return e


@app.route("/generate-conversation", methods=["POST"])
def generate_conversation():
    posted_data = request.get_json()
    lan_code = posted_data["lan_code"]
    topic = posted_data["topic"]
    sentence_num = posted_data["sentence_num"]
    level = posted_data["level"]
    note = None
    try:
        conversations = generate_gpt_conversation(
            lan_code, topic, sentence_num, level, note
        )
        return jsonify(conversations), 200
    except Exception as e:
        print(e)
        return jsonify({"response": "Request failed"}), 400


@app.route("/generate-five", methods=["POST"])
def generate_five_conversation():
    posted_data = request.get_json()
    lan_code = posted_data["lan_code"]
    topic = posted_data["topic"]
    conversations = posted_data["conversations"]
    sentence_num = 5
    level = "similar"

    content_string = " ".join(
        [conversation["content"] for conversation in conversations]
    )

    note = f"previous conversation is about {content_string}."
    try:
        conversations = generate_gpt_conversation(
            lan_code, topic, sentence_num, level, note
        )
        return jsonify(conversations), 200
    except Exception as e:
        print(e)
        return jsonify({"response": "Request failed"}), 400


@app.route("/add_content")
def add_content_route():
    with app.app_context():
        # new_user = User(username="B", password="B", email="B")
        # db.session.add(new_user)
        # db.session.commit()
        # new_conversation = Conversation(
        #     date
        # )
        add_content_to_conversation(1, "How are you?", "A")
        add_content_to_conversation(1, "How are you?", "A")
    return "Content added successfully"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # set the port for heroku
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=port)

    app.run(debug=True)
