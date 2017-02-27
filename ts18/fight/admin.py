from django.contrib import admin
from fight import models
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player','score','ai')

class RecordAdmin(admin.ModelAdmin):
    list_display = ('AI1','AI2','time','result','AI1_scorechange','AI2_scorechange','log')

admin.site.register(models.Player,PlayerAdmin)
admin.site.register(models.Record,RecordAdmin)
# Register your models here.
