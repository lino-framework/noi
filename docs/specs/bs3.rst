.. _noi.specs.bs3:

=====================================================
A read-only interface to Team using generic Bootstrap
=====================================================

.. How to test just this document:

    $ python setup.py test -s tests.SpecsTests.test_bs3
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.bs3.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the read-only public interface of Lino Noi.
implemented in :mod:`lino_noi.projects.bs3`.

Provides readonly anonymous access to the data of
:mod:`lino_noi.projects.team`, using the :mod:`lino.modlib.bootstrap3`
user interface. See also :mod:`lino_noi.projects.public`

This does not use :mod:`lino.modlib.extjs` at all.


.. contents::
  :local:

.. The following was used to reproduce :ticket:`960`:

    >>> res = test_client.get('/tickets/Ticket/13')
    >>> res.status_code
    200



Unassigned tickets
==================

The demo database contains the following "public" tickets:

>>> rt.show(tickets.PublicTickets)
... #doctest: -REPORT_UDIFF
============================================================ ============= =========== ==========
 Description                                                  Ticket type   Topic       Priority
------------------------------------------------------------ ------------- ----------- ----------
 `#115 (Ticket 115) <Detail>`__ by *Jean*                     Bugfix        Lino Voga   100
 `#107 (Ticket 107) <Detail>`__ by *Mathieu*                  Enhancement   Lino Voga   100
 `#91 (Ticket 91) <Detail>`__ by *Jean*                       Bugfix        Lino Voga   100
 `#83 (Ticket 83) <Detail>`__ by *Mathieu*                    Enhancement   Lino Voga   100
 `#75 (Ticket 75) <Detail>`__ by *Luc*                        Upgrade       Lino Voga   100
 `#67 (Ticket 67) <Detail>`__ by *Jean*                       Bugfix        Lino Voga   100
 `#51 (Ticket 51) <Detail>`__ by *Luc*                        Upgrade       Lino Voga   100
 `#43 (Ticket 43) <Detail>`__ by *Jean*                       Bugfix        Lino Voga   100
 `#35 (Ticket 35) <Detail>`__ by *Mathieu*                    Enhancement   Lino Voga   100
 `#27 (Ticket 27) <Detail>`__ by *Luc*                        Upgrade       Lino Voga   100
 `#11 (Class-based Foos and Bars?) <Detail>`__ by *Mathieu*   Enhancement   Lino Voga   100
 **Total (11 rows)**                                                                    **1100**
============================================================ ============= =========== ==========
<BLANKLINE>


This data is being rendered using plain bootstrap HTML:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, "lxml")
>>> links = soup.find_all('a')
>>> len(links)
39
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
#

>>> res = test_client.get('/tickets/Ticket/13')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, "lxml")


>>> links = soup.find_all('a')
>>> len(links)
26
>>> print(links[0].get('href'))
/?ul=en

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Tickets Home en de fr Site About #13 (Bar cannot foo) << < > >> State: Sleeping 
<BLANKLINE>
<BLANKLINE>
(last update ...) Created ... by Jean Topic: Lino Welfare Site: welket Linking to #1 and to blog . This is Lino Noi ... using ...
