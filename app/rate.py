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
from app.utils import replace_ye

LEN_TOO_MUCH = 1
TEST = True
MAX_LEN = 20

rate = Blueprint('rate', __name__, template_folder='templates/rate')
parser = reqparse.RequestParser()

def verify_user(ip, response):
	RECAPTCHA_SECRET_KEY = '6LeGZh4TAAAAAEf9XWVeDVXgXVKv6iBOw15lkWfW'
	url = "https://www.google.com/recaptcha/api/siteverify"
	obj = {
		'secret':RECAPTCHA_SECRET_KEY,
		'response':response,
		'remoteip':ip.split('.')[-1]
	}
	r = requests.post(url,obj)
	data = r.json()
	return data['success']
		

def check_delta(now, timestamp):
	TIME_DELTA = datetime.timedelta(hours = 2)
	return now - timestamp < TIME_DELTA

def check_multiple_vote(prof, ip):
	if TEST:
		return False
	now = datetime.datetime.now()
	for voter in prof.recent_voters:
		if voter.ip == ip:
			if check_delta(now, voter.timestamp):
				voter.timestamp = now
				prof.save()
				return True
			voter.timestamp = now
			prof.save()
			return False
	if len(prof.recent_voters) > MAX_LEN and len(prof.recent_voters) != 0:
		prof.recent_voters.pop(0)
	prof.recent_voters.append(Voter(
								ip = ip,
								timestamp = now 
								))
	prof.save()
	return False

class ProfessorRate(MethodView):
	def average_rate(self, old_av, count, score):
		print old_av, count, score
		return (old_av*(count-1)+score)/(count)

	def apply_rate(self, prof, data):
		prof.helpfulness_count += 1
		prof.helpfulness = self.average_rate(
												prof.helpfulness,
												prof.helpfulness_count,
												data['helpfulness']
											)
		prof.easiness_count += 1
		prof.easiness = self.average_rate(
											prof.easiness,
											prof.easiness_count,
											data['easiness']
										)
		prof.clarity_count += 1
		prof.clarity = self.average_rate(
											prof.clarity,
											prof.clarity_count,
											data['clarity']
										)
		prof.coolness_count += 1
		prof.coolness = self.average_rate(
											prof.coolness,
											prof.coolness_count,
											data['coolness']
										)
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

	def apply_comment(self, prof, data, study):
		if not 'comment' in data.keys():
			raise Exception("COMMENT IS EMPTY")
		if len(data['comment']) > 1000:
			raise Exception("LEN IS TOO MUCH")

		post = Post()
		post.prof = prof
		post.body = data['comment']
		post.clarity = data['clarity']
		post.helpfulness = data['helpfulness']
		post.easiness = data['easiness']
		post.attrs['coolness'] = data['coolness']
		post.attrs['use_textbook'] = data['useTextbook']
		post.attrs['attendance'] = data['attendance']
		post.study = study
		self.append_tags(post, data)
		post.save()
		print "ID"
		print post.id

		# if len(prof.comments)>= 1:
		# 	if prof.comments[-1].id == -1 or prof.comments[-1] == None:
		# 		self.set_id_for_comments(prof)
		# 	cmt.id = prof.comments[-1].id + 1
		# else:
		# 	cmt.id = 0
		# print "CMT ID"
		# prof.comments.append(cmt)
		# prof.save()


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
				return study
		return None

	def create_course(self, prof, data):
		study = Study()
		study.name = data['courseName']

		self.update_course(study, data)
		prof.studies.append(study)
		prof.save()
		return study

	def apply_course(self, prof, data):
		if data['findCourse']:
			if 'selectedCourse' in data.keys() and data['selectedCourse'] != None:
				return self.find_and_update_course(prof, data)
					
		else:
			if 'courseName' in data.keys() and data['courseName'] != None:
				return self.create_course(prof, data)
		return None

	def post(self):
		try:
			data = json.loads(request.data)
			prof = Professor.objects(id=data['id']).first()
			if prof == None:
				raise Exception("PROF NOT FOUND")
				
			# if not 'response' in data.keys():
			# 	raise Exception("FORGET RECAPTCHA")
					
			if check_multiple_vote(prof, request.remote_addr):
				raise Exception("MULTIPLE VOTE")
				
			# if not verify_user(request.remote_addr, data['response']):
			# 	raise Exception("YOU ARE ROBOT")

			prof = Professor.objects(id=data['id']).first()
			if not self.validate(prof, data):
				raise Exception("INVALID DATA")
				
			study = self.apply_course(prof, data)
			if not study:
				raise Exception("INVALID COURSE")
				
			self.apply_rate(prof, data)
			self.apply_tags(prof, data)
			self.apply_comment(prof, data, study)

			print "EVERY THING IS ALRIGHT"
			return jsonify(
				success = True,
				message = "DONE"
			)
			
		except Exception as msg:
			app.logger.error(msg)
			return jsonify(
				success = False,
				message = msg.args[0]
			)
rate.add_url_rule('/rate', 
					view_func=ProfessorRate.as_view('professorRate'))

# def find_cmt(prof, id):
# 	for cmt in prof.comments:
# 		print "ID"
# 		print id
# 		print cmt.id
# 		if str(cmt.id) == id:
# 			return cmt


