# Demonstration of the colouredlogs package.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: January 14, 2018
# URL: https://colouredlogs.readthedocs.io

"""A simple demonstration of the `colouredlogs` package."""

# Standard library modules.
import os
import time

# Modules included in our package.
import colouredlogs

# If my verbose logger is installed, we'll use that for the demo.
try:
    from verboselogs import VerboseLogger as getLogger
except ImportError:
    from logging import getLogger

# Initialize a logger for this module.
logger = getLogger(__name__)

DEMO_DELAY = float(os.environ.get('COLOUREDLOGS_DEMO_DELAY', '1'))
"""The number of seconds between each message emitted by :func:`demonstrate_coloured_logging()`."""


def demonstrate_coloured_logging():
    """Interactively demonstrate the :mod:`colouredlogs` package."""
    # Determine the available logging levels and order them by numeric value.
    decorated_levels = []
    defined_levels = colouredlogs.find_defined_levels()
    normalizer = colouredlogs.NameNormalizer()
    for name, level in defined_levels.items():
        if name != 'NOTSET':
            item = (level, normalizer.normalize_name(name))
            if item not in decorated_levels:
                decorated_levels.append(item)
    ordered_levels = sorted(decorated_levels)
    # Initialize coloured output to the terminal, default to the most
    # verbose logging level but enable the user the customize it.
    colouredlogs.install(level=os.environ.get('COLOUREDLOGS_LOG_LEVEL', ordered_levels[0][1]))
    # Print some examples with different timestamps.
    for level, name in ordered_levels:
        log_method = getattr(logger, name, None)
        if log_method:
            log_method("message with level %s (%i)", name, level)
            time.sleep(DEMO_DELAY)