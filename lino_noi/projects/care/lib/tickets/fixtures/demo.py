# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.api import rt, _
from lino.utils.cycler import Cycler
from lino_noi.lib.tickets.choicelists import TicketStates

from lino.api.dd import str2kw
from lino.api import dd

TICKET_STATES = Cycler(TicketStates.objects())


def user(username, user_type=None, **kw):
    kw.update(username=username, profile=user_type)
    return rt.modules.users.User(**kw)


def faculty(name, fr, en, **kw):
    kw.update(**dd.babelkw('name', de=name, fr=fr, en=en))
    # kw.update(name=name, name_fr=name_fr, name_en=name_en)
    return rt.modules.faculties.Faculty(**kw)


def S(name, **kw):
    kw.update(name=name)
    return rt.modules.tickets.Site(**kw)


def Topic(name, **kw):
    kw.update(**str2kw('name', name))
    return rt.modules.topics.Topic(**kw)


def ticket(user, summary, en, **kw):
    u = rt.models.users.User.objects.get(username=user)
    if en and u.language != 'de':
        summary = en
    kw.update(summary=summary, user=u)
    # if no manual state is specified, take a random one:
    if not 'state' in kw:
        kw.update(state=TICKET_STATES.pop())
    return rt.models.tickets.Ticket(**kw)


def competence(user, faculty, **kw):
    kw.update(
        user=rt.modules.users.User.objects.get(username=user))
    kw.update(faculty=faculty)
    return rt.modules.faculties.Competence(**kw)


def vote(user, ticket, state, **kw):
    u = rt.models.users.User.objects.get(username=user)
    t = rt.models.tickets.Ticket.objects.get(pk=ticket)
    s = rt.models.votes.VoteStates.get_by_name(state)
    return rt.models.votes.Vote(user=u, votable=t, state=s, **kw)



def objects():
    UserTypes = rt.actors.users.UserTypes
    yield user("alex", UserTypes.user)
    yield user("berta", UserTypes.user)
    yield user("christa", UserTypes.user)
    dora = user("dora")
    yield dora
    yield user("eric", UserTypes.connector)

    yield S(_("At home"))  # "Bei mir zu Hause"
    yield S("AZ Ephata")
    yield S("Eupen")

    # TopicGroup = rt.modules.topics.TopicGroup
    # lng = TopicGroup(**str2kw('name', _("Languages")))
    # yield lng
    # fr = Topic(_("French"), topic_group=lng)
    # yield fr
    # de = Topic(_("German"), topic_group=lng)
    # yield de
    # yield Topic(_("English"), topic_group=lng)

    # music = TopicGroup(**str2kw('name', _("Music")))
    # yield music
    # piano = Topic(_("Piano"), topic_group=music)
    # yield piano
    # guitar = Topic(_("Guitar"), topic_group=music)
    # yield guitar

    edu = faculty("Unterricht", "Cours", "Teaching")
    yield edu
    yield faculty(
        "Französischunterricht", "Cours de francais", "French lessons",
        parent=edu)
    yield faculty("Deutschunterricht", "Cours d'allemand",
                  "German lessons", parent=edu)
    math = faculty(
        "Matheunterricht", "Cours de maths", "Maths lessons",
        parent=edu)
    yield math
    
    music = faculty("Musik", "Musique", "Music")
    yield music
    guitar = faculty(
        "Gitarrenunterricht",
        "Cours de guitare", "Guitar lessons", parent=music)
    yield guitar
    piano = faculty(
        "Klavierunterricht",
        "Cours de piano", "Piano lessons", parent=music)
    yield piano

    home = faculty(
        "Haus und Garten", "Maison et jardin", "Home & Garden")
    yield home

    yield faculty(
        "Kleider reparieren", "Réparer des vètements",
        "Repairing clothes", parent=home)
    garden = faculty(
        "Gartenarbeiten", "Travaux de jardin", "Garden works",
        parent=home)
    yield garden
    repair = faculty(
        "Reparaturarbeiten", "Travaux de réparation", "Repair works",
        parent=home)
    yield repair
    renovate = faculty(
        "Renovierung", "Rénovation", "Renovation",
        parent=home)
    yield renovate

    yield faculty("Fahrdienst", "Voiture", "Car driving")
    commissions = faculty("Botengänge", "Commissions", "Shopping")
    yield commissions
    yield faculty("Friseur", "Coiffure", "Hair cutting")
    yield faculty("Babysitting", "Garde enfant", "Babysitting")
    yield faculty("Gesellschafter für Senioren",
                  "Rencontres personnes agées",
                  "Mentoring elderly people")
    yield faculty(
        "Hunde spazierenführen", "Chiens", "Go out with dogs")
    traduire = faculty(
        "Übersetzungsarbeiten",
        "Traductions", "Translations")
    yield traduire
    yield faculty("Briefe schreiben", "Écrire des lettres",
                  "Write letters")

    yield ticket(  #1
        "berta",
        "Mein Wasserhahn tropft, wer kann mir helfen?",
        "My faucet is dripping, who can help?",
        state=TicketStates.closed,
        faculty=repair)
    yield ticket(  #2
        "christa",
        "Mein Rasen muss gemäht werden. Donnerstags oder Samstags",
        "My lawn needs mowing. On Thursday or Saturday."
        "", faculty=garden)
    yield ticket(  #3
        "eric",
        "Wer kann meinem Sohn Klavierunterricht geben?",
        "Who can give piano lessons to my son?",
        faculty=piano, end_user=dora)
    yield ticket(  #4
        "alex",
        "Wer kann meiner Tochter Gitarreunterricht geben?",
        "Who can give guitar lessons to my daughter?",
        faculty=guitar)
    yield ticket(  #5
        "alex",
        "Wer macht Musik auf meinem Geburtstag?",
        "Who would play music on my birthday party?",
        deadline=dd.demo_date(-20),
        faculty=music)
    yield ticket(
        "berta",
        "Wer hilft meinem Sohn sich auf die Mathearbeit am "
        "21.05. vorzubereiten? 5. Schuljahr PDS.",
        "Who helps my sont to prepare for a maths test on May 21?"
        " (5. grade PDS)",
        deadline=dd.demo_date().replace(month=5, day=21),
        faculty=math)
    yield ticket(
        "eric",
        "Wer kann meine Abschlussarbeit korrekturlesen?",
        "Who can review my final work?",
        end_user=dora, 
        deadline=dd.demo_date().replace(month=3, day=12),
        description="Für 5. Jahr RSI zum Thema \"Das "
        "Liebesleben der Kängurus\"  "
        "Muss am 12.03. eingereicht werden.")
    yield ticket(  #8
        "alex",
        "Wer fährt für mich nach Aachen Windeln kaufen?",
        "Who would buy diapers for me in Aachen?",
        description="Ich darf selber nicht über die Grenze.",
        faculty=commissions)

    yield competence('alex', traduire)
    yield competence('berta', traduire)
    # yield competence('berta', traduire, topic=de)
    yield competence('alex', garden)
    yield competence('alex', repair)
    yield competence('christa', piano)
    yield competence('dora', repair)
    yield competence('eric', guitar)
    yield competence('dora', commissions)

    yield vote('alex', 1, 'done')
    yield vote('dora', 1, 'cancelled')
    yield vote('christa', 3, 'candidate')
    
    yield vote('christa', 5, 'candidate')
    yield vote('eric', 5, 'candidate')
    yield vote('dora', 8, 'assigned')
