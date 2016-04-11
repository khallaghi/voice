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

    ''' tags '''
    personal_tags = db.EmbeddedDocumentListField('Tag')
    class_tags = db.EmbeddedDocumentListField('Tag')
    

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

class Tag(db.EmbeddedDocument):
    name = db.StringField(max_length=30)
    count = db.IntField()


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    # author = db.StringField(verbose_name="Name", max_length=255, required=True)

    body = db.StringField(verbose_name="Comment", required=True, max_length=300)
    helpfulness = db.IntField()
    easiness = db.IntField()
    clarity = db.IntField()
    class_tags = db.EmbeddedDocumentListField('Tag')
    personal_tags = db.EmbeddedDocumentListField('Tag')
    study = db.EmbeddedDocumentField('Study')

    coolness = db.IntField()
    use_textbook = db.IntField()
    attendance = db.IntField()




