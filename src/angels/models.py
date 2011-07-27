# -*- coding:utf-8 -*-
from datetime import datetime

from django.db import models

BOOLEAN_CHOICES = [(0, 'да'), (1, 'нет')]

class Change(models.Model):
    id = models.IntegerField(primary_key=True)
    field = models.CharField(max_length=765, blank=True)
    content = models.TextField(blank=True)
    new_content = models.TextField()
    mtime = models.DateTimeField(null=True, blank=True)
    ip = models.CharField(max_length=48, blank=True)
    guy = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'changes'

    def __unicode__(self):
        return 'Change on %s' % self.field

class Helper(models.Model):
    id = models.IntegerField(primary_key=True)
    who = models.CharField(max_length=765, verbose_name='Кто')
    whom = models.ForeignKey('Human', db_column='whom', verbose_name='Кому')
    how = models.TextField(verbose_name='Помощь')
    ctime = models.DateTimeField(verbose_name='Время отправки',
                                 auto_now_add=True)
    visible = models.BooleanField(verbose_name='Скрыть',
                                  choices=BOOLEAN_CHOICES,
                                  default=0)
    class Meta:
        db_table = u'helpers'
        verbose_name = 'Ангел'
        verbose_name_plural = 'Ангелы'

    def __unicode__(self):
        return u'%s (%s)' % (self.who, self.whom)

class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField('Заголовок')
    desc = models.TextField('Текст')
    ctime = models.DateTimeField(verbose_name='Время отправления', auto_now_add=True)
    ip = models.CharField(max_length=48, verbose_name='IP адрес')
    class Meta:
        db_table = u'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __unicode__(self):
        return self.title

class Human(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=765, verbose_name='Фамилия, имя')
    days = models.CharField(max_length=765, verbose_name='Сколько суток', blank=True)
    place = models.ForeignKey('Place', db_column='place', blank=True, null=True, verbose_name='Где сидит (сидел)')
    desc = models.TextField(verbose_name='Описание', default=u'', blank=True)
    ctime = models.DateTimeField(verbose_name='Время создания',
                                 auto_now_add=True)
    mtime = models.DateTimeField(verbose_name='Последнее изменение',
                                 auto_now=True)
    visible = models.BooleanField(verbose_name='Скрыть',
                                  choices=BOOLEAN_CHOICES, default=0)
    new = models.BooleanField(choices=BOOLEAN_CHOICES, default=0)
    detention = models.DateField(null=True, blank=True, verbose_name='Начало срока')
    class Meta:
        db_table = u'people'
        verbose_name = 'Человек'
        verbose_name_plural = 'Список людей'

    def __unicode__(self):
        return self.title

class Place(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=765)
    class Meta:
        db_table = u'places'
        verbose_name = 'Место отсидки'
        verbose_name_plural = 'Места отсидки'

    def __unicode__(self):
        return self.title
