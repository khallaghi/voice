from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from app.models import University, Professor, Faculty
from flask.ext.mongoengine.wtf import model_form

category = Blueprint('category', __name__, template_folder='templates')

class UniversityView(MethodView):
    def get(self):
        universities = University.objects.all()
        return render_template('category/university-view.html', universities=universities)
category.add_url_rule('/university', view_func=UniversityView.as_view('uni'))

class FacultyView(MethodView):
    def get(self,uni):
        print "GEEEET"
        uni = University.objects(id=uni).first()
        faculties = uni.faculties
        return render_template('category/faculty-view.html', faculties=faculties)
category.add_url_rule('/faculty/<uni>', view_func=FacultyView.as_view('faculty'))

class ProfView(MethodView):
    def get(self,fac):
        fac = Faculty.objects(id=fac).first()
        profs = fac.professors
        return render_template('category/prof-view.html', professors = profs)
category.add_url_rule('/professor/<fac>', view_func=ProfView.as_view('professor'))

class ProfileView(MethodView):
    def get(self, prof):
        prof = Professor.objects(id=prof).first()
        return render_template('category/profile.html', professor=prof)
category.add_url_rule('/profile/<prof>', view_func=ProfileView.as_view('profile'))




# class ProfessorProfile(MethodView):

#     form = model_form(Comment, exclude=['created_at'])

#     # def get_context(self, prof_id):
#     #     prof = Professor.objects.get_or_404(_id=prof_id)
#     #     form = self.form(request.form)

#     #     context = {
#     #         "post": post,
#     #         "form": form
#     #     }
#     #     return context

#     def get(self, prof_id):
#         prof = Professor.objects(_id=prof_id)
#     def post(self, ):
#         context = self.get_context(prof_id)
#         form = context.get('form')

#         if form.validate():
#             comment = Comment()
#             form.populate_obj(comment)

#             post = context.get('post')
#             post.comments.append(comment)
#             post.save()

#             return redirect(url_for('posts.detail', slug=slug))

#         return render_template('posts/detail.html', **context)

# Register the urls



# posts.add_url_rule('/<prof_id>/', view_func=DetailView.as_view('detail'))
