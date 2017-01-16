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

Dieses Dokument ist eine eher technische Beschreibung der
Funktionalitäten von Lino Care. Es geht stellenweise sehr ins Detail,
weil es auch Teil der Test-Suite ist.

Für eine Einführung und Übersicht siehe :doc:`/care/index`.

.. contents::
  :local:



Benutzer
========

Lino Care kennt folgenden *Benutzerarten*:

>>> rt.show('users.UserTypes')
====== =========== ============
 Wert   name        Text
------ ----------- ------------
 000    anonymous   Anonym
 100    user        Benutzer
 500    connector   Vermittler
 900    admin       Verwalter
====== =========== ============
<BLANKLINE>


In der Demo-Datenbank gibt es folgende Benutzer:

>>> rt.show('users.Users')
============== ============= ========= ==============
 Benutzername   Benutzerart   Vorname   Familienname
-------------- ------------- --------- --------------
 alex           Benutzer      Alex
 berta          Benutzer      Berta
 christa        Benutzer      Christa
 dora                         Dora
 eric           Vermittler    Eric
 robin          Verwalter     Robin     Rood
 rolf           Verwalter     Rolf      Rompen
 romain         Verwalter     Romain    Raffault
============== ============= ========= ==============
<BLANKLINE>



Fähigkeiten
===========

>>> rt.show(faculties.AllFaculties)
... #doctest: -REPORT_UDIFF
============================= ============================ ========================== =========== =========================
 Bezeichnung                   Bezeichnung (fr)             Bezeichnung (en)           Affinität   Übergeordnete Fähigkeit
----------------------------- ---------------------------- -------------------------- ----------- -------------------------
 Babysitting                   Garde enfant                 Babysitting                100
 Botengänge                    Commissions                  Shopping                   100
 Briefe schreiben              Écrire des lettres           Write letters              100
 Deutschunterricht             Cours d'allemand             German lessons             100         Unterricht
 Fahrdienst                    Voiture                      Car driving                100
 Französischunterricht         Cours de francais            French lessons             100         Unterricht
 Friseur                       Coiffure                     Hair cutting               100
 Gartenarbeiten                Travaux de jardin            Garden works               100         Haus und Garten
 Gesellschafter für Senioren   Rencontres personnes agées   Mentoring elderly people   100
 Gitarrenunterricht            Cours de guitare             Guitar lessons             100         Musik
 Haus und Garten               Maison et jardin             Home & Garden              100
 Hunde spazierenführen         Chiens                       Go out with dogs           100
 Klavierunterricht             Cours de piano               Piano lessons              100         Musik
 Kleider reparieren            Réparer des vètements        Repairing clothes          100         Haus und Garten
 Matheunterricht               Cours de maths               Maths lessons              100         Unterricht
 Musik                         Musique                      Music                      100
 Renovierung                   Rénovation                   Renovation                 100         Haus und Garten
 Reparaturarbeiten             Travaux de réparation        Repair works               100         Haus und Garten
 Unterricht                    Cours                        Teaching                   100
 Übersetzungsarbeiten          Traductions                  Translations               100
 **Total (20 Zeilen)**                                                                 **2000**
============================= ============================ ========================== =========== =========================
<BLANKLINE>


>>> rt.show(faculties.TopLevelFaculties)
... #doctest: +REPORT_UDIFF
============================= ============================ ========================== ==== ============================================================================ =========================
 Bezeichnung                   Bezeichnung (fr)             Bezeichnung (en)           ID   Kinder                                                                       Übergeordnete Fähigkeit
----------------------------- ---------------------------- -------------------------- ---- ---------------------------------------------------------------------------- -------------------------
 Babysitting                   Garde enfant                 Babysitting                16
 Botengänge                    Commissions                  Shopping                   14
 Briefe schreiben              Écrire des lettres           Write letters              20
 Fahrdienst                    Voiture                      Car driving                13
 Friseur                       Coiffure                     Hair cutting               15
 Gesellschafter für Senioren   Rencontres personnes agées   Mentoring elderly people   17
 Haus und Garten               Maison et jardin             Home & Garden              8    *Gartenarbeiten*, *Kleider reparieren*, *Renovierung*, *Reparaturarbeiten*
 Hunde spazierenführen         Chiens                       Go out with dogs           18
 Musik                         Musique                      Music                      5    *Gitarrenunterricht*, *Klavierunterricht*
 Unterricht                    Cours                        Teaching                   1    *Deutschunterricht*, *Französischunterricht*, *Matheunterricht*
 Übersetzungsarbeiten          Traductions                  Translations               19
