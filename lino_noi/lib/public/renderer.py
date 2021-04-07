# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
from lino.modlib.bootstrap3.renderer import Renderer

from lino_xl.lib.tickets.models import Ticket


class Renderer(Renderer):
    
    def get_detail_url(self, ar, actor, pk, *args, **kw):
        if issubclass(actor.model, Ticket):
            return self.front_end.build_plain_url(
                'ticket', str(pk), *args, **kw)
        # return super(Renderer, self).get_detail_url(self, obj, *args, **kw)


