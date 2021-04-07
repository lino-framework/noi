# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# $ python setup.py test -s tests.test_packages

SETUP_INFO = dict(
    name='lino-noi',
    version='21.2.0',
    install_requires=['lino-xl'],
    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("The Lino application used by the Lino team for "
                 "managing their work on the Lino project"),
    long_description="""\

Lino Noi is a customizable ticket management and time tracking
system to use when time is more than money.

- The central project homepage is http://noi.lino-framework.org

- Technical specs are at https://www.lino-framework.org/specs/noi

- This is an integral part of the Lino framework, which is documented
  at https://www.lino-framework.org

- The changelog is at https://www.lino-framework.org/changes

- For introductions, commercial information and hosting solutions
  see https://www.saffre-rumma.net

- This is a sustainably free open-source project. Your contributions are
  welcome.  See https://community.lino-framework.org for details.


""",
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="https://github.com/lino-framework/noi",
    license_files=['COPYING'],
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
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
