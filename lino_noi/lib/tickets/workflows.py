# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
#
# License: BSD (see file COPYING for details)
"""The default :attr:`workflows_module
<lino.core.site.Site.workflows_module>` for :ref:`noi` applications.

This workflow requires that both :mod:`lino_xl.lib.tickets` and
:mod:`lino_xl.lib.votes` are installed.

If :attr:`use_new_unicode_symbols
<lino.core.site.Site.use_new_unicode_symbols>` is True, ticket states
are represented using symbols from the `Miscellaneous Symbols and
Pictographs
<https://en.wikipedia.org/wiki/Miscellaneous_Symbols_and_Pictographs>`__
block, otherwise we use the more widely supported symbols from
`Miscellaneous Symbols
<https://en.wikipedia.org/wiki/Miscellaneous_Symbols>`
`fileformat.info
<http://www.fileformat.info/info/unicode/block/miscellaneous_symbols/list.htm>`__.

"""
from __future__ import unicode_literals

from lino.api import dd, rt, _, pgettext

from lino.utils.instantiator import create_row

from lino_xl.lib.tickets.choicelists import TicketStates
from lino_xl.lib.tickets.roles import Triager
from lino_xl.lib.votes.choicelists import VoteStates, Ratings
from lino.modlib.notify.actions import NotifyingAction

class TicketAction(dd.ChangeStateAction):
    """Base class for ticket actions.

    Make sure that only *triagers* can act on tickets of other users.

    """
    required_vote_states = set([])
    veto_vote_states = set([])

    def attach_to_actor(self, *args):
        Vote = rt.models.votes.Vote
        self.required_vote_states = Vote.resolve_states(self.required_vote_states)
        self.veto_vote_states = Vote.resolve_states(self.veto_vote_states)
        return super(TicketAction, self).attach_to_actor(*args)
    
    def get_action_permission(self, ar, obj, state):
        me = ar.get_user()
        if obj.user != me:
            if not me.profile.has_required_roles([Triager]):
                return False
        return super(TicketAction,
                     self).get_action_permission(ar, obj, state)

    def before_execute(self, ar, obj):
        if len(self.veto_vote_states) or len(self.required_vote_states):
            has_required = False
            for v in rt.models.votes.Vote.objects.filter(votable=obj):
                if v.state in self.required_vote_states:
                    has_required = True
                if v.state in self.veto_vote_states:
                    msg = _("Cannot {action} because {vote} is {state}.")
                    raise Warning(msg.format(
                        vote=v, user=v.user, action=self.label, state=v.state))

            if not has_required:
                msg = _("Cannot {action} because there is "
                        "no vote marked as {states} .")
                raise Warning(msg.format(
                    action=self.label, states=self.required_vote_states))

# class NotifyingTicketAction(TicketAction):
    
#     def get_notify_owner(self, ar, obj):
#         return obj

