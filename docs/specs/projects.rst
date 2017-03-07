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

The difference between "ticket" and "project" might not be clear for a
beginner.  For example something that started as a seemingly
meaningless "ticket" can grow into a whole "project". But if this
happens in reality, then you simply do it

The most visible difference is that projects have a *name* while
tickets just have a *number*.  Another rule of thumb is that tickets
are atomic tasks while projects are a way for grouping tickets into a
common goal. Tickets are short term while projects are medium or long
term. Tickets are individual and have a single author while projects
are group work. The only goal of a ticket is to get resolved while a
project has a more complex definition of goals and requirements.

A project in Noi is called a *product backlog item* (PBI) or a
*Sprint* in Scrum. (At least for the moment we don't see why Lino
should introduce a new database model for differentiating them. We
have the ProjectType



.. contents::
  :local:


Active projects
===============

>>> rt.show(tickets.ActiveProjects)
=========== =============== ============ ==========================================================================================================
 Reference   Name            Start date   Activity overview
----------- --------------- ------------ ----------------------------------------------------------------------------------------------------------
 linö        Framewörk       01/01/2009   New: **4**Talk: **3**Opened: **2**Started: **3**Sleeping: **3**Ready: **2**Closed: **3**Cancelled: **3**
 téam        Téam            01/01/2010   New: **3**Talk: **4**Opened: **3**Started: **2**Sleeping: **3**Ready: **3**Closed: **2**Cancelled: **3**
 docs        Documentatión   01/01/2009   New: **3**Talk: **3**Opened: **3**Started: **4**Sleeping: **2**Ready: **3**Closed: **3**Cancelled: **2**
 research    Research        01/01/1998   New: **2**Talk: **3**Opened: **3**Started: **3**Sleeping: **3**Ready: **3**Closed: **3**Cancelled: **3**
=========== =============== ============ ==========================================================================================================
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
