# -*- coding: utf-8 -*-
from backend.models import Article, Flow, TagGroup
import random


#-----------------------------------------------------------------------------------
#class
class Recoman(object):
    def __init__(self, _postObj):
        self.postObj = _postObj

    def getData(self):
        ran = random.randint(1,2)
        return [Article.objects.get(id=ran),Article.objects.get(id=ran),Article.objects.get(id=ran),
        Article.objects.get(id=ran),Article.objects.get(id=ran),Article.objects.get(id=ran)]
