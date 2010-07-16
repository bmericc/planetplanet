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
    for x in xrange(6):
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
    info_area = 'members'

    authors = Authors.objects.all()

    return render_response(request, 'main/members.html', {'members': authors, 'BASE_URL': BASE_URL,'info_area' : info_area })

def query(request):

    q_form = QueryForm()

    return render_response(request,'main/query.html',{
                                                      'BASE_URL' : BASE_URL,
                                                      'q_form':q_form,
                                                      })

def archive(request,archive_year='',archive_month='',archive_day=''):

    # This setting gets the content truncated which contains more than <truncate_words> words.
    truncate_words = 250
    items_per_page = 25

    #get the last run time
    run_time = RunTime.objects.all()[0]


    ### Determine if the request object includes any querying input or not. ###

    if ( (request.GET) and ('q_author_name' in request.GET or 'q_author_surname' in request.GET or 'q_text' in request.GET ) ):
        # Switch to 'return the result of query' mode.
        info_area = 'query'

        #Querying
        #TODO: We should improve querying method implemented here.
        q_author_name,q_author_surname,q_text = '','',''
        authors = Authors.objects.all()
        if ( ('q_author_name' in request.GET) and (request.GET['q_author_name'] )):
            q_author_name = request.GET['q_author_name']
            authors = authors.filter(author_name__iexact = q_author_name)


        if (('q_author_surname' in request.GET) and (request.GET['q_author_surname'])):
            q_author_surname = request.GET['q_author_surname']
            authors = authors.filter(author_surname__iexact = q_author_surname)


        for item in authors:

            try:
                entries_list |= item.entries_set.all()
            except:
                entries_list = item.entries_set.all()

        if( ('q_text' in request.GET)and(request.GET['q_text'])):
            q_text = request.GET['q_text']
            if (q_author_name or q_author_surname):

                entries_list = entries_list.filter(content_text__icontains = q_text)
            else:
                entries_list = Entries.objects.filter(content_text__icontains = q_text)



        try:
            if(not(entries_list)):
                return HttpResponseRedirect(BASE_URL+"/query")
        except:
                return HttpResponseRedirect(BASE_URL+ "/query")

        #here is gonna be edited [X]
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

        return render_to_response('main/archive.html' ,{
                            'entries_list':entries_list,
                            'p_entries_list':p_entries_list,
                            'truncate_words':truncate_words,
                            'items_per_page':repr(items_per_page),
                            'run_time':run_time,
                            'info_area':info_area,
                            'q_author_name':q_author_name,
                            'q_author_surname':q_author_surname,
                            'q_text':q_text,
                            'BASE_URL':BASE_URL,
                            })
    ### If not ###
    else:
    #Switch to return the result of arguments provided mode(archive viewing mode).
            info_area = 'archive' # \This variable is used for determining which infoarea text should be used in "contenttop" div in /main/base.html

            selected_entries = Entries.objects.select_related()

            # For entry categories
            entries_list1 = selected_entries.filter(entry_id__label_personal = 1)
            entries_list2 = selected_entries.filter(entry_id__label_lkd = 1)
            entries_list3 = selected_entries.filter(entry_id__label_community = 1)
            entries_list = entries_list1 | entries_list2 | entries_list3

        ## Validating arguments provided by urls.py.
            # Check if archive_year is not empty and numeric.
            if((archive_year != '' ) and (str(archive_year).isalnum()) and (not(str(archive_year).isalpha()))):
                entries_list = entries_list.filter(date__year=archive_year)
            else:
                # Fall back to main view.
                return HttpResponseRedirect(BASE_URL+"/main")
                #pass

            # Check if archive_month is not empty and numeric.
            if(archive_month != ''and (str(archive_month).isalnum()) and not(str(archive_month).isalpha())):
                entries_list = entries_list.filter(date__month=archive_month)

            # Check if archive_day is not empty and numeric.
            if(archive_day != ''and (str(archive_day).isalnum()) and not(str(archive_day).isalpha())):
                entries_list = entries_list.filter(date__day=archive_day)
        ##


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




            return render_to_response('main/archive.html' ,{
                                        'entries_list':entries_list,
                                        'p_entries_list':p_entries_list,
                                        'truncate_words':truncate_words,
                                        'items_per_page':repr(items_per_page),
                                        'run_time':run_time,
                                        'archive_year':archive_year,
                                        'archive_month':archive_month,
                                        'archive_day':archive_day,
                                        #'error':error,
                                        'BASE_URL':BASE_URL,
                                        'info_area':info_area,
                                        })
