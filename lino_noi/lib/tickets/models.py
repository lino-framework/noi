# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

import six
from builtins import str

from importlib import import_module
import inspect
from collections import OrderedDict
    
from django.conf import settings
from django.db import models
from django.db.models import Q

from atelier.sphinxconf.base import srcref

from lino import mixins
from lino.api import dd, rt, _, pgettext

from lino.utils.xmlgen.html import E

from lino_xl.lib.cal.mixins import daterange_text
from lino_xl.lib.contacts.mixins import ContactRelated
from lino.modlib.users.mixins import UserAuthored, Assignable
from lino.modlib.comments.mixins import Commentable
from lino_xl.lib.excerpts.mixins import Certifiable
from lino_noi.lib.votes.mixins import Votable
from lino_noi.lib.clocking.mixins import Workable
from lino_noi.lib.clocking.choicelists import ReportingTypes
from lino.utils import join_elems

from .choicelists import TicketEvents, TicketStates, LinkTypes
from .roles import Triager

class Prioritized(dd.Model):
    class Meta:
        abstract = True
    priority = models.SmallIntegerField(_("Priority"), default=100)

    
class TimeInvestment(Commentable):
    class Meta:
        abstract = True

    closed = models.BooleanField(_("Closed"), default=False)
    # private = models.BooleanField(_("Private"), default=True)

    planned_time = models.TimeField(
        _("Planned time"),
        blank=True, null=True)

    # invested_time = models.TimeField(
    #     _("Invested time"), blank=True, null=True, editable=False)


class ProjectType(mixins.BabelNamed):

    class Meta:
        app_label = 'tickets'
        verbose_name = _("Project Type")
        verbose_name_plural = _('Project Types')


class TicketType(mixins.BabelNamed):
    """The type of a :class:`Ticket`."""

    class Meta:
        app_label = 'tickets'
        verbose_name = _("Ticket type")
        verbose_name_plural = _('Ticket types')


#~ class Repository(UserAuthored):
    #~ class Meta:
        #~ verbose_name = _("Repository")
        #~ verbose_name_plural = _('Repositories')


@dd.python_2_unicode_compatible
class Project(mixins.DatePeriod, TimeInvestment,
              mixins.Hierarchical, mixins.Referrable,
              ContactRelated):
    class Meta:
        app_label = 'tickets'
        verbose_name = _("Project")
        verbose_name_plural = _('Projects')

    name = models.CharField(_("Name"), max_length=200)
    # parent = models.ForeignKey(
    #     'self', blank=True, null=True, verbose_name=_("Parent"))
    assign_to = dd.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Assign tickets to"),
        blank=True, null=True,
        help_text=_("The user to whom new tickets will be assigned."))
    type = dd.ForeignKey('tickets.ProjectType', blank=True, null=True)
    description = dd.RichTextField(_("Description"), blank=True)
    srcref_url_template = models.CharField(blank=True, max_length=200)
    changeset_url_template = models.CharField(blank=True, max_length=200)
    # root = models.ForeignKey(
    #     'self', blank=True, null=True, verbose_name=_("Root"))
    if dd.is_installed('clocking'):
        reporting_type = ReportingTypes.field(blank=True)
    else:
        reporting_type = dd.DummyField()

    def __str__(self):
        return self.ref or self.name

    @dd.displayfield(_("Activity overview"))
    def activity_overview(self, ar):
        if ar is None:
            return ''
        TicketsByProject = rt.modules.tickets.TicketsByProject
        elems = []
        for tst in (TicketStates.objects()):
            pv = dict(state=tst)
            sar = ar.spawn(
                TicketsByProject, master_instance=self, param_values=pv)
            num = sar.get_total_count()
            if num > 0:
                elems += [
                    "{0}: ".format(tst.text),
                    sar.ar2button(label=str(num))]
        return E.p(*elems)

    # def save(self, *args, **kwargs):
    #     root = self.parent
    #     while root is not None:
    #         if root.parent is None:
    #             break
    #         else:
    #             root = root.parent
    #     self.root = root
    #     super(Project, self).save(*args, **kwargs)