# class ReportComment(MethodView):
# 	def get(self, prof_id, cmt_id):
# 		prof = Professor.objects(id = prof_id).first()
# 		if prof:
# 			print "BEFORE find_cmt"
# 			cmt = find_cmt(prof, cmt_id)
# 			print "ATER CMT"
# 			print cmt
# 			if cmt:
# 				cmt.reported = 1
# 				prof.reported_comments += 1
# 				print "BEFORE SAVE"
# 				prof.save()
# 				print "IN THE REPORT COMMENT"
# 				return "True"
# 		return "False"
# rate.add_url_rule('/report/<prof_id>/<cmt_id>', 
# 					view_func=ReportComment.as_view('reportComment'))


# class ShowReportedComments(MethodView):
# 	decorators = [requires_auth]
# 	def get_prof_irell_comments(self, prof):
# 		for cmt in prof.comments:
# 			if cmt.reported:
# 				yield {
# 					"body":cmt.body,
# 					"id":cmt.id
# 				}
# 	def get_reported_comments(self):
# 		profs = Professor.objects(reported_comments__gt = 0)
# 		for prof in profs:
# 			cmts = self.get_prof_irell_comments(prof)
# 			yield {
# 				"prof":prof,
# 				"comments":cmts
# 			}
# 	def get(self):
# 		return render_template('report/reported.html',
# 								records=self.get_reported_comments())
# rate.add_url_rule('/report/list', 
# 					view_func=ShowReportedComments.as_view('showReportedComments'))

# class DeleteComment(MethodView):
# 	decorators = [requires_auth]
# 	def get(self, prof_id, cmt_id):
# 		print "POOOOOOOST"
# 		print id
# 		print cmt_id
# 		prof = Professor.objects(id=prof_id).first()
# 		if prof:
# 			cmt = find_cmt(prof, cmt_id)
# 			if cmt:
# 				prof.comments.remove(cmt)
# 				prof.reported_comments -= 1
# 				prof.save()
# 		return redirect(url_for('rate.showReportedComments'));
# rate.add_url_rule('/report/delete/<prof_id>/<cmt_id>', 
# 					view_func=DeleteComment.as_view('delete_comment'))

# class RestoreComment(MethodView):
# 	decorators = [requires_auth]
# 	def get(slef, prof_id, cmt_id):
# 		prof = Professor.objects(id=prof_id).first()
# 		if prof:
# 			cmt = find_cmt(prof, cmt_id)
# 			if cmt:
# 				cmt.reported = 0
# 				prof.reported_comments -= 1
# 				prof.save()
# 		return redirect(url_for('rate.showReportedComments'))
# rate.add_url_rule('/report/restore/<prof_id>/<cmt_id>', 
# 					view_func=RestoreComment.as_view('restore_comment'))

# class ResetService(MethodView):
# 	decorators = [requires_auth]
# 	def get(self):
# 		profs = Professor.objects.all()
# 		for prof in profs:
# 			del prof.helpfulness 
# 			del prof.helpfulness_count 
# 			del prof.easiness 
# 			del prof.easiness_count 
# 			del prof.clarity 
# 			del prof.clarity_count 
# 			del prof.coolness 
# 			del prof.coolness_count 
# 			del prof.reported_comments 
# 			del prof.studies
# 			del prof.recent_voters
# 			del prof.comments
# 			del prof.personal_tags
# 			prof.save()
# 		return "EVERY THING REMOVED"
# rate.add_url_rule('/reset', 
# 					view_func=ResetService.as_view('reset'))

class CommentsCount(MethodView):
	decorators = [requires_auth]
	def get(self):
		profs = Professor.objects.all()
		print profs.count()
		cmt_count = 0
		all_count = 0
		study_count = 0
		for prof in profs:
			all_count += prof.clarity_count
			cmt_count += len(prof.comments)
			study_count += len(prof.studies)
		print all_count, cmt_count, study_count

		result = []
		for fac in Faculty.objects.all():
			count = 0
			for prof in fac.professors:
				print prof.id
				prof_obj = Professor.objects(id=prof.id).first()
				if prof_obj:
					count += prof_obj.comments_count
			result.append((fac.name, count))
		print result
		return render_template('admin/stat.html',result= result, all = all_count, cmt = cmt_count, study = study_count)
rate.add_url_rule('/stat', 
					view_func=CommentsCount.as_view('stat'))


# class MigrateToPost(MethodView):
# 	def get(self):
# 		# decorators = [requires_auth]
# 		profs = Professor.objects()
# 		count = 0
# 		for prof in profs:
# 			for cmt in prof.comments:
# 				post = Post()
# 				post.created_at = cmt.created_at
# 				post.reported = cmt.reported
# 				post.body = cmt.body
# 				post.clarity = cmt.clarity
# 				post.helpfulness = cmt.helpfulness
# 				post.easiness = cmt.easiness
# 				post.attrs['coolness'] = cmt.coolness
# 				post.attrs['use_textbook'] = cmt.use_textbook
# 				post.attrs['attendance'] = cmt.attendance
# 				post.study = cmt.study
# 				post.personal_tags = cmt.personal_tags
# 				post.prof = prof
# 				post.save()
# 				count += 1
# 		print count
# 		return str(count)

# rate.add_url_rule('/migrate-to-post', 
# 	view_func = MigrateToPost.as_view("MigrateToPost"))

# class FixAllYe(MethodView):
# 	def get(self):
# 		for uni in University.objects.all():
# 			uni.name = replace_ye(uni.name)
# 			uni.save()
# 		for fac in Faculty.objects.all():
# 			fac.name = replace_ye(fac.name)
# 			fac.save()
# 		for prof in Professor.objects.all():
# 			prof.name = replace_ye(prof.name)
# 			prof.save()
# 		return "DONE"
# rate.add_url_rule('/fix-all-ye', 
# 	view_func = FixAllYe.as_view("FixAllYe"))