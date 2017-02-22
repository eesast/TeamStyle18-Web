# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django import forms


class Post(models.Model):
	Category_List=(
		('1','赛事公告'),
		('2','技术讨论'),
		('3','bug汇报'),
		)
	title = models.CharField(u'评论标题',max_length=100)
	timestamp = models.DateTimeField(auto_now=True)
	content = models.TextField(u'内容',blank=True, null=True)
	sender = models.ForeignKey(User,on_delete=models.CASCADE)
	category = models.CharField(max_length = 1,default=1,choices=Category_List)
	priority = models.IntegerField(default=1000,verbose_name="优先级")
	def __unicode__(self):
		return self.title

class PostFile(models.Model):
    PERMISSION_CHOICES = {
        ('1',"公开"),
        ('2','登陆可见'),
    }
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    file_attached = models.FileField(upload_to='uploads/', blank=True,null=True)
    permissions = models.CharField(max_length=1,choices=PERMISSION_CHOICES)



class Comment(models.Model):
	post = models.ForeignKey(Post,related_name='p_comment')
	content= models.TextField(max_length=1000)
	replytime = models.DateTimeField(auto_now=True)
	replier = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
	def __unicode__(self):
		return u'%s to post %s' %(self.replier,self.post)


# Create your models here.