@dd.python_2_unicode_compatible
class Site(dd.Model):
    class Meta:
        app_label = 'tickets'
        verbose_name = pgettext("Ticketing", "Site")
        verbose_name_plural = pgettext("Ticketing", "Sites")

    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)
    # responsible_user = dd.ForeignKey(
    #     'users.User', verbose_name=_("Responsible"),
    #     blank=True, null=True)
    name = models.CharField(_("Designation"), max_length=200)
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    def __str__(self):
        return self.name
    
#@dd.python_2_unicode_compatible
class Competence(UserAuthored, Prioritized):

    class Meta:
        app_label = 'tickets'
        verbose_name = pgettext("Ticketing", "Competence")
        verbose_name_plural = pgettext("Ticketing", "Competences")
        unique_together = ['user', 'project']

    project = dd.ForeignKey(
        'tickets.Project', blank=True, null=True,
        related_name="duties_by_project")
    remark = models.CharField(_("Remark"), max_length=200, blank=True)
    description = dd.RichTextField(_("Description"), blank=True)

    # def __str__(self):
    #     return pgettext("{}/{}").format(self.user, self.project)

    @dd.displayfield(_("Tickets overview"))
    def tickets_overview(self, ar):
        if ar is None:
            return ''
        me = ar.get_user()
        # Ticket = rt.models.tickets.Ticket
        Vote = rt.models.votes.Vote
        elems = []

        tickets_by_state = OrderedDict()
        for st in TicketStates.objects():
            tickets_by_state[st] = set()
        for vote in Vote.objects.filter(project=self.project):
            t = vote.votable
            tickets_by_state[t.state].add(t)
            
        items = []
        for st, tickets in tickets_by_state.items():
            if len(tickets) > 0:
                tickets = reversed(sorted(tickets))
                items.append(E.li(
                    E.span("{} : ".format(st.button_text), title=str(st)),
                    *join_elems([x.obj2href(ar) for x in tickets], ', ')
                ))
        elems.append(E.ul(*items))
        return E.p(*elems)

    
#@dd.python_2_unicode_compatible
# class Wish(UserAuthored, Prioritized):

#     class Meta:
#         app_label = 'tickets'
#         verbose_name = pgettext("Ticketing", "Wish")
#         verbose_name_plural = pgettext("Ticketing", "Wishes")

#     ticket = dd.ForeignKey(
#         'tickets.Ticket',
#         related_name='wishes_by_ticket')
#     project = dd.ForeignKey(
#         'tickets.Project',
#         related_name="wishes_by_project")
#     remark = models.CharField(_("Remark"), max_length=200, blank=True)
#     description = dd.RichTextField(_("Description"), blank=True)

    # def __str__(self):
    #     return pgettext("{} for {}").format(self.project, self.ticket)

    
    
# class CloseTicket(dd.Action):
#     #label = _("Close ticket")
#     label = "\u2611"
#     help_text = _("Mark this ticket as closed.")
#     show_in_workflow = True
#     show_in_bbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is not None or obj.closed is not None:
#             return False
#         return super(CloseTicket, self).get_action_permission(ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         now = datetime.datetime.now()
#         for obj in ar.selected_rows:
#             obj.closed = now
#             obj.save()
#             ar.set_response(refresh=True)


# class StandbyTicket(dd.Action):
#     #label = _("Standby mode")
#     label = "\u2a37"
#     label = "\u2609"
#     help_text = _("Put this ticket into standby mode.")
#     show_in_workflow = True
#     show_in_bbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is not None or obj.closed is not None:
#             return False
#         return super(StandbyTicket, self).get_action_permission(
#             ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         now = datetime.datetime.now()
#         for obj in ar.selected_rows:
#             obj.standby = now
#             obj.save()
#             ar.set_response(refresh=True)


# class ActivateTicket(dd.Action):
#     # label = _("Activate")
#     label = "☀"  # "\u2600"
#     help_text = _("Reactivate this ticket from standby mode or closed state.")
#     show_in_workflow = True
#     show_in_bbar = False

#     def get_action_permission(self, ar, obj, state):
#         if obj.standby is None and obj.closed is None:
#             return False
#         return super(ActivateTicket, self).get_action_permission(
#             ar, obj, state)

#     def run_from_ui(self, ar, **kw):
#         for obj in ar.selected_rows:
#             obj.standby = False
#             obj.closed = False
#             obj.save()
#             ar.set_response(refresh=True)


