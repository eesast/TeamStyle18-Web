from __future__ import unicode_literals

from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    file_attached = models.FileField(upload_to='uploads/', blank=True)


    def __unicode__(self):
        return self.title


