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
import operator

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView, ListView

from .models import Platform, Game, Amiibo
from .choices import PLATFORM_CHOICES
from .forms import SearchForm

class PlatformMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PlatformMixin, self).get_context_data(**kwargs)
        game_objects = Game.objects.all().order_by('platform')
        unique_platforms = game_objects.values('platform').distinct()
        unique_platforms_verbose = []
        for item in unique_platforms:
            unique_platforms_verbose.append(item['platform'])
        context['platforms'] = unique_platforms_verbose
        return context


class HomeView(TemplateView):
    template_name = 'coellection/home.html'
    context = {}

    def contributors(self):
        return donor_list()

    def top_donor(self):
        donors = donor_list()
        leaderboard = {}
        for donor in donors:
            count = 0
            games = Game.objects.filter(donor=donor)
            count += games.count()
            platforms = Platform.objects.filter(donor=donor)
            count += platforms.count()
            amiibos = Amiibo.objects.filter(donor=donor)
            count += amiibos.count()
            leaderboard[donor] = count

        top_donor = max(leaderboard.items(), key=operator.itemgetter(1))[0]
        return top_donor + ' ' + str(leaderboard[top_donor])

    def game_count(self):
        return Game.objects.count()

    def platform_count(self):
        return Platform.objects.count()

    def amiibo_count(self):
        return Amiibo.objects.count()


class GameDetail(ListView):
    template_name = 'coellection/game.html'
    context_object_name = 'games'
    model = Game

    def get_queryset(self):
        return Game.objects.filter(slug=self.kwargs.get('slug'))

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
        if self.kwargs.get('platform'):
            return Game.objects.filter(platform=self.kwargs.get('platform'))
        elif self.kwargs.get('arg'):
            return Game.objects.filter(title__startswith=self.kwargs.get('arg'))


class PlatformDetail(ListView):
    template_name = 'coellection/platform.html'
    context_object_name = 'platforms'
    model = Platform

    def get_queryset(self):
        return Platform.objects.filter(slug=self.kwargs.get('slug'))


class PlatformIndex(ListView):
    template_name = 'coellection/platform_list.html'
    model = Platform
    queryset = Platform.objects.all()
    context_object_name = 'platforms'


class AmiiboDetail(ListView):
    template_name = 'coellection/amiibo.html'
    context_object_name = 'amiibos'
    model = Amiibo

    def get_queryset(self):
        return Amiibo.objects.filter(slug=self.kwargs.get('slug'))

class AmiiboIndex(ListView):
    template_name = 'coellection/amiibo_list.html'
    model = Amiibo
    queryset = Amiibo.objects.all()
    context_object_name = 'amiibos'


""" Database Search """


def search(request):
    if 'query' in request.GET and request.GET['query']:
        query = request.GET['query'].strip()
        games = Game.objects.filter(
            Q(title__icontains=query) | 
            Q(donor__icontains=query)).order_by('title')
        platforms = Platform.objects.filter(
            Q(title__icontains=query) |
            Q(donor__icontains=query)).order_by('title')
        amiibos = Amiibo.objects.filter(
            Q(title__icontains=query) |
            Q(donor__icontains=query)).order_by('title')
        return render(request, 'coellection/search_results.html',
            {'games': games, 'platforms': platforms, 'amiibos': amiibos, 'query': query})
    else:
        return HttpResponse('Please submit a search term.')


def donor_list():
    unique_donors = set()
    game_objects = Game.objects.all()
    game_donors = game_objects.values('donor').distinct()
    platform_objects = Platform.objects.all()
    platform_donors = platform_objects.values('donor').distinct()
    amiibo_objects = Amiibo.objects.all()
    amiibo_donors = amiibo_objects.values('donor').distinct()

    for donor in game_donors:
        # print(donor['donor'])
        unique_donors.add(donor['donor'])
    for donor in platform_donors:
        # print(donor['donor'])
        unique_donors.add(donor['donor'])
    for donor in amiibo_donors:
        # print(donor['donor'])
        unique_donors.add(donor['donor'])
    unique_donors.remove('')
    return unique_donors