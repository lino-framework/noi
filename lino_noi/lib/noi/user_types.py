# -*- coding: UTF-8 -*-
# Copyright 2015-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Defines a set of user roles and fills
:class:`lino.modlib.users.choicelists.UserTypes`.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for :ref:`noi`.
"""

from django.utils.translation import ugettext_lazy as _

from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.users.roles import Helper
# from lino.modlib.comments.roles import CommentsReader
from lino.modlib.comments.roles import CommentsUser, CommentsStaff, PrivateCommentsReader, CommentsReader
from lino.core.roles import SiteUser, SiteAdmin
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.tickets.roles import Reporter, Searcher, Triager, TicketsStaff
from lino_xl.lib.working.roles import Worker
from lino_xl.lib.cal.roles import CalendarReader
from lino_xl.lib.votes.roles import VotesStaff, VotesUser
from lino_xl.lib.products.roles import ProductsStaff
from lino_xl.lib.ledger.roles import LedgerStaff

from lino.modlib.users.choicelists import UserTypes


class Customer(SiteUser, OfficeUser, VotesUser, Searcher, Reporter, CommentsUser):
    """
    A **Customer** is somebody who uses our software and may report
    tickets, but won't work on them. Able to comment and view tickets on sites
    where they are contact people. Unable to see any client data other than orgs
    where they are a contact person and themselves.
    """
    pass


class Contributor(Customer, Searcher, Helper, Worker, ExcerptsUser, ContactsUser, CoursesUser):
    """
    A **Contributor** is somebody who works on and see tickets of sites they are team members of.
    """
    pass


class Developer(Contributor, Triager, ExcerptsStaff, CommentsStaff, TicketsStaff, PrivateCommentsReader):
    """
    A **Developer** is a trusted user who has signed an NDA, has access to client contacts.
    Is able to make service reports as well as manage tickets.
    """
    pass


class SiteAdmin(SiteAdmin, Developer, OfficeStaff, VotesStaff, ContactsStaff, CommentsStaff, ProductsStaff, LedgerStaff):
    """
    Can do everything.
    """


# class Anonymous(CommentsReader, CalendarReader):
class Anonymous(CalendarReader, CommentsReader, Searcher):
    pass


UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"), Anonymous, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("Customer"), Customer, 'customer user')
add('200', _("Contributor"), Contributor, 'contributor')
add('400', _("Developer"), Developer, 'developer')
add('900', _("Administrator"), SiteAdmin, 'admin')

# UserTypes.user = UserTypes.customer

# from lino.core.merge import MergeAction
# from lino.api import rt
# lib = rt.models
# for m in (lib.contacts.Company, ):
#     m.define_action(merge_row=MergeAction(
#         m, required_roles=set([ContactsStaff])))
