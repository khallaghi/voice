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

report = Blueprint('report', __name__, template_folder='templates/report')

class ReportPost(MethodView):
	def get(self, post_id):
		try:
			post = Post.objects(id = post_id).first()
			if request.remote_addr in post.reporting_ip:
				raise Exception("MULTIPLE REPORT")
			post.reported += 1
			if len(post.reporting_ip) >= 200:
				del post.reporting_ip[0]
				post.reporting_ip.append(request.remote_addr)
			else:
				post.reporting_ip.append(request.remote_addr)
			post.save()
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
report.add_url_rule('/report/<post_id>/', 
					view_func=ReportPost.as_view('reportPost'))

class showAllPostsRedirect(MethodView):
	decorators = [requires_auth]
	def get(self):
		return redirect(url_for('report.allPosts', page = 0))
report.add_url_rule('/posts', 
		view_func = showAllPostsRedirect.as_view('allPostsRedirect'))

class ShowAllPosts(MethodView):
	decorators = [requires_auth]
	def get(self, page):
		page = int(page)
		posts = Post.objects(deleted = False).order_by('-created_at')
		page_count = int(posts.count()/100)+1
		posts = posts[page*100:(page+1)*100]
		return render_template('/admin/posts.html', posts = posts, page_count = page_count)
report.add_url_rule('/posts/<page>/',
		view_func = ShowAllPosts.as_view('allPosts'))

class ShowReportedPosts(MethodView):
	decorators = [requires_auth]
	def get(self):
		posts = Post.objects(Q(reported__gte = 1) & Q(deleted = False)).order_by('-created_at')
		return render_template('report/reported.html', posts = posts)
 # 'report/reported.html',
								# records=self.get_reported_comments()
report.add_url_rule('/report/list', 
					view_func=ShowReportedPosts.as_view('showReportedPosts'))

class DeletePost(MethodView):
	decorators = [requires_auth]
	def get(self, post_id, page):
		try:
			# print request['page']
			post = Post.objects.get(id = post_id)
			post.deleted = True
			post.reported = 0
			post.save()
			print "after delete"
			
			# return jsonify(
			# 		success = True,
			# 		msg = "DONE"
			# 	)
		except Exception as msg:
			app.logger.error(msg)
			# return jsonify(
			# 	success = False,
			# 	message = msg.args[0]
			# )
		if page == 'report':
			return redirect(url_for('report.showReportedPosts'))
		elif page == 'all':
			return redirect(url_for('report.allPostsRedirect'))
report.add_url_rule('/report/delete/<page>/<post_id>/', 
	view_func = DeletePost.as_view("DeletePost"))

class RestorePost(MethodView):
	decorators = [requires_auth]
	def get(self, post_id, page):
		try:

			post = Post.objects.get(id = post_id)
			post.deleted = False
			post.reported = 0
			post.save()
			# return jsonify(
			# 		success = True,
			# 		message = "DONE"
			# 	)
			
		except Exception as msg:
			app.logger.error(msg)
			# return jsonify(
			# 		success = False,
			# 		message = msg.args[0]
			# 	)
		if page == 'report':
			return redirect(url_for('report.showReportedPosts'))
		elif page == 'all':
			return redirect(url_for('report.allPostsRedirect'))	

report.add_url_rule('/report/restore/<page>/<post_id>/', 
	view_func = RestorePost.as_view("RestorePost"))
