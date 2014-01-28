from django.contrib import admin
from . import models


class CharAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'shard', 'char_id', 'public_key']


class ScriptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'hash']


class BanAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ip', 'expires']


admin.site.register(models.Script, ScriptAdmin)
admin.site.register(models.Char, CharAdmin)
admin.site.register(models.Ban, BanAdmin)

