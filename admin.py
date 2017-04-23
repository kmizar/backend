# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Article, Flow, Tag, TagGroup

admin.site.register(Flow)
admin.site.register(TagGroup)
admin.site.register(Tag)
admin.site.register(Article)
