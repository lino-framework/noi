# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Some demo data for the Vilma project.

"""

from lino.api import dd, rt, _
from lino.utils.mldbc import babel_named as named
from lino.utils.cycler import Cycler
from lino_xl.lib.cal.choicelists import Recurrencies

def objects():
    Line = rt.models.courses.Line
    Topic = rt.models.courses.Topic
    Course = rt.models.courses.Course
    EventType = rt.models.cal.EventType
    Room = rt.models.cal.Room

    school = named(Room, _("School"))
    yield school
    center = named(Room, _("Youth center"))
    yield center
    library = named(Room, _("Library"))
    yield library
    
    training = named(EventType, _("Training"))
    yield training
    workshop = named(EventType, _("Workshop"))
    yield workshop
    camp = named(EventType, _("Camp"))
    yield camp
    
    nature = named(Topic, _("Nature"))
    yield nature
    folk = named(Topic, _("Folk"))
    yield folk
    together = named(Topic, _("Acting together"))
    yield together
    health = named(Topic, _("Health"))
    yield health
    comp = named(Topic, _("Computer"))
    yield comp
    
    yield named(
        Line, _("Photography workshop"),
        event_type=workshop,
        every_unit=Recurrencies.once, topic=together)
    yield named(
        Line, _("Teamwork training"),
        event_type=training,
        every_unit=Recurrencies.once, topic=together)
    yield named(
        Line, _("Folk camp 2017"),
        event_type=camp,
        every_unit=Recurrencies.once, topic=together)
    yield named(
        Line, _("Lino Vilma training"),
        event_type=training,
        every_unit=Recurrencies.weekly, topic=together)

    LINES = Cycler(Line.objects.all())
    for offset in (-60, -10, -5, 1, 10, 30):
        yield Course(line=LINES.pop(), start_date=dd.demo_date(offset))
