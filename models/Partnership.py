import mongoengine
import datetime

class Partnership(mongoengine.EmbeddedDocument):
    type = mongoengine.StringField(required=True, choices=['rhapsodyOfRealities', 'healingStreams', 'campusMinistry', 'innerCityMission', 'ministryProgram'])
    amount = mongoengine.IntField(default=0)
    createdAt = mongoengine.DateTimeField(default=datetime.datetime.now)
    updatedAt = mongoengine.DateTimeField(default=datetime.datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rhapsodyOfRealities = kwargs.get('rhapsodyOfRealities', False)
        self.healingStreams = kwargs.get('healingStreams', False)
        self.campusMinistry = kwargs.get('campusMinistry', False)
        self.innerCityMission = kwargs.get('innerCityMission', False)
        self.ministryProgram = kwargs.get('ministryProgram', False)
        self.amount = kwargs.get('amount', 0)
        self.createdAt = kwargs.get('createdAt', datetime.datetime.now)
        self.updatedAt = kwargs.get('updatedAt', datetime.datetime.now)