# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for `lino_noi.lib.tickets`.

"""

from lino.core.roles import SiteUser

class TicketsUser(SiteUser):
    """A user who can create new tickets.

    """


class Triager(TicketsUser):
    """A user who is responsible for triaging new tickets.

    """


class TicketsStaff(Triager):
    """Can configure tickets functionality.

    """

