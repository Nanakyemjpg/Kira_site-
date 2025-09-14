from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "kira_secret"  # change this in production

# simple fake database (replace with real later)
users = {"demo": "password"}  
uploads = []  

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid login"
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join("static/uploads", file.filename)
        file.save(filepath)
        uploads.append(file.filename)
    return render_template("dashboard.html", uploads=uploads)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_message = request.form["message"]
        # chatbot reply (super basic for now)
        reply = f"Kira says: I love when you say '{user_message}' 😉"
        return render_template("chat.html", reply=reply)
    return render_template("chat.html", reply=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
