from mongoengine import connect, DoesNotExist
from bson import ObjectId
from colorama import Fore
from models.users import KingUser
# from models.records import KingsRecords
connect(alias='core', host='mongodb://localhost:27017/kingsrecord_db')

class KingsRecordDatabase:
    def add_user(self, **kwargs):
        """Creates a new user and adds the user to the database"""
        try:
            user = KingUser(**kwargs)
            user.save()
            return user
        except Exception as e:
            print(f'{Fore.RED}Error creating user: {str(e)}{Fore.RESET}')

    
    def get_user_by_username(self, username):
        """Returns a user by username"""
        try:
            user = KingUser.objects.get(username=username)
            return user
        except DoesNotExist:
            return None
        except Exception as e:
            print(f'{Fore.RED}Error getting user by username: {str(e)}{Fore.RESET}')
            return None