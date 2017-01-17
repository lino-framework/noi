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


The state of a vote
===================

See :class:`lino_noi.lib.votes.choicelists.VoteStates`

>>> rt.login().show(votes.VoteStates)
... #doctest: +REPORT_UDIFF
======= =========== ===========
 value   name        text
------- ----------- -----------
 00      author      Author
 10      watching    Watching
 20      candidate   Candidate
 30      assigned    Assigned
 40      done        Done
 50      rated       Rated
 60      cancelled   Cancelled
======= =========== ===========
<BLANKLINE>



My tasks ("To-Do list")
=======================

Shows your votes having states `assigned` and `done`.

>>> rt.login('luc').user.profile
users.UserTypes.developer:400

>>> rt.login('jean').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
======================================================================================= ====================================================== ==========
 Description                                                                             Actions                                                Priority
--------------------------------------------------------------------------------------- ------------------------------------------------------ ----------
 `#110 (Ticket 110) <Detail>`__ by `mathieu <Detail>`__                                  [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
 `#101 (Ticket 101) <Detail>`__ by `mathieu <Detail>`__ for `marc <Detail>`__            [★] **Done** → [Rate]                                  0
 `#77 (Ticket 77) <Detail>`__ by `mathieu <Detail>`__ for `marc <Detail>`__              [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
 `#68 (Ticket 68) <Detail>`__ by `mathieu <Detail>`__ for `marc <Detail>`__              [★] **Done** → [Rate]                                  0
 `#47 (Ticket 47) <Detail>`__ by `mathieu <Detail>`__ for `marc <Detail>`__              [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
 `#38 (Ticket 38) <Detail>`__ by `mathieu <Detail>`__ for `marc <Detail>`__              [★] **Done** → [Rate]                                  0
 `#14 (Bar cannot baz) <Detail>`__ by `mathieu <Detail>`__ for `marc <Detail>`__         [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
 `#5 (Cannot create Foo) <Detail>`__ by `mathieu <Detail>`__                             [★] **Done** → [Rate]                                  0
 `#2 (Bar is not always baz) <Detail>`__ by `mathieu <Detail>`__ for `marc <Detail>`__   [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
======================================================================================= ====================================================== ==========
<BLANKLINE>


>>> rt.login('mathieu').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
========================================================================== ====================================== ==========
 Description                                                                Actions                                Priority
-------------------------------------------------------------------------- -------------------------------------- ----------
 `#111 (Ticket 111) <Detail>`__ by `luc <Detail>`__ for `marc <Detail>`__   [★] **Done**                           0
 `#57 (Ticket 57) <Detail>`__ by `luc <Detail>`__ for `marc <Detail>`__     [★] **Assigned** → [Watching] [Done]   0
 `#48 (Ticket 48) <Detail>`__ by `luc <Detail>`__ for `marc <Detail>`__     [★] **Done**                           0
========================================================================== ====================================== ==========
<BLANKLINE>

>>> rt.login('luc').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
No data to display



>>> rt.login('luc').show(votes.MyOffers)
... #doctest: +REPORT_UDIFF
======================================================================================== ==================================================
 Description                                                                              Actions
---------------------------------------------------------------------------------------- --------------------------------------------------
 `#109 (Ticket 109) <Detail>`__ by `jean <Detail>`__ for `marc <Detail>`__                [★] **Candidate** → [Watching] [Assign] [Cancel]
 `#46 (Ticket 46) <Detail>`__ by `jean <Detail>`__ for `marc <Detail>`__                  [★] **Candidate** → [Watching] [Assign] [Cancel]
 `#1 (Föö fails to bar when baz) <Detail>`__ by `jean <Detail>`__ for `marc <Detail>`__   [★] **Candidate** → [Watching] [Assign] [Cancel]
======================================================================================== ==================================================
<BLANKLINE>

Note that Luc is a triager, that's why he has permission to [Assign].

>>> from lino_noi.lib.tickets.roles import Triager
>>> rt.login('luc').user.profile.has_required_roles([Triager])
True

