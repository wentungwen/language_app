from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Set a secret key for session management (you should use a strong, random secret key in production)
app.secret_key = "your_secret_key"

# PostgreSQL configuration
db_config = {
    "dbname": "your_database_name",
    "user": "your_database_user",
    "password": "your_database_password",
    "host": "your_database_host",
    "port": "your_database_port",
}

# Routes
@app.route("/")
def index():
    if "user_id" in session:
        return "Hello, " + session["username"] + " (user ID: " + str(session["user_id"]) + ")!<br><a href='/logout'>Logout</a>"
    else:
        return "Welcome! Please <a href='/login'>login</a>."

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user exists
        query = sql.SQL("SELECT user_id, username FROM users WHERE username = %s AND password = %s")
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # Store user data in the session
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("index"))
        else:
            return "Login failed. <a href='/login'>Try again</a>."

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
