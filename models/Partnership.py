import mongoengine
import datetime

class Partnership(mongoengine.EmbeddedDocument):
    type = mongoengine.StringField(required=True, choices=['Rhapsody of Realities', 'Healings Streams', 'Campus Ministry', 'InnerCity Missions', 'Ministry Programs'])
    amount = mongoengine.IntField(default=0)
    Date = mongoengine.StringField(required=True)
    createdAt = mongoengine.DateTimeField(default=datetime.datetime.now)
    updatedAt = mongoengine.DateTimeField(default=datetime.datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.amount = kwargs.get('amount', 0)
        self.createdAt = kwargs.get('createdAt', datetime.datetime.now())
        self.updatedAt = kwargs.get('updatedAt', datetime.datetime.now())