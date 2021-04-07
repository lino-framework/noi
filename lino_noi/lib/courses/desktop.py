# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Database models for this plugin.

"""

from lino_xl.lib.courses.desktop import *

from lino.api import dd, _


# class CourseDetail(CourseDetail):
#     """Customized detail_layout for Courses. Adds a tickets tab
#
#     """
#     main = "general cal_tab enrolments more"
#
#     general = dd.Panel("""
#     line room workflow_buttons name ref
#     deploy.DeploymentsByMilestone
#     """, label=_("General"))
#
#     cal_tab = dd.Panel("""
#     start_date end_date start_time end_time
#     max_events max_date every_unit every
#     monday tuesday wednesday thursday friday saturday sunday
#     cal.EntriesByController
#     """, label=_("Calendar"))
#
#     more_left = """
#     id:8
#     user
#     teacher
#     """
#
#     more = dd.Panel("""
#     more_left:30 blogs.EntriesByController:50
#     description
#     """, label=_("More"))


class MyEnrolments(Enrolments):
    """Show the Enrolments where I am the pupil).

    This requires the :attr:`partner` field in my user settings to
    point to me as a teacher.

    """
    label = _("My enrolments")
    # required_roles = dd.login_required(CoursesTeacher)
    master_key = "pupil"
    column_names = "course #course__ref course__name workflow_buttons *"
    parameters = dict(Enrolments.parameters)
    parameters.update(active=dd.YesNo.field(
            _("Active"),
            help_text=_("Filter courses that are either active/draft or inactive/closed"),
            null=True, blank=True,
            ))

    params_layout = """start_date end_date author state \
        active #course_state participants_only"""

    @classmethod
    def setup_request(self, ar):
        u = ar.get_user()
        ar.master_instance = u #get_child(u, pupil_model)
        super(MyEnrolments, self).setup_request(ar)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyEnrolments, self).param_defaults(ar, **kw)
        kw.update(active=dd.YesNo.yes)
        return kw

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(MyEnrolments, self).get_request_queryset(ar)
        pv = ar.param_values
        exposed_states = CourseStates.filter(is_exposed=True)
        if pv.show_exposed == dd.YesNo.yes:
            qs = qs.filter(course__state__in=exposed_states)
        elif pv.active == dd.YesNo.no:
            qs = qs.exclude(course__state__in=exposed_states)
        return qs




