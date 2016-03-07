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
from django.contrib import admin
from coellection.models import Platform, Game, Amiibo

# Register your models here.
admin.site.register(Platform)
admin.site.register(Game)
admin.site.register(Amiibo)