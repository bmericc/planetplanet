#!/usr/bin/env python
"""The Planet aggregator.

A flexible and easy-to-use aggregator for generating websites.

Visit http://www.planetplanet.org/ for more information and to download
the latest version.

Requires Python 2.1, recommends 2.3.
"""

__authors__ = [ "Scott James Remnant <scott@netsplit.com>",
                "Jeff Waugh <jdub@perkypants.org>" ]
__license__ = "Python"

import datetime

import os
import sys
import time
import locale
import urlparse

import planet

from ConfigParser import ConfigParser

# Default configuration file path
CONFIG_FILE = "config.ini"

# Defaults for the [Planet] config section
PLANET_NAME = "Unconfigured Planet"
PLANET_LINK = "Unconfigured Planet"
PLANET_FEED = None
OWNER_NAME  = "Anonymous Coward"
OWNER_EMAIL = ""
LOG_LEVEL   = "WARNING"
FEED_TIMEOUT = 20 # seconds

# Default template file list
TEMPLATE_FILES = "examples/basic/planet.html.tmpl"

#part for django api usage
import sys
import os
# In order to reduce integration issues, this path gets defined automatically.
sys.path.append("ABSOLUTEPATH")
os.environ['DJANGO_SETTINGS_MODULE'] = 'djagen.settings'
from djagen.collector.models import *

def config_get(config, section, option, default=None, raw=0, vars=None):
    """Get a value from the configuration, with a default."""
    if config.has_option(section, option):
        return config.get(section, option, raw=raw, vars=None)
    else:
        return default

