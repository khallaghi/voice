from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Tag, Comment
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask_restful import reqparse
import json
LEN_TOO_MUCH = 1

rate = Blueprint('rate', __name__, template_folder='templates/rate')
parser = reqparse.RequestParser()
class ProfessorRate(MethodView):
	def average_rate(self, old_av, count, score):
		return ((old_av*count)+score)/(count+1)

	def apply_rate(self, prof, data):
		prof.attr1 = self.average_rate(prof.attr1, prof.attr1_count, data['helpfulness'])
		prof.attr1_count+=1
		prof.attr2 = self.average_rate(prof.attr2, prof.attr2_count, data['easiness'])
		prof.attr2_count += 1
		prof.attr3 = self.average_rate(prof.attr3, prof.attr3_count, data['clarity'])
		prof.attr3_count += 1
		prof.save()

	def apply_tags(self, prof, data):
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

	def validate(self, prof, data):
		if prof == None:
			print "THERE IS NO PROFESSOR"
			return False
		if data['helpfulness']==0 or data['easiness']==0 or data['clarity']==0:
			print "THE FIELDS ARE NOT TRUE"
			return False
		return True

	def append_tags(self, cmt, data):
		for tag in data['tags']:
			tmp_tag = Tag(name = tag)
			cmt.personal_tags.append(tmp_tag)

	def apply_comment(self, prof, data):
		if len(data['comment']) > 300:
			return LEN_TOO_MUCH
		# validate comment for informal comments
		cmt = Comment()
		cmt.body = data['comment']
		cmt.clarity = data['clarity']
		cmt.helpfulness = data['helpfulness']
		cmt.easiness = data['easiness']
		cmt.coolness = data['coolness']
		cmt.use_textbook = data['useTextbook']
		cmt.attendance = data['attendance']

		print "FIRST"
		print cmt.personal_tags
		self.append_tags(cmt, data)
		print "SECOND"
		print cmt.personal_tags
		prof.comments.append(cmt)
		prof.save()

	# def apply_class(self, prof, data):
	# 	if data['study'] != None:

	def post(self):
		data = json.loads(request.data)
		print data
		prof = Professor.objects(id=data['id']).first()
		if not self.validate(prof, data):
			return "invalid data -- 404"
		self.apply_rate(prof, data)
		self.apply_tags(prof, data)
		# self.apply_class(prof, data)

		self.apply_comment(prof, data)
		return "salam"
rate.add_url_rule('/rate', view_func=ProfessorRate.as_view('professorRate'))
