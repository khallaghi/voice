from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Tag, Comment, Study
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
		prof.attr1_count+=1
		prof.attr1 = self.average_rate(prof.attr1, prof.attr1_count, data['helpfulness'])
		prof.attr2_count += 1
		prof.attr2 = self.average_rate(prof.attr2, prof.attr2_count, data['easiness'])
		prof.attr3_count += 1
		prof.attr3 = self.average_rate(prof.attr3, prof.attr3_count, data['clarity'])
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
	def update_course(self, study, data):
		study.helpfulness = self.average_rate(study.helpfulness, 
												study.helpfulness_count,
												data['helpfulness'])
		study.helpfulness_count += 1
		study.easiness = self.average_rate(study.easiness,
											study.easiness_count,
											data['easiness'])
		study.easiness_count += 1
		study.clarity = self.average_rate(study.clarity,
											study.clarity_count,
											data['clarity'])
		study.clarity_count += 1 

	def find_and_update_course(self, prof, data):
		for study in prof.studies:
			if study.name == data['selectedCourse']:
				self.update_course(study, data)
				prof.save()
				return True
		return False

	def create_course(self, prof, data):
		study = Study()
		study.name = data['courseName']

		self.update_course(study, data)
		prof.studies.append(study)
		prof.save()
		return True

	def apply_course(self, prof, data):
		if data['findCourse']:
			if 'selectedCourse' in data.keys() and data['selectedCourse'] != None:
				if self.find_and_update_course(prof, data):
					return True
		else:
			if 'courseName' in data.keys() and data['courseName'] != None:
				if self.create_course(prof, data):
					return True
		return False

	def post(self):
		data = json.loads(request.data)
		print data
		prof = Professor.objects(id=data['id']).first()
		if not self.validate(prof, data):
			return "invalid data -- 404"
		if not self.apply_course(prof, data):
			return "invalid course -- 404"
		self.apply_rate(prof, data)
		self.apply_tags(prof, data)
		self.apply_comment(prof, data)
		return "salam"

rate.add_url_rule('/rate', view_func=ProfessorRate.as_view('professorRate'))
