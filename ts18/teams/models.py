# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=20)
    intro = models.CharField(max_length=50)
    leader = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leads')
    members = models.ManyToManyField(User, related_name='in_team')
    invitationCode = models.CharField(max_length=200)
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' -- ' + self.leader.username




