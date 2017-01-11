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

Übersicht
=========

**Lino Care** ist eine Variante von :ref:`noi`, die angepasst wurde
für den Einsatz in Organisationen, die Menschen helfen, füreinander zu
sorgen.

Während :ref:`noi` als Ticketing-System für das :ref:`Lino-Team
<lino.team>` und andere Softwareprojekte benutzt wird, entstand *Lino
Care* aus der Beobachtung, dass die meisten Konzepte dieser Software
für soziale Zwecke wiederverwertet werden können. Ein anderer Kontext,
aber ähnliche Datenstrukturen. Was Programmierer ein *Ticket* nennen,
nennen wir in Lino Care eine *Bitte*.

Jede Bitte hat einen "Reporter" (den Hilfesuchenden) sowie einen
zugewiesenen "Verantwortlichen" (der sich "darum kümmert").  Außerdem
ist auch wichtig der Status einer Bitte: Offen, Erledigt, "Wartet auf
Reaktion von Dritten", "Wartet auf einen neuen Verantwortlichen", usw.

Es geht um *kostenlosen* Austausch. Hier wird weder von Geld noch von
sonstigen Zahlungseinheiten gesprochen. Es geht nicht um Abrechnen von
Leistungen und Gegenleistungen, sondern um das Kennenlernen und
Vernetzung von Kontakten.

Im Gegensatz zur Patenschaftsbörse wird hier immer nur ein
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

Optionen
========

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

Lino Care wird im Rahmen eines Projektes der **Oikos VoG** entwickelt,
dessen Ziel die Vermittlung kostenloser Freundschaftsdienste zwischen
Immigranten und Hiesigen zwecks Förderung der Integration ist.  Das
Projekt wird mitgetragen von der `König-Baudouin-Stiftung
<https://www.kbs-frb.be/fr/Activities/Grants/2016/2016D36000204568>`__
and dem `Kiwanis
<http://www.kiwanis.be/eupen/unterstutzte-soz-projekte>`_.

Im **Oktober 2015** hatten Johannes und Luc zwei Analysegespräche, bei
denen die Grundidee für Lino Care entstand.  Im **April 2016**
entdeckten sie bei einem weiteren Analysegespräch, dass `Lino Noi
<http://noi.lino-framework.org/index.html>`_ fast ohne Änderungen für
diese Anwendung verwendet werden könnte.  Ein früher Prototyp wurde am
Donnerstag 21. April 2016 in Nispert vorgestellt und besprochen. Eine
Woche später begutachteten Anna und Luc zum ersten Mal gemeinsam die
frisch eingerichtete Datenbank.

Seitdem geht das Projekt nur langsam voran und wurde auch noch nicht
einer breiteren Öffentlichkeit vorgestellt, weil die VoG Oikos im
Sommer 2016 die meisten Mitarbeiter kündigen musste (aus Gründen, die
nichts mit dem Projekt zu tun haben).  Zur Zeit finden Überlegungen
darüber statt, wer die Trägerschaft übernehmen soll.

Technische Spezifikation
========================

Der Rest dieses Dokuments ist eine eher technische Beschreibung der
Funktionalitäten von Lino Care. Es geht stellenweise sehr ins Detail,
weil es auch Teil der Test-Suite ist.


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
 alex           Benutzer
 berta          Benutzer
 christa        Benutzer
 dora
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
 1    alex       Übersetzungsarbeiten   100
 2    berta      Übersetzungsarbeiten   100
 3    alex       Gartenarbeiten         100
 4    alex       Reparaturarbeiten      100
 5    christa    Klavierunterricht      100
 6    dora       Reparaturarbeiten      100
 7    eric       Gitarrenunterricht     100
 8    dora       Botengänge             100
                                        **800**
==== ========== ====================== ===========
<BLANKLINE>

>>> rt.show('tickets.Tickets')
==== =========================================================================================== ========= ==================== ================= =========
 ID   Zusammenfassung                                                                             Autor     Fähigkeit            Aktionen          Projekt
---- ------------------------------------------------------------------------------------------- --------- -------------------- ----------------- ---------
 8    Wer fährt für mich nach Aachen Windeln kaufen?                                              alex      Botengänge           **Geschlossen**
 7    Wer kann meine Abschlussarbeit korrekturlesen?                                              eric                           **Bereit**
 6    Wer hilft meinem Sohn sich auf die Mathearbeit am 21.05. vorzubereiten? 5. Schuljahr PDS.   berta     Matheunterricht      **Schläft**
 5    Wer macht Musik auf meinem Geburtstag?                                                      alex      Musik                **Gestartet**
 4    Wer kann meiner Tochter Gitarreunterricht geben?                                            alex      Gitarrenunterricht   **Offen**
 3    Wer kann meinem Sohn Klavierunterricht geben?                                               eric      Klavierunterricht    **Besprechen**
 2    Mein Rasen muss gemäht werden. Donnerstags oder Samstags                                    christa   Gartenarbeiten       **Neu**
 1    Mein Wasserhahn tropft, wer kann mir helfen?                                                berta     Reparaturarbeiten    **Geschlossen**
