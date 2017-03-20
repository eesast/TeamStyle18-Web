from django.shortcuts import render, get_object_or_404
import time
import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.files import File
from .models import Player, Record
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from wsgiref.util import FileWrapper
from itertools import chain
from operator import attrgetter
import os
import subprocess
import urllib

def getRecords(list1, list2, playerData):
    records=[]
    record_list = sorted(chain(list1, list2), key=attrgetter('time'),reverse=False)
    for record in record_list:
        r={}
        r['time']=record.time
        r['log']=record.log
        if record.AI1==playerData:
            r['scorechange']=record.scorechange
            r['competitor']=record.AI2
            if record.scorechange>0:
                r['result']='胜利'
            elif record.scorechange<0:
                r['result']='失败'
            else:
                r['result']='平局'
        if record.AI2==playerData:
            r['scorechange']=-record.scorechange
            r['competitor']=record.AI1
            if record.scorechange<0:
                r['result']='胜利'
            elif record.scorechange>0:
                r['result']='失败'
            else:
                r['result']='平局'
        records.append(r)
    return records

def index(request):
    if request.user.is_authenticated():
        try:
            data=Player.objects.get(player=request.user)
        except :
            data = Player(player = request.user)
            data.save()
        if request.user.playerdata.running == True:
            return HttpResponseRedirect(reverse('fight:myself'))

    count_info = Player.objects.all()
    time_now = datetime.datetime.now()
    for x in count_info:
        if time_now.day != x.last_reset_time.day:
            x.last_reset_time=datetime.datetime.now()+datetime.timedelta(hours=8)
            x.daily_count=0
            x.save()
    players_list=Player.objects.exclude(ai = None)

    if request.method=='POST':
        error = ''
        compete_id=request.POST['id']
        try:
            competitor=Player.objects.get(id=compete_id)
        except Player.DoesNotExsit:
            return render(request,'fight.html',{'player_list':players_list})

        if (not request.user.playerdata.ai) or (not competitor.ai):
            raise Http404

        if request.user.playerdata.running == False:
       #     error = os.path.join(settings.BASE_DIR, '..','..', 'ts18', 'server', 'fight_server.sh')+ ' %s_%s %s_%s' % (request.user.username, request.user.id, competitor.player.username, competitor.player.id)
            fight = subprocess.run(os.path.join(settings.BASE_DIR, '..','..', 'ts18', 'server', 'fight_server.sh')+ ' %s %s' %
                                          ( request.user.id,
                                           competitor.player.id),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   )
            if fight.returncode == 0:  # process running

                request.user.playerdata.running = True

                rpN =  fight.stdout.decode('utf-8').split()[-1].strip()
                error = rpN
                request.user.playerdata.rpyNumber = rpN
                request.user.playerdata.save()
                r = Record(AI1=request.user.playerdata,
                           AI2=competitor,
                           rpyNumber=rpN)
                r.save()
       #     else:
        #        error += 'RUN FAIL\n' + fight.stdout.decode('utf-8') + fight.stderr.decode('utf-8')

        record_list=request.user.playerdata.ai1_record.all()
        record_list2=request.user.playerdata.ai2_record.all()
        records = getRecords(record_list, record_list2, request.user.playerdata)

        return render(request, 'fight_myself.html', {
                                                     'error':error,'records':records,
                                                     })

    return render(request,'fight.html',{'player_list':players_list})







