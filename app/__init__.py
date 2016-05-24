from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_jsglue import JSGlue
from werkzeug import secure_filename
import os


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
jsglue = JSGlue(app)
jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>',
))
app.jinja_options = jinja_options

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGODB_SETTINGS"] = {'DB': "rate"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    from app.start import home
    app.register_blueprint(home)
    from app.profile import profile
    app.register_blueprint(profile)
    from app.rate import rate
    app.register_blueprint(rate)
    # app.register_blueprint(admin)


register_blueprints(app)
if __name__ == '__main__':
    app.run()