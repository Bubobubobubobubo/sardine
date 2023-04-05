import asyncio

import rich

from .loop import *
from .mixin import *
from .policy import *
from .sansio import *
from sardine.logger import logging, print

__all__ = ("install_policy", "new_event_loop")


def _install_precision_proactor() -> bool:
    if PrecisionProactorEventLoop is None:
        logging.error("[yellow]Skipping precision event loop on non-Windows system")
        return False

    asyncio.set_event_loop_policy(PrecisionProactorEventLoopPolicy())
    message = "[yellow]Installed precision proactor event loop"
    print(message)
    logging.debug(message)
    return True


def _install_precision_sansio() -> bool:
    asyncio.set_event_loop_policy(PrecisionSansIOEventLoopPolicy())
    
    logging.error("[yellow]installed precision Sans I/O event loop")
    logging.warning("[bold red]WARNING: event loop does not networking/subprocesses")
    return True


def _install_precision_selector() -> bool:
    asyncio.set_event_loop_policy(PrecisionSelectorEventLoopPolicy())
    logging.error("[yellow]Installed precision selector event loop")
    return True


def _install_uvloop() -> bool:
    try:
        import uvloop
    except ImportError:
        # Commenting this line: it scares new users!
        # rich.print("[green]uvloop[/green] [yellow]is not installed")
        return False

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    message = "[yellow]Installed uvloop event loop"
    logging.debug(message)
    print(message)
    return True


def install_policy():
    """Installs the best-available event loop policy into asyncio.

    This method must be called before any event loop is created, otherwise
    it will not affect those event loops.
    """
    methods = (
        # _install_precision_sansio,
        _install_uvloop,
        # _install_precision_proactor,
        # _install_precision_selector,
    )
    successful = False
    for func in methods:
        successful = func()
        if successful:
            break

    if not successful:
        logging.warning(
            "[yellow]Warning: No custom event loop applied; rhythm accuracy may be impacted."
            "[yellow]Windows users, ignore this warning!"
        )


def new_event_loop() -> asyncio.BaseEventLoop:
    """Creates the best-available event loop without permanently installing
    a new policy for asyncio.
    """
    last_policy = asyncio.get_event_loop_policy()
    install_policy()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop_policy(last_policy)
    return loop
