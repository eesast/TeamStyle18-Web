from django.core.management.base import BaseCommand, CommandError

from fight.models import Player


class Command(BaseCommand):
    help = 'reset all the player\'s counter to 0 every day'
    def handle(self, *args, **options):
        for 
