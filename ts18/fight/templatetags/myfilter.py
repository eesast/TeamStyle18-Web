from django import template
from file.models import Notification
import os
register = template.Library()

@register.filter(name='score_change')
def score_change(record):
    return none




@register.filter(name = '')
def filename(value):
    try:
        note = Notification.objects.get(file_attached=value)
        return os.path.split(note.file_attached.name)[-1]
    except:
        return none

@register.filter(name = 'filelink')
def filelink(value):
    try:
        note = Notification.objects.get(file_attached=value)
        return 'https://cpclash.eesast.com/download/?file={0}'.format(note.file_attached.name)
    except:
        return None
