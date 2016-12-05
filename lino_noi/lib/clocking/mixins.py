# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines model mixins for this plugin."""


from django.db import models
from django.utils import timezone

from lino.api import dd, rt, _

from lino.mixins.periods import Monthly
from lino.modlib.printing.mixins import DirectPrintAction
from lino.core.roles import SiteUser
from .roles import Worker
from lino_noi.lib.tickets.roles import Triager

from .actions import StartTicketSession, EndTicketSession


class Workable(dd.Model):
    """Base class for things that workers can work on. 

    The model specified in :attr:`ticket_model
    <lino_noi.lib.clocking.Plugin.ticket_model>` must be a subclass of
    this.
    
    For example, in :ref:`noi` tickets are workable, or in
    :ref:`psico` partners are workable.

    """
    class Meta:
        abstract = True

    start_session = StartTicketSession()
    end_session = EndTicketSession()

    def is_workable_for(self, user):
        """Return True if the given user can start a working session on this
        object.

        """
        return True
