# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Player(models.Model):
    player = models.OneToOneField(User, related_name='playerdata')
    score = models.IntegerField(default=1000)
    ai = models.FileField(upload_to='ai_submit',blank=True,null=True)
    lasttime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.player.username


class Record(models.Model):
    AI1 = models.ForeignKey(Player,related_name='ai1_record',verbose_name='ai1')
    AI2 = models.ForeignKey(Player,related_name='ai2_record',verbose_name='ai2')
    time = models.DateTimeField(auto_now=True)
    result_list={
        ('0','AI1_wins'),
        ('1','AI2_wins'),
        ('2','tie'),
    }
    result = models.CharField(max_length=1,choices=result_list)
    AI1_scorechange = models.IntegerField(default=0)
    AI2_scorechange = models.IntegerField(default=0)
    log = models.FileField(upload_to='logs',blank=True,null=True)
    def __str__(self):
        return u'%s competes %s on %s'%(self.AI1,self.AI2,self.time)



# Create your models here.
