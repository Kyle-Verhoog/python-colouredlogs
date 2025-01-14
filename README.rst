colouredlogs: Coloured terminal output for Python's logging module
==================================================================

NOTE: This is a parody of the great `python-colouredlogs`_ project
by Peter Odding. Please use that package as I currently have no
plans to maintain this one. All I've done is `s/color/colour/g`.

.. _`python-colouredlogs`: https://github.com/xolox/python-coloredlogs

The `colouredlogs` package enables coloured terminal output for Python's logging_
module. The ColouredFormatter_ class inherits from `logging.Formatter`_ and uses
`ANSI escape sequences`_ to render your logging messages in colour. It uses only
standard colours so it should work on any UNIX terminal. It's currently tested
on Python 2.6, 2.7, 3.4, 3.5, 3.6 and PyPy. On Windows `colouredlogs`
automatically pulls in Colourama_ as a dependency and enables ANSI escape
sequence translation using Colourama. Here is a screen shot of the demo that is
printed when the command ``colouredlogs --demo`` is executed:


.. image:: https://colouredlogs.readthedocs.io/en/latest/_images/defaults.png

Note that the screenshot above includes custom logging levels defined by my
verboselogs_ package: if you install both `colouredlogs` and `verboselogs` it
will Just Work (`verboselogs` is of course not required to use
`colouredlogs`).

.. contents::
   :local:

Installation
------------

The `colouredlogs` package is available on PyPI_ which means installation should
be as simple as:

.. code-block:: sh

   $ pip install colouredlogs

There's actually a multitude of ways to install Python packages (e.g. the `per
user site-packages directory`_, `virtual environments`_ or just installing
system wide) and I have no intention of getting into that discussion here, so
if this intimidates you then read up on your options before returning to these
instructions ;-).

Usage
-----

Here's an example of how easy it is to get started:

.. code-block:: python

   import colouredlogs, logging

   # Create a logger object.
   logger = logging.getLogger(__name__)

   # By default the install() function installs a handler on the root logger,
   # this means that log messages from your code and log messages from the
   # libraries that you use will all show up on the terminal.
   colouredlogs.install(level='DEBUG')

   # If you don't want to see log messages from libraries, you can pass a
   # specific logger object to the install() function. In this case only log
   # messages originating from that logger will show up on the terminal.
   colouredlogs.install(level='DEBUG', logger=logger)

   # Some examples.
   logger.debug("this is a debugging message")
   logger.info("this is an informational message")
   logger.warning("this is a warning message")
   logger.error("this is an error message")
   logger.critical("this is a critical message")

Format of log messages
----------------------

The ColouredFormatter_ class supports user defined log formats so you can use
any log format you like. The default log format is as follows::

 %(asctime)s %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s

This log format results in the following output::

 2015-10-23 03:32:22 peter-macbook colouredlogs.demo[30462] DEBUG message with level 'debug'
 2015-10-23 03:32:23 peter-macbook colouredlogs.demo[30462] VERBOSE message with level 'verbose'
 2015-10-23 03:32:24 peter-macbook colouredlogs.demo[30462] INFO message with level 'info'
 ...

You can customize the log format and styling using environment variables as
well as programmatically, please refer to the `online documentation`_ for
details.

Enabling millisecond precision
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're switching from `logging.basicConfig()`_ to `colouredlogs.install()`_
you may notice that timestamps no longer include milliseconds. This is because
colouredlogs doesn't output milliseconds in timestamps unless you explicitly
tell it to. There are three ways to do that:

1. The easy way is to pass the `milliseconds` argument to `colouredlogs.install()`_::

    colouredlogs.install(milliseconds=True)

   This became supported in `release 7.1`_ (due to `#16`_).

