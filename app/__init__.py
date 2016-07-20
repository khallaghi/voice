from flask import Flask, request, redirect, url_for
from flask.ext.mongoengine import MongoEngine
from flask_jsglue import JSGlue
from werkzeug import secure_filename
import os


UPLOAD_FOLDER = '../'
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
	# from app.views import category
	# from app.admin import admin
	# app.register_blueprint(category)
	
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
	
	from app.edit import edit
	app.register_blueprint(edit)

	from app.content import content
	app.register_blueprint(content)

	from app.report import report
	app.register_blueprint(report)

	from app.admin import admin
	app.register_blueprint(admin)

	from app.category.view import category
	app.register_blueprint(category)

	from app.user.view import user
	app.register_blueprint(user)

	from app.config import config
	app.register_blueprint(config)

register_blueprints(app)
if __name__ == '__main__':
	app.run()


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/akbar', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('uploaded_file',
									filename=filename))
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form action="" method=post enctype=multipart/form-data>
	  <p><input type=file name=file>
		 <input type=submit value=Upload>
	</form>
	%% filename %%
	<img src="%% filename %%">
	'''