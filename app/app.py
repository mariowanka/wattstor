import logging
import sys

from flask import Flask

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


app = Flask(__name__)


if __name__ == "__main__":
    app.run()
