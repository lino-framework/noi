.. _noi.specs.public:

=================================================================
Experimental interface to Team using Bootstrap and self-made URLs
=================================================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_public
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.public.settings.demo')
    >>> from lino.api.doctest import *

This document describes the :mod:`lino_noi.projects.public` variant of
:ref:`noi` which provides readonly anonymous access to the data of
:mod:`lino_noi.projects.team` using the :mod:`lino_noi.lib.public`
user interface.

The :mod:`lino_noi.lib.public` user interface is yet another way of
providing read-only anonymous access.  But it is experimental,
currently we recommend :ref:`noi.specs.bs3`


.. contents::
  :local:

Public tickets
==============

This is currently the only table publicly available.

The demo database contains the following data:

>>> rt.show(tickets.PublicTickets)
... #doctest: +REPORT_UDIFF
=================================== ============= ============== ==========
 Overview                            Ticket type   Topic          Priority
----------------------------------- ------------- -------------- ----------
 `#111 (Ticket 94) <Detail>`__       Upgrade       Lino Core      100
 `#102 (Ticket 85) <Detail>`__       Upgrade       Lino Voga      100
 `#93 (Ticket 76) <Detail>`__        Upgrade       Lino Cosi      100
 `#75 (Ticket 58) <Detail>`__        Upgrade       Lino Core      100
 `#66 (Ticket 49) <Detail>`__        Upgrade       Lino Voga      100
 `#57 (Ticket 40) <Detail>`__        Upgrade       Lino Cosi      100
 `#48 (Ticket 31) <Detail>`__        Upgrade       Lino Welfare   100
 `#30 (Ticket 13) <Detail>`__        Upgrade       Lino Voga      100
 `#21 (Ticket 4) <Detail>`__         Upgrade       Lino Cosi      100
 `#12 (Foo cannot bar) <Detail>`__   Upgrade       Lino Welfare   100
 **Total (10 rows)**                                              **1000**
=================================== ============= ============== ==========
<BLANKLINE>

The home page:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, 'lxml')
>>> links = soup.find_all('a')
>>> len(links)
28
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
/ticket/111


>>> res = test_client.get('/ticket/13/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, 'lxml')
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Home en de fr #13 Bar cannot foo State: Sticky
<BLANKLINE>
<BLANKLINE>
(last update ...) Reported by: jean ... Topic: Lino Cosi Linking to [ticket 1] and to
 [url http://luc.lino-framework.org/blog/2015/0923.html blog]. This is Lino Noi ... using ...
