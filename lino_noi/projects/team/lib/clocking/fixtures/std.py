# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
from lino_xl.lib.clocking.fixtures.std import objects as parent_objects

from lino.api import rt, dd


def objects():
    yield parent_objects()

    ServiceReport = rt.modules.clocking.ServiceReport
    ExcerptType = rt.modules.excerpts.ExcerptType
    kw = dict(
        build_method='weasy2html',
        # template='service_report.weasy.html',
        # body_template='default.body.html',
        # print_recipient=False,
        primary=True, certifying=True)
    kw.update(dd.str2kw('name', ServiceReport._meta.verbose_name))
    yield ExcerptType.update_for_model(ServiceReport, **kw)
