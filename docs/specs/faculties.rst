.. _noi.specs.faculties:

================================
Faculties management in Lino Noi
================================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_faculties
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


Lino Noi has a notions of **faculties** and **competences** which
might be useful in bigger teams for assigning a ticket to a worker.

They are implemented in :mod:`lino_noi.lib.faculties`.  In the Team
demo database they are not really used.  See also :doc:`care` which
has does more usage of them.


.. contents::
  :local:


>>> rt.show(faculties.TopLevelSkills)
... #doctest: +REPORT_UDIFF
=============== ================== ================== ==== ========== ================
 Designation     Designation (de)   Designation (fr)   ID   Children   Parent faculty
--------------- ------------------ ------------------ ---- ---------- ----------------
 Analysis        Analysis           Analysis           1
 Code changes    Code changes       Code changes       2
 Configuration   Configuration      Configuration      5
 Documentation   Documentation      Documentation      3
 Enhancement     Enhancement        Enhancement        6
 Offer           Offer              Offer              8
 Optimization    Optimization       Optimization       7
 Testing         Testing            Testing            4
=============== ================== ================== ==== ========== ================
<BLANKLINE>


>>> rt.show('faculties.Offers')
... #doctest: +REPORT_UDIFF
==== ================= =============== ============= ==========
 ID   User              Skill           Description   Affinity
---- ----------------- --------------- ------------- ----------
 1    Rolf Rompen       Analysis                      100
 2    Rolf Rompen       Code changes                  70
 3    Rolf Rompen       Documentation                 71
 4    Rolf Rompen       Testing                       42
 5    Rolf Rompen       Configuration                 62
 6    Romain Raffault   Code changes                  76
 7    Romain Raffault   Documentation                 92
 8    Romain Raffault   Testing                       98
 9    Romain Raffault   Configuration                 68
 10   Robin Rood        Analysis                      23
 11   Luc               Analysis                      120
 12   Luc               Code changes                  150
 13   Luc               Documentation                 75
 14   Mathieu           Documentation                 46
 15   Robin Rood        Testing                       65
 16   Mathieu           Testing                       42
 17   Luc               Configuration                 46
 18   Mathieu           Configuration                 92
                                                      **1338**
==== ================= =============== ============= ==========
<BLANKLINE>


>>> show_choices('axel', '/choices/faculties/OffersBySupplier/faculty')
Analysis
Code changes
Configuration
Documentation
Enhancement
Offer
Optimization
Testing
