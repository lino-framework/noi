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
37 apps: lino_startup, staticfiles, about, jinja, bootstrap3, extjs, printing, system, contenttypes, gfks, users, office, countries, contacts, topics, votes, uploads, outbox, xl, excerpts, comments, notify, changes, noi, tickets, faculties, deploy, clocking, lists, blogs, export_excel, tinymce, smtpd, weasyprint, appypod, wkhtmltopdf, dashboard.
48 models:
=========================== ============================ ========= =======
 Name                        Default table                #fields   #rows
--------------------------- ---------------------------- --------- -------
 blogs.Entry                 blogs.Entries                10        3
 blogs.EntryType             blogs.EntryTypes             6         3
 blogs.Tagging               blogs.Taggings               3         3
 changes.Change              changes.Changes              9         0
 clocking.ServiceReport      clocking.ServiceReports      7         1
 clocking.Session            clocking.Sessions            12        17
 clocking.SessionType        clocking.SessionTypes        4         1
 comments.Comment            comments.Comments            8         3
 contacts.Company            contacts.Companies           22        0
 contacts.CompanyType        contacts.CompanyTypes        7         0
 contacts.Partner            contacts.Partners            19        3
 contacts.Person             contacts.Persons             26        0
 contacts.Role               contacts.Roles               4         0
 contacts.RoleType           contacts.RoleTypes           4         0
 contenttypes.ContentType    gfks.ContentTypes            3         49
 countries.Country           countries.Countries          6         8
 countries.Place             countries.Places             8         78
 dashboard.Widget            dashboard.Widgets            5         0
 deploy.Deployment           deploy.Deployments           4         0
 deploy.Milestone            deploy.Milestones            9         8
 excerpts.Excerpt            excerpts.Excerpts            12        2
 excerpts.ExcerptType        excerpts.ExcerptTypes        17        2
 faculties.Competence        faculties.Competences        6         18
 faculties.Faculty           faculties.Faculties          8         8
 gfks.HelpText               gfks.HelpTexts               4         1
 lists.List                  lists.Lists                  7         8
 lists.ListType              lists.ListTypes              4         3
 lists.Member                lists.Members                5         0
 notify.Message              notify.Messages              10        7
 outbox.Attachment           outbox.Attachments           4         0
 outbox.Mail                 outbox.Mails                 9         0
 outbox.Recipient            outbox.Recipients            6         0
 system.SiteConfig           system.SiteConfigs           5         1
 tickets.Link                tickets.Links                4         1
 tickets.Project             tickets.Projects             17        5
 tickets.ProjectType         tickets.ProjectTypes         4         0
 tickets.Site                tickets.Sites                4         3
 tickets.Ticket              tickets.Tickets              26        116
 tickets.TicketType          tickets.TicketTypes          4         3
 tinymce.TextFieldTemplate   tinymce.TextFieldTemplates   5         2
 topics.Interest             topics.Interests             3         6
 topics.Topic                topics.Topics                9         4
 topics.TopicGroup           topics.TopicGroups           5         0
 uploads.Upload              uploads.Uploads              9         0
 uploads.UploadType          uploads.UploadTypes          8         0
 users.Authority             users.Authorities            3         0
 users.User                  users.Users                  17        7
 votes.Vote                  votes.Votes                  9         96
=========================== ============================ ========= =======
<BLANKLINE>



20160702
========

>>> 'cour'.isdigit()
False
>>> 'ref' in rt.models.topics.Topic.quick_search_fields
True

