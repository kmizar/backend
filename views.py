# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Flow, Tag, TagGroup

from django.core.cache import cache


def postList(request, flow=None, tag=None, group=None, group_tag=None):
    ''' Логика страницы со списком статей '''

    if flow:
        cache_key = 'flows_{}'.format(str(flow))
        cache_time = 60*60*10
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.filter(flow__sys_name=flow)
            cache.set(cache_key, query_list, cache_time)

        page_title = str(Flow.objects.get(sys_name = flow).name).title()

    elif tag:
        cache_key = 'tag_{}'.fromat(str(tag))
        cache_time = 60*60*10
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.filter(tags__sys_name=tag)
            cache.set(cache_key, query_list, cache_time)

        page_title = str(Tag.objects.get(sys_name = tag).name).title()

    elif group:
        cache_key = 'group_{}'.fromat(str(group))
        cache_time = 60*60*10
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.filter(group__sys_name=group)
            cache.set(cache_key, query_list, cache_time)

        page_title = str(TagGroup.objects.get(sys_name = group).name).title()

    elif group_tag:
        filterList = group_tag.split('-')
        query_list = Article.objects.filter(group__sys_name=filterList[0], tags__sys_name=filterList[1])
        page_title = u'{} | {}'.format(
            str(TagGroup.objects.get(sys_name = filterList[0]).name).title(),
            str(Tag.objects.get(sys_name = filterList[1]).name).title())

    else:
        cache_key = 'all_articles'
        cache_time = 60*60*10
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.all()
            cache.set(cache_key, query_list, cache_time)

        page_title = u'Последние статьи'

    #filter non-publisher articles and sort data by date publish
    query_list = query_list.filter(published_date__isnull=False).order_by('-published_date')

    paginator = Paginator(query_list, 15)
    page = request.GET.get('page')

    try:
        postObj_list = paginator.page(page)
    except PageNotAnInteger:
        postObj_list = paginator.page(1)
    except EmptyPage:
        postObj_list = paginator.page(paginator.num_pages)

    return render(request, 'pages/cards.html', {
        'postObj_list': postObj_list,
        'page_title'  : u'{} | {}'.format(page_title, 'kmizar.com'),
    })


def postArticle(request, post=None):
    ''' Логика страницы с открытой статьей '''

    postObj = get_object_or_404(Article, pk=post)
    if not postObj.published_date: raise Http404()

    return render(request, 'pages/post.html', {
        'postObj': postObj,
    })


def flowList(request):
    ''' Логика страницы со списком тегов и рубрик '''

    flowObj_list  = Flow.objects.all()
    groupObj_list = TagGroup.objects.all()
    page_title    = u'Рубрики о ремонте и дизайне'

    return render(request, 'pages/hubs.html', {
        'flowObj_list' : flowObj_list,
        'groupObj_list': groupObj_list,
        'page_title'   : page_title,
    })
