# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for :mod:`lino_noi.modlib.contacts`.

"""

from lino.api import dd, _

from lino_xl.lib.contacts.models import *


class PersonDetail(PersonDetail):
    
    main = "general skills"

    general = dd.Panel("""
    address_box:60 contact_box:30 overview
    bottom_box
    """, label=_("General"))

    skills = dd.Panel("""
    faculties.OffersBySupplier topics.InterestsByPartner
    """, label=_("Skills"))


    name_box = "last_name first_name:15 gender title:10"
    info_box = "id:5 language:10"
    bottom_box = "remarks contacts.RolesByPerson"

    
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
Persons.set_detail_layout(PersonDetail())
