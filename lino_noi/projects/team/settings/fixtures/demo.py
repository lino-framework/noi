# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

import datetime

from lino.api import rt, dd, _
from lino.utils import Cycler, i2d

from lino.core.roles import SiteAdmin
from lino_xl.lib.cal.choicelists import DurationUnits
from lino_noi.lib.clocking.roles import Worker
from lino.utils.quantities import Duration

from lino_noi.lib.users.models import create_user

from lino_noi.lib.clocking.choicelists import ReportingTypes

def vote(user, ticket, state, **kw):
    u = rt.models.users.User.objects.get(username=user)
    t = rt.models.tickets.Ticket.objects.get(pk=ticket)
    s = rt.models.votes.VoteStates.get_by_name(state)
    vote = t.get_favourite(u)
    if vote is None:
        vote = rt.models.votes.Vote(user=u, votable=t, state=s, **kw)
    else:
        vote.state = s
    return vote

def objects():
    yield tickets_objects()
    yield clockings_objects()
    yield faculties_objects()
    yield votes_objects()


def tickets_objects():
    # was previously in tickets
    User = rt.models.users.User
    Company = rt.models.contacts.Company
    Topic = rt.models.topics.Topic
    TT = rt.models.tickets.TicketType
    Ticket = rt.models.tickets.Ticket
    Competence = rt.models.tickets.Competence
    Interest = rt.models.topics.Interest
    Milestone = rt.models.deploy.Milestone
    Project = rt.models.tickets.Project
    Site = rt.models.tickets.Site
    Link = rt.models.tickets.Link
    LinkTypes = rt.models.tickets.LinkTypes
    EntryType = rt.models.blogs.EntryType
    Entry = rt.models.blogs.Entry
    Tagging = rt.models.blogs.Tagging

    cons = rt.models.users.UserTypes.consultant
    dev = rt.models.users.UserTypes.developer
    yield create_user("marc")
    yield create_user("mathieu", cons)
    yield create_user("luc", dev)
    yield create_user("jean", rt.models.users.UserTypes.senior)

    USERS = Cycler(User.objects.all())
    WORKERS = Cycler(User.objects.filter(
        username__in='mathieu luc jean'.split()))
    END_USERS = Cycler(User.objects.filter(profile=''))

    yield TT(**dd.str2kw('name', _("Bugfix")))
    yield TT(**dd.str2kw('name', _("Enhancement")))
    yield TT(**dd.str2kw('name', _("Upgrade")))

    TYPES = Cycler(TT.objects.all())

    yield Topic(name="Lino Core", ref="linõ")
    yield Topic(name="Lino Welfare", ref="welfäre")
    yield Topic(name="Lino Cosi", ref="così")
    yield Topic(name="Lino Voga", ref="faggio")
    # ref differs from name

    TOPICS = Cycler(Topic.objects.all())

    for name in "welket welsch pypi".split():

        obj = Company(name=name)
        yield obj
        yield Site(name=name, partner=obj)

    COMPANIES = Cycler(Company.objects.all())
    
    yield Company(name="Saffre-Rumma")
    
    for u in Company.objects.exclude(name="pypi"):
        for i in range(3):
            yield Interest(partner=u, topic=TOPICS.pop())

    SITES = Cycler(Site.objects.exclude(name="pypi"))
    for i in range(7):
        d = dd.today(i*2-20)
        yield Milestone(site=SITES.pop(), expected=d, reached=d)
    yield Milestone(site=SITES.pop(), expected=dd.today())

    RTYPES = Cycler(ReportingTypes.objects())
    
    prj1 = Project(
        name="Framewörk", ref="linö", private=False,
        company=COMPANIES.pop(),
        reporting_type=RTYPES.pop(),
        start_date=i2d(20090101))
    yield prj1
    yield Project(
        name="Téam", ref="téam", start_date=i2d(20100101),
        reporting_type=RTYPES.pop(),
        company=COMPANIES.pop(),
        parent=prj1, private=True)
    prj2 = Project(
        name="Documentatión", ref="docs", private=False,
        reporting_type=RTYPES.pop(),
        company=COMPANIES.pop(),
        start_date=i2d(20090101), parent=prj1)
    yield prj2
    yield Project(
        name="Research", ref="research", private=False,
        company=COMPANIES.pop(),
        start_date=i2d(19980101), parent=prj2)
    yield Project(
        name="Shop", ref="shop", private=False,
        reporting_type=RTYPES.pop(),
        company=COMPANIES.pop(),
        start_date=i2d(20120201), end_date=i2d(20120630))

    PROJECTS = Cycler(Project.objects.all())

    for u in User.objects.all():
        yield Competence(user=u, project=PROJECTS.pop())
        yield Competence(user=u, project=PROJECTS.pop())
    
    SITES = Cycler(Site.objects.all())
    
    TicketStates = rt.models.tickets.TicketStates
    TSTATES = Cycler(TicketStates.objects())
    
    Vote = rt.models.votes.Vote
    VoteStates = rt.models.votes.VoteStates
    VSTATES = Cycler(VoteStates.objects())

    num = [0]
    
    def ticket(summary, **kwargs):
        num[0] += 1
        u = WORKERS.pop()
        kwargs.update(
            ticket_type=TYPES.pop(), summary=summary,
            user=u,
            state=TSTATES.pop(),
            topic=TOPICS.pop())
        if num[0] % 2:
            kwargs.update(site=SITES.pop())
        if num[0] % 4:
            kwargs.update(private=True)
        if num[0] % 5:
            kwargs.update(end_user=END_USERS.pop())
        if False:
            kwargs.update(project=PROJECTS.pop())
        obj = Ticket(**kwargs)
        yield obj
        if obj.state.active:
            yield Vote(
                votable=obj, user=WORKERS.pop(), state=VSTATES.pop())

    yield ticket(
        "Föö fails to bar when baz", project=PROJECTS.pop())
    yield ticket("Bar is not always baz", project=PROJECTS.pop())
    yield ticket("Baz sucks")
    yield ticket("Foo and bar don't baz", project=PROJECTS.pop())
    # a ticket without project:
    yield ticket("Cannot create Foo", description="""<p>When I try to create
    a <b>Foo</b>, then I get a <b>Bar</b> instead of a Foo.</p>""")

    yield ticket("Sell bar in baz", project=PROJECTS.pop())
    yield ticket("No Foo after deleting Bar", project=PROJECTS.pop())
    yield ticket("Is there any Bar in Foo?", project=PROJECTS.pop())
    yield ticket("Foo never matches Bar", project=PROJECTS.pop())
    yield ticket("Where can I find a Foo when bazing Bazes?",
                 project=PROJECTS.pop())
    yield ticket("Class-based Foos and Bars?", project=PROJECTS.pop())
    yield ticket("Foo cannot bar", project=PROJECTS.pop())

    # Example of memo markup:
    yield ticket("Bar cannot foo", project=PROJECTS.pop(),
                 description="""<p>Linking to [ticket 1] and to
                 [url http://luc.lino-framework.org/blog/2015/0923.html blog].</p>
                 """)
 
    yield ticket("Bar cannot baz", project=PROJECTS.pop())
    yield ticket("Bars have no foo", project=PROJECTS.pop())
    yield ticket("How to get bar from foo", project=PROJECTS.pop())

    n = Ticket.objects.count()

    for i in range(100):
        yield ticket("Ticket {}".format(i+n+1), project=PROJECTS.pop())

    for t in Ticket.objects.all():
        t.set_author_votes()
    
    yield Link(
        type=LinkTypes.requires,
        parent=Ticket.objects.get(pk=1),
        child=Ticket.objects.get(pk=2))

    yield EntryType(**dd.str2kw('name', _('Release note')))
    yield EntryType(**dd.str2kw('name', _('Feature')))
    yield EntryType(**dd.str2kw('name', _('Upgrade instruction')))
    
    ETYPES = Cycler(EntryType.objects.all())
    TIMES = Cycler('12:34', '8:30', '3:45', '6:02')
    blogger = USERS.pop()
    
    def entry(offset, title, body, **kwargs):
        kwargs['user'] = blogger
        kwargs['entry_type'] = ETYPES.pop()
        kwargs['pub_date'] = dd.today(offset)
        kwargs['pub_time'] = TIMES.pop()
        return Entry(title=title, body=body, **kwargs)
    
    yield entry(-3, "Hello, world!", "This is our first blog entry.")
    e = entry(-2, "Hello again", "Our second blog entry is about [ticket 1]")
    yield e
    yield Tagging(entry=e, topic=TOPICS.pop())
    
    e = entry(-1, "Our third entry", """\
    Yet another blog entry about [ticket 1] and [ticket 2].
    This entry has two taggings""")
    yield e
    yield Tagging(entry=e, topic=TOPICS.pop())
    yield Tagging(entry=e, topic=TOPICS.pop())

