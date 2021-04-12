# -*- coding: utf-8 -*-

from lino.sphinxcontrib import configure
configure(globals(), 'lino_book.projects.noi1e.settings.demo')

extensions += ['lino.sphinxcontrib.logo']

extensions += ['lino.sphinxcontrib.help_texts_extractor']
help_texts_builder_targets = {
    'lino_noi.': 'lino_noi.lib.noi'
}

# from atelier.sphinxconf import interproject
# interproject.configure(globals(), 'atelier')

project = "Lino Noi"
html_title = "Lino Noi"
copyright = '2014-2021 Rumma & Ko Ltd'

suppress_warnings = ['image.nonlocal_uri']
blogref_format = "https://luc.lino-framework.org/blog/%Y/%m%d.html"

html_context.update(public_url='https://noi.lino-framework.org')
