# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse, Http404
from django.urls import reverse
from django.conf import settings
from wsgiref.util import FileWrapper
import os
import urllib

def introduction(request):

    return render(request, 'introduction.html')

def index(request):

    return render(request, 'index.html')

def rule(request):

    return render(request, 'rule.html')

def noticeIndex(request):

    notice_list = Notification.objects.all()
    return render(request, 'notice.html', {'notice_list' : notice_list})

def download(request):

    try:
        filename = request.GET['file']
    except:
        raise Http404


    notice = get_object_or_404(Notification, file_attached=filename)
    path = notice.file_attached.path
    name = os.path.split(path)[-1]
    name = urllib.parse.quote(name)

    wrapper = FileWrapper(open(path, 'rb'))
    response = HttpResponse(wrapper)
    response['Content-Length'] = notice.file_attached.size
#    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(os.path.split(name)[-1])
    return response

#    with open(the_file_name) as f:
#        c = f.read()
#    return HttpResponse(c)



# Create your views here.
