# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for :mod:`lino_noi.modlib.users`.

"""

from __future__ import unicode_literals

from lino.api import dd, rt, _

from lino_xl.lib.countries.mixins import AddressLocation
from lino.utils.addressable import Addressable
from lino_xl.lib.contacts.mixins import Contactable

from lino.modlib.users.models import *

from .choicelists import UserStates

import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    # thanks to http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

class VerifyUser(dd.Action):
    """Enter your verification code."""
    label = _("Verify")
    http_method = 'POST'
    select_rows = False
    show_in_bbar = True
    parameters = dict(
        email=models.EmailField(_('e-mail address')),
        verification_code=models.CharField(
            _("Verification code"), max_length=50))
    
    def run_from_ui(self, ar, **kw):
        pv = ar.action_param_values
        qs = rt.models.users.User.objects.exclude(verification_code='')
        try:
            user = qs.get(email=pv.email)
        except Exception:
            msg = _("Invalid email address")
            return ar.error(msg)
        if user.verification_code != pv.verification_code:
            msg = _("Invalid verification code")
            return ar.error(msg)
        user.verification_code = ''
        user.save()
        ar.success(_("User {} is now verified.").format(user))

    

# @python_2_unicode_compatible
class User(User, Contactable, AddressLocation, Addressable):

    """
    .. attribute:: callme_mode

        Whether other users can see my contact data.

    .. attribute:: verification_code

        A random string set for every new user. Used for
        online_registration.

    .. attribute:: user_state

    """

    class Meta(User.Meta):
        app_label = 'users'
        abstract = dd.is_abstract_model(__name__, 'User')

    callme_mode = models.BooleanField(
        _('Others may contact me'), default=True)

    verification_code = models.CharField(max_length=200, blank=True)
    
    user_state = UserStates.field(default=UserStates.as_callable('new'))

    verify_user = VerifyUser()

    def on_create(self, ar):
        self.verification_code = id_generator(12)
        return super(User, self).on_create(ar)
    
    def is_editable_by_all(self):
        return self.user_state == UserStates.new
    
    def get_detail_action(self, ar):
        a = super(User, self).get_detail_action(ar)
        if a is not None:
            return a
        if self.callme_mode:
            return rt.actors.users.OtherUsers.detail_action
        
    @dd.htmlbox(_("About me"))
    def about_me(self, ar):
        return self.remarks
        
    @classmethod
    def get_simple_parameters(cls):
        s = super(User, cls).get_simple_parameters()
        s.add('user_state')
        return s

    # def get_default_table(self, ar):
    #     tbl = super(User, self).get_default_table(ar)
    #     return rt.actors.users.OtherUsers
    
    # def __str__(self):
    #     s = self.get_full_name()
    #     if self.callme_mode:
    #         if self.tel:
    #             s += " ({})".format(self.tel)
    #     return s


dd.update_field('users.User', 'remarks', verbose_name=_("About me"))

