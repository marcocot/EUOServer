from django.contrib import admin
from . import models


class AccessInlineAdmin(admin.TabularInline):
    """ Informazioni di accesso ad uno script
    """

    model = models.Access
    extra = 0


class CharAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'shard', 'char_id', 'public_key']
    inlines = [AccessInlineAdmin, ]


class ScriptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'hash']


class BanAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ip', 'expires']


admin.site.register(models.Script, ScriptAdmin)
admin.site.register(models.Char, CharAdmin)
admin.site.register(models.Ban, BanAdmin)
