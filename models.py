# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

#DataBase hooks
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

#RichTextEditor
#Info: github.com/django-ckeditor/django-ckeditor
from ckeditor_uploader.fields import RichTextUploadingField

#ImageField with resize
#Info: github.com/un1t/django-resized
from django_resized import ResizedImageField


class TagGroup(models.Model):
    ''' Группировка тегов '''

    name = models.CharField(max_length=100, unique=True, blank=False)
    icon = ResizedImageField(size=[64,64], upload_to='tag_group_icons/',null=True)
    sys_name    = models.CharField(max_length=100, unique=True, blank=False)
    description = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.sys_name


class Flow(models.Model):
    ''' Рубрики контента '''

    name = models.CharField(max_length=100, unique=True, blank=False)
    sys_name     = models.CharField(max_length=100, unique=True, blank=False)
    created_date = models.DateTimeField(default=timezone.now)

    #Связь с группой (много тегов -> одна группа)
    group = models.ManyToManyField(TagGroup, blank=True)

    def __str__(self):
        return self.sys_name


class Tag(models.Model):
    ''' Теги статьи '''

    name = models.CharField(max_length=50, unique=True, blank=False)
    sys_name     = models.CharField(max_length=50, unique=True, blank=False)
    created_date = models.DateTimeField(default=timezone.now)

    #Связь с группой (много тегов -> одна группа)
    group = models.ForeignKey(TagGroup, blank=False, on_delete=models.CASCADE)

    def  __str__(self):
        return self.sys_name


class Article(models.Model):
    ''' Статья '''

    author = models.ForeignKey('auth.User')
    title  = models.CharField(max_length=200, blank=False)
    text   = RichTextUploadingField()

    created_date   = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    #Связи с темой и тегами статьи
    flow = models.ForeignKey(Flow, blank=False, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def publich(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


#-----------------------------------------------
#Hooks
@receiver(pre_save, sender=Flow)
@receiver(pre_save, sender=Tag)
@receiver(pre_save, sender=TagGroup)
def lower_case(sender, instance, **kwargs):
    instance.name     = instance.name.lower()
    instance.sys_name = instance.sys_name.lower()

@receiver(pre_delete, sender=TagGroup)
def remove_img(sender, instance, **kwargs):
    instance.icon.delete(False)
