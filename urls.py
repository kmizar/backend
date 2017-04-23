# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [

    #Страница со списком постов
    url(r'^$', views.postList),
    url(r'^flows/(?P<flow>[a-z0-9_]+)/$',  views.postList),
    url(r'^tags/(?P<tag>[a-z0-9_]+)/$', views.postList),
    url(r'^groups/(?P<group>[a-z0-9_]+)/$', views.postList),

    #Список рубрик и тегов
    url(r'^flows/$', views.flowList),

    #Статья
    url(r'^post/(?P<post>\d+)/$', views.postArticle),
    
]
