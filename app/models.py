from flask import url_for
from app import db
import datetime

class University(db.Document):
    name = db.StringField(max_length=300, required=True)
    faculties = db.ListField(db.ReferenceField('Faculty'))

class Faculty(db.Document):
    name = db.StringField(max_length=300, required=True)
    uni = db.ReferenceField('University')
    professors = db.ListField(db.ReferenceField('Professor'))

    # @prof_count:
    def prof_count(self):
        return len(self.professors)


class Professor(db.Document):
    ''' Personal Attributes '''
    name = db.StringField(max_length=500, required=True)
    family = db.StringField(max_length=500)
    faculty = db.ReferenceField('Faculty')
    email = db.StringField(required=False)
    website = db.StringField()
    room_no = db.StringField()
    rank = db.StringField()
    pic = db.ImageField()
    image_place = db.StringField()
    image_name = db.StringField()

    ''' Personality rate '''
    helpfulness = db.FloatField(default=0)
    helpfulness_count = db.IntField(default=0)
    easiness = db.FloatField(default=0)
    easiness_count = db.IntField(default=0)
    clarity = db.FloatField(default=0)
    clarity_count = db.IntField(default=0)
    coolness = db.FloatField(default=0)
    coolness_count = db.IntField(default=0)

    ''' settings '''
    reported_comments = db.IntField(default = 0)

    ''' Studies '''
    studies = db.EmbeddedDocumentListField('Study')
    recent_voters = db.EmbeddedDocumentListField('Voter')
    ''' comments '''
    comments = db.EmbeddedDocumentListField('Comment')

    ''' tags '''
    personal_tags = db.EmbeddedDocumentListField('Tag')
    class_tags = db.EmbeddedDocumentListField('Tag')

    @property
    def profile_pic(self):
        if self.image_name:
            return "/static/img/uploaded_images/%s" % self.image_name
        else:
            return "/static/img/uploaded_images/default.png"
    @property
    def comments_count(self):
        return len(self.comments)

    @property
    def posts_count(self):
        return Post.objects(prof = self).count()

    @property
    def posts(self):
        return Post.objects(prof = self)


class Voter(db.EmbeddedDocument):
    ip = db.StringField()
    timestamp = db.DateTimeField()

class Study(db.EmbeddedDocument):
    ''' default attributes '''
    name = db.StringField(max_length=300)
    year = db.IntField()
    term = db.IntField()

    ''' rating options '''
    helpfulness = db.FloatField(default=0)
    helpfulness_count = db.IntField(default=0)
    easiness = db.FloatField(default=0)
    easiness_count = db.IntField(default=0)
    clarity = db.FloatField(default=0)
    clarity_count = db.IntField(default=0)

class Tag(db.EmbeddedDocument):
    name = db.StringField(max_length=30)
    count = db.IntField()


class Comment(db.EmbeddedDocument):
    id = db.IntField(default = -1)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    reported = db.IntField(default = 0)
    # author = db.StringField(verbose_name="Name", max_length=255, required=True)

    body = db.StringField(verbose_name="Comment")
    helpfulness = db.IntField(default=0)
    easiness = db.IntField(default=0)
    clarity = db.IntField(default=0)
    class_tags = db.EmbeddedDocumentListField('Tag')
    personal_tags = db.EmbeddedDocumentListField('Tag')
    study = db.EmbeddedDocumentField('Study')

    coolness = db.IntField()
    use_textbook = db.IntField()
    attendance = db.IntField()

class Post(db.Document):
    created_at = db.DateTimeField(default = datetime.datetime.now, required = True)
    reported = db.IntField(default = 0)
    reporting_ip = db.ListField(db.StringField())

    body = db.StringField()

    helpfulness = db.IntField(default=0)
    easiness = db.IntField(default=0)
    clarity = db.IntField(default=0)

    class_tags = db.EmbeddedDocumentListField('Tag')
    personal_tags = db.EmbeddedDocumentListField('Tag')
    study = db.EmbeddedDocumentField('Study')

    attrs = db.DictField()
    prof = db.ReferenceField('Professor')

    like = db.IntField()
    dislike = db.IntField()
    likers = db.ListField(db.StringField())
    deleted = db.BooleanField(default = False, required = True)

# class ProfView(db.Document):
#     profs = db.ListField(db.ReferenceField())

