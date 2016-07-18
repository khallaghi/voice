from __future__ import division
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Post
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask import jsonify


user = Blueprint('user', __name__, template_folder='templates/user')

# class AddProfessor(MethodView):
	
