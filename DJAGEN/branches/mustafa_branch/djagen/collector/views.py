# -*- coding: utf-8 -*-

# View definitions are created here.
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from djagen.collector.models import *
from djagen.collector.forms import ContactForm, QueryForm
from djagen.collector.wrappers import render_response
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
import magic
import os
import datetime, time
from django.core.paginator import Paginator, EmptyPage, InvalidPage

import string

BASE_URL = settings.BASE_URL

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

    #get the last entries' date
    last_entry_date = Entries.objects.all()[0].date
    day = datetime.timedelta(days=1)
    last_date_li = []
    for x in xrange(5):
        last_entry_date -= day
        last_date_li.append(last_entry_date)

    return render_response(request, 'main/main.html' ,{
                                            'entries_list':entries_list,
                                            'truncate_words':truncate_words,
                                            'items_per_page':repr(items_per_page),
                                            'run_time':run_time,
                                            #'pag_entries_list':pag_entries_list,
                                            'BASE_URL': BASE_URL,
                                            'last_date_li': last_date_li,
                                            'info_area':'main',
                                            })
def member_subscribe(request):
    info_area = 'subscribe'

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        #return HttpResponse(str(request.FILES))
        if form.is_valid():
            human = True
            try:
                check = handle_uploaded_file(request.FILES['hackergotchi'])
            except MultiValueDictKeyError:
                check = (False,False)
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
            return render_response(request, 'main/subscribe.html/',{'submit': 'done', 'BASE_URL': BASE_URL,'info_area':info_area})
    else:
        form = ContactForm()
    return render_response(request, 'main/subscribe.html', {'form': form, 'BASE_URL': BASE_URL,'info_area':info_area})

def handle_uploaded_file(f):

    if not f.name: return False
    #lets create a unique name for the image
    t = str(time.time()).split(".")
    img_name = t[0] + t[1] + f.name.split(".")[1]
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

def list_archives(request):

    entries_list = Entries.objects.select_related()
    ava_years = entries_list.dates('date','year',order='DESC')
    archives_list  = []
    for date in ava_years:
        ava_months = entries_list.filter(date__year = date.year).dates('date','month',order='DESC')
        for month in ava_months:
            ava_days = entries_list.filter(date__year = date.year).filter(date__month = month.month).dates('date','day',order='DESC')
            a = (date,ava_months,ava_days)
        archives_list.append(a)

    return render_to_response('main/archives.html', { 'archives_list': archives_list, 'BASE_URL':BASE_URL})


def list_members(request):
    info_area = 'members'

    authors = Authors.objects.all()

    return render_response(request, 'main/members.html', {'members': authors, 'BASE_URL': BASE_URL,'info_area' : info_area })

def __search(cleaned_data):
    cdata = cleaned_data
    q_author_name = cdata.get('q_author_name','')
    q_author_surname = cdata.get('q_author_surname','')
    q_text = cdata.get('q_text','')

    q_date_from = cdata.get('q_date_from','')
    q_date_till = cdata.get('q_date_till','')

    q_label_personal = cdata.get('q_label_personal','')
    q_label_community = cdata.get('q_label_community','')
    q_label_lkd = cdata.get('q_label_lkd','')
    q_label_eng = cdata.get('q_label_eng','')

    entries_list = Entries.objects.select_related()
        # Name - surname queries.

    if(q_author_name):
        entries_list = entries_list.filter(entry_id__author_name__iexact = q_author_name)
    if(q_author_surname):
        entries_list = entries_list.filter(entry_id__author_surname__iexact = q_author_surname)

    # Label based queries.
    if(q_label_personal == True):
        entries_list = entries_list.filter(entry_id__label_personal = 1)
    if(q_label_community == True):
        entries_list = entries_list.filter(entry_id__label_community = 1)
    if(q_label_lkd == True):
        entries_list = entries_list.filter(entry_id__label_lkd = 1)
    if(q_label_eng == True):
        entries_list = entries_list.filter(entry_id__label_eng = 1)


    # Text search.
    if(q_text):
        entries_list = entries_list.filter(content_text__icontains = q_text)

    # Date based queries.
    if(q_date_from and q_date_till):
        entries_list = entries_list.filter(date__range = (q_date_from,q_date_till))

    return entries_list


