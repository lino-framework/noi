# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
#
# License: BSD (see file COPYING for details)
"""
Database models for `lino_xl.lib.humanlinks`.

"""

from __future__ import unicode_literals
from __future__ import print_function
import six

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from django.db import models

from lino.api import dd, rt
from lino.modlib.users.mixins import UserAuthored, My
from lino.mixins import Created
from .roles import VotesUser, VotesStaff
from .choicelists import VoteStates
from .choicelists import Ratings

config = dd.plugins.votes


@dd.python_2_unicode_compatible
class Vote(UserAuthored, Created):
    """A link between two persons.

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

    state = VoteStates.field(default=VoteStates.interested.as_callable)
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


class AllVotes(Votes):
    required_roles = dd.required(VotesStaff)
    
class MyVotes(My, Votes):
    """Show all my votes.

    """
    column_names = "votable state priority rating nickname *"
    order_by = ['-id']
    
class VotesByVotable(Votes):
    """Show all votes on this object.

    """
    label = _("Votes")
    master_key = 'votable'
    column_names = 'user state priority rating *'
    

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

