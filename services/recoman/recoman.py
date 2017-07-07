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