==== =========================================================================================== ========= ==================== ================= =========
<BLANKLINE>


Das Hauptmenü
=============

>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Stellungnahmen : Meine Angebote, Meine Aufgaben, My votes
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
  - Stellungnahmen : Alle Stellungnahmen, Stellungnahmezustände
  - Büro : Auszüge, Kommentare
  - Bitten : Verknüpfungen, Ticketzustände
  - Fähigkeiten : Kompetenzen
- Site : Info


**Einfache** Benutzer haben ein eingeschränktes Menü:

>>> rt.login('berta').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Stellungnahmen : Meine Angebote, Meine Aufgaben, My votes
- Büro : Meine Kommentare, Meine Benachrichtigungen
- Bitten : Meine Bitten, Wo ich helfen kann
- Site : Info

Bittenlisten
==============


Meine Bitten
------------
  
>>> rt.login('christa').show(tickets.MyTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
+----------------------------------------------------------------------------------+
| overview                                                                         |
+==================================================================================+
| `#2 (Mein Rasen muss gemäht werden. Donnerstags oder Samstags) <Detail>`__ |br|  |
| Bitte state: **Neu** → [☎] [☉] [☐]                                               |
+----------------------------------------------------------------------------------+
<BLANKLINE>


Where I can help
----------------

>>> rt.login('alex').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
+----------------------------------------------------------------------------------------------------------+----------------+-------------+
| overview                                                                                                 | Fähigkeit      | Aktionen    |
+==========================================================================================================+================+=============+
| `#2 (Mein Rasen muss gemäht werden. Donnerstags oder Samstags) <Detail>`__ by `christa <Detail>`__ |br|  | Gartenarbeiten | [☆] **Neu** |
| Bitte state: **Neu**                                                                                     |                |             |
+----------------------------------------------------------------------------------------------------------+----------------+-------------+
<BLANKLINE>

>>> rt.login('berta').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
Keine Daten anzuzeigen

>>> rt.login('eric').show(tickets.SuggestedTickets)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
+-----------------------------------------------------------------------------------------------+--------------------+---------------+
| overview                                                                                      | Fähigkeit          | Aktionen      |
+===============================================================================================+====================+===============+
| `#4 (Wer kann meiner Tochter Gitarreunterricht geben?) <Detail>`__ by `alex <Detail>`__ |br|  | Gitarrenunterricht | [☆] **Offen** |
| Bitte state: **Offen**                                                                        |                    |               |
+-----------------------------------------------------------------------------------------------+--------------------+---------------+
<BLANKLINE>


Meine Hilfsangebote
-------------------

>>> rt.login('christa').show(votes.MyOffers)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
+------------------------------------------------------------------------------------------------------------------+
| Beschreibung                                                                                                     |
+==================================================================================================================+
| `#3 (Wer kann meinem Sohn Klavierunterricht geben?) <Detail>`__ by `eric <Detail>`__ for `dora <Detail>`__ |br|  |
| Bitte state: **Besprechen** |br|                                                                                 |
| Stellungnahme state: **Kandidat** → [Interesse]                                                                  |
+------------------------------------------------------------------------------------------------------------------+
<BLANKLINE>


>>> rt.login('eric').show(votes.MyOffers)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
Keine Daten anzuzeigen



Meine Aufgaben
--------------

>>> rt.login('alex').show(votes.MyTasks)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
Keine Daten anzuzeigen

>>> rt.login('alex').show(votes.MyVotes)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
+--------------------------------------------------------------------------------------------+
| Beschreibung                                                                               |
+============================================================================================+
| `#1 (Mein Wasserhahn tropft, wer kann mir helfen?) <Detail>`__ by `berta <Detail>`__ |br|  |
| Bitte state: **Geschlossen** |br|                                                          |
| Stellungnahme state: **Erledigt**                                                          |
+--------------------------------------------------------------------------------------------+
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
    - **Zuweisbare Arbeiter** (faculties.AssignableWorkersByTicket) [visible for connector admin]
  - (general_2): **Beschreibung** (description), **Kommentare** (CommentsByRFC) [visible for user connector admin]
- **History** (changes.ChangesByMaster) [visible for connector admin]
- **Stellungnahmen** (votes.VotesByVotable) [visible for user connector admin]
- **Mehr** (more) [visible for connector admin]:
  - (more1) [visible for all]:
    - (more1_1): **Erstellt** (created), **Bearbeitet** (modified), **Ticket type** (ticket_type)
    - (more1_2): **Zustand** (state), **Priorität** (priority), **Projekt** (project)
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
