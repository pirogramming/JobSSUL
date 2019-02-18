from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

#
# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         user_model = get_user_model()
#         login_valid = (username == username)
#         pwd_valid = check_password(password, password)
#         if login_valid and pwd_valid:
#             try:
#                 user = user_model.objects.get(email=username)
#                 return user
#             except user_model.DoesNotExist:
#                 return None
#         else:
#             return None

