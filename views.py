# -*- coding: utf-8 -*-
#system
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import Http404

#paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#database
from .models import Article, Flow, Tag, TagGroup
#memcached: python-memcached, yum -y install memcached
from django.core.cache import cache
#forms
from .forms import TagSearcher


#--------------------------------------------------------
#Const
cacheTime  = 60*60*10
cardsCount = 15


#--------------------------------------------------------
#Funcs
def postList(request, flow=None, tag=None, search=None, group=None, group_tag=None):
    ''' Логика страницы со списком статей '''

    #Фильтр статей по потокам(хабам)
    if flow:
        try:
            page_title = str(Flow.objects.get(sys_name = flow).name).title()

            cache_key  = 'flows_{}'.format(flow)
            query_list = cache.get(cache_key)
            if not query_list:
                query_list = Article.objects.filter(flow__sys_name=flow)
                cache.set(cache_key, query_list, cacheTime)

        except:
            return redirect(notFound)

    #Фильтр статей по тегам
    elif search:
        page_title = 'searched'
        search = search.split('_')
        query_list = Article.objects.filter(tags__sys_name__in=search)
    elif tag:
        #try:

        page_title = 'qwerty'#str(Tag.objects.get(sys_name = tag).name).title()

        #cache_key  = 'tag_{}'.format(tag)
        #query_list = cache.get(cache_key)
        #if not query_list:
        query_list = Article.objects.filter(tags__sys_name=tag)
            #cache.set(cache_key, query_list, cacheTime)

        #except:
        #return redirect(notFound)

    #Фильтр статей по группам тегов
    elif group:
        try:
            page_title = str(TagGroup.objects.get(sys_name = group).name).title()

            cache_key = 'group_{}'.format(group)
            query_list = cache.get(cache_key)
            if not query_list:
                query_list = Article.objects.filter(group__sys_name=group)
                cache.set(cache_key, query_list, cacheTime)

        except:
            return redirect(notFound)

    #Фильтр статей по тагам в группе
    elif group_tag:
        try:
            filterList = group_tag.split('-')
            page_title = u'{} | {}'.format(
                str(TagGroup.objects.get(sys_name = filterList[0]).name).title(),
                str(Tag.objects.get(sys_name = filterList[1]).name).title())

            query_list = Article.objects.filter(group__sys_name=filterList[0], tags__sys_name=filterList[1])

        except:
            return redirect(notFound)

    #Без фильтра, вываливаем все
    else:
        page_title = u'Последние статьи'

        cache_key = 'all_articles'
        query_list = cache.get(cache_key)
        if not query_list:
            query_list = Article.objects.all()
            cache.set(cache_key, query_list, cacheTime)

    #Фильтруем неопубликованные статьи и сортируем по дате публикации
    query_list = query_list.filter(published_date__isnull=False).order_by('-published_date')

    #Пагинатор
    paginator = Paginator(query_list, cardsCount)
    page = request.GET.get('page')

    #Серчер
    searcher_form = TagSearcher()

    try:
        postObj_list = paginator.page(page)
    except PageNotAnInteger:
        postObj_list = paginator.page(1)
    except EmptyPage:
        postObj_list = paginator.page(paginator.num_pages)

    return render(request, 'pages/cards.html', {
        'postObj_list'  : postObj_list,
        'page_title'    : page_title,
        'searcher_form' : searcher_form,
        'search': 'bad' if search is None else search,
    })


def postArticle(request, post=None):
    ''' Логика страницы с открытой статьей '''

    postObj = get_object_or_404(Article, pk=post)
    if not postObj.published_date: raise Http404()

    #Инкрементируем счетчик страницы
    postObj.article_count += 1
    postObj.save()

    #Подключаем модуль с рекомендациями
    try:
        from backend.services.recoman.recoman import Recoman
        recoDumper   = Recoman(postObj)
        recoObj_list = recoDumper.getRecoData()

    except ImportError:
        recoObj_list = False

    return render(request, 'pages/post.html', {
        'postObj': postObj,
        'recoObj_list': recoObj_list,
    })


def flowList(request):
    ''' Логика страницы со списком тегов и рубрик '''

    #Достаем потоки(хабы)
    cache_key    = 'flowObj_list'
    flowObj_list = cache.get(cache_key)
    if not flowObj_list:
        flowObj_list  = Flow.objects.all()
        cache.set(cache_key, flowObj_list, cacheTime)

    #Достаем группы тегов
    cache_key     = 'groupObj_list'
    groupObj_list = cache.get(cache_key)
    if not groupObj_list:
        groupObj_list = TagGroup.objects.all()
        cache.set(cache_key, groupObj_list, cacheTime)

    return render(request, 'pages/hubs.html', {
        'flowObj_list' : flowObj_list,
        'groupObj_list': groupObj_list,
    })


def tagsSearcher(request):
    ''' Логика проверки поля ввода + трансформация tagName в tagSysName '''

    if request.method == 'POST':
        tagName = request.POST.getlist('searcher')
        #for e in '!@#$%^&()<>`"/\':;|': tagName = tagName.replace(e, '')

        #try:
        #tagKey = (Tag.objects.get(sys_name=tagName.capitalize())).sys_name
        return redirect(postList, search='_'.join(tagName))
        #except:
        #    return redirect(notFound)
    else:
        raise Http404


def notFound(request):
    ''' Логика обработки пустой страницы с уведомлением not_found '''

    return render(request, 'pages/cards.html', {})
