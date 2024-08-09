import os
import re
import subprocess
import sys
from importlib.metadata import metadata
from io import TextIOWrapper
from types import TracebackType
from typing import Dict, Tuple

# Optional rich feature
try:
    import rich_click as click  # type: ignore

    click.rich_click.TEXT_MARKUP = "rich"
except ImportError:
    import click  # type: ignore

from click import Context, Option, Parameter

from execenv import dotenv
from execenv.verbose import VerboseInfo


def help_text(text: str):
    if hasattr(click, "rich_click"):
        return text
    return re.sub(r"\[([^\]]*)\]", "", text)


def _no_traceback_excepthook(
    exctype: type[BaseException],
    value: BaseException,
    traceback: TracebackType | None,
    /,
):
    pass


def cwd_callback(ctx: Context, param: Option | Parameter, value: str):
    return os.path.abspath(value) if value else None


def env_callback(
    ctx: Context, param: Option | Parameter, values: Tuple[Tuple[str, str]]
):
    env = {}
    for value in values:
        var_name, var_val = value
        env[var_name] = var_val
    return env


def env_file_callback(
    ctx: Context, param: Option | Parameter, values: Tuple[TextIOWrapper]
):
    env_from_file = {}

    for value in values:
        try:
            env_from_file.update(dotenv.parse(value.read()))
        except Exception:
            raise click.BadParameter(".env file must be valid")

    return env_from_file


@click.command(help=metadata(__package__)["Summary"])
@click.argument("command", type=str, nargs=-1, required=True)
@click.option(
    "--keep/--no-keep",
    default=True,
    help=help_text(
        "Whether to keep the current environment. [italic blue]True[/] by default."
    ),
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help=help_text("Run with verbose mode. Log out necessary info."),
)
@click.option(
    "-e",
    "--env",
    multiple=True,
    type=(str, str),
    callback=env_callback,
    help=help_text('Environment variable pair in the format of [gold3]"NAME val"[/].'),
)
@click.option(
    "-f",
    "--env-file",
    multiple=True,
    type=click.File("r"),
    callback=env_file_callback,
    help=help_text(".env file with environment variable pairs."),
)
@click.option(
    "-c",
    "--cwd",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    callback=cwd_callback,
    help=help_text("Current working directory."),
)
@click.version_option(
    None, "--version", "-V", prog_name=__name__, message="%(prog)s v%(version)s"
)
@click.help_option("-h", "--help")
def execenv(
    command: Tuple[str],
    env: Dict[str, str],
    keep: bool,
    cwd: str | None,
    verbose: int | None,
    env_file: Dict[str, str],
):
    """
    Run a certain command with environment variables set.
    """
    try:
        verbose_info = VerboseInfo(locals().copy(), verbose)

        # Construct merged environment
        env_merged = {}
        env_merged.update(env_file)
        env_merged.update(env)
        if keep:
            env_merged.update(os.environ)
        verbose_info.add("env_merged", env_merged, 2)

        verbose_info.show()

        exit(subprocess.run(command, env=env_merged, cwd=cwd, shell=True).returncode)

    except KeyboardInterrupt:
        # Prevent default traceback
        if sys.excepthook is sys.__excepthook__:
            sys.excepthook = _no_traceback_excepthook
        raise


if __name__ == "__main__":
    execenv()
