# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

"""

from lino_xl.lib.courses.desktop import *

from lino.api import dd, _


class CourseDetail(CourseDetail):
    """Customized detail_layout for Courses. Adds a tickets tab

    """
    main = "general events enrolments tickets"
    
    tickets = dd.Panel("""
    deploy.DeploymentsByMilestone
    """, label=_("Tickets"))


Activities.detail_layout = CourseDetail()
# MyActivities.detail_layout = CourseDetail()

