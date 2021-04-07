# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, _
from lino.utils import join_words

from lino_xl.lib.groups.models import *
from lino.modlib.users.mixins import UserAuthored


class Group(Group, UserAuthored):

    class Meta(Group.Meta):
        app_label = 'groups'
        abstract = dd.is_abstract_model(__name__, 'Group')
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

dd.update_field(Group, 'user', verbose_name=_("Team manager"))

Groups.column_names = 'ref name user *'
Groups.detail_layout = """
ref:10 name:60 user id
description MembershipsByGroup
comments.CommentsByRFC tickets.SitesByGroup
"""
