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
 #2 (Bar is not always baz)                        Jean      23/05/2015   09:00:00
 #1 (Föö fails to bar when baz)                    Luc       23/05/2015   09:00:00
 #3 (Baz sucks)                                    Mathieu   23/05/2015   09:00:00
 #11 (Class-based Foos and Bars?)                  Jean      22/05/2015   09:00:00     22/05/2015   11:18:00                          2:18
 #4 (Foo and bar don't baz)                        Luc       22/05/2015   09:00:00     22/05/2015   12:29:00                          3:29
 #9 (Foo never matches Bar)                        Mathieu   22/05/2015   09:00:00     22/05/2015   12:53:00                          3:53
 #14 (Bar cannot baz)                              Mathieu   20/05/2015   09:05:00     20/05/2015   09:17:00                          0:12
 #17 (Ticket 17)                                   Jean      20/05/2015   09:00:00     20/05/2015   10:30:00                          1:30
 #6 (Sell bar in baz)                              Luc       20/05/2015   09:00:00     20/05/2015   09:37:00                          0:37
 #12 (Foo cannot bar)                              Mathieu   20/05/2015   09:00:00     20/05/2015   09:05:00                          0:05
 #20 (Ticket 20)                                   Jean      19/05/2015   09:00:00     19/05/2015   09:10:00                          0:10
 #10 (Where can I find a Foo when bazing Bazes?)   Luc       19/05/2015   09:00:00     19/05/2015   10:02:00                          1:02
 #18 (Ticket 18)                                   Mathieu   19/05/2015   09:00:00     19/05/2015   11:18:00                          2:18
 **Total (13 rows)**                                                                                                                  **15:34**
================================================= ========= ============ ============ ============ ========== ============ ========= ===========
<BLANKLINE>


Some sessions are on private tickets:

>>> from django.db.models import Q
>>> rt.show(clocking.Sessions, column_names="ticket user duration ticket__project", filter=Q(ticket__private=True))
... #doctest: -REPORT_UDIFF
============================ ========= ========== =========
 Ticket                       Worker    Duration   Project
---------------------------- --------- ---------- ---------
 #2 (Bar is not always baz)   Jean                 téam
 #3 (Baz sucks)               Mathieu
 #9 (Foo never matches Bar)   Mathieu   3:53       téam
 #14 (Bar cannot baz)         Mathieu   0:12       téam
 **Total (4 rows)**                     **4:05**
============================ ========= ========== =========
<BLANKLINE>


Worked hours
============

This table shows the last seven days, one row per day, with your
working hours.

>>> rt.login('jean').show(clocking.WorkedHours)
... #doctest: -REPORT_UDIFF
======================================= ========== ========== ========== ==========
 Description                             Regular    Extra      Free       Total
--------------------------------------- ---------- ---------- ---------- ----------
 **Sat 23/05/2015** (`#2 <Detail>`__)               0:01                  0:01
 **Fri 22/05/2015** (`#11 <Detail>`__)   2:18                             2:18
 **Thu 21/05/2015**                                                       0:00
 **Wed 20/05/2015** (`#17 <Detail>`__)   1:30                             1:30
 **Tue 19/05/2015** (`#20 <Detail>`__)                         0:10       0:10
 **Mon 18/05/2015**                                                       0:00
 **Sun 17/05/2015**                                                       0:00
 **Total (7 rows)**                      **3:48**   **0:01**   **0:10**   **3:59**
======================================= ========== ========== ========== ==========
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
    jean worked on [Project #2 ('t\xe9am'), Project #4 ('research'), Project #5 ('shop'), Project #3 ('docs')]
    luc worked on [Project #1 ('lin\xf6'), Project #3 ('docs'), Project #4 ('research')]
    mathieu worked on [Project #2 ('t\xe9am'), Project #5 ('shop'), Project #1 ('lin\xf6')]

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
Partner #107 ('welket')

>>> rt.show(clocking.SessionsByReport, obj)
... #doctest: -REPORT_UDIFF
==================== ============ ========== ============ ================== ========== ======= ======
 Start date           Start time   End Time   Break Time   Description        Regular    Extra   Free
-------------------- ------------ ---------- ------------ ------------------ ---------- ------- ------
 23/05/2015           09:00:00                             `#1 <Detail>`__    0:01
 22/05/2015           09:00:00     11:18:00                `#11 <Detail>`__   2:18
 20/05/2015           09:00:00     09:37:00                `#6 <Detail>`__    0:37
 19/05/2015           09:00:00     11:18:00                `#18 <Detail>`__   2:18
 **Total (4 rows)**                                                           **5:14**
==================== ============ ========== ============ ================== ========== ======= ======
<BLANKLINE>

Note that there are sessions without a duration. Thats because

>>> rt.show(clocking.TicketsByReport, obj)
... #doctest: -REPORT_UDIFF
==== ============================================================ ========== ======== ========== ======= ======
 ID   Description                                                  Project    State    Regular    Extra   Free
---- ------------------------------------------------------------ ---------- -------- ---------- ------- ------
 1    `#1 (Föö fails to bar when baz) <Detail>`__ by *Jean*        linö       New      0:01
 6    `#6 (Sell bar in baz) <Detail>`__ by *Jean*                  research   Ready    0:37
 11   `#11 (Class-based Foos and Bars?) <Detail>`__ by *Mathieu*   research   Opened   2:18
 18   `#18 (Ticket 18) <Detail>`__ by *Luc*                        linö       Talk     2:18
                                                                                       **5:14**
==== ============================================================ ========== ======== ========== ======= ======
<BLANKLINE>


The :class:`ProjectsByReport
<lino_noi.projects.team.lib.clocking.ui.ProjectsByReport>`
table lists all projects and the time invested.

>>> rt.show(clocking.ProjectsByReport, obj)
==================== =========== =================================== ========== ======= ======
 Reference            Name        Tickets                             Regular    Extra   Free
-------------------- ----------- ----------------------------------- ---------- ------- ------
 linö                 Framewörk   `#1 <Detail>`__, `#18 <Detail>`__   2:19
 research             Research    `#11 <Detail>`__, `#6 <Detail>`__   2:55
 **Total (2 rows)**                                                   **5:14**
==================== =========== =================================== ========== ======= ======
<BLANKLINE>


Reporting type
==============

The :attr:`reporting_type` of a session indicates how the client is
going to pay for the work done.

The default implementation offers three choices "Worker", "Employer"
and "Customer". "Worker" is for volunteer work and "private fun" where
the worker does not get paid by anybody.  "Employer" is when working
time should be reported to the employer (but no customer is going to
pay for it directly).  "Customer" is when working time should be
reported to the customer.

>>> rt.show(clocking.ReportingTypes)
======= ========= =========
 value   name      text
------- --------- ---------
 10      regular   Regular
 20      extra     Extra
 30      free      Free
======= ========= =========
<BLANKLINE>


The local site admin can adapt above list to the site's needs. He also
defines a default reporting type:

>>> dd.plugins.clocking.default_reporting_type
<ReportingTypes.regular:10>


