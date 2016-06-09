from flask import Blueprint, request, redirect, render_template, url_for,\
send_from_directory
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import FacultyForm, ProfessorForm, \
									EditProfessorForm
from app.auth import requires_auth
# from PIL import Image
from werkzeug import secure_filename
from app import app
import os
import tempfile
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
# import file
edit = Blueprint('edit', __name__, template_folder='templates/edit')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def save_image(request, prof):
		file = request.files['pic']
		print "this is file"
		print file
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			print filename
			print "before saving file"
			filename = str(prof.id) + '.' + filename.split('.')[-1]
			print filename
			app.config['UPLOAD_FOLDER'] = "/root/rate/app/static/img/uploaded_images/"
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename ))
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			print "filepath is : "
			print filepath
			# image = Image.open(filename)
			# if prof.pic:
				# prof.pic.delete()
			# prof.pic.put(filepath)
			prof.image_name = filename


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class ProfList(MethodView):
	# decorators = [requires_auth]
	def get(self):
		profs = Professor.objects.order_by("faculty")
		# print "count of professors: " + str(profs.count()) 
		return render_template('edit/professor-list.html', profs=profs)

class EditProf(MethodView):
	# decorators = [requires_auth]
	def init_form(self, form, prof):
		form.name.data = prof.name
		form.website.data = prof.website
		form.email.data = prof.email

	def get_context(self, id):
		form = EditProfessorForm()
		prof = Professor.objects(id=id).first()
		self.init_form(form, prof)
		return {
			'prof': prof,
			'form': form
		}

	def get(self, id):
		context = self.get_context(id)
		if not context['prof']:
			return render_template('error/404.html')
		return render_template('edit/editprof.html', **context)
	
	def post(self, id):
		# context = self.get_context(id)
		# prof = context.get('prof')
		form = EditProfessorForm(request.form)
		prof = Professor.objects(id=id).first()
		if not prof:
			return render_template('error/404.html')
		# if form.validate():
		prof.name = form.name.data
		prof.website = form.website.data
		prof.email = form.email.data
		save_image(request, prof)
		prof.save()

		return redirect(url_for('edit.professor_list'))

class DeleteProf(MethodView):
	# decorators = [requires_auth]
	def get(self,id):
		prof = Professor.objects(id=id).first()
		if prof:
			prof.delete()
		return redirect(url_for("edit.professor_list"))

edit.add_url_rule('/prof/delete/<id>', view_func=DeleteProf.as_view('delete_professor'))
edit.add_url_rule('/prof/edit/<id>', view_func=EditProf.as_view('edit_professor'))
edit.add_url_rule('/prof/list', view_func=ProfList.as_view('professor_list'))
