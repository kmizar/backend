# -*- coding: utf-8 -*-
from django import forms
from .models import Tag


#Tag searcher form
class TagSearcher(forms.Form):
    tags = Tag.objects.all()



    OPTIONS = (
        (tag.sys_name, tag.name)
        for tag in tags

    )


    searcher = forms.MultipleChoiceField(choices=OPTIONS, required=True, label='', widget=forms.SelectMultiple(
        attrs={
            'class':'js-example-basic-multiple',
            'style':'width:100%',
        }))




    #searcher = forms.ChoiceField(choices=OPTIONS)
    #widget = forms.ChoiceField(attrs={
    #    'class': 'js-example-basic-multiple',
    #    'multiple': 'multiple',
    #})
    #widget=forms.Select(attrs={'class':'js-example-basic-multiple'})


    #searcher = forms.CharField(
    #    label='',
    #    help_text='',
    #    widget=forms.TextInput(attrs={
    #        'class': 'form-control',
    #        'autocomplete': 'off',
    #    })
    #)


    #class Meta:
    #    model   = Tag
    #    fields  = ('searcher',)
