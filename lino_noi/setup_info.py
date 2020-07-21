# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# $ python setup.py test -s tests.test_packages

SETUP_INFO = dict(
    name='lino-noi',
    version='20.7.0',
    install_requires=['lino-xl'],
    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("The Lino application used by the Lino team for "
                 "managing their work on the Lino project"),
    long_description="""\
.. image:: https://readthedocs.org/projects/lino/badge/?version=latest
    :alt: Documentation Status
    :target: http://lino.readthedocs.io/en/latest/?badge=latest

.. image:: https://coveralls.io/repos/github/lino-framework/noi/badge.svg?branch=master
    :target: https://coveralls.io/github/lino-framework/noi?branch=master

.. image:: https://travis-ci.org/lino-framework/noi.svg?branch=stable
    :target: https://travis-ci.org/lino-framework/noi?branch=stable

.. image:: https://img.shields.io/pypi/v/lino-noi.svg
    :target: https://pypi.python.org/pypi/lino-noi/

.. image:: https://img.shields.io/pypi/l/lino-noi.svg
    :target: https://pypi.python.org/pypi/lino-noi/

Lino Noi is a customizable ticket management and time tracking
system to use when time is more than money.

- The central project homepage is http://noi.lino-framework.org

- Technical documentation, including demo projects, API and tested
  specs see http://www.lino-framework.org/specs/noi

- For *introductions* and *commercial information* about Lino Noi
  please see `www.saffre-rumma.net
  <http://www.saffre-rumma.net/noi/>`__.


""",
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="http://noi.lino-framework.org",
    license='BSD-2-Clause',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
""".splitlines())

SETUP_INFO.update(packages=[str(n) for n in """
lino_noi
lino_noi.lib
lino_noi.lib.noi
lino_noi.lib.noi.fixtures
lino_noi.lib.contacts
lino_noi.lib.contacts.fixtures
lino_noi.lib.public
lino_noi.lib.topics
lino_noi.lib.users
lino_noi.lib.users.fixtures
lino_noi.lib.products
lino_noi.lib.groups
lino_noi.lib.cal
lino_noi.lib.cal.fixtures
lino_noi.lib.courses
lino_noi.lib.tickets
""".splitlines() if n])

SETUP_INFO.update(message_extractors={
    'lino_noi': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(include_package_data=True, zip_safe=False)
# SETUP_INFO.update(package_data=dict())


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l

# l = add_package_data('lino_noi.lib.noi')
# for lng in 'de fr'.split():
#     l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
