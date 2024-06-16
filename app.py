"""
flask app/ui
"""

from flask import Flask, render_template, request, redirect, url_for, session
import main

app = Flask(__name__)
app.secret_key = "royharperiscool"

# display home page at url "/"
@app.route("/")
def home():
    return render_template("index.html")


# marvel character page
@app.route("/marvel/", methods=["POST", "GET"])
def marvel():
    # check for form submission
    if request.method == "POST":
        if "marvelform" in request.form:
            # get entered data
            rawinput = request.form["in"]

            # process and store data
            processedinput = main.removeDuplicates(rawinput)
            titles = main.sortMarvel(processedinput)
            joined = main.formatSorted(titles)
            session["output"] = joined

            # redirect as per PRG pattern
            return redirect(url_for("marvel"))
        
    # check for form data on redirect
    if "output" in session:
        output2 = session.pop("output", None)
    else:
        output2 = ""

    return render_template("marvel.html", output=output2)


# DC character page
@app.route("/dc/", methods=["GET", "POST"])
def dc():
        # check for form submission
    if request.method == "POST":
        if "dcform" in request.form:
            # get entered data
            rawinput = request.form["in"]

            # process and store data
            
            processedinput = main.removeDuplicates(rawinput)
            titles = main.sortDc(processedinput)
            joined = main.formatSorted(titles)
            session["output"] = joined

            # redirect as per PRG pattern
            return redirect(url_for("dc"))
        
    # check for form data on redirect
    if "output" in session:
        output2 = session.pop("output", None)
    else:
        output2 = ""

    return render_template("dc.html", output=output2)
