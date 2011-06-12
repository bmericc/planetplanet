#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField
from datetime import date
from django.contrib.admin import widgets

class ContactForm(forms.Form):

    name = forms.CharField(max_length=25, required=True, error_messages={'required': 'Lütfen adınızı giriniz'}, label='Adınız')
    surname = forms.CharField(max_length=25, required=True, error_messages={'required': 'Lütfen soyadınızı giriniz'}, label='Soyadınız')
    email = forms.EmailField(required=True, error_messages={'required': 'Size ulaşabileceğimiz eposta adresinizi giriniz'}, label='Eposta Adresiniz')
    hackergotchi = forms.FileField(required=False, label='Hacketgotchiniz', help_text='Max 80*80 pixellik Gezegende görünmesini istediğiniz fotoğrafınız')
    feed = forms.URLField(required=True, label='Besleme adresiniz', help_text='Günlüğünüzün XML kaynağının adresi')
    message = forms.CharField(required=False, label='İletişim Mesajınız', widget=forms.widgets.Textarea())
    #field for captcha
    captcha = CaptchaField(label="Captcha Alanı", help_text='Gördüğünü karakterleri aynen yazınız', error_messages={'required': 'Hatalı yazdınız!'})

class QueryForm(forms.Form):
    q_author_name = forms.CharField(max_length=25, required = False, label = 'Adı')
    q_author_surname = forms.CharField(max_length=25, required = False, label = 'Soyadı')
    q_text = forms.CharField(required = False, label = 'Aradığınız metin', widget = forms.widgets.Textarea() )

    q_label_personal = forms.BooleanField(required = False, label = 'Kişisel Günlükler', initial = True)
    q_label_lkd = forms.BooleanField(required = False, label = 'LKD Günlükleri', initial = True)
    q_label_community = forms.BooleanField(required = False, label = 'Topluluk Günlükleri')
    q_label_eng = forms.BooleanField(required = False, label = 'İngilizce Günlükler')


    q_date_from = forms.DateField(required = False, initial=date.today,label = "Şurdan",widget = widgets.AdminDateWidget() )
    q_date_till = forms.DateField(required = False, initial=date.today,label = "Şuraya",widget = widgets.AdminDateWidget() )
