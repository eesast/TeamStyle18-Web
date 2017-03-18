                last = lines[-1]
                a = r.AI1.score
                b = r.AI2.score
                wea = 1.0/(1+10**((b-a)/400.0))
                web = 1.0/(1+10**((a-b)/400.0))
                if '0' in last:
                    r.scorechange = 1 #max([0,(2*b-a)//4]) # AI1 wins
                    r.AI1.score = int(a+32*(1-wea))	 
                    r.AI2.score = int(b+32*(0-web))
                elif '1' in last:
                    r.scorechange = -1 # -max([0,(a-b/2)//4]) # AI2 wins
                    r.AI1.score = int(a+32*(0-wea))
                    r.AI2.score = int(b+32*(1-web))
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
                    error = 'turn:' + last.split()[-1]

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


