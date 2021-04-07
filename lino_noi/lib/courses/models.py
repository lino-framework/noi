# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Database models for this plugin.

"""

from lino_xl.lib.tickets.mixins import Milestone

from lino_xl.lib.courses.models import *
from lino import mixins

class Course(Course, mixins.Referrable):

    quick_search_fields = 'ref name line__name line__topic__name'

    # #Doesn't seem to work... to change the value of .course in MyEnrolements
    # def __str__(self):
    #     if self.ref:
    #         return self.ref
    #     return super(Course, self).__str__()

    class Meta(Course.Meta):
        abstract = dd.is_abstract_model(__name__, 'Course')
