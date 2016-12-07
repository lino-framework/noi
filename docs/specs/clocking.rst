.. _noi.specs.clocking:

==================
Work time tracking
==================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_clocking
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.doctests')
    >>> from lino.api.doctest import *


Lino Noi uses both :mod:`lino_noi.lib.tickets` (Ticket management) and
:mod:`lino_noi.lib.clocking` (Development time tracking).

Note that the demo data is on fictive demo date **May 23, 2015**:

>>> dd.today()
datetime.date(2015, 5, 23)


Sessions
========

A :class:`Session <lino_noi.lib.clocking.models.Session>` is when a
user works on a ticket for a given lapse of time.

When end_time is empty, it means that he is still working.

>>> rt.show(clocking.Sessions, limit=15)
... #doctest: -REPORT_UDIFF
================================================= ========= ============ ============ ============ ========== ============ ========= ===========
 Ticket                                            Worker    Start date   Start time   End Date     End Time   Break Time   Summary   Duration
------------------------------------------------- --------- ------------ ------------ ------------ ---------- ------------ --------- -----------
 #4 (Foo and bar don't baz)                        jean      23/05/2015   09:00:00
 #1 (Föö fails to bar when baz)                    luc       23/05/2015   09:00:00
 #5 (Cannot create Foo)                            marc      23/05/2015   09:00:00
 #2 (Bar is not always baz)                        mathieu   23/05/2015   09:00:00
 #21 (Ticket 4)                                    jean      22/05/2015   09:00:00     22/05/2015   11:18:00                          2:18
 #13 (Bar cannot foo)                              luc       22/05/2015   09:00:00     22/05/2015   12:29:00                          3:29
 #10 (Where can I find a Foo when bazing Bazes?)   marc      22/05/2015   09:00:00     22/05/2015   12:53:00                          3:53
 #14 (Bar cannot baz)                              mathieu   22/05/2015   09:00:00     22/05/2015   09:10:00                          0:10
 #39 (Ticket 22)                                   marc      20/05/2015   09:05:00     20/05/2015   09:17:00                          0:12
 #25 (Ticket 8)                                    jean      20/05/2015   09:00:00     20/05/2015   10:30:00                          1:30
 #30 (Ticket 13)                                   luc       20/05/2015   09:00:00     20/05/2015   09:37:00                          0:37
 #22 (Ticket 5)                                    marc      20/05/2015   09:00:00     20/05/2015   09:05:00                          0:05
 #19 (Ticket 2)                                    mathieu   20/05/2015   09:00:00     20/05/2015   11:02:00                          2:02
 #38 (Ticket 21)                                   jean      19/05/2015   09:00:00     19/05/2015   09:10:00                          0:10
 #34 (Ticket 17)                                   luc       19/05/2015   09:00:00     19/05/2015   10:02:00                          1:02
 **Total (17 rows)**                                                                                                                  **15:28**
================================================= ========= ============ ============ ============ ========== ============ ========= ===========
<BLANKLINE>


Some sessions are on private tickets:

>>> from django.db.models import Q
>>> rt.show(clocking.Sessions, column_names="ticket user duration ticket__project", filter=Q(ticket__private=True))
... #doctest: -REPORT_UDIFF
============================ ========= ========== =========
 Ticket                       Worker    Duration   Project
---------------------------- --------- ---------- ---------
 #5 (Cannot create Foo)       marc
 #2 (Bar is not always baz)   mathieu              téam
 #14 (Bar cannot baz)         mathieu   0:10       téam
 #39 (Ticket 22)              marc      0:12       téam
 #19 (Ticket 2)               mathieu   2:02       téam
 #34 (Ticket 17)              luc       1:02       téam
 **Total (6 rows)**                     **3:26**
============================ ========= ========== =========
<BLANKLINE>


Worked hours
============

This table shows the last seven days, one row per day, with your
working hours.

>>> rt.login('jean').show(clocking.WorkedHours)
... #doctest: -REPORT_UDIFF
======================================= ========== ====== ==========
 Description                             linö       shop   Total
--------------------------------------- ---------- ------ ----------
 **Sat 23/05/2015** (`#4 <Detail>`__)    0:01              0:01
 **Fri 22/05/2015** (`#21 <Detail>`__)   2:18              2:18
 **Thu 21/05/2015**                                        0:00
 **Wed 20/05/2015** (`#25 <Detail>`__)   1:30              1:30
 **Tue 19/05/2015** (`#38 <Detail>`__)   0:10              0:10
 **Mon 18/05/2015**                                        0:00
 **Sun 17/05/2015**                                        0:00
 **Total (7 rows)**                      **3:59**          **3:59**
======================================= ========== ====== ==========
<BLANKLINE>


In the "description" column you see a list of the tickets on which you
worked that day. This is a convenient way to continue some work you
started some days ago.

