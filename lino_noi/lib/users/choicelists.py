# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for this plugin.
"""
from lino.api import dd, _

class UserStates(dd.Workflow):
    """
    The list of possible choices for the `state` field
    of a :class:`User`.
    """
    verbose_name = _("User state")
    verbose_name_plural = _("User states")

add = UserStates.add_item
add('10', _("New"), 'new')
add('20', _("Active"), 'active')
add('30', _("Inactive"), 'inactive')

UserStates.active.add_transition(
    _("Activate"), required_states="new")
UserStates.inactive.add_transition(
    _("Deactivate"), required_states="active")
UserStates.new.add_transition(
    _("Reset"), required_states="inactive")

