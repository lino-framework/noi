# -*- coding: UTF-8 -*-
# Copyright 2015-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Desktop UI for this plugin.

"""

from lino.modlib.users.desktop import *

from lino.api import _

from lino.core import actions
# from lino.modlib.office.roles import OfficeUser
from lino_noi.lib.clocking.roles import Worker
from .choicelists import UserStates

from lino.modlib.users.actions import SendWelcomeMail
#from .models import VerifyUser

class UserDetail(UserDetail):
    """Layout of User Detail in Lino Noi."""

    main = "general contact dashboard.WidgetsByUser"

    general = dd.Panel("""
    box1:45 clocking:15
    topics.InterestsByPartner faculties.CompetencesByUser
    """, label=_("General"))

    if dd.is_installed('clocking'):
        clocking = dd.Panel("""
        open_session_on_new_ticket
        timezone
        """, label=_("Clocking"), required_roles=dd.required(Worker))
    else:
        clocking = dd.DummyPanel()

    # tickets = dd.Panel("""
    # tickets.TicketsByReporter 
    # """, label=_("Tickets"))

    box1 = """
    username profile:20 partner user_site
    language id created modified
    callme_mode mail_mode
    """

    # cal_left = """
    # event_type access_class
    # cal.SubscriptionsByUser
    # """

    # cal = dd.Panel("""
    # cal_left:30 cal.TasksByUser:60
    # """, label=dd.plugins.cal.verbose_name,
    #                required_roles=dd.login_required(OfficeUser))

    contact = dd.Panel("""
    address_box info_box
    remarks:40 users.AuthoritiesGiven:20
    """, label=_("Contact"))

    info_box = """
    email:40
    # url
    phone
    gsm
    """
    address_box = """
    first_name last_name #initials
    country region city zip_code:10
    #addr1
    #street_prefix street:25 street_no #street_box
    # addr2
    """


Users.detail_layout = UserDetail()
Users.parameters.update(user_state=UserStates.field(blank=True))
# Users.simple_parameters = ['profile', 'user_state']
# Users.workflow_state_field = 'user_state'

class OtherUsers(Users):
    hide_top_toolbar = True
    use_as_default_table = False
    editable = False
    required_roles = dd.required()
    detail_layout = dd.DetailLayout("""
    first_name last_name city user_site
    phone gsm
    about_me
    """, window_size=(60, 15))

# def site_setup(site):
#     site.modules.users.Users.set_detail_layout(UserDetail())


class RegisterUserLayout(dd.InsertLayout):

    window_size = (60, 'auto')

    main = """
    first_name last_name
    email language
    gsm phone
    country city 
    street street_no
    username
    """


class RegisterUser(actions.InsertRow):
    """Fill a form in order to register as a new system user.

    """
    
    def get_action_title(self, ar):
        return _("Register new user")


class Register(Users):
    use_as_default_table = False
    insert_layout = RegisterUserLayout()
    # default_list_action_name = 'insert'
    required_roles = set([])
    
    @classmethod
    def get_insert_action(cls):
        return RegisterUser()


class NewUsers(Users):
    """List of new users to be confirmed by the system admin.

    Confirming a new user basically means to manually set the user
    type.

    """
    label = _("New user applications")
    welcome_message_when_count = 0
    required_roles = dd.required(SiteAdmin)
    use_as_default_table = False
    column_names = 'created first_name last_name username profile workflow_buttons *'
    order_by = ['created']

    send_welcome_email = SendWelcomeMail()

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(NewUsers, self).param_defaults(ar, **kw)
        # kw.update(show_closed=dd.YesNo.no)
        kw.update(user_state=UserStates.new)
        return kw



