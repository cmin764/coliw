from flask import redirect, url_for, request, render_template, session

from coliw import coliw


@coliw.route("/")
def index():
    return render_template("index.html")
