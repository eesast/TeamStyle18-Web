# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .models import Team
from .forms import CreateForm
from django.http import HttpResponse, Http404, HttpResponseRedirect


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

    if request.method == 'POST' and request.user.is_authenticated:
       code = request.POST['code']
       print(request.POST['code'])
       try:
           team = Team.objects.get(invitationCode=code)
           team.members.add(request.user)
           if team.members.count() >= 3:
               team.is_full = True
               team.save()
           return HttpResponseRedirect(reverse('teams:myteam'))
       except Team.DoesNotExist:
           note = '邀请码错误'


    teams = Team.objects.all()
    in_team = if_in_team(request.user)
    return render(request, 'team_index.html', {'teams':teams, 'in_team':in_team, 'note':note})



@login_required
def create(request):

    errors = []
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            print('1')
            cd = form.cleaned_data
            name = cd['name']
            intro = cd['intro']
            code = cd['code']

            exist = Team.objects.filter(name=name)
            if exist.count():
                errors.append('队名已被使用')
            existCode = Team.objects.filter(invitationCode=code)
            if existCode.count():
                errors.append('邀请码太短, 可输入长度不大于200字符串')

            if errors:
                return render(request, 'team_create.html', {'form': form, 'errors' : errors })

            else:
                team = Team(name=name, intro=intro, leader=request.user, invitationCode=code)
                team.save()
                request.user.profile.is_leader = True
                request.user.profile.save()
                return HttpResponseRedirect(reverse('teams:myteam'))


    return render(request, 'team_create.html', {'form': form})

@login_required
def myteam(request):

    # kickout a member in a certain team
    if request.method == 'POST' and request.user.profile.is_leader:
        name = request.POST['name']
        team = request.user.leads
        thisone = team.members.get(username=name)
        team.members.remove(thisone)
        if team.members.count() < 3:
            team.is_full = False
            team.save()
        HttpResponseRedirect(reverse('teams:myteam'))

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

