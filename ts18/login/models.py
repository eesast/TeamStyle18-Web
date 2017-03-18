from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings
import os



@python_2_unicode_compatible
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile' )
    login_name = models.CharField(max_length=50, default='')
    student_id = models.CharField(max_length=20, blank=True)
    is_leader = models.BooleanField(default=False)
    scores = models.IntegerField(default=1000,blank=True, null=True)
    image = models.ImageField(upload_to='head_images',
                              default=os.path.join('head_images', 'customer.png'))
    def __str__(self):
        return self.user.username

