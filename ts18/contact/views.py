from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, mail_admins, BadHeaderError
from contact.forms import ContactForm
def contact(request):

    success_submit = False

    if request.method == 'POST':

        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            try:
           #     send_mail( subject,
           #               message,
           #               email,
           #               ['mildwindyu@hotmail.com'],
           #               fail_silently=False,
           #     )
                mail_admins(cd['subject'], cd['message']+'\r\n'+cd['email'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            success_submit = True
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form':form, 'success_submit' : success_submit})

# Create your views here.
