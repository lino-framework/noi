# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _
from lino.utils.instantiator import create_row
#from .choicelists import VoteStates
from .roles import SimpleVotesUser


class VoteAction(dd.Action):
    def goto_vote(self, obj, ar):
        if obj.user == ar.get_user():
            da = rt.actors.votes.MyVotes.detail_action
        else:
            da = rt.actors.votes.VotesByVotable.detail_action
        # da = ar.actor.detail_action
        ar.goto_instance(obj, detail_action=da)


class CreateVote(VoteAction):
    """Define your vote about this object.

    visible only when you don't yet have a vote on this
    object. Clicking it will create a default vote object and show
    that object in a detail window.

    """
    sort_index = 100
    button_text  = u"☆"  # 2606
    show_in_workflow = True
    show_in_bbar = False
    required_roles = dd.login_required(SimpleVotesUser)

    # parameters = dict(
    #     state=VoteStates.field(),
    #     comment=dd.RichTextField(_("Comment"), blank=True))
    # params_layout = dd.Panel("""
    # state
    # comment
    # """, window_size=(50, 12))
    

    def get_action_permission(self, ar, obj, state):
        if not super(CreateVote, self).get_action_permission(ar, obj, state):
            return False
        vote = obj.get_favourite(ar.get_user())
        return vote is None

    def run_from_ui(self, ar, **kw):
        me = ar.get_user()
        obj = ar.selected_rows[0]
        Vote = rt.models.votes.Vote
        options = dict(votable=obj, user=me)
        # pv = ar.action_param_values
        # options.update(state=pv.state)
        vote = create_row(Vote, **options)

        # if pv.comment:
        #     create_row(
        #         rt.models.comments.Comment, 
        #         owner=obj,
        #         short_text=pv.comment, user=ar.get_user())
        
        self.goto_vote(vote, ar)

class EditVote(VoteAction):
    sort_index = 100
    button_text = u"★"  # 2605
    show_in_workflow = True
    show_in_bbar = False

    def run_from_ui(self, ar, **kw):
        self.goto_vote(ar.selected_rows[0], ar)
        


class VotableEditVote(EditVote):
    """Edit your vote about this object.
    """
    def get_action_permission(self, ar, obj, state):
        if not super(VotableEditVote, self).get_action_permission(ar, obj, state):
            return False
        vote = obj.get_favourite(ar.get_user())
        return vote is not None

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        vote = obj.get_favourite(ar.get_user())
        # print(20170116, vote)
        self.goto_vote(vote, ar)
        
        # da = rt.actors.votes.VotesByVotable.detail_action
        # ar.goto_instance(vote, detail_action=da)



