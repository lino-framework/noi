.. _noi.specs.tickets:

=============================
Ticket management in Lino Noi
=============================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tickets
    
    doctest init:
    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the ticket management functions of Lino Noi,
implemented in :mod:`lino_noi.lib.tickets`.


.. contents::
  :local:


Tickets
=======

A :class:`Ticket <lino_noi.lib.tickets.models.Ticket>` represents a
concrete problem introduced by a :attr:`reporter
<lino_noi.lib.tickets.models.Ticket.reporter>` (a system user).

A ticket is usually *assigned* to one and only one user
(:attr:`assigned_to <lino_noi.lib.tickets.models.Ticket.assigned_to>`)
who is expected to work on it. That user might be the customer,
e.g. when the developer has a question.

Lifecycle of a ticket
=====================

The :attr:`state <lino_noi.lib.tickets.models.Ticket.state>` of a
ticket has one of the following values:

>>> rt.show(tickets.TicketStates)
======= =========== =========== ======== ========
 value   name        text        Symbol   Active
------- ----------- ----------- -------- --------
 10      new         New         ⛶        Yes
 15      talk        Talk        ⚔        Yes
 20      opened      Opened      ☉        Yes
 21      sticky      Sticky      ♥        Yes
 22      started     Started     ⚒        Yes
 30      sleeping    Sleeping    ☾        No
 40      ready       Ready       ☐        Yes
 50      closed      Closed      ☑        No
 60      cancelled   Cancelled   ☒        No
======= =========== =========== ======== ========
<BLANKLINE>

There is also a "modern" series of symbols, which can be enabled
site-wide in :attr:`lino.core.site.Site.use_new_unicode_symbols`.

You can see this table in your web interface using
:menuselection:`Explorer --> Tickets --> States`.

.. >>> show_menu_path(tickets.TicketStates)
   Explorer --> Tickets --> States

See :class:`lino_noi.lib.tickets.choicelists.TicketStates` for more
information about every state.

Above table in German:

>>> rt.show(tickets.TicketStates, language="de")
====== =========== ============ ======== ========
 Wert   name        Text         Symbol   Aktive
------ ----------- ------------ -------- --------
 10     new         Neu          ⛶        Ja
 15     talk        Besprechen   ⚔        Ja
 20     opened      Opened       ☉        Ja
 21     sticky      Sticky       ♥        Ja
 22     started     Started      ⚒        Ja
 30     sleeping    Schläft      ☾        Nein
 40     ready       Bereit       ☐        Ja
 50     closed      Closed       ☑        Nein
 60     cancelled   Storniert    ☒        Nein
====== =========== ============ ======== ========
<BLANKLINE>

And in French (not yet fully translated):

>>> rt.show(tickets.TicketStates, language="fr")
======= =========== ========== ======== ========
 value   name        text       Symbol   Active
------- ----------- ---------- -------- --------
 10      new         Nouveau    ⛶        Oui
 15      talk        Talk       ⚔        Oui
 20      opened      Opened     ☉        Oui
 21      sticky      Sticky     ♥        Oui
 22      started     Started    ⚒        Oui
 30      sleeping    Sleeping   ☾        Non
 40      ready       Ready      ☐        Oui
 50      closed      Closed     ☑        Non
 60      cancelled   Annulé     ☒        Non
======= =========== ========== ======== ========
<BLANKLINE>


Note that a ticket also has a checkbox for marking it as :attr:`closed
<lino_noi.lib.tickets.models.Ticket.closed>`.  This means that a ticket
can be marked as "closed" in any of above states.  We don't use this for the moment and are not sure
whether this is a cool feature (:ticket:`372`).

- :attr:`standby <lino_noi.lib.tickets.models.Ticket.standby>` 

Projects
========

The :attr:`project <lino_noi.lib.tickets.models.Ticket.project>` of a
ticket is used to specify "who is going to pay" for it. Lino Noi does
not issue invoices, so it uses this information only for reporting
about it and helping with the decision about whether and how worktime
is being invoiced to the customer.  But the invoicing itself is not
currently a goal of Lino Noi.

So a **project** is something for which somebody is possibly willing
to pay money.

>>> rt.show(tickets.Projects)
=========== =============== ======== ============== =========
 Reference   Name            Parent   Project Type   Private
----------- --------------- -------- -------------- ---------
 linö        Framewörk                               No
 téam        Téam            linö                    Yes
 docs        Documentatión   linö                    No
 research    Research        docs                    No
 shop        Shop                                    No
=========== =============== ======== ============== =========
<BLANKLINE>


>>> rt.show(tickets.TopLevelProjects)
=========== =========== ======== ================
 Reference   Name        Parent   Children
----------- ----------- -------- ----------------
 linö        Framewörk            *téam*, *docs*
 shop        Shop
=========== =========== ======== ================
<BLANKLINE>


Developers can start working on tickets without specifying a project
(i.e. without knowing who is going to pay for their work).  

But after some time every ticket should get assigned to some
project. You can see a list of tickets which have not yet been
assigned to a project:

