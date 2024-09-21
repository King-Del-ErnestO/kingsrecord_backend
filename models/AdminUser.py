import mongoengine
import datetime
import bcrypt

class KingAdminUser(mongoengine.Document):
    title = mongoengine.StringField(required=True)
    firstName = mongoengine.StringField(required=True)
    lastName = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    password = mongoengine.StringField(required=True)
    chapter = mongoengine.StringField(required=True)
    createdAt = mongoengine.DateTimeField(default=datetime.datetime.now)
    phoneNumber = mongoengine.StringField(required=True)
    # updatedAt = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
        'db_alias': 'core',
        'collection': 'king_users',
        'indexes': ['email']
    }

    def __init__(self, **values):
        super().__init__(**values)
        self.firstName = values.get('firstName', None)
        self.lastName = values.get('lastName', None)
        self.email = values.get('email', None)
        self.password = values.get('password')
        self.title = values.get('title', None)
        self.phoneNumber = values.get('phoneNumber', None)
        self.chapter = values.get('chapter', None)

    @staticmethod
    def hash_password(password: str):
        """Hash the password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, my_password: str):
        """Check if the provided password matches the stored hashed password"""
        return bcrypt.checkpw(my_password.encode('utf-8'), self.password.encode('utf-8'))