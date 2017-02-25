# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for :mod:`lino_noi.lib.faculties`.

"""

import logging
# from lino_noi.lib.tickets.models import *

from lino.api import dd, _

# from lino.utils import join_elems
from lino.utils.xmlgen.html import E, join_elems

from django.db import models
from lino.mixins import Hierarchical, Sequenced
from lino.utils.mldbc.mixins import BabelNamed

from lino.modlib.users.mixins import UserAuthored

MAX_WEIGHT = 100

class SkillType(BabelNamed):
    class Meta:
        verbose_name = _("Skill type")
        verbose_name_plural = _("Skill types")
        ordering = ['name']


# class Faculty(BabelNamed, Hierarchical, Sequenced, Referrable):
class Faculty(BabelNamed, Hierarchical, Sequenced):
    """A **faculty** is a skill, knowledge or ability which can be
    required in order to work e.g. on some ticket, and which
    individual users can have (offer) or not.

    """

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ['name']

    affinity = models.IntegerField(
        _("Affinity"), blank=True, default=MAX_WEIGHT,
        help_text=_(
            "How much workers enjoy to get a new ticket "
            "requiring this skill."
            "A number between -{0} and +{0}.").format(MAX_WEIGHT))

    skill_type = dd.ForeignKey(
        'faculties.SkillType', null=True, blank=True)

    remarks = dd.RichTextField(_("Remarks"), blank=True)
    
    # topic_group = dd.ForeignKey(
    #     'topics.TopicGroup', blank=True, null=True,
    #     verbose_name=_("Options category"),
    #     help_text=_("The topic group to use for "
    #                 "specifying additional options."))


dd.update_field(Faculty, 'parent', verbose_name=_("Parent faculty"))


class Competence(UserAuthored, Sequenced):
    """A **competence** is when a given *user* is declared to be competent
    in a given *faculty*.

    .. attribute:: user
    .. attribute:: supplier
    .. attribute:: faculty
    .. attribute:: affinity

    """
    
    allow_cascaded_delete = "supplier user"

    class Meta:
        verbose_name = _("Skill offer")
        verbose_name_plural = _("Skill offers")
        unique_together = ['supplier', 'faculty']

    faculty = dd.ForeignKey('faculties.Faculty')
    supplier = dd.ForeignKey(
        dd.plugins.faculties.supplier_model,
        verbose_name=_("Supplier"),
        blank=True, null=True)
    affinity = models.IntegerField(
        _("Affinity"), blank=True, default=MAX_WEIGHT,
        help_text=_(
            "How much this user likes to get a new ticket "
            "in this faculty."
            "A number between -{0} and +{0}.").format(MAX_WEIGHT))
    description = dd.RichTextField(_("Description"), blank=True)
    
    # topic = dd.ForeignKey(
    #     'topics.Topic', blank=True, null=True,
    #     verbose_name=_("Option"),
    #     help_text=_("Some faculties can require additional "
    #                 "options for a competence."))

    # @dd.chooser()
    # def topic_choices(cls, faculty):
    #     Topic = rt.modules.topics.Topic
    #     if not faculty or not faculty.topic_group:
    #         return Topic.objects.none()
    #     return Topic.objects.filter(topic_group=faculty.topic_group)

    def full_clean(self, *args, **kw):
        if self.affinity is None:
            self.affinity = self.faculty.affinity
        # if self.faculty.product_cat:
        #     if not self.product:
        #         raise ValidationError(
        #             "A {0} competence needs a {1} as option")
        super(Competence, self).full_clean(*args, **kw)

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)


dd.update_field(Competence, 'user', verbose_name=_("User"))


#class Demand(UserAuthored):
class Demand(dd.Model):
    """A **Skill demand** is when a given *end user* declares to need a
    given skill.

    .. attribute:: demander
    .. attribute:: skill

    """
    
    allow_cascaded_delete = "demander"

    class Meta:
        verbose_name = _("Skill demand")
        verbose_name_plural = _("Skill demands")
        # unique_together = ['user', 'faculty', 'topic']
        unique_together = ['demander', 'skill']

    skill = dd.ForeignKey('faculties.Faculty')
    demander = dd.ForeignKey(
        dd.plugins.faculties.demander_model,
        verbose_name=_("Demander"),
        blank=True, null=True)
    importance = models.IntegerField(
        _("Importance"), blank=True, default=MAX_WEIGHT,
        help_text=_(
            "How important this skill is for this demand. "
            "A number between -{0} and +{0}.").format(MAX_WEIGHT))
    # description = dd.RichTextField(_("Description"), blank=True)
    

# if dd.is_installed('tickets'):
#     dd.inject_field(
#         'tickets.Ticket', 'faculty',
#         dd.ForeignKey("faculties.Faculty", blank=True, null=True))

from .ui import *
