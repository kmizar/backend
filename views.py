# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .models import Article, Flow, Tag, TagGroup


def postList(request, flow=None, tag=None, group=None):
    ''' Логика страницы со списком статей '''

    if flow:
        postObj_list = Article.objects.filter(flow__sys_name=flow)

    elif tag:
        postObj_list = Article.objects.filter(tags__sys_name=tag)

    elif group:
        post_tags    = Tag.objects.filter(group__sys_name=group)
        postObj_list = Article.objects.filter(
                        tags__sys_name__in=[tag.sys_name for tag in post_tags]
                       ).distinct()
    else:
        postObj_list = Article.objects.all()

    #filter non-publisher articles
    postObj_list = postObj_list.filter(published_date__isnull=False)
    #paginator
    paginator = Paginator(postObj_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'pages/postList.html', {
        'postObj_list': contacts,
    })


def postArticle(request, post=None):
    ''' Логика страницы с открытой статьей '''

    postObj = get_object_or_404(Article, pk=post)
    if not postObj.published_date: raise Http404()

    return render(request, 'pages/postArticle.html', {
        'postObj': postObj,
    })


def flowList(request):
    ''' Логика страницы со списком тегов и рубрик '''

    flowObj_list  = Flow.objects.all()
    groupObj_list = [
        { 'name' : group.name,
          'icon' : group.icon,
          'tags' : Tag.objects.all().filter(group_id = group.id),
          'description': group.description,
          'sys_name'   : group.sys_name,
        }
        for group in TagGroup.objects.all()
    ]

    return render(request, 'pages/flowList.html', {
        'flowObj_list' : flowObj_list,
        'groupObj_list': groupObj_list,
    })
