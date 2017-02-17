# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines the workflows for :mod:`lino_noi.projects.care`. These are
the same as for :mod:`lino_noi.projects.team`, except that we remove
the :attr:`TicketStates.sticky`.

This module is the first usage of
:meth:`lino.core.choicelists.Choice.remove`

"""
from lino_noi.lib.noi.workflows import *

# TicketStates.sticky.remove()
