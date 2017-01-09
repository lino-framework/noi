================
The votes module
================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_votes
    
    doctest init:
    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


The :mod:`lino_noi.lib.votes` module adds the concept of "votes" to
:ref:`noi`.

A **vote** is when a user has an opinion or interest about a given
ticket (or any other votable).

A **votable**, in :ref:`noi`, is a ticket. But the module is designed
to be reusable in other contexts.


My tasks ("To-Do list")
=======================

Shows your votes having states `assigned` and `done`.

>>> rt.login('luc').user.profile
users.UserTypes.developer:400

>>> rt.login('jean').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
============================================================== ========== ===========================================
 Description                                                    Priority   Actions
-------------------------------------------------------------- ---------- -------------------------------------------
 `#2 (Bar is not always baz) <Detail>`__ by `marc <Detail>`__   0          **Assigned** → [Watching] [Done] [Cancel]
============================================================== ========== ===========================================
<BLANKLINE>

>>> rt.login('mathieu').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
======================================================== ========== ==================================
 Description                                              Priority   Actions
-------------------------------------------------------- ---------- ----------------------------------
 `#111 (Ticket 94) <Detail>`__ by `marc <Detail>`__       0          **Assigned** → [Watching] [Done]
 `#102 (Ticket 85) <Detail>`__ by `marc <Detail>`__       0          **Assigned** → [Watching] [Done]
 `#93 (Ticket 76) <Detail>`__ by `marc <Detail>`__        0          **Assigned** → [Watching] [Done]
 `#84 (Ticket 67) <Detail>`__ by `marc <Detail>`__        0          **Assigned** → [Watching] [Done]
 `#75 (Ticket 58) <Detail>`__ by `luc <Detail>`__         0          **Assigned** → [Watching] [Done]
 `#66 (Ticket 49) <Detail>`__ by `marc <Detail>`__        0          **Assigned** → [Watching] [Done]
 `#57 (Ticket 40) <Detail>`__ by `marc <Detail>`__        0          **Assigned** → [Watching] [Done]
 `#48 (Ticket 31) <Detail>`__ by `marc <Detail>`__        0          **Assigned** → [Watching] [Done]
 `#39 (Ticket 22) <Detail>`__ by `marc <Detail>`__        0          **Assigned** → [Watching] [Done]
 `#30 (Ticket 13) <Detail>`__ by `luc <Detail>`__         0          **Assigned** → [Watching] [Done]
 `#21 (Ticket 4) <Detail>`__ by `marc <Detail>`__         0          **Assigned** → [Watching] [Done]
 `#12 (Foo cannot bar) <Detail>`__ by `marc <Detail>`__   0          **Assigned** → [Watching] [Done]
 `#3 (Baz sucks) <Detail>`__ by `marc <Detail>`__         0          **Assigned** → [Watching] [Done]
======================================================== ========== ==================================
<BLANKLINE>

>>> rt.login('luc').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
============================================================== ========== ==========
 Description                                                    Priority   Actions
-------------------------------------------------------------- ---------- ----------
 `#112 (Ticket 95) <Detail>`__ by `marc <Detail>`__             0          **Done**
 `#103 (Ticket 86) <Detail>`__ by `marc <Detail>`__             0          **Done**
 `#94 (Ticket 77) <Detail>`__ by `marc <Detail>`__              0          **Done**
 `#85 (Ticket 68) <Detail>`__ by `jean <Detail>`__              0          **Done**
 `#76 (Ticket 59) <Detail>`__ by `marc <Detail>`__              0          **Done**
 `#67 (Ticket 50) <Detail>`__ by `marc <Detail>`__              0          **Done**
 `#58 (Ticket 41) <Detail>`__ by `marc <Detail>`__              0          **Done**
 `#49 (Ticket 32) <Detail>`__ by `marc <Detail>`__              0          **Done**
 `#40 (Ticket 23) <Detail>`__ by `jean <Detail>`__              0          **Done**
 `#31 (Ticket 14) <Detail>`__ by `marc <Detail>`__              0          **Done**
 `#22 (Ticket 5) <Detail>`__ by `marc <Detail>`__               0          **Done**
 `#13 (Bar cannot foo) <Detail>`__ by `marc <Detail>`__         0          **Done**
 `#4 (Foo and bar don't baz) <Detail>`__ by `marc <Detail>`__   0          **Done**
============================================================== ========== ==========
<BLANKLINE>




>>> rt.login('luc').show(votes.MyOffers)
... #doctest: +REPORT_UDIFF
================================================================== ==============================================
 Description                                                        Actions
------------------------------------------------------------------ ----------------------------------------------
 `#1 (Föö fails to bar when baz) <Detail>`__ by `marc <Detail>`__   **Candidate** → [Watching] [Assign] [Cancel]
================================================================== ==============================================
<BLANKLINE>
