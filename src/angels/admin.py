# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.utils.safestring import mark_safe

from models import Helper, Message, Human, Place, Status

# class ChangeAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Change, ChangeAdmin)

class HelperAdmin(admin.ModelAdmin):
    list_display = ['who', 'whom', 'how', 'ctime', 'visible']
    list_filter = ['visible']
    fields = ['who', 'whom', 'how', 'ctime', 'visible']
    readonly_fields = ['ctime']
admin.site.register(Helper, HelperAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc', 'ip', 'ctime']
    fields = ['title', 'desc', 'ip', 'ctime']
    readonly_fields = ['ctime']
    ordering = ['-ctime']
admin.site.register(Message, MessageAdmin)

class HumanChangeList(ChangeList):
    def get_results(self, *args, **kwargs):
        ret = super(HumanChangeList, self).get_results(*args, **kwargs)

        helpers = Helper.objects.filter(
            whom__id__in=[human.id for human in self.result_list])

        human_helpers = {}
        for helper in helpers:
            this_human_helpers = human_helpers.get(helper.whom.id, [])
            this_human_helpers.append(helper)
            human_helpers[helper.whom.id] = this_human_helpers

        for human in self.result_list:
            human.cool_helpers = human_helpers.get(human.id, [])

        return ret

class HumanAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'place', 'days', 'detention', 'desc',
                    'helpers_display', 'mtime']
    list_per_page = 250
    list_display_links = ['title']
    list_filter = ['place', 'status', 'days']
    fields = ['title', 'status', 'place', 'days', 'detention', 'desc', 'new', 'visible',
              'ctime', 'mtime']
    readonly_fields = ['id', 'ctime', 'mtime', 'new']
    actions = []

    def get_changelist(self, *args, **kwargs):
        return HumanChangeList

    def helpers_display(self, obj):
        helpers_list = getattr(obj, 'cool_helpers', [])
        if not helpers_list:
            return ''
        helpers_format = (u'<i>%s:</i><br />%s' % (mark_safe(helper.who),
                                                   mark_safe(helper.how))\
            for helper in helpers_list)

        return '<ol><li>%s</li></ol>' % '</li><li>'.join(helpers_format)
    helpers_display.verbose_name = 'Helpers'
    helpers_display.allow_tags = True

admin.site.register(Human, HumanAdmin)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title']
admin.site.register(Place, PlaceAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ['title']
    fields = ['title']
admin.site.register(Status, StatusAdmin)
