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
from django.views.generic import TemplateView, DetailView, ListView

from .models import Platform, Game, Amiibo
from .choices import PLATFORM_CHOICES


class PlatformMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PlatformMixin, self).get_context_data(**kwargs)
        game_objects = Game.objects.all()
        unique_platforms = game_objects.values('platform').distinct()
        unique_platforms_verbose = []
        for item in unique_platforms:
            unique_platforms_verbose.append(item['platform'])
        context['platforms'] = unique_platforms_verbose
        return context


class HomeView(TemplateView):
    template_name = 'coellection/home.html'
    context = {}

    def game_count(self):
        return Game.objects.count()

    def platform_count(self):
        return Platform.objects.count()

    def amiibo_count(self):
        return Amiibo.objects.count()


class GameDetail(DetailView):
    template_name = 'coellection/game.html'
    context_object_name = 'game'
    model = Game


class GameIndex(PlatformMixin, ListView):
    template_name = 'coellection/game_list.html'
    model = Game
    paginate_by = '50'
    queryset = Game.objects.all()
    context_object_name = 'games'


class GameFilter(PlatformMixin, ListView):
    template_name = 'coellection/game_list'
    model = Game
    paginate_by = '50'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.filter(platform=self.kwargs.get('platform'))


class PlatformDetail(DetailView):
    template_name = 'coellection/platform.html'
    context_object_name = 'platform'
    model = Platform


class PlatformIndex(ListView):
    template_name = 'coellection/platform_list.html'
    model = Platform
    queryset = Platform.objects.all()
    context_object_name = 'platforms'


class AmiiboDetail(DetailView):
    template_name = 'coellection/amiibo.html'
    context_object_name = 'amiibo'
    model = Amiibo


class AmiiboIndex(ListView):
    template_name = 'coellection/amiibo_list.html'
    model = Amiibo
    queryset = Amiibo.objects.all()
    context_object_name = 'amiibos'