# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Extends actions for this plugin"""

from lino_noi.lib.clocking.actions import *
from lino.api import dd, rt, _

class EndTicketSessionViaVote(EndTicketSession):
    """End your running session on this ticket via vote.
    """

    def get_action_permission(self, ar, obj, state):
        return super(EndTicketSessionViaVote, self).get_action_permission(
            ar, obj.votable, state)

    def run_from_ui(self, ar, **kw):
        super(StartTicketSessionViaVote, self).run_from_ui(ar, workable=ar.selected_rows[0].votable)

class StartTicketSessionViaVote(StartTicketSession):
    """Start a session on the ticket this vote is attached to"""


    def get_action_permission(self, ar, obj, state):
        return super(StartTicketSessionViaVote, self).get_action_permission(
            ar, obj.votable, state)

    def run_from_ui(self, ar, **kw):
        super(StartTicketSessionViaVote, self).run_from_ui(ar, workable=ar.selected_rows[0].votable)

if True or dd.is_installed('clocking'):  # Sphinx autodoc

    dd.inject_action(
        "votes.Vote",#dd.plugins.clocking.ticket_model, 
        start_session_via_vote=StartTicketSessionViaVote())
    dd.inject_action(
        "votes.Vote",#dd.plugins.clocking.ticket_model,
        end_session_via_vote=EndTicketSessionViaVote())