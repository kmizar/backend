# -*- coding: utf-8 -*-
#system
from django.contrib import admin
#database
from .models import Article, Flow, Tag, TagGroup

#------------------------------------------
#Override django admin
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('article_count',)

#------------------------------------------
#Register models
admin.site.register(Flow)
admin.site.register(TagGroup)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
