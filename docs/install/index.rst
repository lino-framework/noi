.. _noi.install:

Installing Lino Noi
====================

- Install Lino (the framework) as documented in
  :ref:`lino.dev.install`.

- Go to your :xfile:`repositories` directory and download also a copy
  of the *Lino Noi* repository::

    $ cd ~/repositories
    $ git clone https://github.com/lino-framework/noi
    
- Activate a Python environment::

    $ virtualenv env
    $ . env/bin/activate

- Use pip to install Lino Noi as editable package::

    $ pip install -r noi/requirements.txt
    $ pip install -e noi

- Create a local Lino project as explained in :ref:`lino.tutorial.hello`.

- Change your project's :xfile:`settings.py` file so that it looks as
  follows:

  .. literalinclude:: settings.py

