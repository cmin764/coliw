from flask import Flask


coliw = Flask(__name__)
coliw.config.from_object("config")

import views
