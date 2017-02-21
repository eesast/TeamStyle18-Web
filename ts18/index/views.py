# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse, Http404
from django.urls import reverse
from django.conf import settings
from wsgiref.util import FileWrapper
import os
import urllib

def intro(request):

    return render(request, 'intro.html')

def index(request):

    return render(request, 'index.html')

def rule(request):

    return render(request, 'rule.html')

