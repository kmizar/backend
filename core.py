# -*- coding: utf-8 -*-
#system
from django.views.generic import View
from django.shortcuts import render

class MainPage(View):
    cacheTime  = 60*60*10
    cardsCount = 15

    def __init__(self, **kwargs):
        self.kwargs = kwargs


    def get(self, request, **kwargs):

        page_title   = self.getTitle(kwargs)
        postObj_list = self.getObjList(kwargs)

        return render(request, 'pages/cards.html', {
            'postObj_list'   : postObj_list,
            'page_title'     : page_title,
        })
