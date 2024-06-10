"""
flask app
"""

from flask import Flask, render_template, request

app = Flask(__name__)

# display page at url "/"
@app.route("/")
def home():
    return render_template("app.html")