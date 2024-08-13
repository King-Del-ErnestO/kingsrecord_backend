import mongoengine
import datetime
# from models.records import KingsRecords
import bcrypt
class KingUser(mongoengine.Document):
    username = mongoengine.StringField(required=True)
    firstName = mongoengine.StringField(required=True)
    lastName = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    password = mongoengine.StringField(required=True)
    createdAt = mongoengine.DateTimeField(default=datetime.datetime.now)
    # updatedAt = mongoengine.DateTimeField(default=datetime.datetime.now)

    kingsRecord = mongoengine.EmbeddedDocumentListField(KingsRecords)
    meta = {
        'db_alias': 'core',
        'collection': 'king_users',
        'indexes': ['username', 'email']
    }

    def __init__(self, *args, **values):
        self.firstName = values.get('firstName', None)
        self.lastName = values.get('lastName', None)
        self.email = values.get('email', None)
        self.password = self.hash_password(values.get('password'))
        self.username = values.get('username', None)


    def hash_password(password: str):
        """Hash the password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def check_password(self, password: str):
        """Check if the provided password matches the stored hashed password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password)