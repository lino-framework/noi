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
================================================================= ========================================================== ==========
 Description                                                       Actions                                                    Priority
----------------------------------------------------------------- ---------------------------------------------------------- ----------
 `#116 (Ticket 116) <Detail>`__ by `Mathieu <Detail>`__            [▶] [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
 `#107 (Ticket 107) <Detail>`__ by `Mathieu <Detail>`__            [▶] [★] **Done** → [Rate]                                  0
 `#83 (Ticket 83) <Detail>`__ by `Mathieu <Detail>`__              [▶] [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
 `#74 (Ticket 74) <Detail>`__ by `Mathieu <Detail>`__              [▶] [★] **Done** → [Rate]                                  0
 `#50 (Ticket 50) <Detail>`__ by `Mathieu <Detail>`__              [▶] [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
 `#2 (Bar is not always baz) <Detail>`__ by `Mathieu <Detail>`__   [■] [★] **Assigned** → [Watching] [Done] [Rate] [Cancel]   0
================================================================= ========================================================== ==========
<BLANKLINE>



>>> rt.login('mathieu').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
================================================== =================================================== ==========
 Description                                        Actions                                             Priority
-------------------------------------------------- --------------------------------------------------- ----------
 `#84 (Ticket 84) <Detail>`__ by `Luc <Detail>`__   [▶] [★] **Done**                                    0
 `#60 (Ticket 60) <Detail>`__ by `Luc <Detail>`__   [▶] [★] **Assigned** → [Watching] [Done] [Cancel]   0
 `#51 (Ticket 51) <Detail>`__ by `Luc <Detail>`__   [▶] [★] **Done**                                    0
 `#27 (Ticket 27) <Detail>`__ by `Luc <Detail>`__   [▶] [★] **Assigned** → [Watching] [Done] [Cancel]   0
 `#18 (Ticket 18) <Detail>`__ by `Luc <Detail>`__   [▶] [★] **Done**                                    0
================================================== =================================================== ==========
<BLANKLINE>


>>> rt.login('luc').show(votes.MyTasks)
... #doctest: +REPORT_UDIFF
============================================================== =================================================== ==========
 Description                                                    Actions                                             Priority
-------------------------------------------------------------- --------------------------------------------------- ----------
 `#106 (Ticket 106) <Detail>`__ by `Jean <Detail>`__            [▶] [★] **Assigned** → [Watching] [Done] [Cancel]   0
 `#28 (Ticket 28) <Detail>`__ by `Jean <Detail>`__              [▶] [★] **Done**                                    0
 `#4 (Foo and bar don't baz) <Detail>`__ by `Jean <Detail>`__   [▶] [★] **Assigned** → [Watching] [Done] [Cancel]   0
============================================================== =================================================== ==========
<BLANKLINE>



>>> rt.login('luc').show(votes.MyOffers)
... #doctest: -REPORT_UDIFF
================================================================== =============================================
 Description                                                        Actions
------------------------------------------------------------------ ---------------------------------------------
 `#115 (Ticket 115) <Detail>`__ by `Jean <Detail>`__                [▶] [★] **Candidate** → [Watching] [Cancel]
 `#82 (Ticket 82) <Detail>`__ by `Jean <Detail>`__                  [▶] [★] **Candidate** → [Watching] [Cancel]
 `#49 (Ticket 49) <Detail>`__ by `Jean <Detail>`__                  [▶] [★] **Candidate** → [Watching] [Cancel]
 `#1 (Föö fails to bar when baz) <Detail>`__ by `Jean <Detail>`__   [■] [★] **Candidate** → [Watching] [Cancel]
================================================================== =============================================
<BLANKLINE>


Note that Luc is not a triager, that's why he dos not have permission to [Assign].

>>> from lino_noi.lib.tickets.roles import Triager
>>> rt.login('luc').user.profile.has_required_roles([Triager])
False

