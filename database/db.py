from mongoengine import connect, DoesNotExist
from bson import ObjectId
from colorama import Fore
from models.AdminUser import KingAdminUser
from models.FormData import User
# from models.records import KingsRecords
connect(alias='core', host='mongodb+srv://udehdinobi:tOgop2E0oqtxgdAn@kingsrecord.vgiff.mongodb.net/')

class KingsRecordDatabase:
    def reg_admin_user(self, **kwargs):
        """Creates a new admin user and adds the user to the database"""
        try:
            kwargs['password'] = KingAdminUser.hash_password(kwargs['password']) 
            user = KingAdminUser(**kwargs)
            user.save()
            print(user.id)
            return user
        except Exception as e:
            print(f'{Fore.RED}Error creating user: {str(e)}{Fore.RESET}')
            return None
        
    def reg_user(self, **kwargs):
        """Creates a new admin user and adds the user to the database"""
        try:
            user = User(**kwargs)
            user.save()
            print(user.id)
            return user
        except Exception as e:
            print(f'{Fore.RED}Error creating user: {str(e)}{Fore.RESET}')
            return None


    def get_admin_by_email(self, email):
        """Returns a user by email"""
        try:
            user = KingAdminUser.objects.get(email=email)
            return user
        except DoesNotExist:
            return None
        except Exception as e:
            print(f'{Fore.RED}Error getting user by email: {str(e)}{Fore.RESET}')
            return None

    
    def get_user_by_email(self, email):
        """Returns a user by email"""
        try:
            user = User.objects.get(email=email)
            return user
        except DoesNotExist:
            return None
        except Exception as e:
            print(f'{Fore.RED}Error getting user by email: {str(e)}{Fore.RESET}')
            return None
        
    def get_user_by_id(self, user_id):
        """Returns a user by user_id"""
        try:
            user = User.objects.get(id=ObjectId(user_id))
            return user
        except DoesNotExist:
            return None
        except Exception as e:
            print(f'{Fore.RED}Error getting user by id: {str(e)}{Fore.RESET}')
            return None
        
    def get_admin_by_id(self, user_id):
        """Returns a user by user_id"""
        try:
            user = KingAdminUser.objects.get(id=ObjectId(user_id))
            return user
        except DoesNotExist:
            return None
        except Exception as e:
            print(f'{Fore.RED}Error getting user by id: {str(e)}{Fore.RESET}')
            return None
    
    def get_all_users(self):
        """Returns all users"""
        try:
            users = User.objects.all()
            return users
        except DoesNotExist:
            return None
        except Exception as e:
            print(f'{Fore.RED}Error getting all users: {str(e)}{Fore.RESET}')
            return None