.. 
    Find the users who worked on more than one project:
    >>> for u in users.User.objects.all():
    ...     qs = tickets.Project.objects.filter(tickets_by_project__sessions_by_ticket__user=u).distinct()
    ...     if qs.count() > 1:
    ...         print u.username, "worked on", [o for o in qs]
    jean worked on [Project #3 ('docs'), Project #4 ('research'), Project #1 ('lin\xf6')]
    luc worked on [Project #1 ('lin\xf6'), Project #3 ('docs'), Project #2 ('t\xe9am')]
    marc worked on [Project #3 ('docs'), Project #5 ('shop'), Project #2 ('t\xe9am'), Project #1 ('lin\xf6')]
    mathieu worked on [Project #2 ('t\xe9am'), Project #4 ('research')]
    
    jean worked on [Project #2 ('t\xe9am'), Project #5 ('shop'), Project #1 ('lin\xf6')]
    luc worked on [Project #1 ('lin\xf6'), Project #2 ('t\xe9am')]
    marc worked on [Project #3 ('docs'), Project #4 ('research')]
    mathieu worked on [Project #4 ('research'), Project #5 ('shop')]

Render this table to HTML in order to reproduce :ticket:`523`:

>>> url = "/api/clocking/WorkedHours?"
>>> url += "_dc=1442341081053&cw=430&cw=83&cw=83&cw=83&cw=83&cw=83&cw=83&ch=&ch=&ch=&ch=&ch=&ch=&ch=&ci=description&ci=vc0&ci=vc1&ci=vc2&ci=vc3&ci=vc4&ci=vc5&name=0&pv=16.05.2015&pv=23.05.2015&pv=7&an=show_as_html&sr="
>>> res = test_client.get(url, REMOTE_USER="jean")
>>> json.loads(res.content)
{u'open_url': u'/bs3/clocking/WorkedHours?limit=15', u'success': True}


The html version of this table table has only 5 rows (4 data rows and
the total row) because valueless rows are not included by default:

>>> ar = rt.login('jean')
>>> u = ar.get_user()
>>> ar = clocking.WorkedHours.request(user=u)
>>> ar = ar.spawn(clocking.WorkedHours)
>>> lst = list(ar)
>>> len(lst)
7
>>> e = ar.table2xhtml()
>>> len(e.findall('./tbody/tr'))
5




Service Report
==============

A service report (:class:`clocking.ServiceReport
<lino_noi.lib.clocking.ui.ServiceReport>`) is a document which reports
about the hours invested during a given date range.  It can be
addressed to a recipient (a user) and in that case will consider only
the tickets for which this user has specified interest.

It currently contains two tables:

- a list of tickets, with invested time (i.e. the sum of durations
  of all sessions that lie in the given data range)
- a list of projects, with invested time and list of the tickets that
  are assigned to this project.

This report is useful for developers like me because it serves as a
base for writing invoices.


>>> obj = clocking.ServiceReport.objects.get(pk=1)
>>> obj.printed_by.build_method
<BuildMethods.weasy2html:weasy2html>


>>> obj.interesting_for
Partner #100 ('welket')

>>> rt.show(clocking.TicketsByReport, obj)
... #doctest: -REPORT_UDIFF
==== ========================================================================================== ======== ===========
 ID   Description                                                                                State    Time
---- ------------------------------------------------------------------------------------------ -------- -----------
 1    Föö fails to bar when baz. Site: welket. Reporter: jean. Project: linö. Topic: Lino Cosi   New      0:00
 4    Foo and bar don't baz. Reporter: Robin Rood. Project: docs. Topic: Lino Welfare            Sticky   0:00
 13   Bar cannot foo. Site: welket. Reporter: jean. Project: linö. Topic: Lino Cosi              Sticky   3:29
 19   Ticket 2. Site: welket. Reporter: marc. Project: téam. Topic: Lino Core                    New      2:02
 21   Ticket 4. Site: welsch. Reporter: Robin Rood. Project: research. Topic: Lino Cosi          Opened   2:18
 25   Ticket 8. Site: welket. Reporter: Robin Rood. Project: docs. Topic: Lino Cosi              Ready    1:30
 31   Ticket 14. Site: welket. Reporter: marc. Project: research. Topic: Lino Core               Sticky   3:29
 43   Ticket 26. Site: welket. Reporter: luc. Project: linö. Topic: Lino Core                    Ready    2:18
                                                                                                          **15:06**
==== ========================================================================================== ======== ===========
<BLANKLINE>


The :class:`ProjectsByReport
<lino_noi.projects.team.lib.clocking.ui.ProjectsByReport>`
table lists all projects and the time invested.

>>> rt.show(clocking.ProjectsByReport, obj)
==================== =============== ======== ==================================== =========== ============
 Reference            Name            Parent   Tickets                              Time        Total time
-------------------- --------------- -------- ------------------------------------ ----------- ------------
 docs                 Documentatión   linö     `#25 <Detail>`__                     1:30        7:17
 linö                 Framewörk                `#43 <Detail>`__, `#13 <Detail>`__   5:47        15:06
 research             Research        docs     `#31 <Detail>`__, `#21 <Detail>`__   5:47        5:47
 téam                 Téam            linö     `#19 <Detail>`__                     2:02        2:02
 **Total (4 rows)**                                                                 **15:06**
==================== =============== ======== ==================================== =========== ============
<BLANKLINE>


Note our tree structure (which is currently not very visible)::

  - linö
    - docs
      - research
    - téam
  - shop


The `Total time` column in this table is the `Time` invested for this
project and the sum of times invested in all of its children.

The `Total time` for "linö" in above table is **12:09**, which is the
sum of **3:29** (direct time of linö) + **6:28** (time of docs) +
**2:12** (time of research).
