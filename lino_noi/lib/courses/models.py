# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

"""

from lino_xl.lib.tickets.mixins import Milestone

from lino_xl.lib.courses.models import *

class Course(Course, Milestone):

    class Meta(Course.Meta):
        abstract = dd.is_abstract_model(__name__, 'Course')
        
    def get_milestone_users(self):
        for obj in self.get_enrolments():
            u = obj.pupil.get_as_user()
            if u is not None:
                yield u
