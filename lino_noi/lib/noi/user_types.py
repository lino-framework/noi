# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines a set of user roles and fills
:class:`lino.modlib.users.choicelists.UserTypes`.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for
:mod:`lino_noi.projects.team`.

TODO: move this to :mod:`lino_noi.projects.team.roles` because 
this is used only by :mod:`lino_noi.projects.team`
while :mod:`lino_noi.projects.care` does not use this module at all.

"""


from lino.core.roles import UserRole, SiteAdmin
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_noi.lib.tickets.roles import Triager
from lino_noi.lib.clocking.roles import Worker
from lino_noi.lib.votes.roles import VotesStaff, VotesUser

from lino.modlib.users.choicelists import UserTypes
from django.utils.translation import ugettext_lazy as _


class EndUser(OfficeUser, VotesUser):
    """An **end user** is somebody who uses our software and may report
    tickets, but won't work on them.

    """
    pass


class Consultant(EndUser, Worker, ExcerptsUser):
    """A **consultant** is somebody who may both report tickets and work
    on them.

    """
    pass


class Developer(Triager, Consultant):
    """A **developer** is somebody who may both report tickets and work
    on them.

    """
    pass


class Senior(Developer, ExcerptsStaff):
    """A **senior developer** is a *developer* who is additionally
    responsible for triaging tickets

    """
    pass


class SiteAdmin(Senior, SiteAdmin, OfficeStaff, VotesStaff):
    """Can do everything."""

UserTypes.clear()
add = UserTypes.add_item
add('000', _("Anonymous"),        UserRole, 'anonymous',
    readonly=True, authenticated=False)
add('100', _("User"),             EndUser, 'user')
add('200', _("Consultant"),       Consultant, 'consultant')
add('300', _("Hoster"),           Consultant, 'hoster')
add('400', _("Developer"),        Developer, 'developer')
add('490', _("Senior developer"), Senior, 'senior')
add('900', _("Administrator"),    SiteAdmin, 'admin')
