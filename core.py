# -*- coding: utf-8 -*-
#system
from django.views.generic import View
from django.http          import Http404

from django.shortcuts     import redirect
from django.shortcuts     import render

#forms
from .forms import TagSearcher

#paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#memcached: python-memcached, yum -y install memcached
from django.core.cache import cache

#------------------------------------------------------------------
class MainPage(View):
    '''
        Class for main page.
            - Get urls params
            - Create paginator
            - Get content from memchache
            - Render page
            - Include searcher
    '''

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.cacheTime = 60*60*10
        self.cardsCount = 15

    #Startup paginator object
    def getPagination(self, _query_list, _request):
        paginator = Paginator(_query_list, self.cardsCount)
        page = _request.GET.get('page')

        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    #Try to get memcache content
    def getCache(self, *args):
        request_key = [key for key in args[0]]
        if not request_key:
            _cache_key = 'all_articles'
        else:
            request_key = request_key[0]
            _cache_key = '{}_{}'.format(request_key, args[0][request_key])

        return cache.get(_cache_key), _cache_key

    #Main part GET-request
    def get(self, request, **kwargs):

        try:
            page_title = self.getTitle(kwargs)
        except:
            return render(request, 'pages/cards.html', {})

        query_list, cache_key = self.getCache(kwargs)
        if not query_list:
            query_list = self.getQueryList(kwargs)
            cache.set(cache_key, query_list, self.cacheTime)

        query_list = query_list.filter(published_date__isnull=False).order_by('-published_date')
        postObj_list = self.getPagination(query_list, request)

        return render(request, 'pages/cards.html', {
            'postObj_list' : postObj_list,
            'page_title'   : page_title,
            'search'       : TagSearcher(),
        })

    #Main part POST-request
    def post(self, request, **kwargs):

        page_title = self.getTitle(request.POST.getlist('searcher'))
        query_list = self.getQueryList(request)

        query_list = query_list.filter(published_date__isnull=False).order_by('-published_date')
        postObj_list = self.getPagination(query_list, request)

        return render(request, 'pages/cards.html', {
            'postObj_list' : postObj_list,
            'page_title'   : page_title,
            'search'       : TagSearcher(),
        })


class FlowPage(View):
    '''
        Class for flows page.
            - Get content from memchache
            - Render page
    '''

    def __init__(self, **kwargs):
        self.cacheTime = 60*60*10

    #Try to get memcache content
    def getCache(self, _cache_key):
        return cache.get(_cache_key), _cache_key

    #Main part GET-request
    def get(self, request, **kwargs):

        flowObj_list, cache_key = self.getCache('flowObj_list')
        if not flowObj_list:
            flowObj_list = self.getFlowObjList(kwargs)
            cache.set(cache_key, flowObj_list, self.cacheTime)

        groupObj_list, cache_key = self.getCache('groupObj_list')
        if not groupObj_list:
            groupObj_list = self.getGroupObjList(kwargs)
            cache.set(cache_key, flowObj_list, self.cacheTime)

        return render(request, 'pages/hubs.html', {
            'flowObj_list'  : flowObj_list,
            'groupObj_list' : groupObj_list,
        })


class ArticlePage(View):
    '''
        Class for flows page.
            - Render page
            - Include post views increment func
            - Include recoman module
    '''

    #Main part GET-request
    def get(self, request, **kwargs):

        postObj = self.getPostObj(kwargs)
        self.postViewIncrement(postObj)

        #Include recoman
        try:
            from backend.services.recoman.recoman import Recoman
            recoDumper = Recoman(postObj)
            recoObj_list = recoDumper.getRecoData()

        except ImportError:
            recoObj_list = False

        return render(request, 'pages/post.html', {
            'recoObj_list' : recoObj_list,
            'postObj'      : postObj,
        })




















#
