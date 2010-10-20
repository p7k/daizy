# import sys
# import datetime
# import time
# 
# from django.db import models
# 
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User
# 
# _max_timestamp = sys.maxint
# 
# class FacebookPlaylist(models.Model):
#     user = models.ForeignKey(User)
#     fetched_timestamp = models.FloatField(default=_max_timestamp)
# 
#     @property
#     def fetched_datetime(self):
#         return datetime.datetime.fromtimestamp(self.fetched_timestamp)