class SpawnTicket(dd.Action):
    # label = _("Spawn new ticket")
    # label = "\u2611" "☑"
    # label = "⚇"  # "\u2687"
    show_in_workflow = False
    show_in_bbar = False

    def __init__(self, label, link_type):
        self.label = label
        self.link_type = link_type
        self.help_text = _(
            "Spawn a new child ticket {0} this one.").format(
            link_type.as_child())
        super(SpawnTicket, self).__init__()

    def run_from_ui(self, ar, **kw):
        p = ar.selected_rows[0]
        c = rt.modules.tickets.Ticket(
            user=ar.get_user(),
            summary=_("New ticket {0} #{1}".format(
                self.link_type.as_child(), p.id)))
        for k in ('project', 'private'):
            setattr(c, k, getattr(p, k))
        c.full_clean()
        c.save()
        d = rt.modules.tickets.Link(
            parent=p, child=c,
            type=self.link_type)
        d.full_clean()
        d.save()
        ar.success(
            _("New ticket {0} has been spawned as child of {1}.").format(
                c, p))
        ar.goto_instance(c)

@dd.python_2_unicode_compatible
class Ticket(UserAuthored, mixins.CreatedModified,
             TimeInvestment, Votable, Workable, Prioritized):
    
    quick_search_fields = "summary description"

    workflow_state_field = 'state'

    class Meta:
        app_label = 'tickets'
        verbose_name = _("Ticket")
        verbose_name_plural = _('Tickets')
        abstract = dd.is_abstract_model(__name__, 'Ticket')
    project = dd.ForeignKey(
        'tickets.Project', blank=True, null=True,
        related_name="tickets_by_project")
    site = dd.ForeignKey('tickets.Site', blank=True, null=True)
    topic = dd.ForeignKey('topics.Topic', blank=True, null=True)
    # nickname = models.CharField(_("Nickname"), max_length=50, blank=True)
    summary = models.CharField(
        pgettext("Ticket", "Summary"), max_length=200,
        blank=True,
        help_text=_("Short summary of the problem."))
    description = dd.RichTextField(_("Description"), blank=True)
    upgrade_notes = dd.RichTextField(_("Upgrade notes"), blank=True)
    ticket_type = dd.ForeignKey('tickets.TicketType', blank=True, null=True)
    duplicate_of = models.ForeignKey(
        'self', blank=True, null=True, verbose_name=_("Duplicate of"))

    reported_for = dd.ForeignKey(
        'deploy.Milestone',
        related_name='tickets_reported',
        verbose_name='Reported for',
        blank=True, null=True,
        help_text=_("Milestone for which this ticket has been reported."))
    fixed_for = dd.ForeignKey(  # no longer used since 20150814
        'deploy.Milestone',
        related_name='tickets_fixed',
        verbose_name='Fixed for',
        blank=True, null=True,
        help_text=_("The milestone for which this ticket has been fixed."))
    # assigned_to = dd.ForeignKey(
    #     settings.SITE.user_model,
    #     verbose_name=_("Assigned to"),
    #     related_name="assigned_tickets",
    #     blank=True, null=True,
    #     help_text=_("The user who works on this ticket."))

    reporter = dd.ForeignKey(
        settings.SITE.user_model,
        blank=True, null=True,
        verbose_name=_("Reporter"))
    end_user = dd.ForeignKey(
        dd.plugins.tickets.end_user_model,
        verbose_name=_("End user"),
        blank=True, null=True,
        related_name="reported_tickets")
    state = TicketStates.field(default=TicketStates.as_callable('new'))
    # rating = Ratings.field(blank=True)
    deadline = models.DateField(
        verbose_name=_("Deadline"),
        blank=True, null=True)

    # deprecated fields:
    waiting_for = models.CharField(
        _("Waiting for"), max_length=200, blank=True)
    feedback = models.BooleanField(
        _("Feedback"), default=False)
    standby = models.BooleanField(_("Standby"), default=False)

    spawn_triggered = SpawnTicket(
        _("Spawn triggered ticket"),
        LinkTypes.triggers)
    # spawn_triggered = SpawnTicket("⚇", LinkTypes.triggers)  # "\u2687"
    # spawn_ticket = SpawnTicket("", LinkTypes.requires)  # "\u2687"

    # def get_rfc_description(self, ar):
    #     return ar.parse_memo(self.description)

    def full_clean(self):
        if self.id and self.duplicate_of_id == self.id:
            self.duplicate_of = None
        # print "20150523b on_create", self.reporter
        super(Ticket, self).full_clean()
        if self.project:
            # if not self.assigned_to and self.project.assign_to:
            #     self.assigned_to = self.project.assign_to
            if not self.project.private:
                self.private = False

    def get_project_for_vote(self, vote):
        if self.project:
            return self.project
        qs = rt.models.tickets.Competence.objects.filter(user=vote.user)
        qs = qs.order_by('priority')
        if qs.count() > 0:
            return qs[0].project
        return rt.models.tickets.Project.objects.all()[0]
            
    def obj2href(self, ar, **kwargs):
        """Return a tuple (text, attributes) to use when rendering an `<a
        href>` that points to this object.

        """
        kwargs.update(title=self.summary)
        return ar.obj2html(self, "#{}".format(self.id), **kwargs)

    def disabled_fields(self, ar):
        rv = super(Ticket, self).disabled_fields(ar)
        if self.project and not self.project.private:
            rv.add('private')
        if not ar.get_user().profile.has_required_roles([Triager]):
            rv.add('user')
            rv.add('end_user')
        return rv

    # def get_choices_text(self, request, actor, field):
    #     return "{0} ({1})".format(self, self.summary)

    def __str__(self):
        # if self.nickname:
        #     return "#{0} ({1})".format(self.id, self.nickname)
        if False and self.state.button_text:
            return "#{0} ({1} {2})".format(
                self.id, self.state.button_text, self.summary)
        
        return "#{0} ({1})".format(self.id, self.summary)
    

    @dd.chooser()
    def reported_for_choices(cls, site):
        if not site:
            return []
        # return site.milestones_by_site.filter(reached__isnull=False)
        return site.milestones_by_site.all()

    @dd.chooser()
    def fixed_for_choices(cls, site):
        if not site:
            return []
        return site.milestones_by_site.all()

    def get_overview_elems(self, ar):
        """Overrides :meth:`lino.core.model.Model.get_overview_elems`.
        """
        elems = [ ar.obj2html(self) ]  # show full summary
        if self.user and self.user != ar.get_user():
            elems += [ _(" by "), self.user.obj2href(ar)]
        if self.end_user_id:
            elems += [' ', _("for"), ' ', self.end_user.obj2href(ar)]
        # if ar.actor.model is self.__class__:
        #     elems += [E.br(), _("{} state:").format(
        #         self._meta.verbose_name), ' ']
        #     elems += self.get_workflow_buttons(ar)
        # else:
        #     elems += [' (', str(self.state.button_text), ')']
        return elems

    # def get_change_body(self, ar, cw):
    #     return E.tostring(E.p(
    #         _("{user} worked on [ticket {t}]").format(
    #             user=ar.get_user(), t=self.id)))

    def get_vote_raters(self):

        """"Yield the
        :meth:`lino_noi.lib.votes.mixins.Votable.get_vote_raters` for
        this ticket.  This is the author and (if set) the
        :attr:`end_user`.

        """
        if self.user:
            yield self.user
        if issubclass(
                dd.plugins.tickets.end_user_model,
                settings.SITE.user_model):
            if self.end_user:
                yield self.end_user
       
    def is_workable_for(self, user):
        if self.standby or self.closed:
            return False
        if not self.state.active and not user.profile.has_required_roles(
                [Triager]):
            return False
        return True
        
    @dd.displayfield(_("Suppliers"))
    def suppliers(self, ar):
        """Displays a list of candidate suppliers.

        This means: all suppliers who have at least one of the
        skills required by this ticket.

        """
        if ar is None:
            return ''

        Supply = rt.models.faculties.Competence
        Demand = rt.models.faculties.Demand
        faculties = set()
        for dem in Demand.objects.filter(demander=self):
            faculties.add(dem.skill)
            # faculties |= set(dem.skill.get_parental_line())

        elems = []
        for spl in Supply.objects.filter(faculty__in=faculties):
            if spl.supplier is not None:
                elems.append(spl.supplier.obj2href(ar))
        elems = join_elems(elems, ', ')
        return E.p(*elems)


    @dd.displayfield(_("Needed skills"))
    def needed_skills(self, ar):
        """Displays a list of needed skills.

        This means: all skill demands for this ticket.

        """
        if ar is None:
            return ''

        Demand = rt.models.faculties.Demand
        elems = []
        for dem in Demand.objects.filter(demander=self):
            elems.append(dem.skill.obj2href(ar))
        elems = join_elems(elems, ', ')
        return E.p(*elems)