def clockings_objects():
    # was previously in clockings
    Company = rt.models.contacts.Company
    Vote = rt.models.votes.Vote
    SessionType = rt.models.clocking.SessionType
    Session = rt.models.clocking.Session
    Ticket = rt.models.tickets.Ticket
    User = rt.models.users.User
    UserTypes = rt.models.users.UserTypes
    # devs = (UserTypes.developer, UserTypes.senior)
    devs = [p for p in UserTypes.items()
            if p.has_required_roles([Worker])
            and not p.has_required_roles([SiteAdmin])]
    workers = User.objects.filter(profile__in=devs)
    # WORKERS = Cycler(workers)
    TYPES = Cycler(SessionType.objects.all())
    # TICKETS = Cycler(Ticket.objects.all())
    DURATIONS = Cycler([12, 138, 90, 10, 122, 209, 37, 62, 179, 233, 5])

    # every fourth ticket is unassigned and thus listed in
    # PublicTickets
    # for i, t in enumerate(Ticket.objects.exclude(private=True)):
    # for i, t in enumerate(Ticket.objects.all()):
    #     if i % 4:
    #         t.assigned_to = WORKERS.pop()
    #         yield t

    for u in workers:

        VOTES = Cycler(Vote.objects.filter(user=u))
        # TICKETS = Cycler(Ticket.objects.filter(assigned_to=u))
        if len(VOTES) == 0:
            continue

        for offset in (0, -1, -3, -4):

            date = dd.demo_date(offset)
            worked = Duration()
            ts = datetime.datetime.combine(date, datetime.time(9, 0, 0))
            for i in range(7):
                obj = Session(
                    ticket=VOTES.pop().votable,
                    session_type=TYPES.pop(), user=u)
                obj.set_datetime('start', ts)
                d = DURATIONS.pop()
                worked += d
                if offset < 0:
                    ts = DurationUnits.minutes.add_duration(ts, d)
                    obj.set_datetime('end', ts)
                yield obj
                if offset == 0 or worked > 8:
                    break

    ServiceReport = rt.models.clocking.ServiceReport
    welket = Company.objects.get(name="welket")
    yield ServiceReport(
        start_date=dd.today(-90), interesting_for=welket)


