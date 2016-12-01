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

class VoteState(dd.Choice):
    pass


class VoteStates(dd.ChoiceList):
    """The list of possible states of a vote.  This is used as choicelist
    for the :attr:`state <lino_noi.lib.votes.models.Vote.state>`
    field of a vote.

    .. attribute:: interested

        I am interested, I want to get notified when something
        happens.

    .. attribute:: offering
    .. attribute:: active
    .. attribute:: inactive

    """
    required_roles = dd.required(VotesStaff)
    verbose_name = _("Vote state")
    verbose_name_plural = _("Vote states")
    item_class = VoteState

add = VoteStates.add_item
add('10', _("Interested"), 'interested')
add('20', _("Offering help"), 'offering')
add('30', _("Active"), 'active')
add('40', _("Inactive"), 'inactive')


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


