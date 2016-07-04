from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Tag, Comment, Study, Voter, Post
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask_restful import reqparse
import json
from app.auth import requires_auth
from app import app
import requests
from flask import jsonify
import datetime

admin = Blueprint('admin', __name__, template_folder='templates/admin')

class AdminPage(MethodView):
	decorators = [requires_auth]
	def get(self):
		return render_template('/admin/admin-page.html')
admin.add_url_rule('/admin', 
	view_func = AdminPage.as_view("AdminPage"))