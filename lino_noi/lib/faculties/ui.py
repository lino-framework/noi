# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)
from __future__ import unicode_literals

from builtins import str

from django.db import models

from lino.api import dd, rt, _
from lino.modlib.users.mixins import My
from lino.modlib.users.desktop import Users
from lino.utils.xmlgen.html import E
from lino.utils import join_elems
from .roles import SkillsStaff

class SkillTypes(dd.Table):
    required_roles = dd.login_required(dd.SiteStaff)
    model = 'faculties.SkillType'
    stay_in_grid = True
    detail_layout = """
    id name
    SkillsByType
    """
    insert_layout = """
    id
    name
    """

class Skills(dd.Table):
    model = 'faculties.Faculty'
    # order_by = ["ref", "name"]
    detail_layout = """
    id name
    skill_type parent affinity
    remarks
    SkillsByParent OffersBySkill
    """
    insert_layout = """
    name
    parent
    """


class AllSkills(Skills):
    label = _("Skills (all)")
    required_roles = dd.login_required(dd.SiteStaff)
    column_names = 'name parent skill_type remarks *'
    order_by = ["name"]


class TopLevelSkills(Skills):
    label = _("Skills (tree)")
    required_roles = dd.login_required(dd.SiteStaff)
    order_by = ["name"]
    column_names = 'name id children_summary parent *'
    filter = models.Q(parent__isnull=True)
    variable_row_height = True


class SkillsByParent(Skills):
    label = _("Child skills")
    master_key = 'parent'
    column_names = 'seqno name affinity *'
    order_by = ["seqno"]
    # order_by = ["parent", "seqno"]
    # order_by = ["name"]
    

class SkillsByType(Skills):
    master_key = 'skill_type' 

class Offers(dd.Table):
    model = 'faculties.Competence'
    required_roles = dd.login_required(dd.SiteStaff)
    # required_roles = dd.login_required(SocialStaff)
    column_names = 'id user faculty description affinity *'
    order_by = ["id"]


class OffersBySupplier(Offers):
    label = _("My skills")
    required_roles = dd.login_required()
    master_key = 'supplier'
    column_names = 'faculty description affinity *'
    order_by = ["faculty"]

# class OffersByUser(OffersBySupplier):
#     required_roles = dd.login_required()
#     master_key = 'user'
#     column_names = 'seqno faculty description affinity *'
#     order_by = ["seqno"]

#     @classmethod
#     def get_filter_kw(self, ar, **kw):
#         user = ar.master_instance
#         return dict(supplier=user.partner)

class OffersBySkill(Offers):
    master_key = 'faculty'
    column_names = 'user affinity *'
    order_by = ["user"]


class MyOffers(My, Offers):
    required_roles = dd.login_required(SkillsStaff)
    label = _("Skills managed by me")
    column_names = 'faculty supplier description affinity *'
    order_by = ["faculty"]



class Demands(dd.Table):
    model = 'faculties.Demand'
    required_roles = dd.login_required(dd.SiteStaff)
    # required_roles = dd.login_required(SocialStaff)
    column_names = 'id demander skill importance *'
    order_by = ["id"]
    

class DemandsByDemander(Demands):
    required_roles = dd.login_required()
    master_key = 'demander'
    # column_names = 'skill importance user *'
    column_names = 'skill importance *'

    slave_grid_format = 'summary'
    # exclude_vote_states = 'author'
    stay_in_grid = True

    detail_layout = dd.DetailLayout("""
    skill 
    importance
    """, window_size=(40, 'auto'))

    insert_layout = """
    skill
    importance
    """

    @classmethod
    def get_slave_summary(self, obj, ar):
        """Customized :meth:`summary view
        <lino.core.actors.Actor.get_slave_summary>` for this table.

        """
        sar = self.request_from(ar, master_instance=obj)

        html = []

        items = [
            ar.obj2html(o, str(o.skill)) for o in sar]

        sar = self.insert_action.request_from(sar)
        if sar.get_permission():
            btn = sar.ar2button()
            items.append(btn)
            
        if len(items) > 0:
            html += join_elems(items, sep=', ')
            
        return E.p(*html)


if dd.is_installed('tickets'):
    
    from lino_noi.lib.tickets.roles import Triager
    
    class AssignableWorkersByTicket(Users):
        # model = 'users.User'
        use_as_default_table = False
        # model = 'faculties.Competence'
        master = 'tickets.Ticket'
        column_names = 'username #faculties_competence_set_by_user__affinity *'
        label = _("Assignable workers")
        required_roles = dd.login_required(Triager)

        @classmethod
        def get_request_queryset(self, ar):
            ticket = ar.master_instance
            if ticket is None:
                return rt.models.users.User.objects.none()

            # rt.models.faculties.Competence.objects.filter(
            #     faculty=ticket.faculty)
            qs = rt.models.users.User.objects.all()
            # qs = super(
            #     AssignableWorkersByTicket, self).get_request_queryset(ar)

            if ticket.topic:
                qs = qs.filter(
                    faculties_competence_set_by_user__topic=ticket.topic)
            cond = models.Q()
            for dem in rt.models.faculties.Demand.objects.filter(
                    demander=ticket):
                faculties = dem.skill.get_parental_line()
                cond |= models.Q(
                    faculties_competence_set_by_user__faculty__in=faculties)
            qs = qs.filter(cond)
            qs = qs.order_by('faculties_competence_set_by_user__affinity')
            return qs

