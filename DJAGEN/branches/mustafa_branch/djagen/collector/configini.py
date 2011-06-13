#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from django.conf import settings
from djagen.collector.models import *
import ConfigParser

class Handler:

    def __init__(self, id):

        self.id = id

        self.tmp_entries_ini = os.path.join(settings.MAIN_PATH, 'tmp_ini', 'tmp_entries.ini')

        self.config_header_ini = os.path.join(settings.MAIN_PATH, 'gezegen', 'config_header.ini')

        self.config_entries_ini = os.path.join(settings.MAIN_PATH, 'gezegen', 'config_entries.ini')

    def __set_values(self):

        author = Authors.objects.get(author_id = self.id)
        print author
        print author.author_id

        if not author.is_approved:
            return False

        self.name = author.author_name 
        self.surname = author.author_surname
        self.face = author.author_face 
        self.url = author.channel_url

        labels = {
                  author.label_personal:'Personal', 
                  author.label_lkd: 'LKD', 
                  author.label_community: 'Community', 
                  author.label_eng: 'Eng',
                  }

        label_li = [k for k,v in labels.iteritems() if v==1]
        self.author_labels = " ".join(label_li)

        return True

    def create_tmp_entries(self):

        if not self.__set_values(): return 

        config_entries = open(self.config_entries_ini)
        tmp_entries = open(self.tmp_entries_ini, 'w')
        config_header = open(self.config_header_ini)

        Config = ConfigParser.ConfigParser()
        Config.read(self.config_entries_ini)
        sections = Config.sections()
        header = config_header.read()
        config_header.close()
        tmp_entries.write(header)
        found = False
        for section in sections:
            if (section == 'Planet'):
                continue

            config_name = Config.get(section, 'name')
            config_label = Config.get(section, 'label')
            config_id = Config.get(section, 'id')
            config_url = section

            try:
                config_face = Config.get(section, 'face')
            except:
                config_face = None

            if config_id == self.id:
                found = True

                url = self.url
                face = self.face
                name = self.name
                surname = self.surname
                label = self.author_labels
                id = self.id

            else:

                url = config_url
                face = config_face
                name = config_name
                surname = config_name
                label = config_label
                id = config_id

            s = '['+url+']' + '\n'
            s += 'name = ' + name + '\n'
            s += 'surname = ' + surname + '\n'
            s += 'label = ' + label + '\n'
            if face:
                s += 'face = ' + face + '\n'
            s += 'id = ' + id + '\n' + '\n'

            tmp_entries.write(s)

        if found != True:
            url = self.url
            face = self.face
            name = self.name
            surname = self.surname
            label = self.author_labels

            id = self.id
            s = '['+url+']' + '\n'
            s += 'name = ' + name + '\n'
            s += 'surname = ' + surname + '\n'
            s += 'label = ' + label + '\n'
            if face:
                s += 'face = ' + face + '\n'
            s += 'id = ' + str(id) + '\n' + '\n'
            tmp_entries.write(s)

        tmp_entries.close()

