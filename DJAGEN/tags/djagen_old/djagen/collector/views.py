# -*- coding: utf-8 -*-

# View definitions are created here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from djagen.collector.models import *
from djagen.collector.forms import ContactForm
from djagen.collector.wrappers import render_response
from django.conf import settings
import magic
import os
import datetime, time
from django.core.paginator import Paginator, EmptyPage, InvalidPage

import string

def main(request):
    selected_entries = Entries.objects.select_related()
    entries_list1 = selected_entries.filter(entry_id__label_personal = 1)
    entries_list2 = selected_entries.filter(entry_id__label_lkd = 1)
    entries_list3 = selected_entries.filter(entry_id__label_community = 1)
    entries_list = entries_list1 | entries_list2 | entries_list3
    
    # This setting gets the content truncated which contains more than <truncate_words> words.
    truncate_words = 250
    items_per_page = 25

    #get the last run time
    run_time = RunTime.objects.all()[0]
    
    return render_to_response('main.tmpl' ,{
                                            'entries_list':entries_list,
                                            'truncate_words':truncate_words,
                                            'items_per_page':repr(items_per_page),
                                            'run_time':run_time,
                                            #'pag_entries_list':pag_entries_list,
                                            
                                            

                                            })
def member_subscribe(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        #return HttpResponse(str(request.FILES))
        if form.is_valid():
            human = True
            check = handle_uploaded_file(request.FILES['hackergotchi'])
                
            #save the author information
            f = request.FILES['hackergotchi']
            if check[0]:

                #change the name of the file with the unique name created
                f.name = check[1]

                author = Authors(author_name=request.POST['name'], author_surname=request.POST['surname'], author_email=request.POST['email'], channel_url=request.POST['feed'], author_face=f.name, is_approved=0, current_status=5)
            else:
                author = Author(author_name=request.POST['name'], author_surname=request.POST['surname'], author_email=request.POST['email'], channel_url=request.POST['feed'], is_approved=0, current_status=5)
            try:
                author.save()
            
                #save the history with explanation
                author.history_set.create(action_type=5, action_date=datetime.datetime.now(), action_explanation=request.POST['message'])
            except:
                pass
            #send mail part
            #fill it here
            return render_response(request, 'main/subscribe.html/',{'submit': 'done'})
    else:
        form = ContactForm()
    return render_response(request, 'main/subscribe.html', {'form': form})

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

    return render_response(request, 'main/members.html', {'members': authors})


def archive(request,archive_year='',archive_month=''):
    selected_entries = Entries.objects.select_related()
    
    # For entry categories
    entries_list1 = selected_entries.filter(entry_id__label_personal = 1)
    entries_list2 = selected_entries.filter(entry_id__label_lkd = 1)
    entries_list3 = selected_entries.filter(entry_id__label_community = 1)
    entries_list = entries_list1 | entries_list2 | entries_list3    
    
    error = ''
    
    # Validating arguments provided by urls.py.
    if((archive_year != '' ) and (str(archive_year).isalnum()) and (not(str(archive_year).isalpha()))):
        entries_list = entries_list.filter(date__year=archive_year)
    else:
        error = 1
        
    if(archive_month != ''and (str(archive_year).isalnum()) and not(str(archive_year).isalpha())):
        entries_list = entries_list.filter(date__month=archive_month)
    ##    error = 1                                               

    # This setting gets the content truncated which contains more than <truncate_words> words.
    truncate_words = 250
    items_per_page = 25
    
    #get the last run time
    run_time = RunTime.objects.all()[0]
    
    # Pagination
    elements_in_a_page = 25 # This determines, how many elements will be displayed in a paginator page.
    paginator = Paginator(entries_list,elements_in_a_page)
    
    # Validation for page number if it is not int return first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
        
    # If page request is out of range, return last page .
    try:
        p_entries_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        p_entries_list = paginator.page(paginator.num_pages)
   
   
    
    
    
    return render_to_response('archive.tmpl' ,{
                                'entries_list':entries_list,
                                'p_entries_list':p_entries_list,
                                'truncate_words':truncate_words,
                                'items_per_page':repr(items_per_page),
                                'run_time':run_time,
                                'archive_year':archive_year,
                                'archive_month':archive_month,
                                'error':error,
                                })