"""
This is a legacy entrypoint to retain ``sardine.cli.main``. The recommended method
to run this module is to use ``python -m sardine.cli`` or ``sardine-config``.
"""
from sardine.cli import *

if __name__ == "__main__":
    main()
