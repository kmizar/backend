# -*- coding: utf-8 -*-
from django import forms
from .models import Tag

#Tag searcher form
class TagSearcher(forms.ModelForm):
    searcher = forms.CharField(
        label='',
        help_text='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )


    class Meta:
        model   = Tag
        fields  = ('searcher',)
