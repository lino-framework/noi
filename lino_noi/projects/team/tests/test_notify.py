# -*- coding: utf-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Runs some tests about the notification framework.

You can run only these tests by issuing::

  $ go noi
  $ cd lino_noi/projects/team
  $ python manage.py test tests.test_notify

Or::

  $ go noi
  $ python setup.py test -s tests.ProjectsTests.test_team

"""

from __future__ import unicode_literals

import datetime

from mock import patch

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware

from lino import AFTER18
from lino.api import rt
from lino.utils.djangotest import TestCase
from lino.utils import i2d
from lino.core import constants

from lino.modlib.users.choicelists import UserTypes

from lino.utils.instantiator import create

from lino.modlib.notify.models import send_pending_emails_daily
from lino.modlib.notify.models import send_pending_emails_often
from lino.modlib.notify.choicelists import MailModes

import contextlib

@contextlib.contextmanager
def capture_stdout():
    import sys
    from cStringIO import StringIO
    oldout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out
        yield out
    finally:
        sys.stdout = oldout
        out = out.getvalue()


class TestCase(TestCase):
    """Miscellaneous tests."""
    maxDiff = None

    def test_01(self):
        self.assertEqual(settings.SETTINGS_MODULE, None)
        self.assertEqual(settings.LOGGING, {})
        self.assertEqual(settings.SERVER_EMAIL, 'root@localhost')
        
    @patch('lino.api.dd.logger')
    # @patch('settings.SITE')
    def test_comment(self, logger):
        """Test what happens when a comment is posted on a ticket with
        watchers.

        """
        ContentType = rt.modules.contenttypes.ContentType
        Comment = rt.models.comments.Comment
        Ticket = rt.modules.tickets.Ticket
        Vote = rt.modules.votes.Vote
        Message = rt.modules.notify.Message
        User = settings.SITE.user_model

        robin = create(User, username='robin', profile=UserTypes.admin)
        aline = create(User, username='aline', email="aline@example.com")
        obj = create(Ticket, summary="Save the world", user=robin)
        create(Vote, votable=obj, user=aline)
        
        self.assertEqual(Message.objects.count(), 0)
        
        url = "/api/comments/CommentsByRFC"
        post_data = dict()
        post_data[constants.URL_PARAM_ACTION_NAME] = 'submit_insert'
        post_data.update(short_text="I don't agree.")
        post_data[constants.URL_PARAM_MASTER_PK] = obj.pk
        ct = ContentType.objects.get_for_model(Ticket)
        post_data[constants.URL_PARAM_MASTER_TYPE] = ct.id
        response = self.client.post(
            url, post_data,
            REMOTE_USER='robin',
            HTTP_ACCEPT_LANGUAGE='en')
        result = self.check_json_result(
            response, 'rows success message close_window')
        self.assertEqual(result['success'], True)
        self.assertEqual(
            result['message'],
            """Comment "Comment #1" has been created.""")

        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.all()[0]
        # self.assertEqual(msg.message_type)
        self.assertEqual(msg.seen, None)
        self.assertEqual(msg.user, aline)
        self.assertEqual(msg.body, """\
robin commented on #1 (Save the world): I don't agree.""")
        
        # manually set created timestamp so we can test on it later.
        now = datetime.datetime(2016, 12, 22, 19, 45, 55)
        if settings.USE_TZ:
            now = make_aware(now)
        msg.created = now
        msg.save()
        
        settings.SERVER_EMAIL = 'root@example.com'
        
        with capture_stdout() as out:
            send_pending_emails_often()
            
        out = out.getvalue().strip()
        # print(out)
        expected = """send email
Sender: root@example.com
To: aline@example.com
Subject: [Django] 1 notifications

<body>
Dear aline,
You have 1 unseen notifications

<div>
<H3>22/12/2016 19:45</H3>
robin commented on #1 (Save the world): I don't agree.
</div>

<body>
"""
        self.assertEquivalent(expected, out)
        
        self.assertEqual(logger.debug.call_count, 1)
        logger.debug.assert_called_with(
            'Send out %s summaries for %d users.',
            MailModes.often, 1)
        # logger.info.assert_called_with(
        #     'Notify %s users about %s', 1, 'Change by robin')
