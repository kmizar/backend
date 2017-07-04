# -*- coding: utf-8 -*-
#system
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import Http404

#paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#database
from .models import Article, Flow, Tag, TagGroup
#memcached: python-memcached, yum -y install memcached
from django.core.cache import cache


#--------------------------------------------------------
#Const
cacheTime = 60*60*10
carsCount = 15


#--------------------------------------------------------
#Funcs
def postList(request, flow=None, tag=None, group=None, group_tag=None):
    ''' Логика страницы со списком статей '''

    if flow:
        cache_key  = 'flows_{}'.format(flow)
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.filter(flow__sys_name=flow)
            cache.set(cache_key, query_list, cacheTime)

        page_title = str(Flow.objects.get(sys_name = flow).name).title()


    elif tag:
        cache_key = 'tag_{}'.format(tag)
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.filter(tags__sys_name=tag)
            cache.set(cache_key, query_list, cacheTime)

        page_title = str(Tag.objects.get(sys_name = tag).name).title()


    elif group:
        cache_key = 'group_{}'.format(group)
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.filter(group__sys_name=group)
            cache.set(cache_key, query_list, cacheTime)

        page_title = str(TagGroup.objects.get(sys_name = group).name).title()


    elif group_tag:
        filterList = group_tag.split('-')
        query_list = Article.objects.filter(group__sys_name=filterList[0], tags__sys_name=filterList[1])
        page_title = u'{} | {}'.format(
            str(TagGroup.objects.get(sys_name = filterList[0]).name).title(),
            str(Tag.objects.get(sys_name = filterList[1]).name).title())


    else:
        cache_key = 'all_articles'
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.all()
            cache.set(cache_key, query_list, cacheTime)

        page_title = u'Последние статьи'


    #filter non-publisher articles and sort data by date publish
    query_list = query_list.filter(published_date__isnull=False).order_by('-published_date')

    #create paginator object
    paginator = Paginator(query_list, carsCount)
    page = request.GET.get('page')

    try:
        postObj_list = paginator.page(page)
    except PageNotAnInteger:
        postObj_list = paginator.page(1)
    except EmptyPage:
        postObj_list = paginator.page(paginator.num_pages)

    return render(request, 'pages/cards.html', {
        'postObj_list': postObj_list,
        'page_title'  : page_title,
    })


def postArticle(request, post=None):
    ''' Логика страницы с открытой статьей '''

    postObj = get_object_or_404(Article, pk=post)
    if not postObj.published_date: raise Http404()

    #include recoman module
    try:
        from backend.services.recoman.recoman import Recoman
        recoman_check = True
    except ImportError:
        recoman_check = False

    #recoman for article recommendation
    if recoman_check:
        recoDumper = Recoman(postObj)

    return render(request, 'pages/post.html', {
        'postObj': postObj,
    })


def flowList(request):
    ''' Логика страницы со списком тегов и рубрик '''

    cache_key    = 'flowObj_list'
    flowObj_list = cache.get(cache_key)
    if not flowObj_list:
        flowObj_list  = Flow.objects.all()
        cache.set(cache_key, flowObj_list, cacheTime)

    cache_key     = 'groupObj_list'
    groupObj_list = cache.get(cache_key)
    if not groupObj_list:
        groupObj_list = TagGroup.objects.all()
        cache.set(cache_key, groupObj_list, cacheTime)

    return render(request, 'pages/hubs.html', {
        'flowObj_list' : flowObj_list,
        'groupObj_list': groupObj_list,
    })
