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
    main = "general events enrolments more"
    
    general = dd.Panel("""
    line room workflow_buttons name
    deploy.DeploymentsByMilestone
    """, label=_("General"))
    
    events = dd.Panel("""
    start_date end_date start_time end_time
    max_events max_date every_unit every
    monday tuesday wednesday thursday friday saturday sunday
    cal.EntriesByController
    """, label=_("Events"))

    more = dd.Panel("""
    teacher id:8 user 
    description
    """, label=_("More"))


Activities.detail_layout = CourseDetail()
# MyActivities.detail_layout = CourseDetail()

