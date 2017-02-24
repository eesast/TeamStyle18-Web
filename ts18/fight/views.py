from django.shortcuts import render, get_object_or_404
from .models import Player, Record
from django.conf import settings
from django.http import HttpResponse, Http404
from wsgiref.util import FileWrapper
import os
import urllib


def index(request):
    try:
        data=Player.objects.get(player=request.user)
    except :
        data = Player(player = request.user)
        data.save()
    has_submitted=False
    players_list=Player.objects.exclude(ai = None)
    if request.user.playerdata.ai!=None:
        has_submitted=True
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

    else:
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
    old_name = data.ai.name
    if not 'aiupload' in request.FILES:
        return '请上传一个文件'

    file=request.FILES['aiupload']
    name=file.name.lower()

    if not name.endswith(('.cpp','.c')):
        return '请上传cpp或c格式的文件'
    # for compatibale reason
    if old_name.startswith('/'):
        data.ai.name = os.path.join('ai_submit', os.path.split(old_name)[-1])
        data.save()
    try:
        old_path = data.ai.path
        if os.path.exists(old_path):
            os.remove(old_path)
    except:
        pass

    # bind the new avatar to profile
    data.ai=file
    data.save()
    initial_path=data.ai.path

    # rename the new avatar to a regular name, and meanwhile, place the avatar
    # at a required place (using os.rename)
    suffix = name.split('.')[-1]
    data.ai.name=os.path.join(
        'ai_submit',
        'ai_%s_%s.%s' % (request.user.username, request.user.id, suffix)
    )
    new_path=os.path.join(settings.MEDIA_ROOT, data.ai.name)
    os.rename(initial_path,new_path)
    data.save()

def myself(request):
    print(request.FILES)
    try:
        data=Player.objects.get(player=request.user)
    except :
        data = Player(player = request.user)
        data.save()
    error=''
    record_list=[]
    records=[]
    try:
        record_list=request.user.ai1_record.all()
    except:
        pass
    try:
        record_list+=request.user.ai2_record.all()
    except:
        pass
    if not record_list==[]:
        record_list=record_list.order_by('time')
        for record in record_list:
            r={}
            r['time']=record['time']
            r['log']=record['log']
            if record['AI1']==request.user:
                r['scorechange']=record['AI1_scorechange']
                r['competitor']=record['AI2']
                if record['result']=='0':
                    r['result']='胜利'
                if record['result']=='1':
                    r['result']='失败'
                else:
                    r['result']='平局'
            if record['AI2']==request.user:
                r['scorechange']=record['AI2_scorechange']
                r['competitor']=record['AI1']
                if record['result']=='1':
                    r['result']='胜利'
                if record['result']=='0':
                    r['result']='失败'
                else:
                    r['result']='平局'
            records.append(r)

    if request.method=='POST':
        if request.user.is_authenticated():
            print(error)
            error = Get_AI(request)
            print(error)
            return render(request, 'fight_myself.html', {'error':error,'records':records})
    return render(request, 'fight_myself.html', {'error':error,'records':records})



def download(request):
    try:
        filename = request.GET['file']
    except:
        raise Http404
    log = get_object_or_404(Record, log=filename)
    path = log.log.path
    name = os.path.split(path)[-1]
    name = urllib.parse.quote(name)

    wrapper = FileWrapper(open(path, 'rb'))
    response = HttpResponse(wrapper)
    response['Content-Length'] = log.log.size
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(name)[-1])
    return response

def rank(request):
    return None

# Create your views here.