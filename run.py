import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__)

"""
'm going to leave "randomstring123" in there as the second argument because this becomes
the default value if Flask can't find a variable called SECRET.
"""
app.secret_key = os.getenv("SECRET","randomstring123")
messages = []


def add_message(username, message):
    """Add messages to the `messages` list"""
    now = datetime.now().strftime("%H:%M:%S")
    messages.append({"timestamp": now, "from": username, "message": message})


@app.route("/", methods=["GET", "POST"])
def index():
    """Main page with instructions"""
    if request.method == "POST":
        session["username"] = request.form["username"]

    """ This is so that if we change the URL, then we don't have to worry about what redirects
        may be calling it directly. I do want to change my URL, too. I don't like the fact that
        the chat page is here at /username. If I wanted to grow this project and have an about
        page or a contact page, then my URL naming would be very messy.
    """

    if "username" in session:
        return redirect(url_for("user", username=session["username"]))

    return render_template("index.html")


@app.route("/chat/<username>", methods=["GET", "POST"])
def user(username):
    """Add and display chat messages"""
    if request.method == "POST":
        username = session["username"]
        message = request.form["message"]
        add_message(username, message)
        return redirect(url_for("user", username=session["username"]))

    return render_template("chat.html", username=username,
                           chat_messages=messages)


app.run(host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")), debug=False)