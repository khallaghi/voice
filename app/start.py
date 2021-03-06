from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
home = Blueprint('home', __name__, template_folder='templates/home')

class HomePage(MethodView):
	def get(self):
		return redirect(url_for('search.search'))
home.add_url_rule('/home', view_func=HomePage.as_view('home'))


class ManifestPage(MethodView):
	def get(self):
		return render_template("home/manifest.html")
home.add_url_rule("/manifest", view_func=ManifestPage.as_view('manifest'))