# dd.update_field(Ticket, 'user', verbose_name=_("Reporter"))


@dd.python_2_unicode_compatible
class Link(dd.Model):

    class Meta:
        app_label = 'tickets'
        verbose_name = _("Dependency")
        verbose_name_plural = _("Dependencies")

    type = LinkTypes.field(
        default=LinkTypes.requires.as_callable)
    parent = dd.ForeignKey(
        'tickets.Ticket',
        verbose_name=_("Parent"),
        related_name='tickets_children')
    child = dd.ForeignKey(
        'tickets.Ticket',
        blank=True, null=True,
        verbose_name=_("Child"),
        related_name='tickets_parents')

    @dd.displayfield(_("Type"))
    def type_as_parent(self, ar):
        # print('20140204 type_as_parent', self.type)
        return self.type.as_parent()

    @dd.displayfield(_("Type"))
    def type_as_child(self, ar):
        # print('20140204 type_as_child', self.type)
        return self.type.as_child()

    def __str__(self):
        if self.type is None:
            return "Link object"  # super(Link, self).__unicode__()
        return _("%(child)s is %(what)s") % dict(
            child=str(self.child),
            what=self.type_of_parent_text())

    def type_of_parent_text(self):
        return _("%(type)s of %(parent)s") % dict(
            parent=self.parent,
            type=self.type.as_child())


