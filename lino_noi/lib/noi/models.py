# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# Defines a handler for
# :data:`lino.modlib.smtpd.signals.mail_received`.


#from email.parser import Parser

from lino.api import dd
# from lino.modlib.smtpd.signals import mail_received


# @dd.receiver(mail_received)
# def process_message(sender=None, peer=None, mailfrom=None,
#                     rcpttos=None, data=None, **kwargsg):
#     print ('Receiving message from:', peer)
#     print ('Message addressed from:', mailfrom)
#     print ('Message addressed to  :', rcpttos)
#     print ('Message length        :', len(data))
#     msg = Parser().parsestr(data)
#     print ('To: %s' % msg['to'])
#     print ('From: %s' % msg['from'])
#     print ('Subject: %s' % msg['subject'])
#     return None


@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    sender.models.system.SiteConfigs.set_detail_layout("""
    site_company next_partner_id:10 default_build_method
    site_calendar simulate_today hide_events_before
    default_event_type max_auto_events 
    """)

