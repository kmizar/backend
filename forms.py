# -*- coding: utf-8 -*-
#system
from django import forms
#database
from .models import Tag

#------------------------------------------------------------------
#Tag searcher form
class TagSearcher(forms.Form):
    OPTIONS = (
        (tag.sys_name, tag.name) for tag in Tag.objects.all()
    )

    searcher = forms.MultipleChoiceField(
        choices=OPTIONS,
        label='',
        widget=forms.SelectMultiple(
            attrs={
                'class':'js-example-basic-multiple',
                'style':'width:100%',
            }
        )
    )
