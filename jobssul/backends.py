from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:

            user = UserModel.objects.get(email=username)

            return user
        except UserModel.DoesNotExist:
            return None
