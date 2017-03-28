.. _noi.specs.db:

======================
The database structure
======================

.. To run only this test::

    $ python setup.py test -s tests.SpecsTests.test_db

    doctest init:

    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.doctests')
    >>> from lino.api.doctest import *

This document describes the database structure.

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
42 apps: lino_startup, staticfiles, about, jinja, bootstrap3, extjs, printing, system, contenttypes, gfks, office, xl, countries, contacts, users, cal, extensible, courses, topics, votes, excerpts, comments, changes, noi, tickets, faculties, deploy, clocking, lists, blogs, notify, uploads, export_excel, tinymce, smtpd, weasyprint, appypod, dashboard, rest_framework, restful, django_mailbox, mailbox.
70 models:
================================== ============================ ========= =======
 Name                               Default table                #fields   #rows
---------------------------------- ---------------------------- --------- -------
 blogs.Entry                        blogs.Entries                10        3
 blogs.EntryType                    blogs.EntryTypes             6         3
 blogs.Tagging                      blogs.Taggings               3         3
 cal.Calendar                       cal.Calendars                6         1
 cal.Event                          cal.OneEvent                 23        113
 cal.EventPolicy                    cal.EventPolicies            19        6
 cal.EventType                      cal.EventTypes               17        2
 cal.Guest                          cal.Guests                   6         0
 cal.GuestRole                      cal.GuestRoles               4         0
 cal.Priority                       cal.Priorities               5         4
 cal.RecurrentEvent                 cal.RecurrentEvents          21        15
 cal.RemoteCalendar                 cal.RemoteCalendars          7         0
 cal.Room                           cal.Rooms                    7         0
 cal.Subscription                   cal.Subscriptions            4         0
 cal.Task                           cal.Tasks                    17        0
 changes.Change                     changes.Changes              10        0
 clocking.ServiceReport             clocking.ServiceReports      7         1
 clocking.Session                   clocking.Sessions            13        13
 clocking.SessionType               clocking.SessionTypes        4         1
 comments.Comment                   comments.Comments            9         12
 comments.CommentType               comments.CommentTypes        4         0
 contacts.Company                   contacts.Companies           22        4
 contacts.CompanyType               contacts.CompanyTypes        7         0
 contacts.Partner                   contacts.Partners            19        11
 contacts.Person                    contacts.Persons             26        7
 contacts.Role                      contacts.Roles               4         0
 contacts.RoleType                  contacts.RoleTypes           4         0
 contenttypes.ContentType           gfks.ContentTypes            3         71
 countries.Country                  countries.Countries          6         8
 countries.Place                    countries.Places             8         78
 courses.Course                     courses.Activities           29        0
 courses.Enrolment                  courses.Enrolments           13        0
 courses.Line                       courses.Lines                21        0
 courses.Slot                       courses.Slots                5         0
 courses.Topic                      courses.Topics               4         0
 dashboard.Widget                   dashboard.Widgets            5         0
 deploy.Deployment                  deploy.Deployments           5         87
 deploy.Milestone                   deploy.Milestones            13        8
 django_mailbox.Mailbox             mailbox.Mailboxes            6         1
 django_mailbox.Message             mailbox.Messages             13        5
 django_mailbox.MessageAttachment   mailbox.MessageAttachments   4         1
 excerpts.Excerpt                   excerpts.Excerpts            11        2
 excerpts.ExcerptType               excerpts.ExcerptTypes        17        3
 faculties.Competence               faculties.Offers             7         26
 faculties.Demand                   faculties.Demands            4         193
 faculties.Faculty                  faculties.Skills             9         8
 faculties.SkillType                faculties.SkillTypes         4         0
 gfks.HelpText                      gfks.HelpTexts               4         1
 lists.List                         lists.Lists                  7         8
 lists.ListType                     lists.ListTypes              4         3
 lists.Member                       lists.Members                5         0
 mailbox.MessagePointer             mailbox.MessagePointers      3         0
 notify.Message                     notify.Messages              11        6
 system.SiteConfig                  system.SiteConfigs           9         1
 tickets.Competence                 tickets.Competences          5         12
 tickets.Link                       tickets.Links                4         1
 tickets.Project                    tickets.Projects             18        5
 tickets.ProjectType                tickets.ProjectTypes         4         0
 tickets.Site                       tickets.Sites                4         3
 tickets.Ticket                     tickets.Tickets              25        116
 tickets.TicketType                 tickets.TicketTypes          4         3
 tinymce.TextFieldTemplate          tinymce.TextFieldTemplates   5         2
 topics.Interest                    topics.Interests             3         9
 topics.Topic                       topics.Topics                9         4
 topics.TopicGroup                  topics.TopicGroups           5         0
 uploads.Upload                     uploads.Uploads              9         0
 uploads.UploadType                 uploads.UploadTypes          8         0
 users.Authority                    users.Authorities            3         0
 users.User                         users.Users                  43        6
 votes.Vote                         votes.Votes                  9         191
================================== ============================ ========= =======
<BLANKLINE>



20160702
========

>>> 'cour'.isdigit()
False
>>> 'ref' in rt.models.topics.Topic.quick_search_fields
True

