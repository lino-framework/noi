.. _noi.specs.care_de:

========================================
Lino Care, ein soziales Ticketing-System
========================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_care_de
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_noi.projects.care_de.settings')
    >>> from lino.api.doctest import *

(This is basically the German translation of :doc:`care`.)

.. contents::
  :local:

Projektbeschreibung
===================

Ziel des Projekts ist die Vermittlung kostenloser Freundschaftsdienste
zwischen Immigranten und Hiesigen zwecks Förderung der Integration.

Es geht um *kostenlosen* Austausch. Hier wird weder von Geld noch von
sonstigen Zahlungseinheiten gesprochen. Es geht nicht um Abrechnen von
Leistungen und Gegenleistungen, sondern um das Kennenlernen und
Vernetzung von Kontakten.

Im Gegensatz zur Patenschaftsbörse wird hier nur immer ein
punktuelles, zeitlich begrenztes Engagement erwartet.

Im Gegensatz zu Projekten wie `Helpific <https://helpific.com>`__ gibt
es in Lino Care einen Katalog von **Fähigkeiten**, der es uns
ermöglicht, automatisierte Hilfsvorschläge ("Wo kann ich helfen?") zu
machen.

Design-Entscheidungen
=====================

Es wird nicht unterschieden zwischen "Helfern" und "Helfenden", jeder
kann sowohl Anfragen als auch Angebote machen.

Weder Hilfesuchende noch Anbieter brauchen sich selber einzuloggen.
Das Erfassen in der Datenbank wird durch eine Gruppe von *Vermittlern*
gemacht. Diese Mitarbeiter werden auf Vertrauenswürdigkeit geprüft und
erhalten eine Schulung.  Eine weitere Gruppe von Mitarbeitern arbeitet
„draußen“ und hat als Aufgabe, mit vielen Menschen in ständigem
Kontakt zu sein und sowohl Angebote als auch Anfragen zu erkennen und
zu sammeln. Diese Mitarbeiter können ihre Informationen und Berichte
entweder selber eingeben, oder diese "Computerarbeit" durch einen
spezialisierten Mitarbeiter im Büro erledigen lassen.


Funktionsbeschreibung
=====================

Die Anwendung basiert auf einem Ticketing-System, wie es in der
Softwareentwicklung benutzt wird. Jede Hilfeanfrage wird zu einem
"Ticket".  Ein Ticket hat einen "Besitzer" (der Hilfesuchende) sowie
einen zugewiesenen "Verantwortlichen" (der sich "darum kümmert").
Außerdem ist auch wichtig der Status eines Tickets: Offen, Erledigt,
"Wartet auf Reaktion von Dritten", "Wartet auf einen neuen
Verantwortlichen", usw.

Die Mitarbeiter können Berichte ihrer Gespräche und Aktionen in die
Datenbank eintragen, die andere Mitarbeiter später lesen
können. Dadurch wird ein Teamgeist gefördert, der auch ohne viele
Versammlungen auskommt.

Eine mögliche Option ist, dass die Mitarbeiter ihre Arbeitszeit
notieren können. Es wirkt motivierend, wenn man seine ehrenamtlich
geleistete Arbeitszeit irgendwo stehen sieht, slbst wenn man dafür
kein Geld bekommt.

Geschichte
==========

Im **Oktober 2015** hatten Johannes und Luc zwei Analysegespräche, bei
denen die Grundidee für Lino Care entstand.  Im **April 2016** trafen
sie sich wieder und entdeckten bei einem weiteren Analysegespräch,
dass `Lino Noi <http://noi.lino-framework.org/index.html>`_ fast ohne
Änderungen für diese Anwendung verwendet werden könnte.  Ein früher
Prototyp wurde am Donnerstag 21. April 2016 in Nispert vorgestellt und
besprochen. Eine Woche später begutachteten Anna und Luc zum ersten
Mal gemeinsam die frisch eingerichtete Datenbank.




Benutzer
========

Lino Care kennt folgenden Benutzerarten:

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


In der Demo-Datenbank  gibt es folgende Benutzer:

>>> rt.show('users.Users')
============== ============= ========= ==============
 Benutzername   Benutzerart   Vorname   Familienname
-------------- ------------- --------- --------------
 alex           Benutzer
 berta          Benutzer
 christa        Benutzer
 dora           Benutzer
 eric           Vermittler
 robin          Verwalter     Robin     Rood
 rolf           Verwalter     Rolf      Rompen
 romain         Verwalter     Romain    Raffault
============== ============= ========= ==============
<BLANKLINE>



Fähigkeiten
===========

>>> rt.show(faculties.AllFaculties)
... #doctest: -REPORT_UDIFF
============================= ============================ ========================== =========== ==================== =========================
 Bezeichnung                   Bezeichnung (fr)             Bezeichnung (en)           Affinität   Optionen-Kategorie   Übergeordnete Fähigkeit
