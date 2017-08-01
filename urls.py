# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


from backend import views

urlpatterns = [

    #Страница со списком постов
    url(r'^$', views.MainNoFilter.as_view(), name='home'),
    url(r'^flows/(?P<flow>[a-z0-9_]+)/$',              views.MainFlowFilter.as_view()),
#    url(r'^groups/(?P<group>[a-z0-9_]+)/$',            views.postList),
#    url(r'^tags/search/(?P<search>[a-zA-Z0-9_]+)$',                views.postList),
    #url(r'^tags/(?P<tags>)/$',                views.postList),
#    url(r'^groups-tags/(?P<group_tag>[a-z0-9_-]+)/$',  views.postList),

    #Страница - ничего не найдено
#    url(r'^not_found/$', views.notFound),

    #Поиск по тегам, валидация формы
#    url(r'^search/$',  views.tagsSearcher),

    #Список рубрик и тегов
#    url(r'^flows/$', views.flowList, name='flow'),

    #Статья
#    url(r'^post/(?P<post>\d+)/$', views.postArticle),

]
