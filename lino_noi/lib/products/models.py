# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd

from lino.api import _
from lino_xl.lib.products.models import *

ProductTypes.clear()
add = ProductTypes.add_item
add('100', _("Services"), 'default', table_name="products.Products")
# add('200', _("Furniture"), 'furniture', table_name="products.Products")
# add('300', _("Other"), 'default')


class ProductDetail(ProductDetail):
    # Make the sales_price visible
    main = """
    id cat sales_price vat_class delivery_unit
    name
    description
    """
