from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Tag
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask_restful import reqparse
import json

rate = Blueprint('rate', __name__, template_folder='templates/rate')
parser = reqparse.RequestParser()
class ProfessorRate(MethodView):
	def post(self):
		data = json.loads(request.data)
		print data
		if(data['id']==None):
			return "there is no professor"
		prof = Professor.objects(id=data['id']).first()
		if prof == None:
			return "there is no Professor"
		if data['helpfulness']==0 or data['easiness']==0 or data['clarity']==0:
			return "invalid data"
		apply_rate(prof, data['helpfulness'], data['easiness'], data['clarity'])
		# prof.attr1 = data['helpfulness']
		# prof.attr2 = data['easiness']
		# prof.attr3 = data['clarity']
		for tag in data['tags']:
			in_tags = False
			for prof_tag in prof.personal_tags:
				if(prof_tag.name == tag):
					prof_tag.count +=1
					in_tags = True
			if not in_tags:
				temp_tag = Tag(name=tag, count=1)
				prof.personal_tags.append(temp_tag)
		prof.save()



		return "salam"
rate.add_url_rule('/rate', view_func=ProfessorRate.as_view('professorRate'))
