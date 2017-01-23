.. _noi.specs.care_de:

====================================
Lino Care - Technische Spezifikation
====================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_care_de
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.care_de.settings')
    >>> from lino.api.doctest import *

Dieses Dokument ist eine technische Beschreibung der Funktionalitäten
von Lino Care. Es ist auch Teil der Test-Suite.

Die englische Version dieses Dokuments (:doc:`/specs/care`) ist
umfangreicher.

Für eine Einführung und Übersicht siehe :doc:`/care/index`.

.. contents::
  :local:



Das Hauptmenü
=============

**Systemverwalter** haben ei nkomplettes Menü:

>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Stimmabgaben : Meine Kandidaturen, Meine Aufgaben, Meine Interessen, Meine Stimmabgaben
- Büro : Meine Auszüge, Meine Kommentare, Meine Benachrichtigungen
- Bitten : Meine Bitten, Wo ich helfen kann, Aktive Bitten, Alle Bitten, Nicht zugewiesene Bitten, Aktive Projekte
- Berichte :
  - System : Broken GFKs
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Büro : Auszugsarten
  - Bitten : Projekte, Projekte (Hierarchie), Project Types, Ticket types, Umfelder
  - Fähigkeiten : Fähigkeiten (Hierarchie), Fähigkeiten (alle)
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerarten, Änderungen, Benachrichtigungen, All dashboard widgets
  - Stimmabgaben : Alle Stimmabgaben, Stimmabgabezustände
  - Büro : Auszüge, Kommentare
  - Bitten : Verknüpfungen, Ticketzustände
  - Fähigkeiten : Kompetenzen
- Site : Info


**Einfache** Benutzer haben ein eingeschränktes Menü:

>>> rt.login('berta').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Stimmabgaben : Meine Kandidaturen, Meine Aufgaben, Meine Interessen, Meine Stimmabgaben
- Büro : Meine Kommentare, Meine Benachrichtigungen
- Bitten : Meine Bitten, Wo ich helfen kann
- Site : Info

Bewertungen
===========


>>> base = '/choices/votes/Votes/rating'
>>> show_choices("rolf", base + '?query=')
<br/>
Sehr gut
Gut
Ausreichend
Mangelhaft
Ungenügend
Nicht bewertbar


