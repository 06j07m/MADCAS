"""
flask app/ui
"""

from flask import Flask, render_template, request, redirect, url_for, session
import datetime
import main, helper, fileio

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

            # process data
            splitt = helper.getLines(rawinput)
            processedinput = helper.removeDuplicates(splitt)
            titles = main.sortDc(processedinput)
            joined = helper.formatSorted(titles)

            # make cache file name
            datename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            fname = "cache/" + datename

            # store in a file
            fileio.saveTxt(joined, fname)

            # pass file name to cookie(??)
            session["output"] = fname
            
            # redirect as per PRG pattern
            return redirect(url_for("marvel"))
        
    # check for form data on redirect
    if "output" in session:
        fname2 = session.pop("output", None)
        output2 = fileio.openTxt(fname2)
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

            # process data
            splitt = helper.getLines(rawinput)
            processedinput = helper.removeDuplicates(splitt)
            titles = main.sortDc(processedinput)
            joined = helper.formatSorted(titles)

            # make cache file name
            datename = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            fname = "cache/" + datename

            # store in a file
            fileio.saveTxt(joined, fname)

            # pass file name to cookie(??)
            session["output"] = fname

            # redirect as per PRG pattern
            return redirect(url_for("dc"))
        
    # check for form data on redirect
    if "output" in session:
        fname2 = session.pop("output", None)
        output2 = fileio.openTxt(fname2)
    else:
        output2 = ""

    return render_template("dc.html", output=output2)


if __name__ == "__main__":
    app.run(debug=True)