# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines a set of user roles and fills
:class:`lino.modlib.users.choicelists.UserTypes`.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for
:mod:`lino_noi.projects.team`.

Note that :mod:`lino_noi.projects.care` does not use this module at
all.

"""


from lino.core.roles import UserRole, SiteAdmin
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.courses.roles import CoursesUser, CoursesTeacher
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.comments.roles import CommentsReader, CommentsUser, CommentsStaff
from lino_xl.lib.tickets.roles import TicketsUser, Searcher, Triager, TicketsStaff
from lino_xl.lib.clocking.roles import Worker
from lino_xl.lib.cal.roles import CalendarReader
from lino_xl.lib.votes.roles import VotesStaff, VotesUser

from lino.modlib.users.choicelists import UserTypes
from django.utils.translation import ugettext_lazy as _


class EndUser(OfficeUser, VotesUser, TicketsUser, CommentsUser):
    """An **end user** is somebody who uses our software and may report
    tickets, but won't work on them.

    """
    pass


class Consultant(EndUser, Searcher, Worker, ExcerptsUser,
                 ContactsUser, CoursesUser):
    """A **consultant** is somebody who may both report tickets and work
    on them.

    """
    pass


class Developer(Consultant):
    """A **developer** is somebody who may both report tickets and work
    on them.

    """
    pass


class Senior(Developer, Triager, ExcerptsStaff, CommentsStaff):
    """A **senior developer** is a *developer* who is additionally
    responsible for triaging tickets

    """
    pass


class SiteAdmin(Senior, SiteAdmin, OfficeStaff, VotesStaff,
                TicketsStaff, ContactsStaff, CommentsStaff):
    """Can do everything."""


class Anonymous(CommentsReader, CalendarReader):
    pass

UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"),        Anonymous, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("User"),             EndUser, 'user')
add('200', _("Consultant"),       Consultant, 'consultant')
add('300', _("Hoster"),           Consultant, 'hoster')
add('400', _("Developer"),        Developer, 'developer')
add('490', _("Senior developer"), Senior, 'senior')
add('900', _("Administrator"),    SiteAdmin, 'admin')


from lino.core.merge import MergeAction
from lino.api import rt
lib = rt.models
for m in (lib.contacts.Company, ):
    m.define_action(merge_row=MergeAction(
        m, required_roles=set([ContactsStaff])))
