# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines user roles for the Care variant of Lino Noi."""


from lino.core.roles import UserRole, SiteAdmin
from lino.modlib.users.roles import Helper
# from lino.modlib.office.roles import OfficeStaff
from lino_xl.lib.contacts.roles import ContactsUser
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_noi.lib.votes.roles import VotesStaff, VotesUser
from lino_noi.lib.tickets.roles import Triager
from lino_noi.lib.clocking.roles import Worker
from lino.modlib.users.choicelists import UserTypes
from django.utils.translation import ugettext_lazy as _


#class SimpleUser(Helper):
class SimpleUser(Helper, ContactsUser, OfficeUser, VotesUser):
    """A **simple user** is a person who can log into the application in
    order to manage their own pleas and competences and potentially
    can respond to other user's pleas.

    """
    pass


class Connector(SimpleUser, Worker, Triager):
    """A **connector** is a person who knows other persons and who
    introduces pleas on their behalf.

    """
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, Helper, ContactsUser,
                Worker, Triager, VotesStaff):
    """A **site administrator** can do everything."""



UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"),        UserRole, 'anonymous',
    readonly=False, authenticated=False)
add('100', _("User"), SimpleUser, 'user')
add('500', _("Connector"), Connector, 'connector')
add('900', _("Administrator"),    SiteAdmin, 'admin')
