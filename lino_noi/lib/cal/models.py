# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, _

from lino_xl.lib.cal.models import *

class Event(Event, ContactRelated):
    class Meta:
        app_label = 'cal'
        abstract = dd.is_abstract_model(__name__, 'Event')

dd.update_field(Event, 'user', verbose_name=_("Author"))
dd.update_field(Event, 'company', verbose_name=_("Organizer"))
dd.update_field(Event, 'contact_person', verbose_name=_("Contact person"))
    

class EventDetail(EventDetail):
    start = "start_date start_time"
    end = "end_date end_time"
    main = "general GuestsByEvent"
    general = dd.Panel("""
    event_type:20 summary:60 id
    start end access_class #all_day #assigned_to #duration #state
    user room company contact_person
    project owner workflow_buttons 
    # owner created:20 modified:20
    description blogs.EntriesByController #outbox.MailsByController
    """, label=_("General"))
    
Events.set_detail_layout(EventDetail())
