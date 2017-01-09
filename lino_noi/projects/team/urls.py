# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Adds customized urlpatters when use_restful is True.

"""

from __future__ import unicode_literals
from django.conf.urls import url, include
from lino.api import rt
# from lino_noi.libdjango.contrib.auth.models import User

from lino.core.urls import urlpatterns

from rest_framework import serializers, viewsets, routers

Ticket = rt.models.tickets.Ticket
User = rt.models.users.User

# Serializers define the API representation.
class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'author', 'end_user' ) # , 'state')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name') # , 'state')


# ViewSets define the view behavior.
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'users', UserViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('lino.modlib.restful.urls', namespace='rest_framework'))
]
