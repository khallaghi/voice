import datetime
from flask import url_for
from app import db

class University(db.Document):
    name = db.StringField(max_length=300, required=True)
    faculties = db.ListField(db.ReferenceField('Faculty'))

class Faculty(db.Document):
    name = db.StringField(max_length=300, required=True)
    uni = db.ReferenceField('University')
    professors = db.ListField(db.ReferenceField('Professor'))

class Professor(db.Document):
    ''' Personal Attributes '''
    name = db.StringField(max_length=500, required=True)
    family = db.StringField(max_length=500, required=True)
    faculty = db.ReferenceField('Faculty')
    email = db.StringField(required=False)
    website = db.StringField()
    room_no = db.StringField()
    rank = db.StringField()
    # avatar = db.ImageField()

    ''' Personality rate '''
    attr1 = db.IntField()
    attr1_count = db.IntField()
    attr2 = db.IntField()
    attr2_count = db.IntField()
    attr3 = db.IntField()
    attr3_count = db.IntField()

    ''' Studies '''
    studies = db.EmbeddedDocumentListField('Study')

    ''' comments '''
    comments = db.EmbeddedDocumentListField('Comment')


class Study(db.EmbeddedDocument):
    ''' default attributes '''
    name = db.StringField(max_length=300) 
    year = db.IntField()
    term = db.IntField()

    ''' rating options '''
    attr1 = db.IntField()
    attr1_count = db.IntField()
    attr2 = db.IntField()
    attr2_count = db.IntField()
    attr3 = db.IntField()
    attr3_count = db.IntField()


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True, max_length=300)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)

# class Post(db.Document):
#     created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
#     title = db.StringField(max_length=255, required=True)
#     slug = db.StringField(max_length=255, required=True)
#     body = db.StringField(required=True)
#     comments = db.ListField(db.EmbeddedDocumentField("Comment"))

#     def get_absolute_url(self):
#         return url_for('post', kwargs={"slug": self.slug})

#     def __unicode__(self):
#         return self.title

#     meta = {
#         'allow_inheritance': True,
#         'indexes': ['-created_at', 'slug'],
#         'ordering': ['-created_at']
#     }