----------------------------- ---------------------------- -------------------------- ----------- -------------------- -------------------------
 Babysitting                   Garde enfant                 Babysitting                100
 Botengänge                    Commissions                  Shopping                   100
 Briefe schreiben              Écrire des lettres           Write letters              100
 Deutschunterricht             Cours d'allemand             German lessons             100                              Unterricht
 Fahrdienst                    Voiture                      Car driving                100
 Französischunterricht         Cours de francais            French lessons             100                              Unterricht
 Friseur                       Coiffure                     Hair cutting               100
 Gartenarbeiten                Travaux de jardin            Garden works               100                              Haus und Garten
 Gesellschafter für Senioren   Rencontres personnes agées   Mentoring elderly people   100
 Gitarrenunterricht            Cours de guitare             Guitar lessons             100                              Musik
 Haus und Garten               Maison et jardin             Home & Garden              100
 Hunde spazierenführen         Chiens                       Go out with dogs           100
 Klavierunterricht             Cours de piano               Piano lessons              100                              Musik
 Kleider reparieren            Réparer des vètements        Repairing clothes          100                              Haus und Garten
 Matheunterricht               Cours de maths               Maths lessons              100                              Unterricht
 Musik                         Musique                      Music                      100
 Renovierung                   Rénovation                   Renovation                 100                              Haus und Garten
 Reparaturarbeiten             Travaux de réparation        Repair works               100                              Haus und Garten
 Unterricht                    Cours                        Teaching                   100
 Übersetzungsarbeiten          Traductions                  Translations               100         Sprachen
 **Total (20 Zeilen)**                                                                 **2000**
============================= ============================ ========================== =========== ==================== =========================
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
==== ========== ====================== =========== =============
 ID   Benutzer   Fähigkeit              Affinität   Option
---- ---------- ---------------------- ----------- -------------
 1    alex       Übersetzungsarbeiten   100         Französisch
 2    berta      Übersetzungsarbeiten   100         Französisch
 3    berta      Übersetzungsarbeiten   100         Deutsch
 4    alex       Gartenarbeiten         100
 5    alex       Reparaturarbeiten      100
 6    christa    Klavierunterricht      100
 7    eric       Gitarrenunterricht     100
                                        **700**
==== ========== ====================== =========== =============
<BLANKLINE>

>>> rt.show('topics.Topics')
========== ============= ================== ================== ==============
 Referenz   Bezeichnung   Bezeichnung (fr)   Bezeichnung (en)   Themengruppe
---------- ------------- ------------------ ------------------ --------------
            Französisch   Français           French             Sprachen
            Deutsch       Allemand           German             Sprachen
            Englisch      Anglais            English            Sprachen
========== ============= ================== ================== ==============
<BLANKLINE>

>>> rt.show('tickets.Tickets')
==== =========================================================================================== ========== ======= ==================== ================ =========
 ID   Zusammenfassung                                                                             Anfrager   Thema   Fähigkeit            Arbeitsablauf    Projekt
---- ------------------------------------------------------------------------------------------- ---------- ------- -------------------- ---------------- ---------
 8    Wer fährt für mich nach Aachen Windeln kaufen?                                              alex               Botengänge           **Neu**
 7    Wer kann meine Abschlussarbeit korrekturlesen?                                              dora                                    **ZuTun**
 6    Wer hilft meinem Sohn sich auf die Mathearbeit am 21.05. vorzubereiten? 5. Schuljahr PDS.   berta              Matheunterricht      **Neu**
 5    Wer macht Musik auf meinem Geburtstag?                                                      alex               Musik                **Neu**
 4    Wer kann meiner Tochter Gitarreunterricht geben?                                            alex               Gitarrenunterricht   **Besprechen**
 3    Wer kann meinem Sohn Klavierunterricht geben?                                               dora               Klavierunterricht    **Neu**
 2    Mein Rasen muss gemäht werden. Donnerstags oder Samstags                                    christa                                 **Neu**
 1    Mein Wasserhahn tropft, wer kann mir helfen?                                                berta              Reparaturarbeiten    **Neu**
==== =========================================================================================== ========== ======= ==================== ================ =========
<BLANKLINE>


Das Hauptmenü
=============

