import mongoengine
import datetime

class Givings(mongoengine.EmbeddedDocument):
    """Giving model for a user"""
    type = mongoengine.StringField(required=True, choices=['offering', 'tithes', 'specialSeeds', 'donation'])
    amount = mongoengine.IntField(default=0)
    createdAt = mongoengine.DateTimeField(default=datetime.datetime.now)
    updatedAt = mongoengine.DateTimeField(default=datetime.datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.offering = kwargs.get('Offering', False)
        self.tithes = kwargs.get('Tithes', False)
        self.specialSeed = kwargs.get('Special Seeds', False)
        self.donation = kwargs.get('Donations', False)
        self.amount = kwargs.get('amount', 0)
        self.createdAt = kwargs.get('createdAt', datetime.datetime.now)
        self.updatedAt = kwargs.get('updatedAt', datetime.datetime.now)