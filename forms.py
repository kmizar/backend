# -*- coding: utf-8 -*-
from django import forms
from .models import Tag

#Tag searcher form
class TagSearcher(forms.Form):
    OPTIONS = (
        ("AUT", "Austria"),
        ("DEU", "Germany"),
        ("NLD", "Neitherlands"),
    )

    searcher = forms.ChoiceField(choices=OPTIONS, required=True, label='', widget=forms.Select(attrs={'class':'js-example-basic-multiple','multiple':'multiple'}))




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
