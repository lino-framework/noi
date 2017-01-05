# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for :mod:`lino_noi.modlib.contacts`.

"""

from lino.api import dd, _

from lino_xl.lib.contacts.models import *


class CompanyDetail(CompanyDetail):
    main = "general tickets"

    general = dd.Panel("""
    address_box:60 contact_box:30
    bottom_box
    """, label=_("General"))

    tickets = dd.Panel("""
    tickets.ProjectsByCompany topics.InterestsByPartner
    """, label=_("Tickets"))


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

Companies.set_detail_layout(CompanyDetail())
