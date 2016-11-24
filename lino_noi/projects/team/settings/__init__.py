# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""

.. autosummary::
   :toctree:

   doctests
   demo
   www



"""

from __future__ import print_function
from __future__ import unicode_literals

from lino.projects.std.settings import *
from lino.api.ad import _

class Site(Site):

    verbose_name = "Lino Noi"
    version = '1.0.2'

    url = "http://noi.lino-framework.org/"
    server_url = "http://team.lino-framework.org/"

    demo_fixtures = ['std', 'demo', 'demo2']
                     # 'linotickets',
                     # 'tractickets', 'luc']

    project_model = 'tickets.Project'
    textfield_format = 'html'
    user_types_module = 'lino_noi.lib.noi.roles'
    obj2text_template = "**{0}**"

    default_build_method = 'appyodt'
    migration_class = 'lino_noi.lib.noi.migrate.Migrator'

    def get_installed_apps(self):
        """Implements :meth:`lino.core.site.Site.get_installed_apps` for Lino
        Noi.

        """
        yield super(Site, self).get_installed_apps()
        # yield 'lino.modlib.extjs'
        # yield 'lino.modlib.bootstrap3'
        yield 'lino.modlib.gfks'
        # yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino_noi.lib.contacts'
        # yield 'lino_xl.lib.cal'
        # yield 'lino_noi.lib.products'

        yield 'lino_noi.lib.topics'
        yield 'lino_noi.projects.team.lib.tickets'
        yield 'lino_noi.lib.faculties'
        yield 'lino_noi.lib.deploy'
        yield 'lino_noi.projects.team.lib.clocking'
        yield 'lino_xl.lib.lists'
        yield 'lino_xl.lib.blogs'

        # yield 'lino.modlib.uploads'
        # yield 'lino_xl.lib.excerpts'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.smtpd'
        yield 'lino.modlib.weasyprint'
        yield 'lino_xl.lib.appypod'
        yield 'lino.modlib.wkhtmltopdf'

        # yield 'lino.modlib.awesomeuploader'

        yield 'lino_noi.lib.noi'

    def get_default_required(self, **kw):
        # overrides the default behaviour which would add
        # `auth=True`. In Lino Noi everybody can see everything.
        return kw

    def get_admin_main_items(self, ar):
        
        if self.is_installed('blogs'):
            yield self.models.blogs.Entry.latest_entries(ar, max_num=10)

        me = ar.get_user()
        if me.authenticated:
            if me.mail_mode != self.actors.notify.MailModes.immediately:
                yield self.actors.notify.MyMessages
            yield self.actors.clocking.WorkedHours
            yield self.actors.tickets.TicketsToDo
            yield self.actors.tickets.SuggestedTickets
            yield self.actors.tickets.MyTickets
            # yield self.actors.tickets.ActiveTickets
            # yield self.actors.tickets.InterestingTickets
        else:
            # yield self.actors.blogs.LatestEntries
            # from lino_xl.lib.blogs.models import latest_entries
            # yield latest_entries(ar)
            yield self.actors.tickets.PublicTickets
        # yield self.actors.tickets.ActiveProjects

    def setup_quicklinks(self, ar, tb):
        super(Site, self).setup_quicklinks(ar, tb)
        tb.add_action(self.modules.tickets.MyTickets)
        tb.add_action(self.modules.tickets.TicketsToTriage)
        tb.add_action(self.modules.tickets.TicketsToTalk)
        tb.add_action(self.modules.tickets.TicketsToDo)
        tb.add_action(self.modules.tickets.AllTickets)
        tb.add_action(
            self.modules.tickets.AllTickets.insert_action,
            label=_("Submit a ticket"))

        a = self.actors.users.MySettings.default_action
        tb.add_instance_action(ar.get_user(), action=a)
        # handler = self.action_call(None, a, dict(record_id=user.pk))
        # handler = "function(){%s}" % handler
        # mysettings = dict(text=_("My settings"),
        #                   handler=js_code(handler))
        

    def unused_do_site_startup(self):
        """Defines an emitter to send notification emails about changes in
        tickets.

        """
        super(Site, self).do_site_startup()

        from lino.utils.sendchanges import Emitter
        for_obj = self.modules.stars.Star.for_obj

        class TicketEmitter(Emitter):

            model = 'tickets.Ticket'
            watched_fields = '*'
            created_tpl = 'tickets/Ticket/created.eml'
            updated_tpl = 'tickets/Ticket/updated.eml'
            deleted_tpl = 'tickets/Ticket/deleted.eml'

            def get_recipients(self, obj=None, master=None, **kwargs):
                obj = master or obj
                for u in (obj.reporter, obj.assigned_to) + tuple(
                        [o.user for o in for_obj(obj)]):
                    if u and u.email:
                        yield u.email

        TicketEmitter().register()

    def do_site_startup(self):
        super(Site, self).do_site_startup()

        from lino.modlib.changes.models import watch_changes as wc

        wc(self.modules.tickets.Ticket)
        wc(self.modules.comments.Comment, master_key='owner')
        if self.is_installed('extjs'):
            self.plugins.extjs.autorefresh_seconds = 0


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

USE_TZ = True
# TIME_ZONE = 'Europe/Brussels'
# TIME_ZONE = 'Europe/Tallinn'
TIME_ZONE = 'UTC'

