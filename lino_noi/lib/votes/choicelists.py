# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
#
# License: BSD (see file COPYING for details)
"""
Choicelists for this plugin.

"""


from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from .roles import VotesStaff

class VoteState(dd.State):
    show_in_todo = False


class VoteStates(dd.Workflow):
    """The list of possible states of a vote.  This is used as choicelist
    for the :attr:`state <lino_noi.lib.votes.models.Vote.state>`
    field of a vote.

    See :mod:`lino_noi.lib.noi.workflows`.

    """
    required_roles = dd.required(VotesStaff)
    verbose_name = _("Vote state")
    verbose_name_plural = _("Vote states")
    item_class = VoteState
    # max_length = 3
    todo_states = []


class Ratings(dd.ChoiceList):
    verbose_name = _("Rating")
    verbose_name_plural = _("Ratings")

    
add = Ratings.add_item
add('10', _("Very good"))
add('20', _("Good"))
add('30', _("Satisfying"))
add('40', _("Deficient"))
add('50', _("Insufficient"))
add('90', _("Unratable"))


from lino_noi.lib.tickets.choicelists import T00, T24, combine
from lino.modlib.system.choicelists import ObservedEvent


class VoteEvents(dd.ChoiceList):
    verbose_name = _("Observed event")
    verbose_name_plural = _("Observed events")


class VoteEventCreated(ObservedEvent):
    text = _("Created")

    def add_filter(self, qs, pv):
        if pv.start_date:
            qs = qs.filter(created__gte=combine(pv.start_date, T00))
        if pv.end_date:
            qs = qs.filter(created__lte=combine(pv.end_date, T24))
        return qs

VoteEvents.add_item_instance(VoteEventCreated('created'))


