from django.contrib import admin

from .models import Notification

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_attached', )

admin.site.register(Notification , NoteAdmin)
