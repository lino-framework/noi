# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""

.. autosummary::
   :toctree:

   demo
   doctests
   www
   memory
   fixtures



"""

from __future__ import print_function
from __future__ import unicode_literals

from lino_noi.projects.team.settings import *


class Site(Site):

    verbose_name = "Lino Care"

    demo_fixtures = ['std', 'demo', 'demo2']
    user_types_module = 'lino_noi.projects.care.roles'

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.topics.configure(
            partner_model='users.User', menu_group=None)
        # self.plugins.lists.partner_model = 'users.User'
        self.plugins.countries.configure(hide_region=True)

    def get_apps_modifiers(self, **kw):
        kw = super(Site, self).get_apps_modifiers(**kw)

        # remove whole plugin:
        # kw.update(products=None)
        # kw.update(clocking=None)
        kw.update(blogs=None)
        kw.update(deploy=None)
        kw.update(contacts=None)
        kw.update(lists=None)
        kw.update(outbox=None)
        # kw.update(excerpts=None)

        # alternative implementations:
        kw.update(tickets='lino_noi.projects.care.lib.tickets')
        kw.update(users='lino_noi.lib.users')
        return kw


# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'
