# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
#
# License: BSD (see file COPYING for details)
"""
Database models for this plugin.

"""

from __future__ import unicode_literals
from __future__ import print_function
import six

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.db import models
from django.conf import settings

from lino.api import dd, rt
from lino.modlib.users.mixins import UserAuthored, My
from lino.mixins import Created, ObservedPeriod
from .roles import VotesUser, VotesStaff
from .choicelists import VoteStates, VoteEvents
from .choicelists import Ratings

config = dd.plugins.votes


@dd.python_2_unicode_compatible
class Vote(UserAuthored, Created):
    """A **vote** is when a user has an opinion or interest about a given
    ticket (or any other votable).

    .. attribute:: votable

        The ticket (or other votable) being voted.

    .. attribute:: user

        The user who is voting.

    .. attribute:: state

        The state of this vote.  Pointer to :class:`VoteStates
        <lino_noi.lib.votes.choicelists.VoteStates>`.

    .. attribute:: priority

        My personal priority for this ticket.

    .. attribute:: rating

        How the ticket reporter rates my help on this ticket.

    .. attribute:: remark

        Why I am interested in this ticket.

    .. attribute:: nickname
    
        My nickname for this ticket. Optional. 

        If this is specified, then I get a quicklink to this ticket.

    """
    class Meta:
        app_label = 'votes'
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")
        abstract = dd.is_abstract_model(__name__, 'Vote')

    state = VoteStates.field(default=VoteStates.as_callable('watching'))
    votable = dd.ForeignKey(
        config.votable_model, verbose_name=_("Votable"))
    priority = models.SmallIntegerField(_("Priority"), default=0)
    rating = Ratings.field(blank=True)
    remark = dd.RichTextField(_("Remark"), blank=True)
    nickname = models.CharField(_("Nickname"), max_length=50, blank=True)


    def __str__(self):
        return _("{0.user} {0.state} on {0.votable}").format(self)

    def disabled_fields(self, ar):
        df = super(Vote, self).disabled_fields(ar)
        me = ar.get_user()
        if not me.profile.has_required_roles([VotesStaff]):
            if me != self.votable.get_vote_rater(self):
                df.add('rating')
        return df


class Votes(dd.Table):
    model = 'votes.Vote'
    stay_in_grid = True
    detail_layout = dd.FormLayout("""
    user
    votable
    state priority rating
    """, window_size=(40, 'auto'))
    required_roles = dd.required(VotesUser)

    parameters = ObservedPeriod(
        observed_event=VoteEvents.field(blank=True),
        reporter=dd.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Reporter"),
            blank=True, null=True,
            help_text=_("Only rows reported by this user.")),
        show_todo=dd.YesNo.field(_("To do"), blank=True),
        state=VoteStates.field(
            blank=True, help_text=_("Only rows having this state.")))

    params_layout = """
    user state reporter show_todo
    start_date end_date observed_event"""

    @classmethod
    def get_simple_parameters(cls):
        s = super(Votes, cls).get_simple_parameters()
        s.add('state')
        return s

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Votes, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.show_todo == dd.YesNo.no:
            qs = qs.exclude(state__in=VoteStates.todo_states)
        elif pv.show_todo == dd.YesNo.yes:
            qs = qs.filter(state__in=VoteStates.todo_states)

        if pv.observed_event:
            qs = pv.observed_event.add_filter(qs, pv)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Votes, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.start_date or pv.end_date:
            yield daterange_text(
                pv.start_date,
                pv.end_date)



class AllVotes(Votes):
    required_roles = dd.required(VotesStaff)
    
class MyVotes(My, Votes):
    """Show all my votes.

    """
    column_names = "votable state priority rating nickname *"
    order_by = ['-id']
    
    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyVotes, self).param_defaults(ar, **kw)
        # kw.update(state=TicketStates.todo)
        kw.update(show_todo=dd.YesNo.yes)
        return kw


class VotesByVotable(Votes):
    """Show all votes on this object.

    """
    label = _("Votes")
    master_key = 'votable'
    column_names = 'user state priority rating *'


# class MyOfferedVotes(MyVotes):
#     """List of my help offers to other users' requests.

#     Only those which need my attention. 

#     """
    
#     column_names = "votable state priority rating nickname *"
#     order_by = ['-id']
    
# class MyRequestedVotes(MyVotes):
#     """List of other user's help offers on my requests. 

#     Only those which need my attention. 

#     """
#     column_names = "votable state priority rating nickname *"
#     order_by = ['-id']
    

from lino.utils.xmlgen.html import E
from lino.utils import join_elems


def welcome_messages(ar):
    """Yield a message "Your favourites are X, Y, ..." for the welcome
page.

    This message mentions all voted objects of the requesting user
    and whose :attr:`nickname <Vote.nickname>` is not empty.

    """
    Vote = rt.models.votes.Vote
    qs = Vote.objects.filter(user=ar.get_user()).exclude(nickname='')
    qs = qs.order_by('priority')
    if qs.count() > 0:
        chunks = [six.text_type(_("Your favourite {0} are ").format(
            dd.plugins.votes.votable_model._meta.verbose_name_plural))]
        chunks += join_elems([
            ar.obj2html(obj.votable, obj.nickname)
            for obj in qs])
        chunks.append('.')
        yield E.span(*chunks)

dd.add_welcome_handler(welcome_messages)

