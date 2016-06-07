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
