from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask_jsglue import JSGlue
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