def faculties_objects():
    "was previously in faculties.fixtures.demo2"

    Faculty = rt.models.faculties.Faculty
    Competence = rt.models.faculties.Competence
    User = rt.models.users.User

    yield Faculty(**dd.str2kw('name', 'Analysis'))
    yield Faculty(**dd.str2kw('name', 'Code changes'))
    yield Faculty(**dd.str2kw('name', 'Documentation'))
    yield Faculty(**dd.str2kw('name', 'Testing'))
    yield Faculty(**dd.str2kw('name', 'Configuration'))
    yield Faculty(**dd.str2kw('name', 'Enhancement'))
    yield Faculty(**dd.str2kw('name', 'Optimization'))
    yield Faculty(**dd.str2kw('name', 'Offer'))

    Analysis = Faculty.objects.get(name="Analysis")
    Code_changes = Faculty.objects.get(name="Code changes")
    Documentation = Faculty.objects.get(name="Documentation")
    Testing = Faculty.objects.get(name="Testing")
    Configuration = Faculty.objects.get(name="Configuration")

    mathieu = User.objects.get(username="mathieu")
    Robin = User.objects.get(first_name="Robin")
    luc = User.objects.get(username="luc")

    if dd.get_language_info('de'):
        Rolf = User.objects.get(first_name="Rolf")
        yield Competence(faculty=Analysis, user=Rolf)
        yield Competence(faculty=Code_changes, user=Rolf, affinity=70)
        yield Competence(faculty=Documentation, user=Rolf, affinity=71)
        yield Competence(faculty=Testing, user=Rolf, affinity=42)
        yield Competence(faculty=Configuration, user=Rolf, affinity=62)

    if dd.get_language_info('fr'):
        Romain = User.objects.get(first_name="Romain")
        yield Competence(faculty=Code_changes, user=Romain, affinity=76)
        yield Competence(faculty=Documentation, user=Romain, affinity=92)
        yield Competence(faculty=Testing, user=Romain, affinity=98)
        yield Competence(faculty=Configuration, user=Romain, affinity=68)

    yield Competence(faculty=Analysis, user=Robin, affinity=23)
    yield Competence(faculty=Analysis, user=luc, affinity=120)

    yield Competence(faculty=Code_changes, user=luc, affinity=150)

    yield Competence(faculty=Documentation, user=luc, affinity=75)
    yield Competence(faculty=Documentation, user=mathieu, affinity=46)

    yield Competence(faculty=Testing, user=Robin, affinity=65)
    yield Competence(faculty=Testing, user=mathieu, affinity=42)

    yield Competence(faculty=Configuration, user=luc, affinity=46)
    yield Competence(faculty=Configuration, user=mathieu, affinity=92)

    Bar_cannot_foo = rt.models.tickets.Ticket.objects.get(summary='Bar cannot foo')
    Bar_cannot_foo.faculty = Documentation
    Bar_cannot_foo.save()

    Sell_bar_in_baz = rt.models.tickets.Ticket.objects.get(summary='Sell bar in baz')
    Sell_bar_in_baz.faculty = Analysis
    Sell_bar_in_baz.save()

    Foo_cannot_bar = rt.models.tickets.Ticket.objects.get(summary='Foo cannot bar')
    Foo_cannot_bar.faculty = Code_changes
    Foo_cannot_bar.save()

    Foo_never_matches_Bar = rt.models.tickets.Ticket.objects.get(summary='Foo never matches Bar')
    Foo_never_matches_Bar.faculty = Testing
    Foo_never_matches_Bar.save()

def votes_objects():

    yield vote('mathieu', 1, 'candidate')
    yield vote('luc', 1, 'candidate')
    yield vote('jean', 2, 'assigned')
