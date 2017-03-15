.. _noi.specs.projects:

==================
Project management
==================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_projects
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.doctests')
    >>> from lino.api.doctest import *


This document specifies the project management functions of Lino Noi,
implemented in :mod:`lino_noi.lib.tickets`.

.. contents::
  :local:


What is a project?
==================

.. currentmodule:: lino_noi.lib.tickets.models

.. class:: Project

    A **project** is something on which several users work together.

    A Project is something into which somebody (the `partner`) invests
    time, energy and money.  The partner can be either external or the
    runner of the site.

    Projects form a hierarchical tree: each Project can have a
    `parent` (another Project for which it is a sub-project).

    A project in Noi is called a *product backlog item* (PBI) or a
    *Sprint* in Scrum. (At least for the moment we don't see why Lino
    should introduce a new database model for differentiating them. We
    have the ProjectType

    .. attribute:: name

    .. attribute:: parent

    .. attribute:: assign_to

        The user to whom new tickets will be assigned.
        See :attr:`Ticket.assigned_to`.


Ticket versus project
=====================

The difference between "ticket" and "project" might not be obvious.
For example something that started as a seemingly meaningless "ticket"
can grow into a whole "project". But if this happens in reality, then
you simply do it in the database.

The most visible difference is that projects are handled by their
*name* while tickets just have a *number*.  Another rule of thumb is
that tickets are atomic tasks while projects are a way for grouping
tickets into a common goal. Tickets are short term while projects are
medium or long term. Tickets are individual and have a single author
while projects are group work. The only goal of a ticket is to get
resolved while a project has a more complex definition of goals and
requirements.


Competences
===========

>>> rt.show('tickets.Competences')
==== ================= ========== ========== ======== =============
 ID   Author            Priority   Project    Remark   Description
---- ----------------- ---------- ---------- -------- -------------
 3    Luc               100        docs
 8    Romain Raffault   100        docs
 1    Jean              100        linö
 6    Mathieu           100        linö
 11   Robin Rood        100        linö
 4    Luc               100        research
 9    Rolf Rompen       100        research
 5    Mathieu           100        shop
 10   Rolf Rompen       100        shop
 2    Jean              100        téam
 7    Romain Raffault   100        téam
 12   Robin Rood        100        téam
                        **1200**
==== ================= ========== ========== ======== =============
<BLANKLINE>

>>> rt.login("mathieu").show('tickets.MyCompetences')
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF +SKIP
+----------+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Priority | Project | Tickets overview                                                                                                                                                                                         |
+==========+=========+==========================================================================================================================================================================================================+
| 100      | shop    | ⛶ : `#33 <Detail>`__, `#1 <Detail>`__, `#113 <Detail>`__, `#89 <Detail>`__, `#65 <Detail>`__, `#41 <Detail>`__, `#17 <Detail>`__, `#105 <Detail>`__, `#81 <Detail>`__, `#57 <Detail>`__, `#9 <Detail>`__ |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☎ : `#42 <Detail>`__, `#98 <Detail>`__, `#74 <Detail>`__, `#50 <Detail>`__, `#26 <Detail>`__, `#2 <Detail>`__, `#114 <Detail>`__, `#90 <Detail>`__, `#66 <Detail>`__, `#18 <Detail>`__                   |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☉ : `#27 <Detail>`__, `#107 <Detail>`__, `#83 <Detail>`__, `#59 <Detail>`__, `#35 <Detail>`__, `#11 <Detail>`__, `#99 <Detail>`__, `#75 <Detail>`__, `#51 <Detail>`__, `#3 <Detail>`__                   |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ⚒ : `#36 <Detail>`__, `#116 <Detail>`__, `#92 <Detail>`__, `#68 <Detail>`__, `#44 <Detail>`__, `#20 <Detail>`__, `#108 <Detail>`__, `#84 <Detail>`__, `#60 <Detail>`__, `#12 <Detail>`__                 |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☾ : `#101 <Detail>`__, `#77 <Detail>`__, `#53 <Detail>`__, `#29 <Detail>`__, `#5 <Detail>`__                                                                                                             |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☐ : `#38 <Detail>`__, `#94 <Detail>`__, `#70 <Detail>`__, `#46 <Detail>`__, `#22 <Detail>`__, `#110 <Detail>`__, `#86 <Detail>`__, `#62 <Detail>`__, `#14 <Detail>`__                                    |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☑ : `#103 <Detail>`__, `#79 <Detail>`__, `#55 <Detail>`__, `#31 <Detail>`__, `#7 <Detail>`__                                                                                                             |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☒ : `#96 <Detail>`__, `#72 <Detail>`__, `#48 <Detail>`__, `#24 <Detail>`__                                                                                                                               |
+----------+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 100      | linö    | ⛶ : `#89 <Detail>`__, `#1 <Detail>`__, `#113 <Detail>`__, `#41 <Detail>`__, `#65 <Detail>`__, `#97 <Detail>`__, `#73 <Detail>`__, `#49 <Detail>`__, `#25 <Detail>`__, `#17 <Detail>`__                   |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☎ : `#98 <Detail>`__, `#50 <Detail>`__, `#26 <Detail>`__, `#10 <Detail>`__, `#2 <Detail>`__, `#74 <Detail>`__, `#106 <Detail>`__, `#82 <Detail>`__, `#58 <Detail>`__, `#34 <Detail>`__                   |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☉ : `#107 <Detail>`__, `#59 <Detail>`__, `#35 <Detail>`__, `#19 <Detail>`__, `#83 <Detail>`__, `#115 <Detail>`__, `#91 <Detail>`__, `#67 <Detail>`__, `#43 <Detail>`__, `#11 <Detail>`__                 |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ⚒ : `#92 <Detail>`__, `#4 <Detail>`__, `#116 <Detail>`__, `#44 <Detail>`__, `#20 <Detail>`__, `#68 <Detail>`__, `#100 <Detail>`__, `#76 <Detail>`__, `#52 <Detail>`__, `#28 <Detail>`__                  |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☾ : `#13 <Detail>`__, `#109 <Detail>`__, `#85 <Detail>`__, `#61 <Detail>`__, `#37 <Detail>`__                                                                                                            |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☐ : `#94 <Detail>`__, `#6 <Detail>`__, `#46 <Detail>`__, `#22 <Detail>`__, `#70 <Detail>`__, `#102 <Detail>`__, `#78 <Detail>`__, `#54 <Detail>`__, `#30 <Detail>`__                                     |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☑ : `#15 <Detail>`__, `#111 <Detail>`__, `#87 <Detail>`__, `#63 <Detail>`__, `#39 <Detail>`__                                                                                                            |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         |                                                                                                                                                                                                          |
|          |         | ☒ : `#8 <Detail>`__, `#104 <Detail>`__, `#80 <Detail>`__, `#56 <Detail>`__, `#32 <Detail>`__                                                                                                             |
+----------+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **200**  |         |                                                                                                                                                                                                          |
+----------+---------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
<BLANKLINE>


Choosing a project
==================

>>> base = '/choices/tickets/Tickets/project'
>>> show_choices("robin", base + '?query=')
<br/>
linö
téam
docs
research
shop

>>> show_choices("robin", base + '?query=frame')
linö



.. class:: ProjectType

    The type of a :class:`Project`.
           


.. class:: TimeInvestment
           
    Model mixin for things which represent a time investment.  This
    currently just defines a group of three fields:

    .. attribute:: closed

        Whether this investment is closed, i.e. certain things should
        not change anymore.

    .. attribute:: private

        Whether this investment is private, i.e. should not be
        publicly visible anywhere.
        
        The default value is True.  Tickets on public projects cannot
        be private, but tickets on private projects may be manually
        set to public.

    .. attribute:: planned_time

        The time (in hours) we plan to work on this project or ticket.

           

    
