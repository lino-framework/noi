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
======================================================= ============= ============== ==========
 Description                                             Ticket type   Topic          Priority
------------------------------------------------------- ------------- -------------- ----------
 `#111 (Ticket 111) <Detail>`__ by *luc* for *marc*      Upgrade       Lino Core      100
 `#102 (Ticket 102) <Detail>`__ by *luc* for *marc*      Upgrade       Lino Voga      100
 `#93 (Ticket 93) <Detail>`__ by *luc* for *marc*        Upgrade       Lino Cosi      100
 `#75 (Ticket 75) <Detail>`__ by *luc*                   Upgrade       Lino Core      100
 `#66 (Ticket 66) <Detail>`__ by *luc* for *marc*        Upgrade       Lino Voga      100
 `#57 (Ticket 57) <Detail>`__ by *luc* for *marc*        Upgrade       Lino Cosi      100
 `#48 (Ticket 48) <Detail>`__ by *luc* for *marc*        Upgrade       Lino Welfare   100
 `#30 (Ticket 30) <Detail>`__ by *luc*                   Upgrade       Lino Voga      100
 `#21 (Ticket 21) <Detail>`__ by *luc* for *marc*        Upgrade       Lino Cosi      100
 `#12 (Foo cannot bar) <Detail>`__ by *luc* for *marc*   Upgrade       Lino Welfare   100
 **Total (10 rows)**                                                                  **1000**
======================================================= ============= ============== ==========
<BLANKLINE>


This data is being rendered using plain bootstrap HTML:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, "lxml")
>>> links = soup.find_all('a')
>>> len(links)
58
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
27
>>> print(links[0].get('href'))
/?ul=en

>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Tickets Home en de fr Site About #13 (Bar cannot foo) << < > >> State: Sticky
<BLANKLINE>
<BLANKLINE>
(last update ...) Created ... by jean Topic: Lino Cosi Site: welket Linking to #1 and to blog . Hackerish comment ... This is Lino Noi ... using ...
