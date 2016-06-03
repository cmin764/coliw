import os

from flask import Flask

import config
from coliw.caller import call


coliw = Flask(__name__)

conf_name = os.getenv("FLASK_CONFIG") or "default"
conf_cls = config.config[conf_name]
coliw.config.from_object(conf_cls)
conf_cls.init_app(coliw)


import views
