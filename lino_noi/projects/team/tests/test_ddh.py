# -*- coding: utf-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Runs some tests about the disable-delete handler and cascading deletes.

You can run only these tests by issuing::

  $ go noi
  $ cd lino_noi/projects/team
  $ python manage.py test tests.test_ddh

Or::

  $ go noi
  $ python setup.py test -s tests.DemoTests.test_std

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt


def create(m, **kwargs):
    obj = m(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class DDHTests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        from lino.modlib.users.choicelists import UserTypes
        Ticket = rt.models.tickets.Ticket
        User = rt.models.users.User
        Star = rt.models.votes.Vote
        # ContentType = rt.modules.contenttypes.ContentType
        # ct_Ticket = ContentType.objects.get_for_model(Ticket)

        robin = create(User, username='robin',
                       first_name="Robin",
                       profile=UserTypes.admin,
                       language="en")

        def createit():
            return create(Ticket, summary="Test", user=robin)

        #
        # If there are no vetos, user can ask to delete it
        #
        obj = createit()
        obj.delete()

        obj = createit()

        if False:
            try:
                robin.delete()
                self.fail("Expected veto")
            except Warning as e:
                self.assertEqual(
                    str(e), "Cannot delete User Robin "
                    "because 1 Tickets refer to it.")

        
        create(Star, votable=obj, user=robin)
        
        try:
            robin.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                str(e), "Cannot delete User Robin "
                "because 1 Tickets refer to it.")

        self.assertEqual(Star.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)

        try:
            obj.delete()
            self.fail("Expected veto")
        except Warning as e:
            self.assertEqual(
                str(e), "Cannot delete Ticket #2 (Test) because "
                "1 Votes refer to it.")
