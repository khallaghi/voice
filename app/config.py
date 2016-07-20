from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask import jsonify
from app.auth import requires_auth

config = Blueprint('config', __name__)
class UpdateAllProf(MethodView):
	def get(self):
		for prof in Professor.objects():
			if prof.published == False:
				continue
			else:
				prof.published = True
				prof.save()
		return "DONE"
config.add_url_rule('/config/update-pub', view_func=UpdateAllProf.as_view('update_published'))
