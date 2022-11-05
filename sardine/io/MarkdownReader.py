from rich.markdown import Markdown
from rich.console import Console
import platform
import pathlib
from webbrowser import open as web_open

__all__ = ("open_sardinopedia", "print_sardinopedia")

if platform.system() in ["Linux", "Darwin"]:
    SARDINOPEDIA_PATH = pathlib.Path(__file__).parents[2] / "docs/sardinopedia.md"
else:
    SARDINOPEDIA_PATH = pathlib.Path(__file__).parents[2] / "docs\\sardinopedia.md"


def print_sardinopedia():
    with open(SARDINOPEDIA_PATH, "r") as sardinopedia:
        console = Console()
        console.print(Markdown(sardinopedia.read()))


def open_sardinopedia():
    """Open the Sardinopedia file in external app"""
    web_open("file://" + str(SARDINOPEDIA_PATH))
