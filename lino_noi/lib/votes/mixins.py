# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for this plugin.
"""

from lino.api import dd, rt, _
from lino.utils.instantiator import create_row
from lino.modlib.notify.mixins import ChangeObservable
from .choicelists import VoteStates
from .roles import SimpleVotesUser
from .actions import CreateVote, EditVote, VotableEditVote

class Votable(ChangeObservable):
    """Base class for models that can be used as
    :attr:`lino_noi.lib.votes.Plugin.votable_model`.

    """
    class Meta(object):
        abstract = True

    create_vote = CreateVote()
    edit_vote = VotableEditVote()

    def get_vote_raters(self):
        """Yield or return a list of the users who are allowed to rate the
        votes on this votable.

        Lino automatically (in :meth:`after_ui_save`) creates an
        **author vote** for each of them.

        """
        return []

    def get_favourite(self, user):
        """Return the vote of the given user about this votable, or None if no
vote exists.

        There should be either 0 or 1 vote per user and votable.

        """
        if user.authenticated:
            qs = rt.models.votes.Vote.objects.filter(
                votable=self, user=user)
            if qs.count() == 0:
                return None
            return qs[0]

    def get_change_observers(self):
        for x in super(Votable, self).get_change_observers():
            yield x
        for vote in rt.models.votes.Vote.objects.filter(votable=self):
            yield (vote.user, vote.mail_mode or vote.user.mail_mode)

    def set_author_votes(self):
        """Verifies that every vote rater has a vote."""
        for user in self.get_vote_raters():
            vote = self.get_favourite(user)
            if vote is None:
                create_row(
                    rt.models.votes.Vote, user=user, votable=self,
                    state=VoteStates.author)
            # elif vote.state != VoteStates.author:
            #     vote.state = VoteStates.author
            #     vote.full_clean()
            #     vote.save()
                
    def after_ui_save(self, ar, cw):
        self.set_author_votes()
        super(Votable, self).after_ui_save(ar, cw)
