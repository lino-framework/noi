.. _noi.specs.bs3:

=====================================================
A read-only interface to Team using generic Bootstrap
=====================================================

.. How to test only this document:

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


The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: -REPORT_UDIFF
============================================= ======= ============= ========== =========== ==========
 Overview                                      State   Ticket type   Project    Topic       Priority
--------------------------------------------- ------- ------------- ---------- ----------- ----------
 `#113 (Ticket 96) <Detail>`__                 New     Enhancement   linö       Lino Cosi   100
 `#105 (Ticket 88) <Detail>`__                 New     Upgrade       docs       Lino Cosi   100
 `#97 (Ticket 80) <Detail>`__                  New     Bugfix        shop       Lino Cosi   100
 `#81 (Ticket 64) <Detail>`__                  New     Upgrade       research   Lino Cosi   100
 `#73 (Ticket 56) <Detail>`__                  New     Bugfix        linö       Lino Cosi   100
 `#65 (Ticket 48) <Detail>`__                  New     Enhancement   docs       Lino Cosi   100
 `#57 (Ticket 40) <Detail>`__                  New     Upgrade       shop       Lino Cosi   100
 `#41 (Ticket 24) <Detail>`__                  New     Enhancement   research   Lino Cosi   100
 `#33 (Ticket 16) <Detail>`__                  New     Upgrade       linö       Lino Cosi   100
 `#25 (Ticket 8) <Detail>`__                   New     Bugfix        docs       Lino Cosi   100
 `#17 (Ticket 0) <Detail>`__                   New     Enhancement   shop       Lino Cosi   100
 `#1 (Föö fails to bar when baz) <Detail>`__   New     Bugfix        linö       Lino Cosi   100
 **Total (12 rows)**                                                                        **1200**
============================================= ======= ============= ========== =========== ==========
<BLANKLINE>


This data is being rendered using plain bootstrap HTML:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, "lxml")
>>> links = soup.find_all('a')
>>> len(links)
35
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
Tickets Home en de fr Site About #13 (Bar cannot foo) << < > >> State: Sleeping
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: Rolf Rompen ... Topic: Lino Cosi Site: welket Linking to #1 and to blog . This is Lino Noi ... using ...
