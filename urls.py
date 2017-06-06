# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [

    #Страница со списком постов
    url(r'^$', views.postList, name='home'),
    url(r'^flows/(?P<flow>[a-z0-9_]+)/$',              views.postList),
    url(r'^groups/(?P<group>[a-z0-9_]+)/$',            views.postList),
    url(r'^tags/(?P<tag>[a-z0-9_]+)/$',                views.postList),
    url(r'^groups-tags/(?P<group_tag>[a-z0-9_-]+)/$',  views.postList),

    #Список рубрик и тегов
    url(r'^flows/$', views.flowList, name='flow'),

    #Статья
    url(r'^post/(?P<post>\d+)/$', views.postArticle),

]
