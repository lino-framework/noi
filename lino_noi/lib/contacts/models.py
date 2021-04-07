# -*- coding: UTF-8 -*-
# Copyright 2015-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Database models for :mod:`lino_noi.modlib.contacts`.

"""

from lino.api import dd, _
from lino.utils import join_words

from lino_xl.lib.contacts.models import *


PartnerDetail.address_box = dd.Panel("""
    name_box
    country #region city zip_code:10
    #addr1
    #street_prefix street:25 street_no street_box
    #addr2
    """, label=_("Address"))

PartnerDetail.contact_box = dd.Panel("""
    url
    phone
    gsm #fax
    """, label=_("Contact"))



class Person(Person):
    
    class Meta(Person.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')
        
    def __str__(self):
        words = []
        words.append(self.first_name)
        words.append(self.last_name)
        return join_words(*words)


class PersonDetail(PersonDetail):
    
    main = "general contact #skills tickets"

    general = dd.Panel("""
    overview info_box
    contacts.RolesByPerson
    """, label=_("General"))

    info_box = """
    id:5
    language:10
    email:40
    """
    
    contact = dd.Panel("""
    address_box:60 contact_box:30
    remarks tickets.SitesByPerson #topics.InterestsByPartner
    """, label=_("Contact"))

    # skills = dd.Panel("""
    # skills.OffersByEndUser skills.SuggestedTicketsByEndUser
    # """, label=dd.plugins.skills.verbose_name)

    tickets = dd.Panel("""
    tickets.TicketsByEndUser tickets.SitesByPerson
    """, label=dd.plugins.tickets.verbose_name)


    name_box = "last_name first_name:15 gender #title:10"

    
class CompanyDetail(CompanyDetail):
    main = "general contact #skills tickets"

    general = dd.Panel("""
    overview info_box
    contacts.RolesByCompany
    """, label=_("General"))

    info_box = """
    id:5
    language:10
    email:40
    """
    
    contact = dd.Panel("""
    address_box:60 contact_box:30 
    remarks
    """, label=_("Contact"))

    # skills = dd.Panel("""
    # skills.OffersByEndUser topics.InterestsByPartner
    # """, label=dd.plugins.skills.verbose_name)

    tickets = dd.Panel("""
    tickets.SitesByCompany
    """, label=dd.plugins.tickets.verbose_name)


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.models.contacts
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())

# Companies.set_detail_layout(CompanyDetail())
# Persons.set_detail_layout(PersonDetail())
Persons.column_names = 'last_name first_name gsm email city *'