# dd.inject_field(
#     'users.User', 'project',
#     dd.ForeignKey(
#         'tickets.Project',
#         blank=True, null=True, related_name="users_by_project",
#         help_text=_("The project you are currently working on")))


@dd.receiver(dd.post_startup)
def setup_memo_commands(sender=None, **kwargs):

    """See :doc:`/specs/memo`."""

    Ticket = sender.models.tickets.Ticket
    
    sender.kernel.memo_parser.register_django_model(
        'ticket', Ticket, title=lambda obj: obj.summary)
    
    # def ticket2html(parser, s):
    #     args = s.split(None, 1)
    #     if len(args) == 1:
    #         pk = s
    #         txt = None
    #     else:
    #         pk = args[0]
    #         txt = args[1]
            
    #     ar = parser.context['ar']
    #     kw = dict()
    #     # dd.logger.info("20161019 %s", ar.renderer)
    #     pk = int(pk)
    #     obj = Ticket.objects.get(pk=pk)
    #     if txt is None:
    #         txt = "#{0}".format(obj.id)
    #         kw.update(title=obj.summary)
    #     e = ar.obj2html(obj, txt, **kw)
    #     return E.tostring(e)
    #     # url = rnd.get_detail_url(obj)
    #     # title = obj.summary
    #     # return '<a href="{0}" title="{2}">{1}</a>'.format(url, text, title)

    # sender.memo_parser.register_command('ticket', ticket2html)

    # def ticket2memo(obj):
    #     return "[ticket {}] ({})".format(obj.id, obj.summary)
    # sender.memo_parser.register_renderer(Ticket, ticket2memo)


    def py2html(parser, s):
        args = s.split(None, 1)
        if len(args) == 1:
            txt = s
        else:
            s = args[0]
            txt = args[1]
        parts = s.split('.')
        try:
            obj = import_module(parts[0])
            for p in parts[1:]:
                obj = getattr(obj, p)
            mod = inspect.getmodule(obj)
            url = srcref(mod)
        except Exception as e:
            url = "Oops: {}".format(e)
        # fn = inspect.getsourcefile(obj)
        if url:
            # lines = inspect.getsourcelines(s)
            return '<a href="{0}" target="_blank">{1}</a>'.format(url, txt)
        return "<pre>{}</pre>".format(s)
    sender.kernel.memo_parser.register_command('py', py2html)


    # rnd = sender.site.plugins.extjs.renderer
    
    # def f(s):
    #     pk = int(s)
    #     obj = sender.modules.tickets.Ticket.objects.get(pk=pk)
    #     url = rnd.get_detail_url(obj)
    #     text = "#{0}".format(obj.id)
    #     title = obj.summary
    #     return '<a href="{0}" title="{2}">{1}</a>'.format(url, text, title)

    # rnd.memo_parser.register_command('ticket', f)


from .ui import *
