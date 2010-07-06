# -*- coding: utf-8 -*-

# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponse
from djagen.collector.models import *
from djagen.collector.forms import ContactForm
from djagen.collector.wrappers import render_response
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
import magic
import os
import datetime, time

BASE_URL = settings.BASE_URL


def main(request):
    selected_entries = Entries.objects.select_related()
    entries_list1 = selected_entries.filter(entry_id__label_personal = 1)
    entries_list2 = selected_entries.filter(entry_id__label_lkd = 1)
    entries_list3 = selected_entries.filter(entry_id__label_community = 1)
    entries_list = entries_list1 | entries_list2 | entries_list3
    # This setting truncating content which has more than <truncate_words> words.
    truncate_words = 250
    items_per_page = 25

    #get the last run time
    run_time = RunTime.objects.all()[0]

    #get the last entries' date
    last_entry_date = Entries.objects.all()[0].date
    day = datetime.timedelta(days=1)
    last_date_li = []
    for x in xrange(6):
        last_entry_date -= day
        last_date_li.append(last_entry_date)

    return render_response(request, 'main/main.html' ,{
                                            'entries_list':entries_list,
                                            'truncate_words':truncate_words,
                                            'items_per_page':repr(items_per_page),
                                            'run_time':run_time,
                                            'BASE_URL': BASE_URL,
                                            'last_date_li': last_date_li,
                                            })

def member_subscribe(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        #return HttpResponse(str(request.FILES))
        if form.is_valid():
            human = True
            try:
                check = handle_uploaded_file(request.FILES['hackergotchi'])
            except MultiValueDictKeyError:
                check = (False, '')
                
            #save the author information
            if check[0]:
                f = request.FILES['hackergotchi']

                #change the name of the file with the unique name created
                f.name = check[1]

                author = Authors(author_name=request.POST['name'], author_surname=request.POST['surname'], author_email=request.POST['email'], channel_url=request.POST['feed'], author_face=f.name, is_approved=0, current_status=5)
            else:
                author = Authors(author_name=request.POST['name'], author_surname=request.POST['surname'], author_email=request.POST['email'], channel_url=request.POST['feed'], is_approved=0, current_status=5)
                author.save()
            
                #save the history with explanation
                author.history_set.create(action_type=5, action_date=datetime.datetime.now(), action_explanation=request.POST['message'])
            #send mail part
            #fill it here
            return render_response(request, 'main/subscribe.html/',{'submit': 'done', 'BASE_URL': BASE_URL})
    else:
        form = ContactForm()
    return render_response(request, 'main/subscribe.html', {'form': form, 'BASE_URL': BASE_URL})

def handle_uploaded_file(f):

    if not f.name: return False
    #lets create a unique name for the image
    t = str(time.time()).split(".")
    img_name = t[0] + t[1].f.name.split(".")[1]
    f.name = img_name
    path = os.path.join(settings.FILE_UPLOAD_TEMP_DIR, f.name)
    
    destination = open(path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

    m = magic.open(magic.MAGIC_MIME)
    m.load()
    t = m.file(path)
    if t.split('/')[0] == 'image':
        return (True, f.name)
    else:
        os.unlink(path)
        return (False, '')

def list_members(request):

    authors = Authors.objects.all()

    return render_response(request, 'main/members.html', {'members': authors, 'BASE_URL': BASE_URL})
