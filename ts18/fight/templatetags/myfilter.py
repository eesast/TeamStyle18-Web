from django import template
from fight.models import Player
import os
register = template.Library()

@register.filter(name='score_change')
def score_change(record):
    return None




@register.filter(name = 'filename')
def filename(value):
    try:
        note = Player.objects.get(ai=value)
        return os.path.split(note.ai.name)[-1]
    except:
        return None

@register.filter(name = 'filelink')
def filelink(value):
    try:
        note = Player.objects.get(ai=value)
        return 'https://cpclash.eesast.com/download/?file={0}'.format(note.ai.name)
    except:
        return None
