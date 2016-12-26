# import os ; print "20161219 %s (pid:%s)" % (__name__, os.getpid())

import datetime

from ..settings import *


class Site(Site):
    """Defines and instantiates a demo version of Lino Care."""

    # default_ui = 'lino_extjs6.extjs6'
    
    the_demo_date = datetime.date(2015, 5, 23)

    languages = "en de fr"

    def unused_setup_plugins(self):
        """Change the default value of certain plugin settings.

        - :attr:`excerpts.responsible_user
          <lino_xl.lib.excerpts.Plugin.responsible_user>` is set to
          ``'jean'`` who is both senior developer and site admin in
          the demo database.

        """
        super(Site, self).setup_plugins()
        if self.is_installed('excerpts'):
            self.plugins.excerpts.configure(responsible_user='robin')

            # print "20161219 a"
SITE = Site(globals())
# print "20161219 b"
DEBUG = True

# the following line should not be active in a checked-in version
# DATABASES['default']['NAME'] = ':memory:'
