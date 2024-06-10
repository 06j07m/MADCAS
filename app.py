"""
flask app/ui
"""

from flask import Flask, render_template, request

app = Flask(__name__)

# display home page at url "/"
@app.route("/")
def home():
    return render_template("index.html")


# marvel character page
@app.route("/marvel/")
def marvel():
    return render_template("marvel.html")


# DC character page
@app.route("/dc/")
def dc():
    return render_template("dc.html")