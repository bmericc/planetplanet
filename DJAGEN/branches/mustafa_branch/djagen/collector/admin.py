#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from djagen.collector.models import *

from django.conf import settings

import os
import datetime
import shutil

from djagen.collector.configini import *

class AuthorsAdmin (admin.ModelAdmin):

    list_display = ('author_id', 'author_name', 'author_email', 'author_face', 'current_status', 'is_approved', 'label_personal', 'label_lkd', 'label_community', 'label_eng')
    list_select_related = True

    search_fields = ['author_name', 'author_surname', 'author_email']

    def save_model(self, request, obj, form, change):

        #get the values for saving
        author_name = obj.author_name
        author_surname = obj.author_surname
        author_face = obj.author_face
        channel_url = obj.channel_url

        current_status = obj.current_status
        is_approved = obj.is_approved

        #creating the history
        now = datetime.datetime.now()
        action_type = current_status

        author_id = obj.author_id
        if author_id:
            #then this is an update
            author = Authors.objects.get(author_id = author_id)
            pre_status = author.is_approved
            current_status = obj.is_approved
            obj.save()
        else:
            obj.save()
            author = Authors.objects.get(author_name=author_name, author_surname=author_surname, channel_url=channel_url)
            pre_status = None
            current_status = author.is_approved

        author.history_set.create(action_type=action_type, action_date=now, action_owner=request.user.username)


        #create tmp_config.ini here
        handler = Handler(author.author_id)
        handler.create_tmp_entries()

        if pre_status != current_status:
            a_face = author.author_face

            images_path = os.path.join(settings.MAIN_PATH, 'www', 'images')
            heads_path = os.path.join(images_path, 'heads')
            face_path = os.path.join(heads_path, a_face)

            tmp_image_path = os.path.join(settings.MAIN_PATH, 'temp_ini', a_face)

            if os.path.exists(tmp_image_path):
                shutil.move(tmp_image_path, face_path)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'action_date', 'action_author', 'action_owner')

admin.site.register(History, HistoryAdmin)
admin.site.register(Authors, AuthorsAdmin)

