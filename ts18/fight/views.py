from django.shortcuts import render, get_object_or_404
from .models import Player, Record
from django.conf import settings
from django.http import HttpResponse, Http404
from wsgiref.util import FileWrapper
from itertools import chain
from operator import attrgetter
import os
import urllib


def index(request):
    has_submitted=False
    if request.user.is_authenticated():
        try:
            data=Player.objects.get(player=request.user)
        except :
            data = Player(player = request.user)
            data.save()
        if request.user.playerdata.ai!=None:
            has_submitted=True

    players_list=Player.objects.exclude(ai = None)

    if request.method=='POST':
        compete_id=request.POST.get('compete_id','')
        try:
            competitor=Player.objects.get(id=compete_id)
        except Player.DoesNotExsit:
            if request.user.is_authenticated():
                return render(request,'fight_after_login.html',{'player_list':players_list,'has_submitted':has_submitted})
            else:
                return render(request,'fight.html',{'player_list':players_list,'has_submitted':has_submitted})
        if has_submitted==True:
            pass#接入api


    if request.user.is_authenticated():
        return render(request,'fight_after_login.html',{'player_list':players_list,'has_submitted':has_submitted})
    else:
        return render(request,'fight.html',{'player_list':players_list,'has_submitted':has_submitted})






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
        request.user.playerdata.ai.name = os.path.join('ai_submit', os.path.split(old_name)[-1])
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
    suffix = name.split('.')[-1]
    request.user.playerdata.ai.name=os.path.join(
        'ai_submit',
        'ai_%s_%s.%s' % (request.user.username, request.user.id, suffix)
    )
    new_path=os.path.join(settings.MEDIA_ROOT, request.user.playerdata.ai.name)
    if os.path.exists(new_path):
        os.remove(new_path)
    os.rename(initial_path,new_path)
    request.user.playerdata.save()
    request.user.save()

def myself(request):
    try:
        data=Player.objects.get(player=request.user)
    except :
        data = Player(player = request.user)
        data.save()
    error=''
    record_list=[]
    records=[]
    record_list=request.user.playerdata.ai1_record.all()
    record_list2=request.user.playerdata.ai2_record.all()
    record_list = sorted(chain(record_list,record_list2), key=attrgetter('time'),reverse=False)

    if not record_list==[]:
        for record in record_list:
            r={}
            r['time']=record.time
            r['log']=record.log
            if record.AI1==request.user.playerdata:
                r['scorechange']=record.scorechange
                r['competitor']=record.AI2
                if record.scorechange>0:
                    r['result']='胜利'
                elif record.scorechange<0:
                    r['result']='失败'
                else:
                    r['result']='平局'
            if record.AI2==request.user.playerdata:
                r['scorechange']=-record.scorechange
                r['competitor']=record.AI1
                if record.scorechange<0:
                    r['result']='胜利'
                elif record.scorechange>0:
                    r['result']='失败'
                else:
                    r['result']='平局'
            records.append(r)

    if request.method=='POST':
        if request.user.is_authenticated():
            error = Get_AI(request)
            return render(request, 'fight_myself.html', {'player':request.user.playerdata,'error':error,'records':records})

    return render(request, 'fight_myself.html', {'player':request.user.playerdata,'error':error,'records':records})

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


