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

When choosing a topic, the search text looks in both the reference and
the designation:

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
 Lino Core
 Lino Welfare
 Lino Cosi
==============
<BLANKLINE>

>>> obj = topics.Topic.objects.get(ref="welfäre")
>>> rt.show(topics.InterestsByTopic, obj)
... #doctest: +REPORT_UDIFF
=========
 Partner
---------
 welket
 welsch
=========
<BLANKLINE>



Filtering tickets by topic
==========================

>>> pv = dict(topic=rt.models.topics.Topic.get_by_ref("così"))
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
===== =========================== ========= =========== =============== =============== ==========
 ID    Summary                     Author    Topic       Faculty         Actions         Project
----- --------------------------- --------- ----------- --------------- --------------- ----------
 113   Ticket 113                  mathieu   Lino Cosi                   **Started**     linö
 109   Ticket 109                  jean      Lino Cosi                   **New**         téam
 105   Ticket 105                  luc       Lino Cosi                   **Sleeping**    docs
 101   Ticket 101                  mathieu   Lino Cosi                   **Talk**        research
 97    Ticket 97                   mathieu   Lino Cosi                   **Ready**       shop
 93    Ticket 93                   luc       Lino Cosi                   **Opened**      linö
 89    Ticket 89                   luc       Lino Cosi                   **Closed**      téam
 85    Ticket 85                   jean      Lino Cosi                   **Sticky**      docs
 81    Ticket 81                   mathieu   Lino Cosi                   **Cancelled**   research
 77    Ticket 77                   mathieu   Lino Cosi                   **Started**     shop
 73    Ticket 73                   jean      Lino Cosi                   **New**         linö
 69    Ticket 69                   luc       Lino Cosi                   **Sleeping**    téam
 65    Ticket 65                   mathieu   Lino Cosi                   **Talk**        docs
 61    Ticket 61                   mathieu   Lino Cosi                   **Ready**       research
 57    Ticket 57                   luc       Lino Cosi                   **Opened**      shop
 53    Ticket 53                   luc       Lino Cosi                   **Closed**      linö
 49    Ticket 49                   jean      Lino Cosi                   **Sticky**      téam
 45    Ticket 45                   mathieu   Lino Cosi                   **Cancelled**   docs
 41    Ticket 41                   mathieu   Lino Cosi                   **Started**     research
 37    Ticket 37                   jean      Lino Cosi                   **New**         shop
 33    Ticket 33                   luc       Lino Cosi                   **Sleeping**    linö
 29    Ticket 29                   mathieu   Lino Cosi                   **Talk**        téam
 25    Ticket 25                   mathieu   Lino Cosi                   **Ready**       docs
 21    Ticket 21                   luc       Lino Cosi                   **Opened**      research
 17    Ticket 17                   luc       Lino Cosi                   **Closed**      shop
 13    Bar cannot foo              jean      Lino Cosi   Documentation   **Sticky**      linö
 9     Foo never matches Bar       mathieu   Lino Cosi   Testing         **Cancelled**   téam
 5     Cannot create Foo           mathieu   Lino Cosi                   **Started**
 1     Föö fails to bar when baz   jean      Lino Cosi                   **New**         linö
===== =========================== ========= =========== =============== =============== ==========
<BLANKLINE>

 


Topic groups
============

>>> rt.show(topics.TopicGroups)
No data to display

>>> show_menu_path(topics.TopicGroups)
Configure --> Contacts --> Topic groups
