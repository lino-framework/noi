.. _noi.coming: 

===============
Lino Noi coming
===============

TODO:

- Remove the online registration feature to fix :ticket:`2624`.

- Don't show the ✋ (assign to me) button on a ticket when it is
  already assigned.

- TicketsBySite : the ticket states in the summary (ready, open,
  started, etc) should appear in the constant workflow order.
  Currently the state with then most urgent ticket appears first.

- Don't show closed and sleeping sites in "Sites Overview".

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