#     def get_notify_recipients(self, ar, obj):
#         yield obj.get_notify_recipients(ar)

    
class MarkTicketOpened(TicketAction):
    """Mark this ticket as open.
    """
    label = pgettext("verb", "Open")
    required_states = 'talk new closed'
    # show_in_bbar = True

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} opened {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject
    
    
class MarkTicketStarted(TicketAction):
    """Mark this ticket as started.
    """
    label = pgettext("verb", "Start")
    required_states = 'new talk opened'

    def unused_before_execute(self, ar, obj):
        for v in rt.models.votes.Vote.objects.filter(votable=obj):
            if v.state == rt.actors.votes.VoteStates.assigned:
                return  # ok
        raise Warning(
            _("Cannot start when nobody is assigned"))

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} activated {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject
    
class MarkTicketReady(TicketAction):
    """Mark this ticket as ready.
    """
    required_states = "new opened started talk"
    
class MarkTicketClosed(TicketAction):
    """Mark this ticket as closed.
    """
    # label = pgettext("verb", "Close")
    required_states = 'talk started opened ready'
    veto_vote_states = 'assigned'
    required_vote_states = 'done cancelled'

class MarkTicketRefused(TicketAction):
    """Mark this ticket as refused.
    """
    required_states = 'talk started opened ready'
    veto_vote_states = 'assigned'


class MarkTicketTalk(TicketAction):
    """Mark this ticket as talk.
    """
    label = pgettext("verb", "Talk")
    required_states = "new opened started sleeping ready"

    # def get_notify_subject(self, ar, obj):
    #     subject = _("{user} wants to talk about {ticket}.").format(
    #         user=ar.get_user(), ticket=obj)
    #     return subject


# TicketStates.sticky.add_transition(
#     required_states="new")
# TicketStates.new.add_transition(
#     required_states="sticky")
TicketStates.sleeping.add_transition(
    required_states="new talk opened started")
TicketStates.talk.add_transition(MarkTicketTalk)
TicketStates.opened.add_transition(MarkTicketOpened)
TicketStates.started.add_transition(MarkTicketStarted)
TicketStates.ready.add_transition(MarkTicketReady)
TicketStates.closed.add_transition(MarkTicketClosed)
TicketStates.cancelled.add_transition(MarkTicketRefused)


# class VoteAction(dd.ChangeStateAction, NotifyingAction):
class VoteAction(dd.ChangeStateAction):
    
    managed_by_votable_author = False
    # msg_template = _("{user} marked {vote} as {state}.")
    required_votable_states = set([])

    def attach_to_actor(self, *args):
        self.required_votable_states = \
            dd.plugins.votes.votable_model.resolve_states(
                self.required_votable_states)
        return super(VoteAction, self).attach_to_actor(*args)
    
    def get_confirmation_msg_context(self, ar, obj, **kwargs):
        kwargs = super(VoteAction, self).get_confirmation_msg_context(
            ar, obj, **kwargs)
        kwargs.update(
            voter=obj.user,
            vote=obj,
            ticket=obj.votable)
        return kwargs
    
    # def get_notify_subject(self, ar, obj):
    #     subject = _(self.msg_template).format(
    #         user=ar.get_user(),
    #         voter=obj.user,
    #         vote=obj,
    #         state=obj.state,
    #         ticket=obj.votable)
    #     return subject
    
    # def get_notify_owner(self, ar, obj):
    #     return obj.votable.get_notify_owner(ar, obj)

    # def get_notify_recipients(self, ar, obj):
    #     yield obj.votable.get_notify_recipients(ar)

    def get_action_permission(self, ar, obj, state):
        if not obj.votable_id:
            return False
        if len(self.required_votable_states) and not obj.votable.state in self.required_votable_states:
            return False
        me = ar.get_user()
        if self.managed_by_votable_author is not None:
            if self.managed_by_votable_author:
                mgr = obj.votable.user
            else:
                mgr = obj.user
            if mgr != me:
                if not me.profile.has_required_roles([Triager]):
                    return False
        # if self.target_state.name == 'watching':
        #     print("20170115", mgr, self)
        # return True
        return super(VoteAction,
                     self).get_action_permission(ar, obj, state)

class MarkVoteWatching(VoteAction):
    """You are watching this ticket but have no opinion."""
    # label = _("Watching")
    managed_by_votable_author = False
    required_states = "invited pro con candidate assigned"
    # required_votable_states = 'new talk opened started'
    # confirmation_msg_template = _("Revoke {voter}'s {vote}.")
    

class MarkVotePro(VoteAction):
    """You declare that you support this ticket."""
    # label = _("Pro")
    managed_by_votable_author = False
    required_states = "invited watching candidate assigned"
    # required_votable_states = 'new talk opened started'
    confirmation_msg_template = _("{voter} speaks for {ticket}.")
    

class MarkVoteCon(VoteAction):
    """You declare that you are against this ticket."""
    # label = _("Con")
    managed_by_votable_author = False
    required_states = "invited watching candidate assigned"
    # required_votable_states = 'new talk opened started'
    confirmation_msg_template = _("{voter} speaks against {ticket}.")
    

class MarkVoteCandidate(VoteAction):
    
    # label = _("Candidate")
    managed_by_votable_author = False
    msg_template = _("{user} candidates for {ticket}.")
    required_states = "watching pro"
    required_votable_states = 'new talk opened'
    

class MarkVoteAssigned(VoteAction):
    # label = _("Assigned")
    # label = pgettext("verb", "Assign")
    managed_by_votable_author = True
    required_states = 'watching candidate'
    required_votable_states = 'new talk opened started ready'
    #msg_template = _("{user} assigned {voter} for {ticket}.")
    # confirmation_msg_template = _("Assign {voter} for {ticket}.")

    def unused_before_execute(self, ar, obj):
        for v in obj.__class__.objects.filter(votable_id=obj.votable_id):
            if v != obj and v.state == VoteStates.candidate:
                raise Warning(
                    _("Cannot assign while there are other candidates"))


class MarkVoteCancelled(VoteAction):
    """You declare that you are no longer interested in this ticket."""
    
    # label = pgettext("verb", "Cancel")
    managed_by_votable_author = None
    required_states = 'invited pro con candidate assigned'
    required_votable_states = 'new talk opened started ready'
    # msg_template = _("{user} cancelled {vote} for {ticket}.")
    confirmation_msg_template = _("Cancel {voter}'s {vote}.")


class MarkVoteDone(VoteAction):
    # label = _("Done")
    managed_by_votable_author = False
    required_states = 'assigned'
    required_votable_states = 'new talk opened started ready'
    msg_template = _("{user} confirmed {ticket} {state} by {voter}.")

    
class MarkVoteRated(VoteAction):
    """Rate this vote and mark it as rated.

    .. attribute:: rating

        How you rate this job.

    .. attribute:: comment

        Your comment related to your rating.

    """
    label = _("Rate")
    managed_by_votable_author = True
    required_states = 'assigned done'
    required_votable_states = 'new talk opened started ready'
    parameters = dict(
        rating=Ratings.field(),
        comment=dd.RichTextField(_("Comment"), blank=True))
    # params_layout = dd.ParamsLayout("""
    params_layout = dd.Panel("""
    rating
    comment
    """, window_size=(50, 12))

    # def param_defaults(self, obj, ar, **kw):
    #     kw.update(rating=obj.rating)
    #     return kw
    
    def before_execute(self, ar, obj):
        pv = ar.action_param_values
        # print(20170116, pv)
        obj.rating = pv.rating
        if pv.comment:
            create_row(
                rt.models.comments.Comment, 
                owner=obj.votable,
                short_text=pv.comment, user=ar.get_user())

    # def get_action_permission(self, ar, obj, state):
    #     if not obj.rating:
    #         return False
    #     return super(MarkVoteRated,
    #                  self).get_action_permission(ar, obj, state)



# VoteStates.watching.add_transition(
    # required_states="candidate assigned")

VoteStates.cancelled.add_transition(MarkVoteCancelled)
VoteStates.watching.add_transition(MarkVoteWatching)
VoteStates.pro.add_transition(MarkVotePro)
VoteStates.con.add_transition(MarkVoteCon)
VoteStates.candidate.add_transition(MarkVoteCandidate)
VoteStates.assigned.add_transition(MarkVoteAssigned)
VoteStates.done.add_transition(MarkVoteDone)
VoteStates.rated.add_transition(MarkVoteRated)



# TicketStates.favorite_states = (TicketStates.sticky, )
# TicketStates.work_states = (TicketStates.todo, TicketStates.new)
# TicketStates.waiting_states = (TicketStates.done, )

