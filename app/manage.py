import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from app import app

app.debug = True
if __name__ == "__main__":
    app.run()