def Get_AI(request):
    try:
        data=Player.objects.get(player=request.user)
    except :
        data = Player(player = request.user)
        data.save()
    old_name = request.user.playerdata.ai.name
    if not 'aiupload' in request.FILES:
        return '请上传一个文件'

    new_ai=request.FILES['aiupload']
    name=new_ai.name.lower()

    if not name.endswith(('.cpp','.c')):
        return '请上传cpp或c格式的文件'
    # for compatibale reason
    if old_name.startswith('/'):
        request.user.playerdata.ai.name = os.path.join('submits', os.path.split(old_name)[-1])
        request.user.playerdata.save()
    try:
        old_path = request.user.playerdata.ai.path
        if os.path.exists(old_path):
            os.remove(old_path)
    except:
        pass
    # bind the new avatar to profile
    request.user.playerdata.ai=new_ai
    request.user.playerdata.save()
    initial_path=request.user.playerdata.ai.path

    # rename the new avatar to a regular name, and meanwhile, place the avatar
    # at a required place (using os.rename)
    pathdir = os.path.join(
        settings.BASE_DIR, '..','..','ts18','submits', '%s' % request.user.id)
    request.user.playerdata.ai.name=os.path.join(
        'submits',
        '%s' % request.user.id,'playerMain.cpp')

    new_path=os.path.join(pathdir, 'playerMain.cpp')

    if not os.path.exists(pathdir):
        os.mkdir(pathdir)

    if os.path.exists(new_path):
        os.remove(new_path)

    os.rename(initial_path,new_path)
    request.user.playerdata.save()
    request.user.save()
    cpl = subprocess.run(os.path.join(settings.BASE_DIR,'..', '..', 'ts18', 'server', 'compile.sh') + ' %s' % request.user.id, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if cpl.returncode != 0:
        request.user.playerdata.ai.delete()
        return 'COMPILATION ERROR\n' + cpl.stdout.decode('utf-8')

@login_required
def myself(request):
    try:
        data=Player.objects.get(player=request.user)
    except :
        data = Player(player = request.user)
        data.save()
    record_list=request.user.playerdata.ai1_record.all()
    record_list2=request.user.playerdata.ai2_record.all()
    records = getRecords(record_list, record_list2, request.user.playerdata)
#    record_list = sorted(chain(record_list,record_list2), key=attrgetter('time'),reverse=False)
#
#    if not record_list==[]:
#        for record in record_list:
#            r={}
#            r['time']=record.time
#            r['log']=record.log
#            if record.AI1==request.user.playerdata:
#                r['scorechange']=record.scorechange
#                r['competitor']=record.AI2
#                if record.scorechange>0:
#                    r['result']='胜利'
#                elif record.scorechange<0:
#                    r['result']='失败'
#                else:
#                    r['result']='平局'
#            if record.AI2==request.user.playerdata:
#                r['scorechange']=-record.scorechange
#                r['competitor']=record.AI1
#                if record.scorechange<0:
#                    r['result']='胜利'
#                elif record.scorechange>0:
#                    r['result']='失败'
#                else:
#                    r['result']='平局'
#            records.append(r)

    error=''
    running = request.user.playerdata.running
    if request.method=='POST':
        if request.user.is_authenticated():
            error = Get_AI(request)
            if not error:
                error = 'Success'
            return render(request, 'fight_myself.html', {'error':error,'records':records})

    if running == True:
        rpN = request.user.playerdata.rpyNumber.strip()
        # search the rpyfile and print the process
        rpyPath = os.path.join(settings.BASE_DIR, '..', '..', 'ts18', 'fight_result', rpN + '.rpy')
        txtPath = os.path.join(settings.BASE_DIR, '..', '..', 'ts18', 'fight_result', rpN+'.txt')
        error = rpyPath
        if os.path.exists(rpyPath):
            request.user.playerdata.running = False
            request.user.playerdata.count += 1
            request.user.playerdata.save()
            r = Record.objects.get(rpyNumber=rpN)
            r.log = rpyPath
            with open(txtPath, 'r') as f:
                lines = f.readlines()
                last = lines[-1]
                a = r.AI1.score
                b = r.AI2.score
                wea = 1./(1+10**((b-a)/400.))
                web = 1./(1+10**((a-b)/400.))
                if '0' in last:
                    r.scorechange = 1
                    r.AI1.score = int(a+32*(1-wea))	 
                    r.AI2.score = int(b+32*(0-web))
                elif '1' in last:
                    r.scorechange = -1
                    r.AI1.score = int(a+32*(1-wea))	 
                    r.AI2.score = int(b+32*(0-web))
                else:
                    r.scorechange = 0
                    r.AI1.score = int(a+32*(0.5-wea))	 
                    r.AI2.score = int(b+32*(0.5-web))
            r.AI1.save()
            r.AI2.save()
            r.save()
            time.sleep(0.5)
            return HttpResponseRedirect(reverse('fight:myself'))
        else:
            time.sleep(0.05)
            with open(txtPath, 'r') as f:
                lines = f.readlines()
                last = lines[-1]
                turn = last.split()[-1]
                if len(turn) > 4 or last.split()[0] != 'server':
                    request.user.playerdata.running = False
                    request.user.playerdata.save()
                    error = 'Platform Crashed'
                else:
                    error = 'turn:' + turn

    return render(request, 'fight_myself.html', {'error':error,'records':records })

@login_required
def aidownload(request):
    try:
        url = request.POST['path']
    except:
        raise Http404
    path = os.path.join( settings.BASE_DIR, '..', '..', 'ts18', url)
    name = os.path.split(path)[-1]
    name = urllib.parse.quote(name)
    wrapper = FileWrapper(open(path, 'rb'))
    response = HttpResponse(wrapper)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(name)[-1])
    return response

@login_required
def logdownload(request):
    try:
        url = request.POST['log']
    except:
        raise Http404
    name = os.path.split(url)[-1]
    name = urllib.parse.quote(name)
    wrapper = FileWrapper(open(url, 'rb'))
    response = HttpResponse(wrapper)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(name)[-1])
    return response


