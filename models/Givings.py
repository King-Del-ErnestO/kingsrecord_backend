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
        self.offering = kwargs.get('offering', False)
        self.tithes = kwargs.get('tithes', False)
        self.specialSeed = kwargs.get('specialSeed', False)
        self.donation = kwargs.get('donation', False)
        self.amount = kwargs.get('amount', 0)
        self.createdAt = kwargs.get('createdAt', datetime.datetime.now)
        self.updatedAt = kwargs.get('updatedAt', datetime.datetime.now)