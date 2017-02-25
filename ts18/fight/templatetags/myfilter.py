from django import template
from fight.models import Player, Record
import os
register = template.Library()

@register.filter(name='logname')
def logname(value):
    try:
        note = Record.objects.get(log=value)
        return os.path.split(note.log.name)[-1]
    except:
        return None

@register.filter(name = 'loglink')
def loglink(value):
    try:
        note = Record.objects.get(log=value)
        return 'https://cpclash.eesast.com/logdownload/?file={0}'.format(note.ai.name)
    except:
        return None

@register.filter(name = 'ainame')
def ainame(value):
    try:
        note = Player.objects.get(ai=value)
        return os.path.split(note.ai.name)[-1]
    except:
        return None

@register.filter(name = 'ailink')
def ailink(value):
    try:
        note = Player.objects.get(ai=value)
        return 'https://cpclash.eesast.com/aidownload/?file={0}'.format(note.ai.name)
    except:
        return None
