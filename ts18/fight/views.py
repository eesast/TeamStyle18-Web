from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
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
<<<<<<< HEAD

=======
    has_submitted=False
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9
    if request.user.is_authenticated():
        try:
            data=Player.objects.get(player=request.user)
        except :
            data = Player(player = request.user)
            data.save()
<<<<<<< HEAD
      
        if request.user.playerdata.running == True:
            return HttpResponseRedirect(reverse('fight:myself')
=======
        if request.user.playerdata.ai!=None:
            has_submitted=True
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9

    players_list=Player.objects.exclude(ai = None)

    if request.method=='POST':
<<<<<<< HEAD
        compete_id=request.POST['id']
=======
        compete_id=request.POST.get('id','')
        print(request.POST)
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9
        try:
            competitor=Player.objects.get(id=compete_id)
        except Player.DoesNotExsit:
            return render(request,'fight.html',{'player_list':players_list,'has_submitted':has_submitted})

<<<<<<< HEAD
        if request.user.playerdata.running == False:
            error = 'in process'
            fight = subprocess.run(os.path.join(settings.BASE_DIR, '..','..', 'ts18', 'server', 'fight_server.sh')+' %s_%s %s_%s' %
                                          (request.user.username, request.user.id,
                                          competitor.player.username, competitor.player.id),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   )
            if fight.returncode == 0:  # process running
                request.user.playerdata.running = True
                rpN =  fight.stdout.decode('utf-8')
                request.user.playerdata.rpyNumber = rpN
                request.user.playerdata.save()
                r = Record(AI1=request.user.playerdata,
                           AI2=competitor,
                           rpyNumber=rpN)
                r.save()
            else:
                error = 'RUN FAIL\n' + fight.stdout.decode('utf-8')
=======
        running = request.user.playerdata.running
        if has_submitted == True and request.user.playerdata.running == False:
            error = ''
            print(os.path.join(settings.BASE_DIR,'..', '..', 'ts18', 'server', 'compile.sh') + ' %s_%s' % (request.user.username, request.user.id))
            cpl = subprocess.run(os.path.join(settings.BASE_DIR,'..', '..', 'ts18', 'server', 'compile.sh') + ' %s_%s' % (request.user.username, request.user.id),
                                         shell=True, stdout=subprocess.PIPE)

            if cpl.returncode == 0: #compile completed
                fight = subprocess.run(os.path.join(settings.BASE_DIR, '..','..', 'ts18', 'server', 'fight_server.sh')+' %s_%s %s_%s' %
                                              (request.user.username, request.user.id,
                                              competitor.player.username, competitor.player.id),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       )

                if fight.returncode == 0:  # process running
                    request.user.playerdata.running = True
                    rpN =  fight.stdout.decode('utf-8')
                    request.user.playerdata.rpyNumber = rpN
                    request.user.playerdata.save()
                    r = Record(AI1=request.user.playerdata,
                               AI2=competitor,
                               rpyNumber=rpN)
                    r.save()
                else:
                    error = 'run fail,' + fight.stdout.decode('utf-8')
            else:
                error = 'compile fail,' + cpl.stdout.decode('utf-8')
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9

            record_list=request.user.playerdata.ai1_record.all()
            record_list2=request.user.playerdata.ai2_record.all()
            records = getRecords(record_list, record_list2, request.user.playerdata)

<<<<<<< HEAD
     #   return render(request, 'fight_myself.html', {'player':request.user.playerdata,
     #                                                'error':error,'records':records,
     #                                                })

    return render(request,'fight.html',{'player_list':players_list})
=======
        return render(request, 'fight_myself.html', {'player':request.user.playerdata,
                                                     'error':error,'records':records,
                                                     'running':request.user.playerdata.running})

    return render(request,'fight.html',{'player_list':players_list,'has_submitted':has_submitted})
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9






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
        settings.BASE_DIR, '..','..','ts18','submits', '%s_%s' % (request.user.username, request.user.id))
    request.user.playerdata.ai.name=os.path.join(
        'submits',
        '%s_%s' % (request.user.username, request.user.id),'playerMain.cpp')

    new_path=os.path.join(pathdir, 'playerMain.cpp')

    if not os.path.exists(pathdir):
        os.mkdir(pathdir)

    if os.path.exists(new_path):
        os.remove(new_path)

    os.rename(initial_path,new_path)
    request.user.playerdata.save()
    request.user.save()
<<<<<<< HEAD
    cpl = subprocess.run(os.path.join(settings.BASE_DIR,'..', '..', 'ts18', 'server', 'compile.sh') + ' %s_%s' % (request.user.username, request.user.id), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if cpl.returncode != 0:
        request.user.playerdata.ai.delete()
        return 'COMPILATION ERROR\n' + cpl.stdout.decode('utf-8')
=======
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9

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
<<<<<<< HEAD
            return render(request, 'fight_myself.html', {'player':request.user.playerdata,'error':error,'records':records})
=======
            return render(request, 'fight_myself.html', {'player':request.user.playerdata,'error':error,'records':records, 'running':running})
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9

    if running == True:
        # search the rpyfile and print the process
        rpyPath = os.path.join(settings.BASE_DIR, '..', '..', 'fight_result', request.user.playerdata.rpyNumber+'.rpy')
        if os.path.exists(rpyPath):
            request.user.playerdata.update(running=False)
            r = Record.objects.get(rpyNumber=request.user.playerdata.rpyNumber)
            r.log.path = rpyPath
            r.log.name = request.user.playerdata.rpyNumber+'.rpy'
            with open(os.path.join(settings.MEDIA_ROOT, 'fight_result', request.user.playerdata.rpyNumber+'.txt'),'r') as f:
                lines = f.readlines()
                last = lines[-1]
                if '0' in last:
                    r.scorechange = 1 # AI1 wins
<<<<<<< HEAD
                    r.AI1.score += 1
                    r.AI2.score -= 1
                elif '1' in last:
                    r.scorechange = -1 # AI2 wins
                    r.AI1.score -= 1
                    r.AI2.score += 1
=======
                elif '1' in last:
                    r.scorechange = -1 # AI2 wins
>>>>>>> 9c8b3b19e31cde0c07bd26f91136833a3dab16e9
            r.save()
            return HttpResponseRedirect(reverse('fight:myself'))

    return render(request, 'fight_myself.html', {'player':request.user.playerdata,'error':error,'records':records })

def aidownload(request):
    try:
        filename = request.GET['file']
    except:
        raise Http404
    player = get_object_or_404(Player, ai=filename)
    path = player.ai.path
    name = os.path.split(path)[-1]
    name = urllib.parse.quote(name)

    wrapper = FileWrapper(open(path, 'rb'))
    response = HttpResponse(wrapper)
    response['Content-Length'] = player.ai.size
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(name)[-1])
    return response

def logdownload(request):
    try:
        filename = request.GET['file']
    except:
        raise Http404
    Log = get_object_or_404(Record, log=filename)
    path = Log.log.path
    name = os.path.split(path)[-1]
    name = urllib.parse.quote(name)

    wrapper = FileWrapper(open(path, 'rb'))
    response = HttpResponse(wrapper)
    response['Content-Length'] = Log.log.size
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(name)[-1])
    return response


