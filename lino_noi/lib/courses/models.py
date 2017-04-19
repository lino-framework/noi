# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

"""

from lino_xl.lib.tickets.mixins import Milestone

from lino_xl.lib.courses.models import *
from lino import mixins

class Course(Course, Milestone, mixins.Referrable):

    quick_search_fields = 'ref name line__name line__topic__name'

    # #Doesn't seem to work... to change the value of .course in MyEnrolements
    # def __str__(self):
    #     if self.ref:
    #         return self.ref
    #     return super(Course, self).__str__()

    class Meta(Course.Meta):
        abstract = dd.is_abstract_model(__name__, 'Course')
        
    def get_milestone_users(self):
        for obj in self.get_enrolments():
            u = obj.pupil.get_as_user()
            if u is not None:
                yield u
