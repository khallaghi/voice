from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "rate"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)
def register_blueprints(app):
    # Prevents circular imports
    from app.views import category
    # from app.admin import admin
    app.register_blueprint(category)
    from app.add import add
    app.register_blueprint(add)
    from app.search import search
    app.register_blueprint(search)
    # app.register_blueprint(admin)


register_blueprints(app)
if __name__ == '__main__':
    app.run()