============================= ============================ ========================== ==== ============================================================================ =========================
<BLANKLINE>


>>> rt.show('faculties.Competences')
==== ========== ====================== ===========
 ID   Benutzer   Fähigkeit              Affinität
---- ---------- ---------------------- -----------
 1    Alex       Übersetzungsarbeiten   100
 2    Berta      Übersetzungsarbeiten   100
 3    Alex       Gartenarbeiten         100
 4    Alex       Reparaturarbeiten      100
 5    Christa    Klavierunterricht      100
 6    Dora       Reparaturarbeiten      100
 7    Eric       Gitarrenunterricht     100
 8    Dora       Botengänge             100
                                        **800**
==== ========== ====================== ===========
<BLANKLINE>

>>> rt.show('tickets.Tickets')
==== =========================================================================================== ========= ==================== ================= =========
 ID   Zusammenfassung                                                                             Autor     Fähigkeit            Aktionen          Projekt
---- ------------------------------------------------------------------------------------------- --------- -------------------- ----------------- ---------
 8    Wer fährt für mich nach Aachen Windeln kaufen?                                              Alex      Botengänge           **Bereit**
 7    Wer kann meine Abschlussarbeit korrekturlesen?                                              Eric                           **Schläft**
 6    Wer hilft meinem Sohn sich auf die Mathearbeit am 21.05. vorzubereiten? 5. Schuljahr PDS.   Berta     Matheunterricht      **Gestartet**
 5    Wer macht Musik auf meinem Geburtstag?                                                      Alex      Musik                **Offen**
 4    Wer kann meiner Tochter Gitarreunterricht geben?                                            Alex      Gitarrenunterricht   **Offen**
 3    Wer kann meinem Sohn Klavierunterricht geben?                                               Eric      Klavierunterricht    **Besprechen**
 2    Mein Rasen muss gemäht werden. Donnerstags oder Samstags                                    Christa   Gartenarbeiten       **Neu**
 1    Mein Wasserhahn tropft, wer kann mir helfen?                                                Berta     Reparaturarbeiten    **Geschlossen**
==== =========================================================================================== ========= ==================== ================= =========
<BLANKLINE>


Das Hauptmenü
=============

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
  - System : Datenbankmodelle, Vollmachten, Benutzerarten, Änderungen, Benachrichtigungen
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

Bittenlisten
==============


Meine Bitten
------------
  
