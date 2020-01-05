from accounts.models import User, Token
from django.contrib.auth.backends import BaseBackend


class PasswordlessAuthenticationBackend(object):
    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
            print(token)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            print("user does not exist")
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            print("token does not exist")
            return None

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
