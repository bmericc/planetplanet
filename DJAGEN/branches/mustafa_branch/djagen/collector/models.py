from django.db import models
import datetime, unicodedata, random, time
import re

# Create your models here.
ACTION_CHOICES = (
        (1, u'Removed'),
        (2, u'Approved'),
        (3, u'Paused'),
        (4, u'Readded'),
        (5, u'Applied'),
        (6, u'Editted')
    )

class Authors (models.Model):
    author_id = models.AutoField(primary_key=True, help_text="Author ID")
    author_name = models.CharField(max_length=50, help_text="Author Name")
    author_surname = models.CharField(max_length=50, help_text="Author Name")
    #we dont keep emails at the config.ini files, this part should be entered at the admin page
    author_email = models.EmailField(null=True, blank=True, help_text="Author Email Address")
    #the png file name of the author
    author_face = models.CharField(max_length=30, null=True, blank=True, help_text="Author Face Name")
    channel_subtitle = models.TextField(null=True, blank=True, help_text="Channel Subtitle")
    channel_title = models.TextField(null=True, blank=True, help_text="Channel Title")
    #URL of the feed.
    channel_url = models.URLField(help_text="Channel URL")
    #Link to the original format feed
    channel_link = models.URLField(null=True, blank=True, help_text="Channel Link")
    channel_urlstatus = models.IntegerField(null=True, blank=True, help_text="Channel URL Status")

    #use this field to check whether the author is shown on the planet or not, like banned situations
    current_status = models.SmallIntegerField(default=2, choices=ACTION_CHOICES, help_text="Current Status of the Author")
    #whether the application to the planet is approved, the approved ones will be shown at the planet
    is_approved = models.BooleanField(default=1, help_text="Approve Status of the Author")

    #planets that the channel belongs to
    #at the config.ini the entries should be obe of the belows:
    #label = Personal
    #label = LKD
    #label = Eng
    #label = Community
    label_personal = models.BooleanField(default=1, help_text="Channnels at the Personal Blog Page")
    label_lkd = models.BooleanField(default=0, help_text="Channels that are belong to LKD Blogs")
    label_community = models.BooleanField(default=0, help_text="Channels that are belong to some community blogs")
    label_eng = models.BooleanField(default=0, help_text="Channels that have English entries")
    #at the main page, lets just show personal and lkd for now, for communities lets ask them a special rss

    def __unicode__(self):
        return u'%s %s' % (self.author_name, self.author_surname)

    class Meta:
        #order according to the author_name, ascending
        ordering = ['author_name']

# keep the history for the action that are done on the member urls
class History (models.Model):
    action_type = models.SmallIntegerField(choices=ACTION_CHOICES)
    action_date = models.DateTimeField()
    action_explanation = models.TextField(help_text="Reason of Action", blank=True, null=True)
    action_author = models.ForeignKey('Authors')
    action_owner = models.CharField(max_length=20, help_text="The user who did the action")

    def __unicode__(self):
            return str(self.action_type)

    class Meta:
        #order descending, show the last actions at top
        ordering = ['-action_date']

class Entries (models.Model):
    id_hash = models.CharField(max_length=50, help_text="Hash of the ID", primary_key=True)
    title = models.CharField(max_length=150, help_text="Entry Title")
    content_html = models.TextField(help_text="Entry Orginal Content")
    content_text = models.TextField(help_text="Entry Pure Text Content")
    summary = models.TextField(help_text="Entry Summary", null=True, blank=True)
    link = models.URLField(help_text="Link to Entry")
    date = models.DateTimeField(help_text="Date of the entry")
    entry_id = models.ForeignKey('Authors')

    def __unicode__(self):

        return self.title

    class Meta:

        ordering = ['-date']
        
    def sanitize(self, data):
        p = re.compile(r'<[^<]*?/?>')
        return p.sub('', data)

class RunTime (models.Model):
    run_time = models.DateTimeField(help_text="Run time of the planet script", auto_now=True)

    def __unicode__(self):

        return self.run_time

    class Meta:

        ordering = ['-run_time']

    def get_run_time(self):

        dt = ".".join(map(lambda x: str(x), [self.run_time.day, self.run_time.month, self.run_time.year]))
        hm = ":".join(map(lambda x: str(x), [self.run_time.hour, self.run_time.minute]))

        rslt = " ".join([dt, hm])
        return rslt

