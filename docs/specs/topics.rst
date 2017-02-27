.. _noi.specs.topics:

=============================
Topics in Lino Noi
=============================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_topics
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the ticket management functions of Lino Noi,
implemented in :mod:`lino_noi.lib.tickets`.


.. contents::
  :local:



Topics
========

The :attr:`topic <lino_noi.lib.tickets.models.Ticket.topic>` of a
ticket is what Trac calls "component". Topics are a "customer-side"
classification of the different components which are being developed
by the team that uses a given Lino Noi site.

There are 4 topics in the demo database.

>>> show_menu_path(topics.AllTopics)
Configure --> Contacts --> Topics



>>> rt.show(topics.AllTopics)
=========== ============== ================== ================== =============
 Reference   Designation    Designation (de)   Designation (fr)   Topic group
----------- -------------- ------------------ ------------------ -------------
 linõ        Lino Core
 welfäre     Lino Welfare
 così        Lino Cosi
 faggio      Lino Voga
=========== ============== ================== ================== =============
<BLANKLINE>


Choosing a topic
================

When choosing a topic, the search text looks in both the
:guilabel:`Reference` and the :guilabel:`Designation` field:

>>> base = '/choices/tickets/Tickets/topic'
>>> show_choices("robin", base + '?query=')
<br/>
Lino Core
Lino Welfare
Lino Cosi
Lino Voga

Note that we have a topic whose `ref` is different from `name`, and
that the search works in both fields:

>>> obj = topics.Topic.get_by_ref('faggio')
>>> print(obj.ref)
faggio
>>> print(obj.name)
Lino Voga

>>> show_choices("robin", base + '?query=fag')
Lino Voga

>>> show_choices("robin", base + '?query=voga')
Lino Voga


Interests
=========

Every partner can have its list of "interests". They will get notified
about changes in these topics even when they did not report the
ticket.


>>> obj = contacts.Partner.objects.get(name="welket")
>>> rt.show(topics.InterestsByPartner, obj)
... #doctest: +REPORT_UDIFF
==============
 Topic
--------------
 Lino Welfare
 Lino Cosi
 Lino Voga
==============
<BLANKLINE>

>>> obj = topics.Topic.objects.get(ref="welfäre")
>>> rt.show(topics.InterestsByTopic, obj)
... #doctest: +REPORT_UDIFF
=============
 Partner
-------------
 Rood Robin
 Rompen Rolf
 Marc
 Mathieu
 Luc
 welket
 welsch
=============
<BLANKLINE>



Filtering tickets by topic
==========================

>>> pv = dict(topic=rt.models.topics.Topic.get_by_ref("così"))
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
===== ========================== ========= =========== =============== ==========
 ID    Summary                    Author    Topic       Actions         Project
----- -------------------------- --------- ----------- --------------- ----------
 116   Ticket 116                 Mathieu   Lino Cosi   **Started**     research
 112   Ticket 112                 Luc       Lino Cosi   **Cancelled**   shop
 108   Ticket 108                 Luc       Lino Cosi   **Started**     linö
 104   Ticket 104                 Jean      Lino Cosi   **Cancelled**   téam
 100   Ticket 100                 Jean      Lino Cosi   **Started**     docs
 96    Ticket 96                  Mathieu   Lino Cosi   **Cancelled**   research
 92    Ticket 92                  Mathieu   Lino Cosi   **Started**     shop
 88    Ticket 88                  Luc       Lino Cosi   **Cancelled**   linö
 84    Ticket 84                  Luc       Lino Cosi   **Started**     téam
 80    Ticket 80                  Jean      Lino Cosi   **Cancelled**   docs
 76    Ticket 76                  Jean      Lino Cosi   **Started**     research
 72    Ticket 72                  Mathieu   Lino Cosi   **Cancelled**   shop
 68    Ticket 68                  Mathieu   Lino Cosi   **Started**     linö
 64    Ticket 64                  Luc       Lino Cosi   **Cancelled**   téam
 60    Ticket 60                  Luc       Lino Cosi   **Started**     docs
 56    Ticket 56                  Jean      Lino Cosi   **Cancelled**   research
 52    Ticket 52                  Jean      Lino Cosi   **Started**     shop
 48    Ticket 48                  Mathieu   Lino Cosi   **Cancelled**   linö
 44    Ticket 44                  Mathieu   Lino Cosi   **Started**     téam
 40    Ticket 40                  Luc       Lino Cosi   **Cancelled**   docs
 36    Ticket 36                  Luc       Lino Cosi   **Started**     research
 32    Ticket 32                  Jean      Lino Cosi   **Cancelled**   shop
 28    Ticket 28                  Jean      Lino Cosi   **Started**     linö
 24    Ticket 24                  Mathieu   Lino Cosi   **Cancelled**   téam
 20    Ticket 20                  Mathieu   Lino Cosi   **Started**     docs
 16    How to get bar from foo    Luc       Lino Cosi   **Cancelled**   research
 12    Foo cannot bar             Luc       Lino Cosi   **Started**     shop
 8     Is there any Bar in Foo?   Jean      Lino Cosi   **Cancelled**   linö
 4     Foo and bar don't baz      Jean      Lino Cosi   **Started**     docs
===== ========================== ========= =========== =============== ==========
<BLANKLINE>

 


Topic groups
============

>>> rt.show(topics.TopicGroups)
No data to display

>>> show_menu_path(topics.TopicGroups)
Configure --> Contacts --> Topic groups
