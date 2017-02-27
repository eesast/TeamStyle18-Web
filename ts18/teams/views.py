# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Team
from django.http import HttpResponse, Http404, HttpResponseRedirect
import hashlib


def if_in_team(user):
    in_team = False
    if user.is_authenticated:
        if user.in_team.all() or user.profile.is_leader:
            in_team = True
    return in_team

def get_user_info(user):
    if user.is_authenticated:
        in_team = if_in_team(user)
        is_leader = user.profile.is_leader
        team = ''
        if is_leader:
            team = user.leads
            app_list = team.application_set.all()
        else:
            teams = user.in_team.all()
            for t in teams:
                if user in t.members.all():
                    team = t

        return {
                 'in_team': in_team,
                 'is_leader': is_leader,
                 'team': team,
                 'errors': [],
        }

    return None



def index(request):
    # user joins a group by posting a invitation code.
    note = ''

    if request.method == 'POST':
       code = request.POST['code']
       foundTeam = Team.objects.filter(invitationCode=code)
       if not foundTeam.count():
           note = '错误的邀请码'
       else:
           team = foundTeam[0]
           if team.is_full:
               note = '队伍已满'
       if not note:
          team.members.add(request.user)
          if team.members.count() >= 3:
              team.is_full = True
              team.save()
          return HttpResponseRedirect(reverse('teams:myteam'))


    teams = Team.objects.all()
    return render(request, 'team_index.html', {'teams':teams, 'note':note})




def create(request):

    errors = []
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name = cd['name']
            intro = cd['intro']
            code = cd['code']

            exist = Team.objects.filter(name=name)
            if exist.count():
                errors.append('队名已被使用')
            existCode = Team.objects.filter(invitationCode=code)
            if existCode.count():
                errors.append('邀请码太短')

            if errors:
                return render(request, 'team_create.html', {'form': form, 'errors' : errors })

            else:
                team = Team(name=name, intro=intro, leader=request.user, invitationCode=code)
                team.save()
                request.user.profile.is_leader = True
                request.user.profile.save()
                return HttpResponseRedirect(reverse('teams:my_team'))


    return render(request, 'team_create.html', {'form': form})

@login_required
def myteam(request):
    user_info_dict = get_user_info(request.user)
    return render(request, 'team_myteam.html', user_info_dict)

@login_required
def dismiss(request):

    if request.method == 'POST':
        user = request.user
        team_id = request.POST['team_id']
        team = get_object_or_404(Team, pk=team_id)
        team.members.clear()
        team.delete()
        user.profile.is_leader = False
        user.profile.save()

    return HttpResponseRedirect(reverse('teams:index'))

