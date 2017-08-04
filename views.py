# -*- coding: utf-8 -*-
#system
from django.shortcuts import get_object_or_404
from backend import core

#database
from .models import Article, Flow, Tag, TagGroup

#------------------------------------------------------------------
class MainPageNoFilter(core.MainPage):
    ''' https://kmizar.com '''

    def getTitle(self, *kwargs):
        return u'Последние статьи'

    def getQueryList(self, *kwargs):
        return Article.objects.all()


class MainPageFlowFilter(core.MainPage):
    ''' https://kmizar.com/flows/flow_name '''

    def getTitle(self, *args):
        return str(Flow.objects.get(
            sys_name = args[0]['flow']).name).title()

    def getQueryList(self, *args):
        return Article.objects.filter(flow__sys_name=args[0]['flow'])


class MainPageTagFilter(core.MainPage):
    ''' https://kmizar.com/tags/tag_name '''

    def getTitle(self, *args):
        return str(Tag.objects.get(
            sys_name = args[0]['tag']).name).title()

    def getQueryList(self, *args):
        return Article.objects.filter(tags__sys_name=args[0]['tag'])


class MainPageGroupFilter(core.MainPage):
    ''' https://kmizar.com/groups/group_name '''

    def getTitle(self, *args):
        return str(TagGroup.objects.get(sys_name=args[0]['group']).name).title()

    def getQueryList(self, *args):
        return Article.objects.filter(group__sys_name=args[0]['group'])


class MainPageGroupTagFilter(core.MainPage):
    ''' https://kmizar.com/groups-tags/group_tag '''

    def getCache(self, *args):
        return None, None

    def getTitle(self, *args):
        filterList = (args[0]['group_tag']).split('-')
        return u'{} | {}'.format(
            str(TagGroup.objects.get(sys_name=filterList[0]).name).title(),
            str(Tag.objects.get(sys_name=filterList[1]).name).title()
        )

    def getQueryList(self, *args):
        filterList = (args[0]['group_tag']).split('-')
        return Article.objects.filter(group__sys_name=filterList[0],tags__sys_name=filterList[1])


class MainPageSearchFilter(core.MainPage):
    ''' https://kmizar.com/search/ '''

    def getTitle(self):
        return u'Результат поиска'

    def getQueryList(self, request):
        search_args = request.POST.getlist('searcher')
        return Article.objects.filter(tags__sys_name__in=search_args)


class FlowPage(core.FlowPage):
    ''' https://kmizar.com/flows '''

    def getFlowObjList(self, *args):
        return Flow.objects.all()

    def getGroupObjList(self, *args):
        return TagGroup.objects.all()


class ArticlePage(core.ArticlePage):
    ''' https://kmizar.com/post/post_id '''

    def postViewIncrement(self, postObj):
        postObj.article_count += 1
        postObj.save()

    def getPostObj(self, *args):
        postObj = get_object_or_404(Article, pk=args[0]['post'])
        if not postObj.published_date: raise Http404()

        return postObj
