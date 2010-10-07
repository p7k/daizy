from django.db import models
from registration.models import RegistrationProfile

class FacebookProfile(RegistrationProfile):
    """Extends the basic registration profile to accomodate facebookies"""
    about_me = models.TextField(blank=True, null=True)
    facebook_id = models.IntegerField(blank=True, null=True)
    facebook_name = models.CharField(max_length=255, blank=True, null=True)
    facebook_profile_url = models.TextField(blank=True, null=True)
    website_url = models.TextField(blank=True, null=True)
    blog_url = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/fb_avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
