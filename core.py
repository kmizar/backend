# -*- coding: utf-8 -*-
#system
from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import Http404

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

    #Main part
    def get(self, request, **kwargs):

        try:
            page_title = self.getTitle(kwargs)
        except:
            return redirect(notFound)

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


class TagSearcher1(View):
    def get(self, request, **kwargs):
        if request.method == 'POST':
            form = TagSearcher(request.POST)

            if form.is_valid():
                tagsList = self.getTagsList()
                return redirect('yandex.ru')

            else:
                return redirect('/')




















#
