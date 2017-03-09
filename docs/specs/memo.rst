.. _noi.specs.memo:

=============
Memo commands
=============

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_memo
    
    doctest init:

    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino import startup
    >>> startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *

The :attr:`description
<lino_noi.lib.tickets.models.Ticket.description>` of a ticket and the
text of a comment (:mod:`short_text
<lino.modlib.comments.models.Comment.short_text>`) are rich HTML text
fields which can contain simple HTML formatting like links, tables,
headers, enumerations.

And additionally they can contain :mod:`memo <lino.utils.memo>` markup
commands, i.e. text of the form ``[foo bar baz]``. These memo commands
are going to be "rendered" when this text is being displayed at
certain places.

Examples:

.. _memo.url:

url
===

Insert a link to an external web page. The first argument is the URL
(mandatory). If no other argument is given, the URL is used as
text. Otherwise the remaining text is used as the link text.

The link will always open in a new window (``target="_blank"``)

Usage examples:

- ``[url http://www.example.com]``
- ``[url http://www.example.com example]``
- ``[url http://www.example.com another example]``

..  test:
    >>> ses = rt.login()
    >>> print(ses.parse_memo("See [url http://www.example.com]."))
    See <a href="http://www.example.com" target="_blank">http://www.example.com</a>.
    >>> print(ses.parse_memo("See [url http://www.example.com example]."))
    See <a href="http://www.example.com" target="_blank">example</a>.
    
    >>> print(ses.parse_memo("""See [url https://www.example.com
    ... another example]."""))
    See <a href="https://www.example.com" target="_blank">another example</a>.

    A possible situation is that you forgot the space:
    
    >>> print(ses.parse_memo("See [urlhttp://www.example.com]."))
    See [urlhttp://www.example.com].

    A pitfall is when your editor inserted a non-breaking space:
    
    >>> print(ses.parse_memo("See [url&nbsp;http://www.example.com example]."))
    See <a href="&nbsp;http://www.example.com" target="_blank">example</a>.
    

.. _memo.ticket:

ticket
======

Refer to a ticket. Usage example: 

  See ``[ticket 1]``.

Note that the current renderer decides how to render the link. For
example, the default user interface :mod:`lino.modlib.extjs` (or
:mod:`lino_extjs6.extjs6`, depending on our :attr:`default_ui
<lino.core.site.Site.default_ui>` setting) will render it like this:

>>> ses = rt.login('robin',
...     renderer=settings.SITE.kernel.default_ui.renderer)
>>> print(ses.parse_memo("See [ticket 1]."))
See <a href="javascript:Lino.tickets.Tickets.detail.run(null,{ &quot;record_id&quot;: 1 })" title="F&#246;&#246; fails to bar when baz">#1</a>.

While the :mod:`lino.modlib.bootstrap3` user interface will render it
like this:

>>> ses = rt.login(renderer=dd.plugins.bootstrap3.renderer)
>>> print(ses.parse_memo("See [ticket 1]."))
See <a href="/bs3/tickets/Tickets/1" title="F&#246;&#246; fails to bar when baz">#1</a>.

Or the plain text renderer will render:

>>> ses = rt.login()
>>> print(ses.parse_memo("See [ticket 1]."))
See <a href="Detail" title="F&#246;&#246; fails to bar when baz">#1</a>.


.. _memo.py:

py
==

Refer to a Python object.

Usage examples:

- ``[py lino]``
- ``[py lino.utils.memo]``
- ``[py lino_noi.lib.tickets.models.Project]``
- ``[py lino_noi.lib.tickets.models.Project tickets.Project]``
  
..  
    >>> ses = rt.login()
    >>> print(ses.parse_memo("[py lino]."))
    <a href="https://github.com/lsaffre/lino/blob/master/lino/__init__.py" target="_blank">lino</a>.
    >>> print(ses.parse_memo("[py lino_noi.lib.tickets.models.Project]."))
    <a href="https://github.com/lsaffre/noi/blob/master/lino_noi/lib/tickets/models.py" target="_blank">lino_noi.lib.tickets.models.Project</a>.
    >>> print(ses.parse_memo("[py lino_noi.lib.tickets.models.Project.foo]."))
    <a href="Oops: type object 'Project' has no attribute 'foo'" target="_blank">lino_noi.lib.tickets.models.Project.foo</a>.
    
    >>> print(ses.parse_memo("[py lino_noi.lib.tickets.models.Project Project]."))
    <a href="https://github.com/lsaffre/noi/blob/master/lino_noi/lib/tickets/models.py" target="_blank">Project</a>.

    Non-breaking spaces are removed from command text:
    
    >>> print(ses.parse_memo(u"[py lino]."))
    <a href="https://github.com/lsaffre/lino/blob/master/lino/__init__.py" target="_blank">lino</a>.



>>> ar = rt.login('robin')
>>> obj = rt.models.tickets.Ticket.objects.get(pk=1)
>>> txt = ar.obj2memo(obj)
>>> print(txt)
[ticket 1] (Föö fails to bar when baz)

>>> print(ar.parse_memo(txt))
<a href="Detail" title="F&#246;&#246; fails to bar when baz">#1</a> (Föö fails to bar when baz)

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_memo_commands())
... #doctest: +NORMALIZE_WHITESPACE
<BLANKLINE>
- [ticket ...] :
  Insert a reference to the specified database object.
<BLANKLINE>
  The first argument is mandatory and specifies the
  primary key.
<BLANKLINE>
  If there is more than one argument, all remaining text
  is used as the text of the link.
<BLANKLINE>
    
