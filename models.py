# -*- coding: utf-8 -*-

### coellection(django) ###
### GNU/GPL v2
### Author: Cody Rocker
### Author_email: cody.rocker.83@gmail.com
### 2016
#-----------------------------------
#   Requires:                    """
#    - xlrd 0.9.4                """
#    - Django 1.9.3              """
#-----------------------------------
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from .choices import *


class Platform(models.Model):
    # Basic info
    title = models.CharField(max_length=140)
    upc = models.CharField(verbose_name='UPC', max_length=64, blank=True)
    serial = models.CharField(max_length=64, blank=True)
    model = models.CharField(max_length=64, blank=True)
    modded = models.BooleanField(default=False)
    slug = models.SlugField(default='', max_length=64, editable=False)

    # Conditional ratings
    plays = models.IntegerField(verbose_name='Works', choices=PLAYS_CHOICES, default=2)
    box = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    manual = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    insert = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    vid_cable = models.IntegerField(verbose_name='Video Cable', choices=CONDITION_CHOICES, default=0)
    pwr_cable = models.IntegerField(verbose_name='Power Cable', choices=CONDITION_CHOICES, default=0)

    # Optional extras
    donor = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'slug': self.slug,}
        return reverse('platform', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[:64])
        super(Platform, self).save(*args, **kwargs)


class Game(models.Model):
    # Basic info
    title = models.CharField(max_length=140)
    platform = models.CharField(max_length=32, verbose_name='Platform', choices=PLATFORM_CHOICES)
    upc = models.CharField(verbose_name='UPC', max_length=64, blank=True)
    slug = models.SlugField(default='', max_length=64, editable=False)

    # Conditional ratings
    plays = models.IntegerField(verbose_name='Works', choices=PLAYS_CHOICES, default=2)
    media_cond = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    label = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    dust_cover = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    box = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    c_box = models.BooleanField(verbose_name='Custom/Display Box', default=False)
    manual = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    insert = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    battery = models.IntegerField(choices=CART_BATT_CHOICES, default=0)

    # Optional extras
    donor = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.get_platform_display())

    def get_absolute_url(self):
        kwargs = {'slug': self.slug,}
        return reverse('game', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[:64])
        super(Game, self).save(*args, **kwargs)


class Amiibo(models.Model):
    # Basic info
    title = models.CharField(max_length=140)
    upc = models.CharField(verbose_name='UPC', max_length=32, blank=True)
    slug = models.SlugField(default='', max_length=64, editable=False)

    # Conditional ratings
    plays = models.IntegerField(verbose_name='Works', choices=PLAYS_CHOICES, default=2)
    box = models.IntegerField(choices=CONDITION_CHOICES, default=0)
    figure = models.IntegerField(choices=CONDITION_CHOICES, default=0)

    # Optional extras
    donor = models.CharField(max_length=64, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {'slug': self.slug,}
        return reverse('amiibo', kwargs=kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[:64])
        super(Amiibo, self).save(*args, **kwargs)