>>> rt.login('christa').show(tickets.MyTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================================================================ ===============================
 Beschreibung                                                                 Aktionen
---------------------------------------------------------------------------- -------------------------------
 `#2 (Mein Rasen muss gemäht werden. Donnerstags oder Samstags) <Detail>`__   [★] **Neu** → [☾] [☎] [☉] [☐]
============================================================================ ===============================
<BLANKLINE>


Where I can help
----------------

>>> rt.login('alex').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================================================================================================== ================ =============
 Beschreibung                                                                                         Fähigkeit        Aktionen
---------------------------------------------------------------------------------------------------- ---------------- -------------
 `#2 (Mein Rasen muss gemäht werden. Donnerstags oder Samstags) <Detail>`__ by `Christa <Detail>`__   Gartenarbeiten   [☆] **Neu**
==================================================================================================== ================ =============
<BLANKLINE>

>>> rt.login('berta').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
Keine Daten anzuzeigen

>>> rt.login('eric').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
========================================================================================= ==================== ===============
 Beschreibung                                                                              Fähigkeit            Aktionen
----------------------------------------------------------------------------------------- -------------------- ---------------
 `#4 (Wer kann meiner Tochter Gitarreunterricht geben?) <Detail>`__ by `Alex <Detail>`__   Gitarrenunterricht   [☆] **Offen**
========================================================================================= ==================== ===============
<BLANKLINE>


Meine Hilfsangebote
-------------------

>>> rt.login('christa').show(votes.MyOffers)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================================================================================================ ================================
 Beschreibung                                                                                                 Aktionen
------------------------------------------------------------------------------------------------------------ --------------------------------
 `#5 (Wer macht Musik auf meinem Geburtstag?) <Detail>`__ by `Alex <Detail>`__                                [★] **Kandidat** → [Interesse]
 `#3 (Wer kann meinem Sohn Klavierunterricht geben?) <Detail>`__ by `Eric <Detail>`__ for `Dora <Detail>`__   [★] **Kandidat** → [Interesse]
============================================================================================================ ================================
<BLANKLINE>


>>> rt.login('eric').show(votes.MyOffers)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=============================================================================== =====================================================
 Beschreibung                                                                    Aktionen
------------------------------------------------------------------------------- -----------------------------------------------------
 `#5 (Wer macht Musik auf meinem Geburtstag?) <Detail>`__ by `Alex <Detail>`__   [★] **Kandidat** → [Interesse] [Zuweisen] [Absagen]
=============================================================================== =====================================================
<BLANKLINE>



Meine Aufgaben
--------------

>>> rt.login('alex').show(votes.MyTasks)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
Keine Daten anzuzeigen

>>> rt.login('alex').show(votes.MyVotes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================================================================================== ==================
 Beschreibung                                                                           Aktionen
-------------------------------------------------------------------------------------- ------------------
 `#8 (Wer fährt für mich nach Aachen Windeln kaufen?) <Detail>`__                       [★] **Autor**
 `#5 (Wer macht Musik auf meinem Geburtstag?) <Detail>`__                               [★] **Autor**
 `#4 (Wer kann meiner Tochter Gitarreunterricht geben?) <Detail>`__                     [★] **Autor**
 `#1 (Mein Wasserhahn tropft, wer kann mir helfen?) <Detail>`__ by `Berta <Detail>`__   [★] **Erledigt**
====================================================================================== ==================
<BLANKLINE>



Rating a help offer
===================


>>> base = '/choices/votes/Votes/rating'
>>> show_choices("rolf", base + '?query=')
<br/>
Sehr gut
Gut
Ausreichend
Mangelhaft
Ungenügend
Nicht bewertbar


The detail layout of a ticket
=============================

Here is a textual description of the fields and their layout used in
the detail window of a ticket.

>>> from lino.utils.diag import py2rst
>>> print(py2rst(tickets.Tickets.detail_layout, True))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
(main) [visible for all]:
- **Allgemein** (general):
  - (general_1):
    - (general1):
      - (general1_1): **Zusammenfassung** (summary), **ID** (id), **Deadline** (deadline)
      - (general1_2): **Autor** (user), **End user** (end_user), **Fähigkeit** (faculty)
      - (general1_3): **Umfeld** (site), **Aktionen** (workflow_buttons)
    - **Stimmabgaben** (votes.VotesByVotable) [visible for user connector admin]
  - (general_2): **Beschreibung** (description), **Kommentare** (CommentsByRFC) [visible for user connector admin]
- **History** (changes.ChangesByMaster) [visible for connector admin]
- **Mehr** (more) [visible for connector admin]:
  - (more_1) [visible for all]:
    - (more1):
      - (more1_1): **Erstellt** (created), **Bearbeitet** (modified), **Ticket type** (ticket_type)
      - (more1_2): **Zustand** (state), **Priorität** (priority), **Projekt** (project)
    - **Zuweisbare Arbeiter** (faculties.AssignableWorkersByTicket) [visible for connector admin]
  - (more_2) [visible for all]: **Lösung** (upgrade_notes), **Verknüpfungen** (LinksByTicket) [visible for connector admin]
<BLANKLINE>


Configuring your preferences
============================

>>> show_choices('axel', '/choices/faculties/CompetencesByUser/faculty')
Babysitting
Botengänge
Briefe schreiben
Deutschunterricht
Fahrdienst
Französischunterricht
Friseur
Gartenarbeiten
Gesellschafter für Senioren
Gitarrenunterricht
Haus und Garten
Hunde spazierenführen
Klavierunterricht
Kleider reparieren
Matheunterricht
Musik
Renovierung
Reparaturarbeiten
Unterricht
Übersetzungsarbeiten
