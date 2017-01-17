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
    """The state of a vote.

    .. attribute:: vote_name

        Translatable text. How a vote is called when in this state.

    """
    # def __init__(self, value, text, vote_name, name=None, **kwargs):
    #     super(VoteState, self).__init__(value, text, name)
    #     self.vote_name = vote_name


class VoteStates(dd.Workflow):
    """The list of possible states of a vote.  This is used as choicelist
    for the :attr:`state <lino_noi.lib.votes.models.Vote.state>`
    field of a vote.

    The default implementation defines the following choices:

    .. attribute:: author

        Reserved for the author's vote.  Lino automatically creates an
        **author vote** for every author of a ticket (see
        :meth:`get_vote_raters
        <lino_noi.lib.votes.choicelists.Votable.get_vote_raters>`).


    .. attribute:: watching
    .. attribute:: candidate
    .. attribute:: assigned
    .. attribute:: done
    .. attribute:: rated
    .. attribute:: cancelled


    """
    required_roles = dd.required(VotesStaff)
    # verbose_name = _("Vote state")
    verbose_name_plural = _("Vote states")
    item_class = VoteState
    # max_length = 3
    # todo_states = []

add = VoteStates.add_item
# add('10', _("Watching"), _("Interest"), 'watching')
# add('20', _("Candidate"), _("Offer"), 'candidate', show_in_todo=True)
# add('30', _("Assigned"), _("Job to do"), 'assigned', show_in_todo=True)
# add('40', _("Done"), _("Job done"), 'done')
# add('50', _("Rated"), _("Job rated"), 'rated')
# add('60', _("Cancelled"), _("Cancelled offer"), 'cancelled')  # Absage
add('00', _("Author"), 'author')
add('10', _("Watching"), 'watching')
add('20', _("Candidate"), 'candidate', show_in_todo=True)
add('30', _("Assigned"), 'assigned', show_in_todo=True)
add('40', _("Done"), 'done')
add('50', _("Rated"), 'rated')
add('60', _("Cancelled"), 'cancelled')  # Absage
    


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


# class VoteView(dd.Choice):
#     show_states = set([])
    
#     # def __init__(self, value, text=None, name=None, **kwargs):
#     #     super(VoteView, self).__init__(value, text)
#     # def __init__():

# class VoteViews(dd.ChoiceList):
#     """The list of known vote views.

#     This list is populated in :mod:`lino_noi.lib.noi.workflows`.
#     """
#     verbose_name = _("Vote view")
#     verbose_name_plural = _("Vote views")
#     item_class = VoteView


