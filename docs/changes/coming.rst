.. _noi.coming: 

===============
Lino Noi coming
===============

DONE:

- Don't show the ✋ (assign to me) button on a ticket when it is
  already assigned.

- Hotfix for :ticket:`2624`.

- Don't show closed and sleeping sites in "Sites Overview".

TODO:

- TicketsBySite : the ticket states in the summary (ready, open,
  started, etc) should appear in their constant workflow order.
  Currently they appear in a random order, depending on the sort order
  of the table (i.e. priority, -id).

  But maybe a table (state X priority) would be more useful than the
  current ordered list.

- Add a filter param on Tickets to show only tickets in sites that are
  in an exposed state.

  But there are already so many filter parameters on tickets. Can't
  you just go to the site detail?

- A text field "Post a comment" in the detail of a ticket.
  This would be a virtual field `Commentable.post_comment`, 
  The field would be
  editable and the setter would add a comment with self as owner.

- Have per ticket a list of comments and other tickets that refer to
  this ticket in their text (i.e. the body of a command or the
  :attr:`description` of a ticket.  Wen saving a comment, Lino parses
  the :attr:`body` and searches for memo commands.  But this time the
  purpose is to fill a list of referred objects, not to render
  them.

  :meth:`lino.utils.memo.Parser.register_django_model`

  :attr:`lino.core.kernel.Kernel.memo_parser`

