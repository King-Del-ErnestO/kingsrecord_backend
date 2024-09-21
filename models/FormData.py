import mongoengine
import datetime
from models.Partnership import Partnership
from models.Givings import Givings

class User(mongoengine.Document):
    title = mongoengine.StringField(max_length=100, required=True)
    firstName = mongoengine.StringField(max_length=100, required=True)
    lastName = mongoengine.StringField(max_length=100, required=True)
    Date = mongoengine.StringField(required=True)
    email = mongoengine.StringField(max_length=100, required=True)
    phoneNumber = mongoengine.StringField(max_length=100, required=True)
    partnership = mongoengine.EmbeddedDocumentListField(Partnership)
    givings = mongoengine.EmbeddedDocumentListField(Givings)
    createdAt = mongoengine.DateTimeField(default=datetime.datetime.now)


    meta = {
        'db_alias': 'core',
        'collection': 'users',
        'indexes': ['email']
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', None)
        self.firstName = kwargs.get('firstName', None)
        self.lastName = kwargs.get('lastName', None)
        self.Date = kwargs.get('Date', None)
        self.email = kwargs.get('email', None)
        self.phoneNumber = kwargs.get('phoneNumber', None)
        self.partnership = kwargs.get('partnership', None)
        self.givings = kwargs.get('givings', None)
        self.createdAt = kwargs.get('createdAt', datetime.datetime.now)

    def update(self, **kwargs):
        self.title = kwargs.get('title', self.title)
        self.firstName = kwargs.get('firstName', self.firstName)
        self.lastName = kwargs.get('lastName', self.lastName)
        self.Date = kwargs.get('Date', self.Date)
        self.email = kwargs.get('email', self.email)
        self.phoneNumber = kwargs.get('phoneNumber', self.phoneNumber)
        self.partnership = kwargs.get('partnership', self.partnership)
        self.givings = kwargs.get('givings', self.givings)
        self.updatedAt = datetime.datetime.now()
        self.save()

    def add_partnership(self, type, amount, createdAt):
        self.partnership.append(Partnership(type=type, amount=amount, createdAt=createdAt))
        self.save()

    def add_giving(self, type, amount, createdAt):
        self.givings.append(Givings(type=type, amount=amount, createdAt=createdAt))
        self.save()

    def __str__(self):
        return f'{self.firstName} {self.lastName}'