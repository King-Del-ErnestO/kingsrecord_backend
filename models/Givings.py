import mongoengine
import datetime

class Givings(mongoengine.EmbeddedDocument):
    """Giving model for a user"""
    type = mongoengine.StringField(required=True, choices=['Offering', 'Tithes', 'Special Seeds', 'Donation'])
    amount = mongoengine.IntField(default=0)
    Date = mongoengine.StringField(required=False)
    createdAt = mongoengine.DateTimeField(default=datetime.datetime.now)
    updatedAt = mongoengine.DateTimeField(default=datetime.datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.amount = kwargs.get('amount', 0)
        self.createdAt = kwargs.get('createdAt', datetime.datetime.now())
        self.updatedAt = kwargs.get('updatedAt', datetime.datetime.now())