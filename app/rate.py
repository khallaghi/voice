from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Tag, Comment, Study
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask_restful import reqparse
import json
from app.auth import requires_auth
from app import app
LEN_TOO_MUCH = 1

rate = Blueprint('rate', __name__, template_folder='templates/rate')
parser = reqparse.RequestParser()
class ProfessorRate(MethodView):
	def average_rate(self, old_av, count, score):
		print old_av, count, score
		return (old_av*(count-1)+score)/(count)

	def apply_rate(self, prof, data):
		prof.helpfulness_count += 1

		prof.helpfulness = self.average_rate(prof.helpfulness, prof.helpfulness_count, data['helpfulness'])
		prof.easiness_count += 1
		prof.easiness = self.average_rate(prof.easiness, prof.easiness_count, data['easiness'])
		prof.clarity_count += 1
		prof.clarity = self.average_rate(prof.clarity, prof.clarity_count, data['clarity'])
		prof.coolness_count += 1
		prof.coolness = self.average_rate(prof.coolness, prof.coolness_count, data['coolness'])
		prof.save()

	def apply_tags(self, prof, data):
		for tag in data['tags']:
			in_tags = False
			for prof_tag in prof.personal_tags:
				if(prof_tag.name == tag):
					prof_tag.count += 1
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

	def set_id_for_comments(self, prof):
		i = 0
		for cmt in prof.comments:
			cmt.id = i
			i += 1
		prof.save()
	def apply_comment(self, prof, data):
		if not 'comment' in data:
			print "comment is empty"
			return
		if len(data['comment']) > 1000:
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
		cmt.study = prof.studies[-1]

		print "FIRST"
		print cmt.personal_tags
		self.append_tags(cmt, data)
		print "SECOND"
		print cmt.personal_tags
		if len(prof.comments)>= 1:
			if prof.comments[-1].id == -1 or prof.comments[-1] == None:
				print "OVERRIDE ID OF COMMENT"
				self.set_id_for_comments(prof)
			cmt.id = prof.comments[-1].id + 1
		else:
			cmt.id = 0
		print "CMT ID"
		print cmt.id
		prof.comments.append(cmt)
		prof.save()

	# def apply_class(self, prof, data):
	# 	if data['study'] != None:
	def update_course(self, study, data):
		study.helpfulness_count += 1
		study.helpfulness = self.average_rate(study.helpfulness, 
												study.helpfulness_count,
												data['helpfulness'])
		study.easiness_count += 1
		study.easiness = self.average_rate(study.easiness,
											study.easiness_count,
											data['easiness'])
		study.clarity_count += 1
		study.clarity = self.average_rate(study.clarity,
											study.clarity_count,
											data['clarity'])
		 

	def find_and_update_course(self, prof, data):
		for study in prof.studies:
			if study.name == data['selectedCourse']:
				app.logger.warning("STUDY NAME")
				app.logger.warning(study.name.encode('utf-8'))
				app.logger.warning(data['selectedCourse'].encode('utf-8'))
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
		print "before apply_Rate"
		self.apply_rate(prof, data)
		self.apply_tags(prof, data)
		self.apply_comment(prof, data)
		return "salam"

rate.add_url_rule('/rate', view_func=ProfessorRate.as_view('professorRate'))

def find_cmt(prof, id):
	for cmt in prof.comments:
		print "ID"
		print id
		print cmt.id
		if str(cmt.id) == id:
			return cmt

class ReportComment(MethodView):
	def get(self, prof_id, cmt_id):
		prof = Professor.objects(id = prof_id).first()
		if prof:
			print "BEFORE find_cmt"
			cmt = find_cmt(prof, cmt_id)
			print "ATER CMT"
			print cmt
			if cmt:
				cmt.reported = 1
				prof.reported_comments += 1
				print "BEFORE SAVE"
				prof.save()
				print "IN THE REPORT COMMENT"
				return "True"
		return "False"
rate.add_url_rule('/report/<prof_id>/<cmt_id>', 
					view_func=ReportComment.as_view('reportComment'))

class ShowReportedComments(MethodView):
	decorators = [requires_auth]
	def get_prof_irell_comments(self, prof):
		for cmt in prof.comments:
			if cmt.reported:
				yield {
					"body":cmt.body,
					"id":cmt.id
				}
	def get_reported_comments(self):
		profs = Professor.objects(reported_comments__gt = 0)
		for prof in profs:
			cmts = self.get_prof_irell_comments(prof)
			yield {
				"prof":prof,
				"comments":cmts
			}
	def get(self):
		return render_template('report/reported.html',
								records=self.get_reported_comments())
rate.add_url_rule('/report/list', 
					view_func=ShowReportedComments.as_view('showReportedComments'))

class DeleteComment(MethodView):
	decorators = [requires_auth]
	def get(self, prof_id, cmt_id):
		print "POOOOOOOST"
		print id
		print cmt_id
		prof = Professor.objects(id=prof_id).first()
		if prof:
			cmt = find_cmt(prof, cmt_id)
			if cmt:
				prof.comments.remove(cmt)
				prof.reported_comments -= 1
				prof.save()
		return redirect(url_for('rate.showReportedComments'));
rate.add_url_rule('/report/delete/<prof_id>/<cmt_id>', 
					view_func=DeleteComment.as_view('delete_comment'))

class RestoreComment(MethodView):
	decorators = [requires_auth]
	def get(slef, prof_id, cmt_id):
		prof = Professor.objects(id=prof_id).first()
		if prof:
			cmt = find_cmt(prof, cmt_id)
			if cmt:
				cmt.reported = 0
				prof.reported_comments -= 1
				prof.save()
		return redirect(url_for('rate.showReportedComments'))
rate.add_url_rule('/report/restore/<prof_id>/<cmt_id>', 
					view_func=RestoreComment.as_view('restore_comment'))

