from django.contrib import admin
from django.shortcuts import redirect
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

    def get_actions(self, request):
        actions = super(ScriptAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            return []
        return actions

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_list_display(self, request):
        if request.user.is_superuser:
            return super(ScriptAdmin, self).get_list_display(request)

        return ['title', 'hash']

    def change_view(self, request, object_id, extra_content=None):
        if request.user.is_superuser:
            return super(ScriptAdmin, self).change_view(request, object_id, extra_content)

        return redirect('admin:backend_script_changelist')

class BanAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ip', 'expires']


admin.site.register(models.Script, ScriptAdmin)
admin.site.register(models.Char, CharAdmin)
admin.site.register(models.Ban, BanAdmin)
