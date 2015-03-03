# coding=utf-8

from app.server import app as app_server
from flask.ext.runner import Runner

import app.views
import app.viewsapi

runner = Runner(app_server)

if __name__ == "__main__":
    runner.run()
