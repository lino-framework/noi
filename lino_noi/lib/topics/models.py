# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Database models for this plugin.

"""

from lino.api import dd, _

from lino_xl.lib.topics.models import *


class TopicDetail(dd.DetailLayout):
    main = """
    id ref name topic_group
    description
    tickets.TicketsByTopic topics.InterestsByTopic
    """


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

Topics.set_detail_layout(TopicDetail())
