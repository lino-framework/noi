# -*- coding: UTF-8 -*-
# Copyright 2014-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""An experimental plugin which provides a customized public vire for
Lino Noi. Not used in reality.

.. autosummary::
   :toctree:

    models
    fixtures.linotickets
    migrate

"""

from lino.api.ad import Plugin


class Plugin(Plugin):

    ui_handle_attr_name = 'noi'

    url_prefix = 'noi'

    needs_plugins = ['lino.modlib.bootstrap3']

    def on_ui_init(self, ui):
        from .renderer import Renderer
        self.renderer = Renderer(self)

    def get_patterns(self):
        from django.conf.urls import url  # , include
        from . import views

        Ticket = self.site.modules.tickets.Ticket
        urlpatterns = [
            url(r'^$',
                views.Index.as_view(),
                name='index'),
            url(r'^ticket/(?P<pk>[0-9]+)/$',
                views.Detail.as_view(model=Ticket)),
            # url('', include('lino.core.urls'))
        ]

        return urlpatterns

    def get_index_view(self):
        from . import views
        return views.Index.as_view()