>>> pv = dict(has_project=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
==== =================== ================= =========== ========= ============= =========
 ID   Summary             Reporter          Topic       Faculty   Actions       Project
---- ------------------- ----------------- ----------- --------- ------------- ---------
 5    Cannot create Foo   luc               Lino Cosi             **Started**
 3    Baz sucks           Romain Raffault   Lino Core             **Opened**
==== =================== ================= =========== ========= ============= =========
<BLANKLINE>


Distribution of tickets per project
===================================

In our demo database, tickets are distributed over the different
projects as follows (not a realistic distribution):

>>> for p in tickets.Project.objects.all():
...         print p.ref, p.tickets_by_project.count()
linö 23
téam 23
docs 23
research 23
shop 22



Private tickets
===============

Tickets are private by default. But when they are assigned to a public
project, then their privacy is removed.

So the private tickets are (1) those in project "téam" and (2) those
without project:

>>> pv = dict(show_private=dd.YesNo.yes)
>>> rt.show(tickets.Tickets, param_values=pv,
...     column_names="id summary assigned_to project")
... #doctest: +REPORT_UDIFF
===== ======================= ============= =========
 ID    Summary                 Assigned to   Project
----- ----------------------- ------------- ---------
 114   Ticket 97                             téam
 109   Ticket 92                             téam
 104   Ticket 87                             téam
 99    Ticket 82                             téam
 94    Ticket 77                             téam
 89    Ticket 72                             téam
 84    Ticket 67                             téam
 79    Ticket 62                             téam
 74    Ticket 57                             téam
 69    Ticket 52                             téam
 64    Ticket 47                             téam
 59    Ticket 42                             téam
 54    Ticket 37                             téam
 49    Ticket 32                             téam
 44    Ticket 27                             téam
 39    Ticket 22                             téam
 34    Ticket 17                             téam
 29    Ticket 12                             téam
 24    Ticket 7                              téam
 19    Ticket 2                              téam
 14    Bar cannot baz                        téam
 9     Foo never matches Bar                 téam
 5     Cannot create Foo
 3     Baz sucks
 2     Bar is not always baz                 téam
===== ======================= ============= =========
<BLANKLINE>


And these are the public tickets:

>>> pv = dict(show_private=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv,
...     column_names="id summary assigned_to project")
... #doctest: +REPORT_UDIFF
===== =========================================== ============= ==========
 ID    Summary                                     Assigned to   Project
----- ------------------------------------------- ------------- ----------
 116   Ticket 99                                                 research
 115   Ticket 98                                                 docs
 113   Ticket 96                                                 linö
 112   Ticket 95                                                 shop
 111   Ticket 94                                                 research
 110   Ticket 93                                                 docs
 108   Ticket 91                                                 linö
 107   Ticket 90                                                 shop
 106   Ticket 89                                                 research
 105   Ticket 88                                                 docs
 103   Ticket 86                                                 linö
 102   Ticket 85                                                 shop
 101   Ticket 84                                                 research
 100   Ticket 83                                                 docs
 98    Ticket 81                                                 linö
 97    Ticket 80                                                 shop
 96    Ticket 79                                                 research
 95    Ticket 78                                                 docs
 93    Ticket 76                                                 linö
 92    Ticket 75                                                 shop
 91    Ticket 74                                                 research
 90    Ticket 73                                                 docs
 88    Ticket 71                                                 linö
 87    Ticket 70                                                 shop
 86    Ticket 69                                                 research
 85    Ticket 68                                                 docs
 83    Ticket 66                                                 linö
 82    Ticket 65                                                 shop
 81    Ticket 64                                                 research
 80    Ticket 63                                                 docs
 78    Ticket 61                                                 linö
 77    Ticket 60                                                 shop
 76    Ticket 59                                                 research
 75    Ticket 58                                                 docs
 73    Ticket 56                                                 linö
 72    Ticket 55                                                 shop
 71    Ticket 54                                                 research
 70    Ticket 53                                                 docs
 68    Ticket 51                                                 linö
 67    Ticket 50                                                 shop
 66    Ticket 49                                                 research
 65    Ticket 48                                                 docs
 63    Ticket 46                                                 linö
 62    Ticket 45                                                 shop
 61    Ticket 44                                                 research
 60    Ticket 43                                                 docs
 58    Ticket 41                                                 linö
 57    Ticket 40                                                 shop
 56    Ticket 39                                                 research
 55    Ticket 38                                                 docs
 53    Ticket 36                                                 linö
 52    Ticket 35                                                 shop
 51    Ticket 34                                                 research
 50    Ticket 33                                                 docs
 48    Ticket 31                                                 linö
 47    Ticket 30                                                 shop
 46    Ticket 29                                                 research
 45    Ticket 28                                                 docs
 43    Ticket 26                                                 linö
 42    Ticket 25                                                 shop
 41    Ticket 24                                                 research
 40    Ticket 23                                                 docs
 38    Ticket 21                                                 linö
 37    Ticket 20                                                 shop
 36    Ticket 19                                                 research
 35    Ticket 18                                                 docs
 33    Ticket 16                                                 linö
 32    Ticket 15                                                 shop
 31    Ticket 14                                                 research
 30    Ticket 13                                                 docs
 28    Ticket 11                                                 linö
 27    Ticket 10                                                 shop
 26    Ticket 9                                                  research
 25    Ticket 8                                                  docs
 23    Ticket 6                                                  linö
 22    Ticket 5                                                  shop
 21    Ticket 4                                                  research
 20    Ticket 3                                                  docs
 18    Ticket 1                                                  linö
 17    Ticket 0                                                  shop
 16    How to get bar from foo                                   research
 15    Bars have no foo                                          docs
 13    Bar cannot foo                                            linö
 12    Foo cannot bar                                            shop
 11    Class-based Foos and Bars?                                research
 10    Where can I find a Foo when bazing Bazes?                 docs
 8     Is there any Bar in Foo?                                  linö
 7     No Foo after deleting Bar                                 shop
 6     Sell bar in baz                                           research
 4     Foo and bar don't baz                                     docs
 1     Föö fails to bar when baz                                 linö
===== =========================================== ============= ==========
<BLANKLINE>



There are 5 private and 11 public tickets in the demo database.

>>> tickets.Ticket.objects.filter(private=True).count()
25
>>> tickets.Ticket.objects.filter(private=False).count()
91

My tickets
==========

>>> rt.login('jean').show(tickets.MyTickets)
... #doctest: +REPORT_UDIFF
============================================= =============== ============== ============= ==============================
 Overview                                      Faculty         Topic          Assigned to   Actions
--------------------------------------------- --------------- -------------- ------------- ------------------------------
 `#110 (Ticket 93) <Detail>`__                                 Lino Voga                    [▶] **Talk**
 `#97 (Ticket 80) <Detail>`__                                  Lino Cosi                    [▶] **Ready** → [⚔]
 `#93 (Ticket 76) <Detail>`__                                  Lino Cosi                    [▶] **Opened** → [⚒] [☑] [⚔]
 `#76 (Ticket 59) <Detail>`__                                  Lino Welfare                 [▶] **Sticky** → [⛶]
 `#64 (Ticket 47) <Detail>`__                                  Lino Welfare                 [▶] **New** → [♥] [☉] [⚔]
 `#59 (Ticket 42) <Detail>`__                                  Lino Core                    [▶] **Started** → [☑] [⚔]
 `#47 (Ticket 30) <Detail>`__                                  Lino Core                    [▶] **Talk**
 `#34 (Ticket 17) <Detail>`__                                  Lino Voga                    [▶] **Ready** → [⚔]
 `#30 (Ticket 13) <Detail>`__                                  Lino Voga                    [▶] **Opened** → [⚒] [☑] [⚔]
 `#13 (Bar cannot foo) <Detail>`__             Documentation   Lino Cosi                    [▶] **Sticky** → [⛶]
 `#1 (Föö fails to bar when baz) <Detail>`__                   Lino Cosi                    [▶] **New** → [♥] [☉] [⚔]
============================================= =============== ============== ============= ==============================
<BLANKLINE>


To-Do list
==========

>>> rt.login('luc').user.profile
users.UserTypes.developer:400

>>> rt.login('luc').show(votes.MyVotes)
... #doctest: +REPORT_UDIFF
=============================== ============ ========== ======== ==========
 Votable                         Vote state   Priority   Rating   Nickname
------------------------------- ------------ ---------- -------- ----------
 #8 (Is there any Bar in Foo?)   Assigned     0
 #110 (Ticket 93)                Ready        0
 #93 (Ticket 76)                 Assigned     0
 #76 (Ticket 59)                 Candidate    0
 #64 (Ticket 47)                 Assigned     0
 #47 (Ticket 30)                 Candidate    0
 #34 (Ticket 17)                 Ready        0
=============================== ============ ========== ======== ==========
<BLANKLINE>



Sites
=====

Lino Noi has a list of all sites for which we do support:

>>> rt.show(tickets.Sites)
============= ========= ======== ====
 Designation   Partner   Remark   ID
------------- --------- -------- ----
 pypi          pypi               3
 welket        welket             1
 welsch        welsch             2
============= ========= ======== ====
<BLANKLINE>

A ticket may or may not be "local", i.e. specific to a given site.
When a ticket is site-specific, we simply assign the `site` field.  We
can see all local tickets for a given site object:

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF +SKIP
===== =========================================== ================= ============== =============== =============== ==========
 ID    Summary                                     Reporter          Topic          Faculty         Actions         Project
----- ------------------------------------------- ----------------- -------------- --------------- --------------- ----------
 115   Ticket 98                                   marc              Lino Core                      **ToDo**        docs
 112   Ticket 95                                   Robin Rood        Lino Welfare                   **Cancelled**   shop
 109   Ticket 92                                   mathieu           Lino Cosi                      **Sleeping**    téam
 106   Ticket 89                                   jean              Lino Voga                      **Talk**        research
 103   Ticket 86                                   Romain Raffault   Lino Core                      **Done**        linö
 100   Ticket 83                                   luc               Lino Welfare                   **Sticky**      docs
 97    Ticket 80                                   Rolf Rompen       Lino Cosi                      **New**         shop
 94    Ticket 77                                   marc              Lino Voga                      **Ready**       téam
 91    Ticket 74                                   Robin Rood        Lino Core                      **ToDo**        research
 88    Ticket 71                                   mathieu           Lino Welfare                   **Cancelled**   linö
 85    Ticket 68                                   jean              Lino Cosi                      **Sleeping**    docs
 82    Ticket 65                                   Romain Raffault   Lino Voga                      **Talk**        shop
 79    Ticket 62                                   luc               Lino Core                      **Done**        téam
 76    Ticket 59                                   Rolf Rompen       Lino Welfare                   **Sticky**      research
 73    Ticket 56                                   marc              Lino Cosi                      **New**         linö
 70    Ticket 53                                   Robin Rood        Lino Voga                      **Ready**       docs
 67    Ticket 50                                   mathieu           Lino Core                      **ToDo**        shop
 64    Ticket 47                                   jean              Lino Welfare                   **Cancelled**   téam
 61    Ticket 44                                   Romain Raffault   Lino Cosi                      **Sleeping**    research
 58    Ticket 41                                   luc               Lino Voga                      **Talk**        linö
 55    Ticket 38                                   Rolf Rompen       Lino Core                      **Done**        docs
 52    Ticket 35                                   marc              Lino Welfare                   **Sticky**      shop
 49    Ticket 32                                   Robin Rood        Lino Cosi                      **New**         téam
 46    Ticket 29                                   mathieu           Lino Voga                      **Ready**       research
 43    Ticket 26                                   jean              Lino Core                      **ToDo**        linö
 40    Ticket 23                                   Romain Raffault   Lino Welfare                   **Cancelled**   docs
 37    Ticket 20                                   luc               Lino Cosi                      **Sleeping**    shop
 34    Ticket 17                                   Rolf Rompen       Lino Voga                      **Talk**        téam
 31    Ticket 14                                   marc              Lino Core                      **Done**        research
 28    Ticket 11                                   Robin Rood        Lino Welfare                   **Sticky**      linö
 25    Ticket 8                                    mathieu           Lino Cosi                      **New**         docs
 22    Ticket 5                                    jean              Lino Voga                      **Ready**       shop
 19    Ticket 2                                    Romain Raffault   Lino Core                      **ToDo**        téam
 16    How to get bar from foo                     luc               Lino Welfare                   **Cancelled**   research
 13    Bar cannot foo                              Rolf Rompen       Lino Cosi      Documentation   **Sleeping**    linö
 10    Where can I find a Foo when bazing Bazes?   marc              Lino Voga                      **Talk**        docs
 7     No Foo after deleting Bar                   Robin Rood        Lino Core                      **Done**        shop
 4     Foo and bar don't baz                       mathieu           Lino Welfare                   **Sticky**      docs
 1     Föö fails to bar when baz                   jean              Lino Cosi                      **New**         linö
===== =========================================== ================= ============== =============== =============== ==========
<BLANKLINE>


Note that the above table shows no state change actions in the
Actions column because it is being requested by anonymous. For an
authenticated developer it looks like this:

>>> rt.login('luc').show(tickets.TicketsBySite, welket)
... #doctest: +REPORT_UDIFF  +SKIP
===== =========================================== ================= ============== =============== ================================ ==========
 ID    Summary                                     Reporter          Topic          Faculty         Actions                          Project
----- ------------------------------------------- ----------------- -------------- --------------- -------------------------------- ----------
 115   Ticket 98                                   marc              Lino Core                      [▶] **ToDo**                     docs
 112   Ticket 95                                   Robin Rood        Lino Welfare                   **Cancelled**                    shop
 109   Ticket 92                                   mathieu           Lino Cosi                      **Sleeping**                     téam
 106   Ticket 89                                   jean              Lino Voga                      [▶] **Talk**                     research
 103   Ticket 86                                   Romain Raffault   Lino Core                      **Done**                         linö
 100   Ticket 83                                   luc               Lino Welfare                   [▶] **Sticky**                   docs
 97    Ticket 80                                   Rolf Rompen       Lino Cosi                      [▶] **New**                      shop
 94    Ticket 77                                   marc              Lino Voga                      [▶] **Ready**                    téam
 91    Ticket 74                                   Robin Rood        Lino Core                      [▶] **ToDo**                     research
 88    Ticket 71                                   mathieu           Lino Welfare                   **Cancelled**                    linö
 85    Ticket 68                                   jean              Lino Cosi                      **Sleeping**                     docs
 82    Ticket 65                                   Romain Raffault   Lino Voga                      [▶] **Talk**                     shop
 79    Ticket 62                                   luc               Lino Core                      **Done**                         téam
 76    Ticket 59                                   Rolf Rompen       Lino Welfare                   [▶] **Sticky**                   research
 73    Ticket 56                                   marc              Lino Cosi                      [▶] **New**                      linö
 70    Ticket 53                                   Robin Rood        Lino Voga                      [▶] **Ready**                    docs
 67    Ticket 50                                   mathieu           Lino Core                      [▶] **ToDo**                     shop
 64    Ticket 47                                   jean              Lino Welfare                   **Cancelled**                    téam
 61    Ticket 44                                   Romain Raffault   Lino Cosi                      **Sleeping**                     research
 58    Ticket 41                                   luc               Lino Voga                      [▶] **Talk** → [🐜] [🕸] [☐] [🗑]   linö
 55    Ticket 38                                   Rolf Rompen       Lino Core                      **Done**                         docs
 52    Ticket 35                                   marc              Lino Welfare                   [▶] **Sticky**                   shop
 49    Ticket 32                                   Robin Rood        Lino Cosi                      [▶] **New**                      téam
 46    Ticket 29                                   mathieu           Lino Voga                      [▶] **Ready**                    research
 43    Ticket 26                                   jean              Lino Core                      [▶] **ToDo**                     linö
 40    Ticket 23                                   Romain Raffault   Lino Welfare                   **Cancelled**                    docs
 37    Ticket 20                                   luc               Lino Cosi                      **Sleeping** → [🗑]               shop
 34    Ticket 17                                   Rolf Rompen       Lino Voga                      [▶] **Talk**                     téam
 31    Ticket 14                                   marc              Lino Core                      **Done**                         research
 28    Ticket 11                                   Robin Rood        Lino Welfare                   [▶] **Sticky**                   linö
 25    Ticket 8                                    mathieu           Lino Cosi                      [▶] **New**                      docs
 22    Ticket 5                                    jean              Lino Voga                      [▶] **Ready**                    shop
 19    Ticket 2                                    Romain Raffault   Lino Core                      [▶] **ToDo**                     téam
 16    How to get bar from foo                     luc               Lino Welfare                   **Cancelled**                    research
 13    Bar cannot foo                              Rolf Rompen       Lino Cosi      Documentation   **Sleeping**                     linö
 10    Where can I find a Foo when bazing Bazes?   marc              Lino Voga                      [▶] **Talk**                     docs
 7     No Foo after deleting Bar                   Robin Rood        Lino Core                      **Done**                         shop
 4     Foo and bar don't baz                       mathieu           Lino Welfare                   [▶] **Sticky**                   docs
 1     Föö fails to bar when baz                   jean              Lino Cosi                      [▶] **New**                      linö
===== =========================================== ================= ============== =============== ================================ ==========
<BLANKLINE>




Milestones
==========

Every site can have its list of "milestones" or "releases". A
milestone is when a site gets an upgrade of the software which is
running there. 

A milestone is not necessary an *official* release of a new
version. It just means that you release some changed software to the
users of that site.

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(rt.actors.deploy.MilestonesBySite, welket)
... #doctest: -REPORT_UDIFF
======= ============== ============ ======== ====
 Label   Expected for   Reached      Closed   ID
------- -------------- ------------ -------- ----
         15/05/2015     15/05/2015   No       7
         11/05/2015     11/05/2015   No       5
         07/05/2015     07/05/2015   No       3
         03/05/2015     03/05/2015   No       1
======= ============== ============ ======== ====
<BLANKLINE>


Deployments
===========

Every milestone has its list of "deployments", i.e. the tickets that
are being fixed when this milestone is reached.

The demo database currently does not have any deployments:

>>> rt.show(rt.actors.deploy.Deployments)
No data to display


Release notes
=============

Lino Noi has an excerpt type for printing a milestone.  This is used
to produce *release notes*.

>>> obj = deploy.Milestone.objects.get(pk=7)
>>> rt.show(rt.actors.deploy.DeploymentsByMilestone, obj)
No data to display

>>> rt.show(clocking.OtherTicketsByMilestone, obj)
No data to display



Dependencies between tickets
============================

>>> rt.show(tickets.LinkTypes)
... #doctest: +REPORT_UDIFF
======= =========== ===========
 value   name        text
------- ----------- -----------
 10      requires    Requires
 20      triggers    Triggers
 30      suggests    Suggests
 40      obsoletes   Obsoletes
======= =========== ===========
<BLANKLINE>




>>> rt.show(tickets.Links)
... #doctest: +REPORT_UDIFF
==== ================= ================================ ============================
 ID   Dependency type   Parent                           Child
---- ----------------- -------------------------------- ----------------------------
 1    Requires          #1 (Föö fails to bar when baz)   #2 (Bar is not always baz)
==== ================= ================================ ============================
<BLANKLINE>


Comments
========

Currently the demo database contains just some comments...

>>> rt.show(comments.Comments, column_names="id user short_text")
==== ================= ===================
 ID   Author            Short text
---- ----------------- -------------------
 1    Romain Raffault   Hackerish comment
 2    Rolf Rompen       Hackerish comment
 3    Robin Rood        Hackerish comment
==== ================= ===================
<BLANKLINE>


>>> obj = tickets.Ticket.objects.get(pk=7)
>>> rt.show(comments.CommentsByRFC, obj)
<BLANKLINE>


Filtering tickets
=================


>>> show_fields(tickets.Tickets)
+-----------------+-----------------+--------------------------------------------------------------+
| Internal name   | Verbose name    | Help text                                                    |
+=================+=================+==============================================================+
| reporter        | Reporter        | Only rows reporter by this user.                             |
+-----------------+-----------------+--------------------------------------------------------------+
| assigned_to     | Assigned to     | Only tickets assigned to this user.                          |
+-----------------+-----------------+--------------------------------------------------------------+
| interesting_for | Interesting for | Only tickets interesting for this partner.                   |
+-----------------+-----------------+--------------------------------------------------------------+
| site            | Site            | Select a site if you want to see only tickets for this site. |
+-----------------+-----------------+--------------------------------------------------------------+
| project         | Project         |                                                              |
+-----------------+-----------------+--------------------------------------------------------------+
| state           | State           | Only rows having this state.                                 |
+-----------------+-----------------+--------------------------------------------------------------+
| has_project     | Has project     |                                                              |
|                 |                 | A choicelist with two values "Yes" and "No".                 |
+-----------------+-----------------+--------------------------------------------------------------+
| show_assigned   | Assigned        | Whether to show assigned tickets                             |
+-----------------+-----------------+--------------------------------------------------------------+
| show_active     | Active          | Whether to show active tickets                               |
+-----------------+-----------------+--------------------------------------------------------------+
| show_todo       | To do           |                                                              |
|                 |                 | A choicelist with two values "Yes" and "No".                 |
+-----------------+-----------------+--------------------------------------------------------------+
| show_private    | Private         |                                                              |
|                 |                 | A choicelist with two values "Yes" and "No".                 |
+-----------------+-----------------+--------------------------------------------------------------+
| start_date      | Period from     | Start date of observed period                                |
+-----------------+-----------------+--------------------------------------------------------------+
| end_date        | until           | End date of observed period                                  |
+-----------------+-----------------+--------------------------------------------------------------+
| observed_event  | Observed event  |                                                              |
+-----------------+-----------------+--------------------------------------------------------------+
| topic           | Topic           |                                                              |
+-----------------+-----------------+--------------------------------------------------------------+
| feasable_by     | Feasable by     | Show only tickets for which I am competent.                  |
+-----------------+-----------------+--------------------------------------------------------------+

>>> rt.login('robin').show(rt.actors.tickets.Tickets)
... #doctest: +REPORT_UDIFF +ELLIPSIS
===== =========================================== ================= ============== =============== ============================== ==========
 ID    Summary                                     Reporter          Topic          Faculty         Actions                        Project
----- ------------------------------------------- ----------------- -------------- --------------- ------------------------------ ----------
 116   Ticket 99                                   Romain Raffault   Lino Welfare                   [▶] **Closed** → [☉]           research
 115   Ticket 98                                   marc              Lino Core                      [▶] **Ready** → [⚔]            docs
 114   Ticket 97                                   luc               Lino Voga                      [▶] **Sleeping** → [⚔]         téam
 113   Ticket 96                                   Robin Rood        Lino Cosi                      [▶] **Started** → [☑] [⚔]      linö
 112   Ticket 95                                   Romain Raffault   Lino Welfare                   [▶] **Sticky** → [⛶]           shop
 111   Ticket 94                                   marc              Lino Core                      [▶] **Opened** → [⚒] [☑] [⚔]   research
 110   Ticket 93                                   jean              Lino Voga                      [▶] **Talk**                   docs
 109   Ticket 92                                   Rolf Rompen       Lino Cosi                      [▶] **New** → [♥] [☉] [⚔]      téam
 108   Ticket 91                                   Romain Raffault   Lino Welfare                   [▶] **Cancelled**              linö
 107   Ticket 90                                   mathieu           Lino Core                      [▶] **Closed** → [☉]           shop
 106   Ticket 89                                   luc               Lino Voga                      [▶] **Ready** → [⚔]            research
 105   Ticket 88                                   jean              Lino Cosi                      [▶] **Sleeping** → [⚔]         docs
 104   Ticket 87                                   Rolf Rompen       Lino Welfare                   [▶] **Started** → [☑] [⚔]      téam
 103   Ticket 86                                   mathieu           Lino Core                      [▶] **Sticky** → [⛶]           linö
 102   Ticket 85                                   luc               Lino Voga                      [▶] **Opened** → [⚒] [☑] [⚔]   shop
 101   Ticket 84                                   Robin Rood        Lino Cosi                      [▶] **Talk**                   research
 100   Ticket 83                                   Romain Raffault   Lino Welfare                   [▶] **New** → [♥] [☉] [⚔]      docs
 99    Ticket 82                                   mathieu           Lino Core                      [▶] **Cancelled**              téam
 98    Ticket 81                                   marc              Lino Voga                      [▶] **Closed** → [☉]           linö
 97    Ticket 80                                   jean              Lino Cosi                      [▶] **Ready** → [⚔]            shop
 96    Ticket 79                                   Robin Rood        Lino Welfare                   [▶] **Sleeping** → [⚔]         research
 95    Ticket 78                                   Romain Raffault   Lino Core                      [▶] **Started** → [☑] [⚔]      docs
 94    Ticket 77                                   marc              Lino Voga                      [▶] **Sticky** → [⛶]           téam
 93    Ticket 76                                   jean              Lino Cosi                      [▶] **Opened** → [⚒] [☑] [⚔]   linö
 92    Ticket 75                                   Rolf Rompen       Lino Welfare                   [▶] **Talk**                   shop
 91    Ticket 74                                   mathieu           Lino Core                      [▶] **New** → [♥] [☉] [⚔]      research
 90    Ticket 73                                   marc              Lino Voga                      [▶] **Cancelled**              docs
 89    Ticket 72                                   luc               Lino Cosi                      [▶] **Closed** → [☉]           téam
 88    Ticket 71                                   Robin Rood        Lino Welfare                   [▶] **Ready** → [⚔]            linö
 87    Ticket 70                                   Rolf Rompen       Lino Core                      [▶] **Sleeping** → [⚔]         shop
 86    Ticket 69                                   mathieu           Lino Voga                      [▶] **Started** → [☑] [⚔]      research
 85    Ticket 68                                   luc               Lino Cosi                      [▶] **Sticky** → [⛶]           docs
 84    Ticket 67                                   Robin Rood        Lino Welfare                   [▶] **Opened** → [⚒] [☑] [⚔]   téam
 83    Ticket 66                                   Romain Raffault   Lino Core                      [▶] **Talk**                   linö
 82    Ticket 65                                   marc              Lino Voga                      [▶] **New** → [♥] [☉] [⚔]      shop
 81    Ticket 64                                   luc               Lino Cosi                      [▶] **Cancelled**              research
 80    Ticket 63                                   jean              Lino Welfare                   [▶] **Closed** → [☉]           docs
 79    Ticket 62                                   Rolf Rompen       Lino Core                      [▶] **Ready** → [⚔]            téam
 78    Ticket 61                                   Romain Raffault   Lino Voga                      [▶] **Sleeping** → [⚔]         linö
 77    Ticket 60                                   marc              Lino Cosi                      [▶] **Started** → [☑] [⚔]      shop
 76    Ticket 59                                   jean              Lino Welfare                   [▶] **Sticky** → [⛶]           research
 75    Ticket 58                                   Rolf Rompen       Lino Core                      [▶] **Opened** → [⚒] [☑] [⚔]   docs
 74    Ticket 57                                   mathieu           Lino Voga                      [▶] **Talk**                   téam
 73    Ticket 56                                   luc               Lino Cosi                      [▶] **New** → [♥] [☉] [⚔]      linö
 72    Ticket 55                                   jean              Lino Welfare                   [▶] **Cancelled**              shop
 71    Ticket 54                                   Robin Rood        Lino Core                      [▶] **Closed** → [☉]           research
 70    Ticket 53                                   Romain Raffault   Lino Voga                      [▶] **Ready** → [⚔]            docs
 69    Ticket 52                                   mathieu           Lino Cosi                      [▶] **Sleeping** → [⚔]         téam
 68    Ticket 51                                   luc               Lino Welfare                   [▶] **Started** → [☑] [⚔]      linö
 67    Ticket 50                                   Robin Rood        Lino Core                      [▶] **Sticky** → [⛶]           shop
 66    Ticket 49                                   Romain Raffault   Lino Voga                      [▶] **Opened** → [⚒] [☑] [⚔]   research
 65    Ticket 48                                   marc              Lino Cosi                      [▶] **Talk**                   docs
 64    Ticket 47                                   jean              Lino Welfare                   [▶] **New** → [♥] [☉] [⚔]      téam
 63    Ticket 46                                   Robin Rood        Lino Core                      [▶] **Cancelled**              linö
 62    Ticket 45                                   Rolf Rompen       Lino Voga                      [▶] **Closed** → [☉]           shop
 61    Ticket 44                                   mathieu           Lino Cosi                      [▶] **Ready** → [⚔]            research
 60    Ticket 43                                   marc              Lino Welfare                   [▶] **Sleeping** → [⚔]         docs
 59    Ticket 42                                   jean              Lino Core                      [▶] **Started** → [☑] [⚔]      téam
 58    Ticket 41                                   Rolf Rompen       Lino Voga                      [▶] **Sticky** → [⛶]           linö
 57    Ticket 40                                   mathieu           Lino Cosi                      [▶] **Opened** → [⚒] [☑] [⚔]   shop
 56    Ticket 39                                   luc               Lino Welfare                   [▶] **Talk**                   research
 55    Ticket 38                                   Robin Rood        Lino Core                      [▶] **New** → [♥] [☉] [⚔]      docs
 54    Ticket 37                                   Rolf Rompen       Lino Voga                      [▶] **Cancelled**              téam
 53    Ticket 36                                   Romain Raffault   Lino Cosi                      [▶] **Closed** → [☉]           linö
 52    Ticket 35                                   marc              Lino Welfare                   [▶] **Ready** → [⚔]            shop
 51    Ticket 34                                   luc               Lino Core                      [▶] **Sleeping** → [⚔]         research
 50    Ticket 33                                   Robin Rood        Lino Voga                      [▶] **Started** → [☑] [⚔]      docs
 49    Ticket 32                                   Romain Raffault   Lino Cosi                      [▶] **Sticky** → [⛶]           téam
 48    Ticket 31                                   marc              Lino Welfare                   [▶] **Opened** → [⚒] [☑] [⚔]   linö
 47    Ticket 30                                   jean              Lino Core                      [▶] **Talk**                   shop
 46    Ticket 29                                   Rolf Rompen       Lino Voga                      [▶] **New** → [♥] [☉] [⚔]      research
 45    Ticket 28                                   Romain Raffault   Lino Cosi                      [▶] **Cancelled**              docs
 44    Ticket 27                                   mathieu           Lino Welfare                   [▶] **Closed** → [☉]           téam
 43    Ticket 26                                   luc               Lino Core                      [▶] **Ready** → [⚔]            linö
 42    Ticket 25                                   jean              Lino Voga                      [▶] **Sleeping** → [⚔]         shop
 41    Ticket 24                                   Rolf Rompen       Lino Cosi                      [▶] **Started** → [☑] [⚔]      research
 40    Ticket 23                                   mathieu           Lino Welfare                   [▶] **Sticky** → [⛶]           docs
 39    Ticket 22                                   luc               Lino Core                      [▶] **Opened** → [⚒] [☑] [⚔]   téam
 38    Ticket 21                                   Robin Rood        Lino Voga                      [▶] **Talk**                   linö
 37    Ticket 20                                   Romain Raffault   Lino Cosi                      [▶] **New** → [♥] [☉] [⚔]      shop
 36    Ticket 19                                   mathieu           Lino Welfare                   [▶] **Cancelled**              research
 35    Ticket 18                                   marc              Lino Core                      [▶] **Closed** → [☉]           docs
 34    Ticket 17                                   jean              Lino Voga                      [▶] **Ready** → [⚔]            téam
 33    Ticket 16                                   Robin Rood        Lino Cosi                      [▶] **Sleeping** → [⚔]         linö
 32    Ticket 15                                   Romain Raffault   Lino Welfare                   [▶] **Started** → [☑] [⚔]      shop
 31    Ticket 14                                   marc              Lino Core                      [▶] **Sticky** → [⛶]           research
 30    Ticket 13                                   jean              Lino Voga                      [▶] **Opened** → [⚒] [☑] [⚔]   docs
 29    Ticket 12                                   Rolf Rompen       Lino Cosi                      [▶] **Talk**                   téam
 28    Ticket 11                                   mathieu           Lino Welfare                   [▶] **New** → [♥] [☉] [⚔]      linö
 27    Ticket 10                                   marc              Lino Core                      [▶] **Cancelled**              shop
 26    Ticket 9                                    luc               Lino Voga                      [▶] **Closed** → [☉]           research
 25    Ticket 8                                    Robin Rood        Lino Cosi                      [▶] **Ready** → [⚔]            docs
 24    Ticket 7                                    Rolf Rompen       Lino Welfare                   [▶] **Sleeping** → [⚔]         téam
 23    Ticket 6                                    mathieu           Lino Core                      [▶] **Started** → [☑] [⚔]      linö
 22    Ticket 5                                    luc               Lino Voga                      [▶] **Sticky** → [⛶]           shop
 21    Ticket 4                                    Robin Rood        Lino Cosi                      [▶] **Opened** → [⚒] [☑] [⚔]   research
 20    Ticket 3                                    Romain Raffault   Lino Welfare                   [▶] **Talk**                   docs
 19    Ticket 2                                    marc              Lino Core                      [▶] **New** → [♥] [☉] [⚔]      téam
 18    Ticket 1                                    luc               Lino Voga                      [▶] **Cancelled**              linö
 17    Ticket 0                                    jean              Lino Cosi                      [▶] **Closed** → [☉]           shop
 16    How to get bar from foo                     Rolf Rompen       Lino Welfare                   [▶] **Ready** → [⚔]            research
 15    Bars have no foo                            Romain Raffault   Lino Core                      [▶] **Sleeping** → [⚔]         docs
 14    Bar cannot baz                              marc              Lino Voga                      [▶] **Started** → [☑] [⚔]      téam
 13    Bar cannot foo                              jean              Lino Cosi      Documentation   [▶] **Sticky** → [⛶]           linö
 12    Foo cannot bar                              Rolf Rompen       Lino Welfare   Code changes    [▶] **Opened** → [⚒] [☑] [⚔]   shop
 11    Class-based Foos and Bars?                  mathieu           Lino Core                      [▶] **Talk**                   research
 10    Where can I find a Foo when bazing Bazes?   luc               Lino Voga                      [▶] **New** → [♥] [☉] [⚔]      docs
 9     Foo never matches Bar                       jean              Lino Cosi      Testing         [▶] **Cancelled**              téam
 8     Is there any Bar in Foo?                    Robin Rood        Lino Welfare                   [▶] **Closed** → [☉]           linö
 7     No Foo after deleting Bar                   Romain Raffault   Lino Core                      [▶] **Ready** → [⚔]            shop
 6     Sell bar in baz                             mathieu           Lino Voga      Analysis        [▶] **Sleeping** → [⚔]         research
 5     Cannot create Foo                           luc               Lino Cosi                      [▶] **Started** → [☑] [⚔]
 4     Foo and bar don't baz                       Robin Rood        Lino Welfare                   [▶] **Sticky** → [⛶]           docs
 3     Baz sucks                                   Romain Raffault   Lino Core                      [▶] **Opened** → [⚒] [☑] [⚔]
 2     Bar is not always baz                       marc              Lino Voga                      [▶] **Talk**                   téam
 1     Föö fails to bar when baz                   jean              Lino Cosi                      [▶] **New** → [♥] [☉] [⚔]      linö
===== =========================================== ================= ============== =============== ============================== ==========
<BLANKLINE>





The detail layout of a ticket
=============================

Here is a textual description of the fields and their layout used in
the detail window of a ticket.

>>> from lino.utils.diag import py2rst
>>> print(py2rst(tickets.Tickets.detail_layout, True))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
(main) [visible for all]:
- **General** (general):
  - (general_1):
    - (general1):
      - (general1_1): **Summary** (summary), **ID** (id), **Reporter** (reporter)
      - (general1_2): **Site** (site), **Topic** (topic), **Project** (project), **Private** (private)
      - (general1_3): **Actions** (workflow_buttons), **Assigned to** (assigned_to), **Faculty** (faculty)
    - **Deployments** (deploy.DeploymentsByTicket) [visible for user consultant hoster developer senior admin]
  - (general_2): **Description** (description), **Comments** (CommentsByRFC) [visible for user consultant hoster developer senior admin], **Sessions** (SessionsByTicket) [visible for consultant hoster developer senior admin]
- **More** (more):
  - (more_1):
    - (more1):
      - (more1_1): **Created** (created), **Modified** (modified), **Reported for** (reported_for), **Ticket type** (ticket_type)
      - (more1_2): **State** (state), **Duplicate of** (duplicate_of), **Planned time** (planned_time), **Priority** (priority)
    - **Duplicates** (DuplicatesByTicket)
  - (more_2): **Upgrade notes** (upgrade_notes), **Dependencies** (LinksByTicket) [visible for senior admin]
- **History** (changes.ChangesByMaster) [visible for senior admin]
- **Votes** (votes.VotesByVotable) [visible for user consultant hoster developer senior admin]    
<BLANKLINE>



