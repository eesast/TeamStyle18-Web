# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db import models
import datetime

class Player(models.Model):
    player = models.OneToOneField(User, related_name='playerdata')
    score = models.IntegerField(default=1000)
    ai = models.FileField(upload_to='submits',blank=True,null=True)
    running = models.BooleanField(default=False)
    rpyNumber = models.CharField(default='', max_length=100)
    lasttime = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    daily_count = models.IntegerField(default=0)
    last_reset_time = models.DateTimeField(default = '2017-3-20 00:00:02')
    def __str__(self):
        return self.player.username


class Record(models.Model):
    AI1 = models.ForeignKey(Player,related_name='ai1_record',verbose_name='ai1')
    AI2 = models.ForeignKey(Player,related_name='ai2_record',verbose_name='ai2')
    time = models.DateTimeField(auto_now=True)
    scorechange = models.IntegerField(default=0) # positive means AI_1 wins.
    rpyNumber = models.CharField(default='', max_length=100)
    log = models.CharField(default='', max_length=100)
    def __str__(self):
        return u'%s competes %s on %s'%(self.AI1,self.AI2,self.time)



