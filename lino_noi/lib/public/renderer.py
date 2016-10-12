# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
from lino.modlib.bootstrap3.renderer import Renderer

from lino_noi.lib.tickets.models import Ticket


class Renderer(Renderer):
    
    def instance_handler(self, ar, obj, **kw):
        return self.get_detail_url(obj, **kw)
            
    def get_detail_url(self, obj, *args, **kw):
        if isinstance(obj, Ticket):
            return self.plugin.build_plain_url(
                'ticket', str(obj.id), *args, **kw)
        # return super(Renderer, self).get_detail_url(self, obj, *args, **kw)