2. Alternatively you can change the log format `to include 'msecs'`_::

    %(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s

   Here's what the call to `colouredlogs.install()`_ would then look like::

    colouredlogs.install(fmt='%(asctime)s,%(msecs)03d %(hostname)s %(name)s[%(process)d] %(levelname)s %(message)s')

   Customizing the log format also enables you to change the delimiter that
   separates seconds from milliseconds (the comma above). This became possible
   in `release 3.0`_ which added support for user defined log formats.

3. If the use of ``%(msecs)d`` isn't flexible enough you can instead add ``%f``
   to the date/time format, it will be replaced by the value of ``%(msecs)03d``.
   Support for the ``%f`` directive was added to `release 9.3`_ (due to `#45`_).

Changing text styles and colours
--------------------------------

The online documentation contains `an example of customizing the text styles and
colours <https://colouredlogs.readthedocs.io/en/latest/#changing-the-colours-styles>`_.

Coloured output from cron
-------------------------

When `colouredlogs` is used in a cron_ job, the output that's e-mailed to you by
cron won't contain any ANSI escape sequences because `colouredlogs` realizes
that it's not attached to an interactive terminal. If you'd like to have colours
e-mailed to you by cron there are two ways to make it happen:

.. contents::
   :local:

Modifying your crontab
~~~~~~~~~~~~~~~~~~~~~~

Here's an example of a minimal crontab::

    MAILTO="your-email-address@here"
    CONTENT_TYPE="text/html"
    * * * * * root colouredlogs --to-html your-command

The ``colouredlogs`` program is installed when you install the `colouredlogs`
Python package. When you execute ``colouredlogs --to-html your-command`` it runs
``your-command`` under the external program ``script`` (you need to have this
installed). This makes ``your-command`` think that it's attached to an
interactive terminal which means it will output ANSI escape sequences which
will then be converted to HTML by the ``colouredlogs`` program. Yes, this is a
bit convoluted, but it works great :-)

Modifying your Python code
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ColouredCronMailer_ class provides a context manager that automatically
enables HTML output when the ``$CONTENT_TYPE`` variable has been correctly set
in the crontab.

This requires my capturer_ package which you can install using ``pip install
'colouredlogs[cron]'``. The ``[cron]`` extra will pull in capturer_ 2.4 or newer
which is required to capture the output while silencing it - otherwise you'd
get duplicate output in the emails sent by ``cron``.

The context manager can also be used to retroactively silence output that has
already been produced, this can be useful to avoid spammy cron jobs that have
nothing useful to do but still email their output to the system administrator
every few minutes :-).

Contact
-------

The latest version of `colouredlogs` is available on PyPI_ and GitHub_. The
`online documentation`_ is available on Read The Docs and includes a
changelog_. For bug reports please create an issue on GitHub_. If you have
questions, suggestions, etc. feel free to send me an e-mail at
`peter@peterodding.com`_.

License
-------

This software is licensed under the `MIT license`_.

© 2018 Peter Odding.


.. External references:
.. _#16: https://github.com/xolox/python-coloredlogs/issues/16
.. _#45: https://github.com/xolox/python-coloredlogs/issues/45
.. _ANSI escape sequences: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
.. _capturer: https://pypi.python.org/pypi/capturer
.. _changelog: https://colouredlogs.readthedocs.org/en/latest/changelog.html
.. _Colourama: https://pypi.python.org/pypi/colorama
.. _ColouredCronMailer: https://colouredlogs.readthedocs.io/en/latest/api.html#colouredlogs.converter.ColouredCronMailer
.. _ColouredFormatter: https://colouredlogs.readthedocs.io/en/latest/api.html#colouredlogs.ColouredFormatter
.. _colouredlogs.install(): https://colouredlogs.readthedocs.io/en/latest/api.html#colouredlogs.install
.. _cron: https://en.wikipedia.org/wiki/Cron
.. _GitHub: https://github.com/kyle-verhoog/python-colouredlogs
.. _logging.basicConfig(): https://docs.python.org/2/library/logging.html#logging.basicConfig
.. _logging.Formatter: https://docs.python.org/2/library/logging.html#logging.Formatter
.. _logging: https://docs.python.org/2/library/logging.html
.. _MIT license: https://en.wikipedia.org/wiki/MIT_License
.. _online documentation: https://colouredlogs.readthedocs.io/
.. _per user site-packages directory: https://www.python.org/dev/peps/pep-0370/
.. _peter@peterodding.com: peter@peterodding.com
.. _PyPI: https://pypi.python.org/pypi/colouredlogs
.. _release 3.0: https://colouredlogs.readthedocs.io/en/latest/changelog.html#release-3-0-2015-10-23
.. _release 7.1: https://colouredlogs.readthedocs.io/en/latest/changelog.html#release-7-1-2017-07-15
.. _release 9.3: https://colouredlogs.readthedocs.io/en/latest/changelog.html#release-9-3-2018-04-29
.. _to include 'msecs': https://stackoverflow.com/questions/6290739/python-logging-use-milliseconds-in-time-format
.. _verboselogs: https://pypi.python.org/pypi/verboselogs
.. _virtual environments: http://docs.python-guide.org/en/latest/dev/virtualenvs/
