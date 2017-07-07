# -*- coding: utf-8 -*-
from backend.models import Article, Flow, TagGroup
import random


#-----------------------------------------------------------------------------------
#class
class Recoman(object):
    def __init__(self, _postObj):
        self.postObj = _postObj

    def getRecoData(self):
        tagsList = self.postObj.tags.all()
        recoData = []

        while len(tagsList) > 0:
            articles = Article.objects.filter(
                tags__in=self.postObj.tags.all()
            ).exclude(id=self.postObj.id).distinct().order_by('-id')[:3]

            for data in articles:
                if data not in recoData:
                    recoData.append(data)

            if len(recoData) > 2:
                return recoData

            tagsList = tagsList.exclude(id=tagsList[len(tagsList)-1].id)


        else:
            return recoData





#    def getMaxSimilarRecomendations(self):
#        '''
#            Берем наиболее подходящие статьи, где все теги пересекаются
#        '''
#        return Article.objects.filter(
#            tags__in=self.postObj.tags.all()
#        ).exclude(id=self.postObj.id).distinct().order_by('-id')[:3]

#    def getMinSimilarRecomendations(self):
#        '''
#            Добираем рекомендации из статей с неполным пересечением тегов
#        '''
#        tags_list  = self.postObj.tags.all()
#        tags_count = len(tags_list)
#        articles   = []

#        while tags_count > 1:
#            data = Article.objects.filter(
#                tags__in=self.postObj.tags.all()[:tags_count]
#            ).exclude(id=self.postObj.id).distinct().order_by('-id')[:3]
#            for i in data:
#                articles.append[i]
#            tags_count -= 1

#        return articles


#    def getRecoData(self):
#        recoList = []

        #if article have tags
#        if self.postObj.tags:
#            recoList = self.getMaxSimilarRecomendations()
#            if len(recoList) < 3:
#                recoList += self.getMinSimilarRecomendations()

        #if no tags in article
#        else:
#            recoList = False

#        return recoList


















#
