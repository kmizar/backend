# -*- coding: utf-8 -*-
from backend.models import Article, Flow, TagGroup

#-----------------------------------------------------------------------------------
#class
class Recoman(object):
    def __init__(self, _postObj):
        self.postObj  = _postObj
        self.tagsList = _postObj.tags.all()

    def getTagCombinationList(self):
        '''
            Фомируем список возможных комбинаций тегов,
            с максимальной длиной в 2 элемента, возвращаем отсортированный
            список по длине.
        '''

        combinationList = []
        for item in range(0, len(self.tagsList)):
            combinationList.append([ self.tagsList[item] ])
            for i in range(0, item):
                combinationList.append([
                    self.tagsList[item],
                    self.tagsList[i]
                ])

        return sorted(combinationList,key=len,reverse=True)

    def getRecoData(self):
        '''
            Формируеи рекомендации, делая запросы в БД исходя из списка
            тегов (список статей из БД получаем в случайной сортировке),
            ограничиваем максимальную длин рекомендация: 4

            В блоке try/except исключаем из рекомендация дубликаты и тек. статью
        '''

        tagCombinationList = self.getTagCombinationList()

        recoArticlesList = []
        for tagsGroup in tagCombinationList:
            if len(recoArticlesList) > 4:
                break
            else:
                try:
                    recoArticlesList.append(
                        Article.objects.filter(
                            tags__in=tagsGroup
                        ).exclude(id=self.postObj.id).exclude(id__in=[x.id for x in recoArticlesList]).order_by('?')[1]
                    )
                except: pass

        return recoArticlesList