>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Büro : Meine Mitteilungen, Meine Favoriten, Meine Auszüge, Meine Kommentare
- Bitten : Meine Bitten, Wo ich helfen kann, Zu tun, Aktive Bitten, Bitten, Nicht zugewiesene Bitten, Aktive Projekte
- Arbeitszeit : Sitzungen
- Berichte :
  - System : Broken GFKs
  - Arbeitszeit : Dienstleistungsberichte
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Themen : Themen, Themengruppen
  - Büro : Auszugsarten, Meine Einfügetexte
  - Bitten : Projekte, Projekte (Hierarchie), Project Types, Ticket types, Umfelder
  - Fähigkeiten : Fähigkeiten (Hierarchie), Fähigkeiten (alle)
  - Arbeitszeit : Session Types
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerarten, Mitteilungen, Änderungen
  - Themen : Interessen
  - Büro : Favoriten, Auszüge, Kommentare, Einfügetexte
  - Bitten : Verknüpfungen, Zustände
  - Fähigkeiten : Kompetenzen
  - Arbeitszeit : Sitzungen
- Site : Info


**Einfache** Benutzer haben ein eingeschränktes Menü:

>>> rt.login('berta').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Büro : Meine Mitteilungen, Meine Favoriten, Meine Auszüge, Meine Kommentare
- Bitten : Meine Bitten, Wo ich helfen kann, Zu tun
- Konfigurierung :
 - Orte : Länder
 - Büro : Meine Einfügetexte
- Site : Info

Bittenlisten
==============


Meine Bitten
------------

  
>>> rt.login('christa').show(tickets.MyTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
============================================================================ =========== ======= =============== ===========================================
 Overview                                                                     Fähigkeit   Thema   Zugewiesen zu   Arbeitsablauf
---------------------------------------------------------------------------- ----------- ------- --------------- -------------------------------------------
 `#2 (Mein Rasen muss gemäht werden. Donnerstags oder Samstags) <Detail>`__                                       [✋] [☆] **Neu** → [📌] [🗪] [🐜] [🕸] [☐] [🗑]
============================================================================ =========== ======= =============== ===========================================
<BLANKLINE>


Where I can help
----------------

>>> rt.login('christa').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
================================================================= ========== ======= =================== =================
 Overview                                                          Anfrager   Thema   Fähigkeit           Arbeitsablauf
----------------------------------------------------------------- ---------- ------- ------------------- -----------------
 `#5 (Wer macht Musik auf meinem Geburtstag?) <Detail>`__          alex               Musik               [✋] [☆] **Neu**
 `#3 (Wer kann meinem Sohn Klavierunterricht geben?) <Detail>`__   dora               Klavierunterricht   [✋] [☆] **Neu**
================================================================= ========== ======= =================== =================
<BLANKLINE>


My to-do list
-------------

>>> rt.login('christa').show(tickets.TicketsToDo)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
Keine Daten anzuzeigen


Rating a ticket
===============

>>> base = '/choices/tickets/Tickets/rating'
>>> show_choices("rolf", base + '?query=')
<br/>
Sehr gut
Gut
Ausreichend
Mangelhaft
Ungenügend
Nicht bewertbar

>>> show_choices("robin", base + '?query=')  #doctest: +SKIP
<br/>
Very good
Good
Satisfying
Deficient
Insufficient
Unratable

>>> show_choices("romain", base + '?query=')  #doctest: +SKIP
<br/>
Très bien
Bien
Satisfaisant
Médiocre
Insuffisant
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
      - (general1_2): **Anfrager** (reporter), **Fähigkeit** (faculty), **Thema** (topic), **Zugewiesen zu** (assigned_to)
      - (general1_3): **Umfeld** (site), **Arbeitsablauf** (workflow_buttons), **Bewertung** (rating)
    - **Zuweisbare Arbeiter** (faculties.AssignableWorkersByTicket) [visible for connector admin]
  - (general_2): **Beschreibung** (description), **Kommentare** (CommentsByRFC) [visible for user connector admin], **Sitzungen** (SessionsByTicket) [visible for connector admin]
- **History** (history_tab_1) [visible for connector admin]:
  - **Änderungen** (changes.ChangesByMaster) [visible for user connector admin]
  - **Beobachtet durch** (stars.StarsByController) [visible for user connector admin]
- **Mehr** (more) [visible for connector admin]:
  - (more1) [visible for all]:
    - (more1_1): **Erstellt** (created), **Bearbeitet** (modified), **Ticket type** (ticket_type)
    - (more1_2): **Zustand** (state), **Priorität** (priority), **Projekt** (project)
  - (more_2) [visible for all]: **Lösung** (upgrade_notes), **Verknüpfungen** (LinksByTicket) [visible for connector admin]
<BLANKLINE>


Topic groups
============


>>> show_menu_path(topics.TopicGroups, language='en')
Configure --> Topics --> Topic groups

>>> rt.show(topics.TopicGroups)
==== ============= ================== ================== ==============
 ID   Bezeichnung   Bezeichnung (fr)   Bezeichnung (en)   Beschreibung
---- ------------- ------------------ ------------------ --------------
 1    Sprachen      Langues            Languages
==== ============= ================== ================== ==============
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
