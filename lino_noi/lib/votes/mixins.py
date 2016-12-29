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

def get_favourite(obj, user):
    if user.authenticated:
        qs = rt.models.votes.Vote.objects.filter(votable=obj, user=user)
        if qs.count() == 0:
            return None
        return qs[0]



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
        vote = get_favourite(obj, ar.get_user())
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
        vote = get_favourite(obj, ar.get_user())
        return vote is not None

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        vote = get_favourite(obj, ar.get_user())
        ar.goto_instance(vote)



class Votable(ChangeObservable):
    """Base class for models that can be used as
    :attr:`lino_noi.lib.votes.Plugin.votable_model`.

    """
    class Meta(object):
        abstract = True

    create_vote = CreateVote()
    edit_vote = EditVote()

    def get_vote_rater(self):
        """Return the user who is allowed to rate votes on this votable.

        If this returns something, then a vote will automatically be
        created.

        """
        return None

    # def get_votable_author(self):
    #     """Return the user who is the author of this votable.

    #     """
    #     return None

    def get_change_observers(self):
        for vote in rt.models.votes.Vote.objects.filter(votable=self):
            yield (vote.user, vote.mail_mode or vote.user.mail_mode)

    def after_ui_save(self, ar, cw):
        super(Votable, self).after_ui_save(ar, cw)
        if cw is None:
            user = self.get_vote_rater()
            if user:
                # vote = get_favourite(self, user)
                # if vote is None:
                create_row(rt.models.votes.Vote,
                           user=user, votable=self,
                           state=rt.actors.votes.VoteStates.watching)

