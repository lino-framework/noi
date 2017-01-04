# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for this plugin.
"""
from lino.api import dd, _


from lino.core.roles import SiteAdmin

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


    
class MarkUserActive(dd.ChangeStateAction):
    """Activate this user. This requires that the user has confirmed their
    verifcation code, and that a username and password are set.

    """
    label = _("Activate")
    required_states = 'new'
    required_roles = dd.required(SiteAdmin)
    # show_in_bbar = True
    
    def get_action_permission(self, ar, obj, state):
        if not obj.profile or not obj.username:
            return False
        if obj.verification_code:
            return False
        return super(MarkUserActive,
                     self).get_action_permission(ar, obj, state)

    


UserStates.active.add_transition(MarkUserActive)
UserStates.inactive.add_transition(
    _("Deactivate"), required_states="active")
UserStates.new.add_transition(
    _("Reset"), required_states="inactive")

