from fishery.console import ConsoleManager
import click

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}


@click.group(
    context_settings=CONTEXT_SETTINGS,
    help="Starts sardine in an asyncio REPL.",
    invoke_without_command=True,
)
@click.version_option(
    package_name="sardine",
    prog_name=__package__,
    message="%(prog)s for %(package)s v%(version)s",
)
@click.pass_context
def main(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        console = ConsoleManager()
        console.start()


# fishery web
# fishery web --host
# fishery web --port
# fishery web --host --port
@main.command(
    short_help="Starts sardine as a web server.",
    help="""
        This command starts sardine as a web server. The server can be accessed
        at http://localhost:8000 by default.
        """,
)
@click.option(
    "-h",
    "--host",
    default="localhost",
    help="The host to bind the server to.",
    show_default=True,
    type=str,
)
@click.option(
    "-p",
    "--port",
    default=8000,
    help="The port to bind the server to.",
    show_default=True,
    type=int,
)
@click.option(
    "--no-browser",
    is_flag=True,
    help="Prevents the server from opening a browser window.",
)
def web(host: str, port: int, no_browser: bool):
    from .server import WebServer

    consoleManager = ConsoleManager()
    server = WebServer(host=host, port=port)
    server.start_in_thread(consoleManager.console)
    if not no_browser:
        server.open_in_browser()
    consoleManager.start()


if __name__ == "__main__":
    main()
