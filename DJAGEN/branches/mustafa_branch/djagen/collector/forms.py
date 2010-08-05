#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField

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
    q_date_year = forms.DateField(input_formats = '%y',required = False, label = 'Blog girdisine ait yıl(Örn:2010)', widget=forms.widgets.DateTimeInput())
    q_date_month = forms.DateField(input_formats = '%m',required = False, label = 'Blog girdisine ait ay(Örn:03)', widget=forms.widgets.DateTimeInput())
    q_date_day = forms.DateField(input_formats = '%d',required = False, label = 'Blog girdisine ait gün (Örn:27)', widget=forms.widgets.DateTimeInput())
