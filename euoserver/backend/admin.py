from django.contrib import admin
from . import models


class ScriptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'hash']


admin.site.register(models.Script, ScriptAdmin)
admin.site.register(models.Char)

