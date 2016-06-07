import json

from flask import (
    request, render_template, session,
    abort, jsonify
)

from coliw import coliw, call
from coliw.utils import ENCODING


@coliw.route("/")
def index():
    return render_template("index.html")


@coliw.route("/command", methods=["POST"])
def command():
    cmd = request.form.get("cmd")
    cmd = json.loads(cmd).encode(ENCODING)
    if not cmd:
        abort(400)
    code, resp = call(cmd)
    return jsonify(code=code, response=resp)


@coliw.route("/history", methods=["GET", "POST"])
def history():
    if request.method == "GET":
        data = session.get("data", None)
        if not data:
            return jsonify(status=False)
        return jsonify(status=True, **data)

    elif request.method == "POST":
        sh_idx = request.form.get("h_idx")
        sh_list = request.form.get("h_list")
        sh_text = request.form.get("h_text")
        data = {
            "h_idx": sh_idx,
            "h_list": sh_list,
            "h_text": sh_text
        }
        session["data"] = data
        return jsonify(status=True)

    abort(400)
