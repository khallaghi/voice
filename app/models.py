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

    # @prof_count:
    def prof_count(self):
        return len(self.professors)

class Professor(db.Document):
    ''' Personal Attributes '''
    name = db.StringField(max_length=500, required=True)
    family = db.StringField(max_length=500, required=True)
    faculty = db.ReferenceField('Faculty')
    email = db.StringField(required=False)
    website = db.StringField()
    room_no = db.StringField()
    rank = db.StringField()
    # pic = db.ImageField()
    image_place = db.StringField()
    image_name = db.StringField()
    ''' Personality rate '''
    attr1 = db.IntField(default=0)
    attr1_count = db.IntField(default=0)
    attr2 = db.IntField(default=0)
    attr2_count = db.IntField(default=0)
    attr3 = db.IntField(default=0)
    attr3_count = db.IntField(default=0)

    ''' Studies '''
    studies = db.EmbeddedDocumentListField('Study')

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
         
    

class Study(db.EmbeddedDocument):
    ''' default attributes '''
    name = db.StringField(max_length=300) 
    year = db.IntField()
    term = db.IntField()

    ''' rating options '''
    helpfulness = db.IntField(default=0)
    helpfulness_count = db.IntField(default=0)
    easiness = db.IntField(default=0)
    easiness_count = db.IntField(default=0)
    clarity = db.IntField(default=0)
    clarity_count = db.IntField(default=0)

class Tag(db.EmbeddedDocument):
    name = db.StringField(max_length=30)
    count = db.IntField()


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    # author = db.StringField(verbose_name="Name", max_length=255, required=True)

    body = db.StringField(verbose_name="Comment", required=True, max_length=300)
    helpfulness = db.IntField(default=0)
    easiness = db.IntField(default=0)
    clarity = db.IntField(default=0)
    class_tags = db.EmbeddedDocumentListField('Tag')
    personal_tags = db.EmbeddedDocumentListField('Tag')
    study = db.EmbeddedDocumentField('Study')

    coolness = db.IntField()
    use_textbook = db.IntField()
    attendance = db.IntField()