def query(request):

    # Determine if method is  POST.
    if (request.method == 'POST'):
        ## If Yes:
        form = QueryForm(request.POST)

        # Determine if all of them were valid.
        if (form.is_valid()):
            cdata = form.cleaned_data
            entries_list = __search(cdata)
            p_entries_list = entries_list

            truncate_words = 250
            items_per_page = 25

            #get the last run time
            run_time = RunTime.objects.all()[0]
            info_area = 'search'

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
          #--



            return render_to_response('main/searchresult.html' ,{
                                'entries_list':entries_list,
                                'p_entries_list':p_entries_list,
                                'truncate_words':truncate_words,
                                'items_per_page':repr(items_per_page),
                                'run_time':run_time,
                                'info_area':info_area,
                                #'q_author_name':q_author_name,
                                #'q_author_surname':q_author_surname,
                                #'q_text':q_text,
                                'BASE_URL':BASE_URL,
                                })



        """else:
           # Issue an error message and show the form again.
            form = SearchForm(request.POST)
            info_area = "query"

            return render_to_response('main/query.html', {'q_form': form, 'BASE_URL': BASE_URL,'info_area':info_area})"""
    else:
        # Show the form.

        info_area = 'query'
        form = QueryForm()

    return render_to_response('main/query.html', {'q_form': form, 'BASE_URL': BASE_URL,'info_area':info_area})


def archive(request,archive_year=None,archive_month=None,archive_day=None,label=None):
    info_area = 'archive'
    # This setting gets the content truncated which contains more than <truncate_words> words.
    truncate_words = 250
    items_per_page = 25

    #get the last run time
    run_time = RunTime.objects.all()[0]

 # Now we are creating few scenarios depending on the incoming variables.
    # This part is for validation.
    if ('q_author_name' in request.GET and request.GET['q_author_name']): #If that exists and not empty
        q_author_name = request.GET['q_author_name']
    else:
        q_author_name = ""
    if ('q_author_surname' in request.GET and request.GET['q_author_surname']): #If that exists and not empty
        q_author_surname = request.GET['q_author_surname']
    else:
        q_author_surname = ""
    if ('q_text' in request.GET and request.GET['q_text']): #If that exists and not empty
        q_text = request.GET['q_text']
    else:
        q_text = ""
    if ((label == "personal") or 'q_label_personal' in request.GET and request.GET['q_label_personal'] == '1'): #If that exists and not empty
        q_label_personal = 1
    else:
        q_label_personal = ""
    if ((label == "community") or 'q_label_community' in request.GET and request.GET['q_label_community'] == '1'):
        q_label_community = 1
    else:
        q_label_community = ""

    if ((label == "lkd") or 'q_label_lkd' in request.GET and request.GET['q_label_lkd']=='1'):
        q_label_lkd = 1
    else:
        q_label_lkd = ""
    if ((label == "eng") or 'q_label_eng' in request.GET and request.GET['q_label_eng']=='1'):
        q_label_eng = 1
    else:
        q_label_eng = ""
    #--
#--

# Querying
    entries_list = Entries.objects.select_related()
        # Name - surname queries.

    if(q_author_name):
        entries_list = entries_list.filter(entry_id__author_name__iexact = q_author_name)
        if(q_author_surname):
            entries_list = entries_list.filter(entry_id__author_surname__iexact = q_author_surname)
    elif(q_author_surname):
        entries_list = entries_list.filter(entry_id__author_surname__iexact = q_author_surname)

    # Label based queries.
    if(q_label_personal):
        entries_list = entries_list.filter(entry_id__label_personal = 1)
    if(q_label_community):
        entries_list = entries_list.filter(entry_id__label_community = 1)
    if(q_label_lkd):
        entries_list = entries_list.filter(entry_id__label_lkd = 1)
    if(q_label_eng):
        entries_list = entries_list.filter(entry_id__label_eng = 1)



    # Text search.
    if(q_text):
        entries_list = entries_list.filter(content_text__icontains = q_text)
    # Date based queries.
    if(archive_year):
        entries_list = entries_list.filter(date__year = archive_year)
        if(archive_month):
            entries_list = entries_list.filter(date__month = archive_month)
            if(archive_day):
                entries_list = entries_list.filter(date__day = archive_day)

#--

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
  #--

    return render_to_response('main/archive.html' ,{
                        'entries_list':entries_list,
                        'p_entries_list':p_entries_list,
                        'truncate_words':truncate_words,
                        'items_per_page':repr(items_per_page),
                        'run_time':run_time,
                        'info_area':info_area,
                        'archive_year' : archive_year,
                        'archive_month' : archive_month,
                        'archive_day' : archive_day,
                        'q_author_name':q_author_name,
                        'q_author_surname':q_author_surname,
                        'q_text':q_text,
                        'BASE_URL':BASE_URL,
                        })

def issue_error(request,error_msg=None):
    info_area = 'error'
    if not(error_msg):
        error_msg = 'Bilinmeyen bir hata oluştu!'
    return render_response(request, 'main/error.html', {'error_msg': error_msg,'info_area' : info_area })
