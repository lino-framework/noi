# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
#
# License: BSD (see file COPYING for details)
"""
The `demo` fixture for this plugin.


"""

from __future__ import unicode_literals

from lino.utils.cycler import Cycler
from lino.api import rt


def objects():

    Vote = rt.models.votes.Vote
    VoteStates = rt.models.votes.VoteStates
    Ticket = rt.models.tickets.Ticket
    User = rt.models.users.User

    STATES  = Cycler(VoteStates.objects())
    USERS = Cycler(User.objects.all())
    TICKETS = Cycler(Ticket.objects.all())
    for i in range(20):
        USERS.pop()  # not every user votes
        obj = Vote(
            state=STATES.pop(), user=USERS.pop(), votable=TICKETS.pop())
        if obj.user == obj.votable.reporter:
            obj.state = VoteStates.active
        yield obj
