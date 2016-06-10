from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Tag, Comment, Study
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm

content = Blueprint('content', __name__, template_folder='templates/content')

class AboutUs(MethodView):
	def get(self):
		return render_template("content/aboutus.html")
content.add_url_rule('/aboutus', view_func=AboutUs.as_view('aboutus'))


class ContactUs(MethodView):
	def get(self):
		return render_template("content/contactus.html")
content.add_url_rule('/contactus', view_func=ContactUs.as_view('contactus'))
