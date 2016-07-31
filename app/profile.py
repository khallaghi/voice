from __future__ import division
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty, Post
from flask.ext.mongoengine.wtf import model_form
from app.forms import SearchForm
from mongoengine import Q
from flask import jsonify


profile = Blueprint('profile', __name__, template_folder='templates/profile')
def get_color(range):
	# color = int(range/5*(int("ffebee",16)-int("b71c1c",16))+int("b71c1c",16))

	# # print color
	# code = str(hex(color))
	# code = "#" + code[2:]
	# return code
	if(range<1):
		return "#D50000"
	if(range<2):
		return "#D50000"
	if(range<3):
		return "#FFAB00"
	if(range<4):
		return "#AEEA00"
	if(range<5):
		return "#00C853"
	if(range==5):
		return "#1B5E20"
def get_val(attr):
	return float("{0:.2f}".format(attr))
def get_studies_result(prof):
		for study in prof.studies:
			study_result = {}
			study_result['name'] = study.name
			# study_result['id'] = study.id
			temp = {}
			temp['value'] = get_val(study.helpfulness)
			temp['color'] = get_color(study.helpfulness)
			study_result['helpfulness'] = temp
			temp = {}
			temp['value'] = get_val(study.easiness)
			temp['color'] = get_color(study.easiness)
			study_result['easiness'] = temp
			temp = {}
			temp['value'] = get_val(study.clarity)
			temp['color'] = get_color(study.clarity)
			study_result['clarity'] = temp
			yield study_result
def get_tags(tags):
	comment_list = []
	for tag in tags:
		tag_dict = {}
		tag_dict['name'] = tag.name
		tag_dict['count'] = tag.count
		comment_list.append(tag_dict)

	return sorted(comment_list, key=lambda comment: comment["count"], reverse=True)


def get_comments(prof):
	posts = Post.objects(prof = prof, deleted = False).order_by("created_at")
	for cmt in posts:
		comment_dict = {}
		comment_dict['body'] = cmt.body
		comment_dict['helpfulness'] = cmt.helpfulness
		comment_dict['easiness'] = cmt.easiness
		comment_dict['clarity'] = cmt.clarity
		comment_dict['class_tags'] = get_tags(cmt.class_tags)
		comment_dict['personal_tags'] = get_tags(cmt.personal_tags)
		if cmt.study:
			comment_dict['study'] = cmt.study.name
		else:
			comment_dict['study'] = ""

		# comment_dict['study'] = cmt.study.name
		comment_dict['coolness'] = cmt.attrs['coolness']
		if 'use_textbook' in cmt.attrs.keys():
			comment_dict['use_textbook'] = cmt.attrs['use_textbook']
		comment_dict['attendance'] = cmt.attrs['attendance']
		comment_dict['id'] = str(cmt.id)
		# comment_dict['reported'] = cmt.reported
		yield comment_dict
class ProfProfile(MethodView):

	def get_context(self,id):
		professor = Professor.objects.get_or_404(id=id)
		return professor

	def most_choosen_tags(self,prof):
		selected_tags = []
		# sel_tag = None
		tags = prof.personal_tags
		DEFINED = 10
		for i in range(0,DEFINED):
			sel_tag = None
			for tag in tags:
				if tag.count == 0:
					continue
				if sel_tag==None:
					sel_tag = tag
				elif sel_tag.count < tag.count :
					sel_tag = tag
			# print sel_tag
			if sel_tag != None:
				del tags[tags.index(sel_tag)]
				selected_tags.append(sel_tag)
		return selected_tags

	def get(self,id):
		prof = self.get_context(id)
		tags = self.most_choosen_tags(prof)
		all_posts = Post.objects(prof=prof).count()
		removed_posts = Post.objects(prof=prof, deleted=True).count()
		# rate_form = SearchForm(request.form)

		return render_template('profile/profile.html',
								prof=prof,
								tags=tags,
								all_posts=all_posts,
								removed_posts=removed_posts)

class ProfResult(MethodView):
	def get_context(self, id):
		prof = Professor.objects(id=id).first()
		if prof==None:
			print "404"
			return
		if prof.helpfulness==None:
			prof.helpfulness = 0;
		if prof.helpfulness_count==None:
			prof.helpfulness_count=0;
		if prof.easiness==None:
			prof.easiness = 0;
		if prof.easiness_count==None:
			prof.easiness_count=0;
		if prof.clarity==None:
			prof.clarity = 0;
		if prof.clarity_count==None:
			prof.clarity_count=0;
		prof.save()
		result = {}
		main_result = {}
		res = {}
		res['value'] = get_val(prof.helpfulness)
		res['color'] = get_color(prof.helpfulness)
		main_result['helpfulness'] = res
		res = {}
		res['value'] = get_val(prof.easiness)
		res['color'] = get_color(prof.easiness)
		main_result['easiness'] = res
		res = {}
		res['value'] = get_val(prof.clarity)
		res['color'] = get_color(prof.clarity)
		main_result['clarity'] = res

		result['main_result'] = main_result
		result['studies_result'] = [stdy_res for stdy_res in get_studies_result(prof)]
		result['comments'] = [comment for comment in get_comments(prof)]
		result['personal_tags'] = [tag for tag in get_tags(prof.personal_tags)]
		return result
	
	def get(self, id):
		result = self.get_context(id)
		return jsonify(**result) 

class FacProfile(MethodView):
	def get_context(self,id):
		fac = Faculty.objects.get_or_404(id=id)
		return fac
	def get(self):
		fac = get_context(id)
		return render_template('profile/faculty.html', faculty=fac)

class UniProfile(MethodView):
	def get_context(self,id):
		uni = University.objects.get_or_404(id=id)
		return uni
	def get(self,id):
		uni = get_context(id)
		return render_template('profile/uni.html', uni=uni)
profile.add_url_rule('/prof/<id>', view_func=ProfProfile.as_view('prof'))
profile.add_url_rule('/fac/<id>', view_func=FacProfile.as_view('faculty'))
profile.add_url_rule('/uni/<id>', view_func=UniProfile.as_view('uni'))
profile.add_url_rule('/prof/getResults/<id>', view_func=ProfResult.as_view('prof result'))
