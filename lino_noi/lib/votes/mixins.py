# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for this plugin.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.utils.xmlgen.html import E, lines2p


class Votable(dd.Model):
    """Base class for models that can be used as
    :attr:`lino_noi.lib.votes.Plugin.votable_model`.

    """
    class Meta(object):
        abstract = True

    def get_vote_rater(self, vote):
        """Return the user who is allowed to rate votes on this votable."""
        return None