def main():
    config_file = CONFIG_FILE
    offline = 0
    verbose = 0

    for arg in sys.argv[1:]:
        if arg == "-h" or arg == "--help":
            print "Usage: planet [options] [CONFIGFILE]"
            print
            print "Options:"
            print " -v, --verbose       DEBUG level logging during update"
            print " -o, --offline       Update the Planet from the cache only"
            print " -h, --help          Display this help message and exit"
            print
            sys.exit(0)
        elif arg == "-v" or arg == "--verbose":
            verbose = 1
        elif arg == "-o" or arg == "--offline":
            offline = 1
        elif arg.startswith("-"):
            print >>sys.stderr, "Unknown option:", arg
            sys.exit(1)
        else:
            config_file = arg

    # Read the configuration file
    config = ConfigParser()
    config.read(config_file)
    if not config.has_section("Planet"):
        print >>sys.stderr, "Configuration missing [Planet] section."
        sys.exit(1)

    # Read the [Planet] config section
    planet_name = config_get(config, "Planet", "name",        PLANET_NAME)
    planet_link = config_get(config, "Planet", "link",        PLANET_LINK)
    planet_feed = config_get(config, "Planet", "feed",        PLANET_FEED)
    owner_name  = config_get(config, "Planet", "owner_name",  OWNER_NAME)
    owner_email = config_get(config, "Planet", "owner_email", OWNER_EMAIL)
    if verbose:
        log_level = "DEBUG"
    else:
        log_level  = config_get(config, "Planet", "log_level", LOG_LEVEL)
    feed_timeout   = config_get(config, "Planet", "feed_timeout", FEED_TIMEOUT)
    template_files = config_get(config, "Planet", "template_files",
                                TEMPLATE_FILES).split(" ")

    # Default feed to the first feed for which there is a template
    if not planet_feed:
        for template_file in template_files:
            name = os.path.splitext(os.path.basename(template_file))[0]
            if name.find('atom')>=0 or name.find('rss')>=0:
                planet_feed = urlparse.urljoin(planet_link, name)
                break

    # Define locale
    if config.has_option("Planet", "locale"):
        # The user can specify more than one locale (separated by ":") as
        # fallbacks.
        locale_ok = False
        for user_locale in config.get("Planet", "locale").split(':'):
            user_locale = user_locale.strip()
            try:
                locale.setlocale(locale.LC_ALL, user_locale)
            except locale.Error:
                pass
            else:
                locale_ok = True
                break
        if not locale_ok:
            print >>sys.stderr, "Unsupported locale setting."
            sys.exit(1)

    # Activate logging
    planet.logging.basicConfig()
    planet.logging.getLogger().setLevel(planet.logging.getLevelName(log_level))
    log = planet.logging.getLogger("planet.runner")
    try:
        log.warning
    except:
        log.warning = log.warn

    # timeoutsocket allows feedparser to time out rather than hang forever on
    # ultra-slow servers.  Python 2.3 now has this functionality available in
    # the standard socket library, so under 2.3 you don't need to install
    # anything.  But you probably should anyway, because the socket module is
    # buggy and timeoutsocket is better.
    if feed_timeout:
        try:
            feed_timeout = float(feed_timeout)
        except:
            log.warning("Feed timeout set to invalid value '%s', skipping", feed_timeout)
            feed_timeout = None

    if feed_timeout and not offline:
        try:
            from planet import timeoutsocket
            timeoutsocket.setDefaultSocketTimeout(feed_timeout)
            log.debug("Socket timeout set to %d seconds", feed_timeout)
        except ImportError:
            import socket
            if hasattr(socket, 'setdefaulttimeout'):
                log.debug("timeoutsocket not found, using python function")
                socket.setdefaulttimeout(feed_timeout)
                log.debug("Socket timeout set to %d seconds", feed_timeout)
            else:
                log.error("Unable to set timeout to %d seconds", feed_timeout)

    # run the planet
    my_planet = planet.Planet(config)
    my_planet.run(planet_name, planet_link, template_files, offline)



    ## This is where archiving is done! ##
    #add the current channels to the db
    channels = my_planet.channels()
    for channel in channels:
       ### This part seperates surname from name do not activate it if needn't.
        words = channel.name.split()
        if len(words) == 1:
            author_name = words[0]
            author_surname == None
        else:
            author_surname = words[-1]
            words.pop()
            tmp_first_name = ''
            for word in words: tmp_first_name += ' ' + word
            author_name = tmp_first_name[1:]
       ###                                                                 ###
        #print channel.name
       #author_name = channel.name
       #author_surname = channel.surname

        try:
            author_face = channel.face
        except:
            author_face = None
        try:
            channel_subtitle = channel.subtitle
        except:
            channel_subtitle = None
        try:
            channel_title = channel.title
        except:
            channel_title = None

        channel_url = channel.url

        try:
            channel_link = channel.link
        except:
            channel_link = None

        try:
            channel_urlstatus = channel.url_status
        except:
            channel_urlstatus = None
        label = channel.label

        label_personal = 0
        label_lkd = 0
        label_community = 0
        label_eng = 0
        if label == "Personal":
            label_personal = 1
        if label == "LKD":
            label_lkd = 1
        if label == "Community":
            label_community = 1
        if label == "Eng":
            label_eng = 1
        id = channel.id

        try:
            author = Authors.objects.get(author_id=id)

            #update the values with the ones at the config file
            author.author_name = author_name
            author.author_surname = author_surname
            #print author_name
            author.author_face = author_face
            author.channel_subtitle = channel_subtitle
            author.channel_title = channel_title
            author.channel_url = channel_url
            author.channel_link = channel_link
            author.channel_url_status = channel_urlstatus
            author.label_personal = label_personal
            author.label_lkd = label_lkd
            author.label_community = label_community
            author.label_eng = label_eng

        except Exception, ex:
            #print ex
            author = Authors(author_id=id, author_name=author_name, author_surname=author_surname, author_face=author_face, channel_subtitle=channel_subtitle, channel_title=channel_title, channel_url=channel_url, channel_link=channel_link, channel_urlstatus=channel_urlstatus, label_personal=label_personal, label_lkd=label_lkd, label_community=label_community, label_eng=label_eng)


        author.save()

        #entry issues
        items = channel.items()
        for item in items:
            id_hash = item.id_hash

            try:
                #Only check for get if that fails then switch to create new entry mode.
                entry = author.entries_set.get(id_hash = item.id_hash)

                try:
                    entry.title = item.title
                except:
                    #print "title"
                    entry.title = None
                try:
                    entry.content_html = item.content
                except:
                    entry.content_html = None
                try:
                    entry.content_text = entry.sanitize(item.content)
                except:
                    entry.content_text = None
                try:

                    entry.summary = item.summary
                except:
                    #print "summary"
                    entry.summary = None
                try:

                    entry.link = item.link
                except:
                    #print "link"
                    entry.link = None

                d = item.date


                entry.date = datetime.datetime(d[0], d[1], d[2], d[3], d[4], d[5])


            except:
                content_html = item.content
                #content_text = entry.sanitize(content_html)
                d = item.date
                if not item.has_key('summary'): summary = None
                else: summary = item.summary
                entry = author.entries_set.create(id_hash= item.id_hash, title=item.title, content_html=item.content, summary=summary, link=item.link, date=datetime.datetime(d[0], d[1], d[2], d[3], d[4], d[5]))
                entry.content_text = entry.sanitize(content_html)

            entry.save()

        #datetime issue
        r = RunTime()
        r.save()

    my_planet.generate_all_files(template_files, planet_name,
        planet_link, planet_feed, owner_name, owner_email)


if __name__ == "__main__":
    main()

