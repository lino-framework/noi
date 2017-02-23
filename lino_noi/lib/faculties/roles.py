# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""User roles for this plugin.

"""

from lino.core.roles import SiteUser


class SkillsUser(SiteUser):
    pass

class SkillsStaff(SkillsUser):
    pass
