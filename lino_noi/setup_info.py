# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Luc Saffre
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-noi',
    version='2017.2.0',
    install_requires=['lino-xl',
                      'channels',
                      'djangorestframework'],
    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("The Lino application used by the Lino team for "
                 "managing their work on the Lino project"),
    long_description="""\
.. image:: https://readthedocs.org/projects/lino/badge/?version=latest
    :alt: Documentation Status
    :target: http://lino.readthedocs.io/en/latest/?badge=latest

.. image:: https://coveralls.io/repos/github/khchine5/noi/badge.svg?branch=master
    :target: https://coveralls.io/github/khchine5/noi?branch=master

.. image:: https://travis-ci.org/khchine5/noi.svg?branch=master
    :target: https://travis-ci.org/khchine5/noi?branch=master

.. image:: https://img.shields.io/pypi/v/lino-noi.svg
    :target: https://pypi.python.org/pypi/lino-noi/

.. image:: https://img.shields.io/pypi/l/lino-noi.svg
    :target: https://pypi.python.org/pypi/lino-noi/

Lino Noi is a customizable ticket management and time tracking
system to use when time is more than money.

- For *introductions* and *commercial information* about Lino Noi
  please see `www.saffre-rumma.net
  <http://www.saffre-rumma.net/noi/>`__.

- The central project homepage is http://noi.lino-framework.org


""",
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="http://noi.lino-framework.org",
    license='BSD License',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_noi',
    'lino_noi.lib',
    'lino_noi.lib.noi',
    'lino_noi.lib.noi.fixtures',
    'lino_noi.lib.contacts',
    'lino_noi.lib.public',
    'lino_noi.lib.users',
    'lino_noi.lib.topics',
    'lino_noi.lib.users.fixtures',
    'lino_noi.lib.cal',
    'lino_noi.lib.cal.fixtures',
    'lino_noi.projects.bs3',
    'lino_noi.projects.bs3.settings',
    'lino_noi.projects.bs3.tests',
    'lino_noi.projects',
    'lino_noi.projects.team',
    'lino_noi.projects.team.tests',
    'lino_noi.projects.team.settings',
    'lino_noi.projects.team.settings.fixtures',
    'lino_noi.projects.team.lib',
    'lino_noi.projects.team.lib.tickets',
    'lino_noi.projects.team.lib.clocking',
    'lino_noi.projects.team.lib.clocking.fixtures',
    'lino_noi.projects.vilma',
    'lino_noi.projects.vilma.settings',
    'lino_noi.projects.public',
    'lino_noi.projects.care',
    'lino_noi.projects.care.settings',
    'lino_noi.projects.care.settings.fixtures',
    'lino_noi.projects.care.tests',
    'lino_noi.projects.care.lib',
    'lino_noi.projects.care.lib.tickets',
    'lino_noi.projects.care_de',
    'lino_noi.projects.public.settings',
    'lino_noi.projects.public.tests',
])

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
