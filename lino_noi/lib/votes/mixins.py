# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for this plugin.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.utils.xmlgen.html import E, lines2p
from lino.utils.instantiator import create_row
from lino.modlib.notify.mixins import ChangeObservable
from .roles import SimpleVotesUser


class CreateVote(dd.Action):
    """Define your vote about this object.

    visible only when you don't yet have a vote on this
    object. Clicking it will create a default vote object and show
    that object in a detail window.

    """
    sort_index = 100
    button_text  = u"☆"  # 2606
    show_in_workflow = True
    show_in_bbar = False
    required_roles = dd.required(SimpleVotesUser)

    def get_action_permission(self, ar, obj, state):
        if not super(CreateVote, self).get_action_permission(ar, obj, state):
            return False
        vote = obj.get_favourite(ar.get_user())
        return vote is None

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        Vote = rt.models.votes.Vote
        vote = Vote(votable=obj, user=ar.get_user())
        vote.full_clean()
        vote.save()
        ar.goto_instance(vote)


class EditVote(dd.Action):
    """Edit your vote about this object.
    """
    sort_index = 100
    button_text = u"★"  # 2605

    show_in_workflow = True
    show_in_bbar = False

    def get_action_permission(self, ar, obj, state):
        if not super(EditVote, self).get_action_permission(ar, obj, state):
            return False
        vote = obj.get_favourite(ar.get_user())
        return vote is not None

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        vote = obj.get_favourite(ar.get_user())
        ar.goto_instance(vote)



class Votable(ChangeObservable):
    """Base class for models that can be used as
    :attr:`lino_noi.lib.votes.Plugin.votable_model`.

    """
    class Meta(object):
        abstract = True

    create_vote = CreateVote()
    edit_vote = EditVote()

    def get_vote_raters(self):
        """Yield or return a list of the users who are allowed to rate the
votes on this votable.

        As a side effect, Lino will automatically (in
        :meth:`after_ui_save`) create a vote for each of them.

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

    def after_ui_save(self, ar, cw):
        """Verifies that every vote rater has a vote."""
        if cw is None:
            for user in self.get_vote_raters():
                vote = self.get_favourite(user)
                if vote is None:
                    create_row(rt.models.votes.Vote,
                               user=user, votable=self,
                               state=rt.actors.votes.VoteStates.watching)

        super(Votable, self).after_ui_save(ar, cw)
