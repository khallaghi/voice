from __future__ import division
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
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
	if(range<=1):
		return "#B71C1C"
	if(range<=2):
		return "#FDD835"
	if(range<=3):
		return "#CDDC39"
	if(range<=4):
		return "#8BC34A"
	if(range<=5):
		return "#4CAF50"
def get_val(attr):
	return float("{0:.2f}".format(attr))
def get_studies_result(prof):
		for study in prof.studies:
			study_result = {}
			study_result['name'] = study.name
			temp = {}
			temp['value'] = get_val(study.attr1)
			temp['color'] = get_color(study.attr1)
			study_result['helpfulness'] = temp
			temp = {}
			temp['value'] = get_val(study.attr2)
			temp['color'] = get_color(study.attr2)
			study_result['easiness'] = temp
			temp = {}
			temp['value'] = get_val(study.attr3)
			temp['color'] = get_color(study.attr3)
			study_result['clarity'] = temp
			yield study_result

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
			print sel_tag
			if sel_tag != None:
				del tags[tags.index(sel_tag)]
				selected_tags.append(sel_tag)
		return selected_tags

	def get(self,id):
		prof = self.get_context(id)
		tags = self.most_choosen_tags(prof)
		# rate_form = SearchForm(request.form)
		return render_template('profile/profile.html',prof=prof, tags=tags)

class ProfResult(MethodView):
	def get_context(self, id):
		prof = Professor.objects(id=id).first()
		if prof==None:
			print "404"
			return
		if prof.attr1==None:
			prof.attr1 = 0;
		if prof.attr1_count==None:
			prof.attr1_count=0;
		if prof.attr2==None:
			prof.attr2 = 0;
		if prof.attr2_count==None:
			prof.attr2_count=0;
		if prof.attr3==None:
			prof.attr3 = 0;
		if prof.attr3_count==None:
			prof.attr3_count=0;
		prof.save()
		result = {}
		main_result = {}
		res = {}
		res['value'] = get_val(prof.attr1)
		res['color'] = get_color(prof.attr1)
		main_result['helpfulness'] = res
		res = {}
		res['value'] = get_val(prof.attr2)
		res['color'] = get_color(prof.attr2)
		main_result['easiness'] = res
		res = {}
		res['value'] = get_val(prof.attr3)
		res['color'] = get_color(prof.attr3)
		main_result['clarity'] = res

		result['main_result'] = main_result
		result['studies_result'] = [stdy_res for stdy_res in get_studies_result(prof)]
		return result
	
	def get(self, id):
		result = self.get_context(id)
		print "GEEETTTT PROFRESULTs"
		print result
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
profile.add_url_rule('/fac/<id>', view_func=FacProfile.as_view('faculty profile'))
profile.add_url_rule('/uni/<id>', view_func=UniProfile.as_view('uni profile'))
profile.add_url_rule('/prof/getResults/<id>', view_func=ProfResult.as_view('prof result'))