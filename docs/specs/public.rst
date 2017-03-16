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
============================================================ ============= =========== ==========
 Description                                                  Ticket type   Topic       Priority
------------------------------------------------------------ ------------- ----------- ----------
 `#115 (Ticket 115) <Detail>`__ by *Jean*                     Bugfix        Lino Voga   100
 `#99 (Ticket 99) <Detail>`__ by *Luc*                        Upgrade       Lino Voga   100
 `#91 (Ticket 91) <Detail>`__ by *Jean*                       Bugfix        Lino Voga   100
 `#83 (Ticket 83) <Detail>`__ by *Mathieu*                    Enhancement   Lino Voga   100
 `#75 (Ticket 75) <Detail>`__ by *Luc*                        Upgrade       Lino Voga   100
 `#59 (Ticket 59) <Detail>`__ by *Mathieu*                    Enhancement   Lino Voga   100
 `#51 (Ticket 51) <Detail>`__ by *Luc*                        Upgrade       Lino Voga   100
 `#43 (Ticket 43) <Detail>`__ by *Jean*                       Bugfix        Lino Voga   100
 `#35 (Ticket 35) <Detail>`__ by *Mathieu*                    Enhancement   Lino Voga   100
 `#19 (Ticket 19) <Detail>`__ by *Jean*                       Bugfix        Lino Voga   100
 `#11 (Class-based Foos and Bars?) <Detail>`__ by *Mathieu*   Enhancement   Lino Voga   100
 **Total (11 rows)**                                                                    **1100**
============================================================ ============= =========== ==========
<BLANKLINE>

The home page:

>>> res = test_client.get('/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, 'lxml')
>>> links = soup.find_all('a')
>>> len(links)
26
>>> print(links[0].get('href'))
/?ul=de
>>> print(links[1].get('href'))
/?ul=fr
>>> print(links[2].get('href'))
/ticket/115


>>> res = test_client.get('/ticket/13/')
>>> res.status_code
200
>>> soup = BeautifulSoup(res.content, 'lxml')
>>> print(soup.get_text(' ', strip=True))
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF +ELLIPSIS
Home en de fr #13 Bar cannot foo State: Sleeping
<BLANKLINE>
<BLANKLINE>
(last update ...) Created ... by Jean Topic: Lino Welfare Linking to [ticket 1] and to
 [url http://luc.lino-framework.org/blog/2015/0923.html blog]. This is Lino Noi ... using ...
