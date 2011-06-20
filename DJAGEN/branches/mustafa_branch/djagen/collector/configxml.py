#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from xml.dom import minidom

class Handler:

    def __init__(self):

        self.main_url = "/home/oguz/django-projects/djagen/gezegen"
        self.gezegen_url = os.path.join(self.main_url,"gezegen")
        self.entries_xml = os.path.join(self.gezegen_url, "config_entries.xml")
        self.header_xml = os.path.join(self.gezegen_url, 'config_header.xml')
        self.tmp_ini_dir_path = os.path.join(self.main_url, "tmp_ini")

    def get_doc(self, type="entries"):

        if type == "entries":
            self.doc = minidom.parse(self.entries_xml)
        else:
            self.doc = minidom.parse(self.header_xml)
        return self.doc

    def get_tag_entries(self,tag):

        self.entries = self.doc.getElementsByTagName(tag)
        return self.entries

    def set_ini_variables(self, id, name, feed, nick, face, label):

        self.tmp_ini = {'id': id, 'name': name, 'feed': feed, 'nick': nick, 'face': face, 'label': label}

    def open_file(self):
        path = os.path.join(self.tmp_ini_dir_path, 'tmp.ini')
        self.f = open(path, "w")

    def create_header(self):

        for header in self.entries:

            children = header.childNodes
            for child in children:
                if child.nodeType == child.TEXT_NODE: continue
                else:
                    node_name = child.nodeName
                    f_child = child.firstChild
                    node_value = f_child.nodeValue

                    s = []
                    if node_name != "header_name":
                        s.append(node_name)
                        s.append("=")
                    s.append(node_value)
                    s.append("\n")
                    ss = " ".join(s)
                    self.f.write(ss)

    def traverse(self):

        for entry in self.entries:

            nodes = entry.childNodes

            for node in nodes:

                child = node.firstChild
                self.face = None

                if node.nodeType == node.TEXT_NODE: continue

                if node.nodeName == "feed":
                    self.feed = child.toxml()

                if node.nodeName == "name":
                    self.name = child.toxml()

                if node.nodeName == "nick":
                    self.nick = child.toxml()

                if node.nodeName == "label":
                    self.label = child.toxml()

                if node.nodeName == "face":
                    self.face = child.toxml()

                if node.nodeName == "id":
                    self.id = child.toxml()

            if int(self.tmp_ini['id']) == int(self.id):

                self.write_to_file(self.tmp_ini)

            else:

                config = {'id': self.id, 'name': self.name, 'feed': self.feed, 'nick': self.nick, 'label': self.label, 'face': self.face}
                self.write_to_file(config)


    def write_to_file(self, dic):

        feed = "feed = " + dic['feed'] + "\n"
        name = "name = " + dic['name'] + "\n"
        nick = "nick = " + dic['nick'] + "\n"
        label = "label = " + dic['label'] + "\n"
        id = "id = " + dic['id'] + "\n"

        self.f.write("\n")
        self.f.write(feed)
        self.f.write(name)
        self.f.write(nick)
        if dic['face']:
            face = "face = " + dic['face'] + "\n"
            self.f.write(face)
        self.f.write(label)
        self.f.write(id)

    def close_file(self):
        self.f.close()


