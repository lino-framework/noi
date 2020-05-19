# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
Base Django settings for Lino Noi applications.

"""

from lino.projects.std.settings import *
from lino.api.ad import _
from lino_noi import SETUP_INFO

class Site(Site):

    verbose_name = "Lino Noi"
    version = SETUP_INFO['version']
    url = "http://noi.lino-framework.org/"

    demo_fixtures = ['std', 'minimal_ledger', 'demo', 'demo2', 'checksummaries']
                     # 'linotickets',
                     # 'tractickets', 'luc']

    # project_model = 'tickets.Project'
    # project_model = 'deploy.Milestone'
    textfield_format = 'html'
    user_types_module = 'lino_noi.lib.noi.user_types'
    workflows_module = 'lino_noi.lib.noi.workflows'
    # custom_layouts_module = 'lino_noi.lib.noi.layouts'
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
        yield 'lino_xl.lib.calview'
        # yield 'lino_xl.lib.extensible'
        # yield 'lino_noi.lib.courses'
        # yield 'lino_noi.lib.products'

        # yield 'lino_noi.lib.topics'
        # yield 'lino_xl.lib.votes'
        # yield 'lino_xl.lib.stars'
        yield 'lino_noi.lib.tickets'
        # yield 'lino_xl.lib.skills'
        # yield 'lino_xl.lib.deploy'
        yield 'lino_xl.lib.working'
        yield 'lino_xl.lib.lists'
        # yield 'lino_xl.lib.blogs'

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
        yield 'lino.modlib.checkdata'
        # yield 'lino.modlib.wkhtmltopdf'
        yield 'lino.modlib.dashboard'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi.lib.noi'
        # yield 'lino_xl.lib.inbox'
        # yield 'lino_xl.lib.mailbox'
        # yield 'lino_xl.lib.meetings'
        yield 'lino_xl.lib.github'
        # yield 'lino.modlib.social_auth'
        yield 'lino_xl.lib.userstats'
        yield 'lino_noi.lib.groups'

        yield 'lino_noi.lib.products'
        yield 'lino_xl.lib.invoicing'

    def get_plugin_configs(self):
        yield super(Site, self).get_plugin_configs()
        yield ('tickets', 'end_user_model', 'contacts.Person')
        yield ('working', 'ticket_model', 'tickets.Ticket')


    # def setup_plugins(self):
    #     super(Site, self).setup_plugins()
    #     # self.plugins.comments.configure(
    #     #     commentable_model='tickets.Ticket')
    #     # self.plugins.skills.configure(
    #     #     demander_model='tickets.Ticket')
    #     # self.plugins.tickets.configure(
    #     #     site_model='cal.Room',
    #     #     milestone_model='courses.Course')
    #     self.plugins.working.configure(
    #         ticket_model='tickets.Ticket')


    def get_default_required(self, **kw):
        # overrides the default behaviour which would add
        # `auth=True`. In Lino Noi everybody can see everything.
        return kw

    def setup_quicklinks(self, user, tb):
        super(Site, self).setup_quicklinks(user, tb)
        # tb.add_action(self.models.courses.MyCourses)
        # tb.add_action(self.models.meetings.MyMeetings)
        # tb.add_action(self.modules.deploy.MyMilestones)
        # tb.add_action(self.models.tickets.MyTickets)
        # tb.add_action(self.models.tickets.TicketsToTriage)
        # tb.add_action(self.models.tickets.TicketsToTalk)
        # tb.add_action(self.modules.tickets.TicketsToDo)
        tb.add_action(self.models.tickets.RefTickets)
        tb.add_action(self.models.tickets.ActiveTickets)
        tb.add_action(self.models.tickets.AllTickets)
        tb.add_action(
            self.models.tickets.AllTickets.insert_action,
            label=_("Submit a ticket"))

        a = self.models.users.MySettings.default_action
        tb.add_instance_action(
            user, action=a, label=_("My settings"))
        # handler = self.action_call(None, a, dict(record_id=user.pk))
        # handler = "function(){%s}" % handler
        # mysettings = dict(text=_("My settings"),
        #                   handler=js_code(handler))


    def do_site_startup(self):
        super(Site, self).do_site_startup()

        from lino.utils.watch import watch_changes as wc

        wc(self.modules.tickets.Ticket, ignore=['_user_cache'])
        wc(self.modules.comments.Comment, master_key='owner')
        # wc(self.modules.working.Session, master_key='owner')

        if self.is_installed('votes'):
            wc(self.modules.votes.Vote, master_key='votable')

        if self.is_installed('deploy'):
            wc(self.modules.deploy.Deployment, master_key='ticket')

        if self.is_installed('extjs'):
            self.plugins.extjs.autorefresh_seconds = 0

        # from lino.core.merge import MergeAction
        # from lino_xl.lib.contacts.roles import ContactsStaff
        # lib = self.models
        # for m in (lib.contacts.Company, ):
        #     m.define_action(merge_row=MergeAction(
        #         m, required_roles=set([ContactsStaff])))

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

USE_TZ = True
# TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = 'Europe/Tallinn'
TIME_ZONE = 'UTC'
