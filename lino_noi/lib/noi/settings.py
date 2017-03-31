# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Base Django settings for Lino Noi applications.

"""

from __future__ import print_function
from __future__ import unicode_literals

from lino.projects.std.settings import *
from lino.api.ad import _
from lino_noi import SETUP_INFO

class Site(Site):

    verbose_name = "Lino Noi"
    version = SETUP_INFO['version']
    url = "http://noi.lino-framework.org/"

    demo_fixtures = ['std', 'demo', 'demo2']
                     # 'linotickets',
                     # 'tractickets', 'luc']

    # project_model = 'tickets.Project'
    # project_model = 'deploy.Milestone'
    textfield_format = 'html'
    user_types_module = 'lino_noi.lib.noi.user_types'
    workflows_module = 'lino_noi.lib.noi.workflows'
    obj2text_template = "**{0}**"

    default_build_method = 'appyodt'
    
    # experimental use of rest_framework:
    # root_urlconf = 'lino_book.projects.team.urls'
    
    # TODO: move migrator to lino_noi.projects.team
    migration_class = 'lino_noi.lib.noi.migrate.Migrator'

    auto_configure_logger_names = "atelier django lino lino_xl lino_noi"

    def get_installed_apps(self):
        """Implements :meth:`lino.core.site.Site.get_installed_apps` for Lino
        Noi.

        """
        yield super(Site, self).get_installed_apps()
        # yield 'lino.modlib.extjs'
        # yield 'lino.modlib.bootstrap3'
        yield 'lino.modlib.gfks'
        # yield 'lino.modlib.system'
        # yield 'lino.modlib.users'
        yield 'lino_noi.lib.contacts'
        yield 'lino_noi.lib.users'
        yield 'lino_noi.lib.cal'
        yield 'lino_xl.lib.extensible'
        yield 'lino_noi.lib.courses'
        # yield 'lino_noi.lib.products'

        yield 'lino_noi.lib.topics'
        yield 'lino_xl.lib.votes'
        yield 'lino_noi.lib.tickets'
        yield 'lino_xl.lib.faculties'
        yield 'lino_xl.lib.deploy'
        yield 'lino_noi.lib.clocking'
        yield 'lino_xl.lib.lists'
        yield 'lino_xl.lib.blogs'

        yield 'lino.modlib.changes'
        yield 'lino.modlib.notify'
        yield 'lino.modlib.uploads'
        # yield 'lino_xl.lib.outbox'
        # yield 'lino_xl.lib.excerpts'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.smtpd'
        yield 'lino.modlib.weasyprint'
        yield 'lino_xl.lib.appypod'
        # yield 'lino.modlib.wkhtmltopdf'
        yield 'lino.modlib.dashboard'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi.lib.noi'
        yield 'lino.modlib.restful'
        # yield 'lino_xl.lib.inbox'
        yield 'lino_xl.lib.mailbox'


    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.comments.configure(
            commentable_model='tickets.Ticket')
        self.plugins.faculties.configure(
            demander_model='tickets.Ticket')
        self.plugins.tickets.configure(
            site_model='cal.Room',
            milestone_model='courses.Course')

    def get_default_required(self, **kw):
        # overrides the default behaviour which would add
        # `auth=True`. In Lino Noi everybody can see everything.
        return kw

    def setup_quicklinks(self, user, tb):
        super(Site, self).setup_quicklinks(user, tb)
        tb.add_action(self.actors.courses.MyActivities)
        # tb.add_action(self.modules.deploy.MyMilestones)
        tb.add_action(self.actors.tickets.MyTickets)
        tb.add_action(self.actors.tickets.TicketsToTriage)
        tb.add_action(self.actors.tickets.TicketsToTalk)
        # tb.add_action(self.modules.tickets.TicketsToDo)
        tb.add_action(self.actors.tickets.AllTickets)
        tb.add_action(
            self.actors.tickets.AllTickets.insert_action,
            label=_("Submit a ticket"))

        a = self.actors.users.MySettings.default_action
        tb.add_instance_action(
            user, action=a, label=_("My settings"))
        # handler = self.action_call(None, a, dict(record_id=user.pk))
        # handler = "function(){%s}" % handler
        # mysettings = dict(text=_("My settings"),
        #                   handler=js_code(handler))
        

    def do_site_startup(self):
        super(Site, self).do_site_startup()

        from lino.modlib.changes.models import watch_changes as wc

        wc(self.modules.tickets.Ticket)
        wc(self.modules.comments.Comment, master_key='owner')
        if self.is_installed('extjs'):
            self.plugins.extjs.autorefresh_seconds = 0
        if self.is_installed('votes'):
            wc(self.modules.votes.Vote, master_key='votable')


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

USE_TZ = True
# TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = 'Europe/Tallinn'
TIME_ZONE = 'UTC'

