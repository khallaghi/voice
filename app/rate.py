from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q

rate = Blueprint('profile', __name__, template_folder='templates/rate')

class ProfRate(MethodView):
	form = 
