#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from django.contrib import admin
from web.models import  Tztedayrpt
from web.models import Tzteiparea
from web.models import Thwiparea
from web.models import T3AUsr

from import_export import resources


class TztedayrptAdmin(admin.ModelAdmin):
    list_display = ('nodename', 'avgwidth', 'sjjdll','peakjdll','jdllper','sjepgbf','peakepgbf','epgbfper')

class TzteipareaResource(resources.ModelResource):

	class Meta:
		model = Tzteiparea

admin.site.register(Tztedayrpt,TztedayrptAdmin)