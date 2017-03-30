"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

SETUP_INFO = {}

# load SETUP_INFO:
fn = ROOTDIR.child('lino_noi', 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))

from lino.utils.pythontest import TestCase

# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = "lino_noi.settings.test"


# class BaseTestCase(TestCase):
#     project_root = ROOTDIR
#     django_settings_module = 'lino_noi.settings.test'


class PackagesTests(TestCase):

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])




