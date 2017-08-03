# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


from backend import views

urlpatterns = [

    #Страница со списком постов
    url(r'^$', views.MainPageNoFilter.as_view(),       name='home'),
    url(r'^flows/(?P<flow>[a-z0-9_]+)/$',              views.MainPageFlowFilter.as_view()),
    url(r'^tags/(?P<tag>[a-z0-9_]+)/$',                views.MainPageTagFilter.as_view()),
    url(r'^groups/(?P<group>[a-z0-9_]+)/$',            views.MainPageGroupFilter.as_view()),
    url(r'^groups-tags/(?P<group_tag>[a-z0-9_-]+)/$',  views.MainPageGroupTagFilter.as_view()),

    #Страница рубрик и тегов
    url(r'^flows/$', views.FlowPage.as_view(), name='flow'),

    #Страница со статьей
    url(r'^post/(?P<post>\d+)/$', views.ArticlePage.as_view()),



#    url(r'^search/$', views.MainTagSearcher.as_view()),



#    url(r'^tags/search/(?P<search>[a-zA-Z0-9_]+)$',                views.postList),



#    url(r'^groups/(?P<group>[a-z0-9_]+)/$',            views.postList),

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
