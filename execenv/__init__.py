import os
import subprocess
import sys
from importlib.metadata import metadata
from io import TextIOWrapper
from types import TracebackType
from typing import Callable, Dict, Optional, Tuple, Type, Union

# Optional rich feature
try:
    import rich_click as click  # type: ignore
    from rich.highlighter import ReprHighlighter
    from rich_click import rich_config

    help_config = click.RichHelpConfiguration(highlighter=ReprHighlighter())

except ImportError:
    import click  # type: ignore

    def rich_config(help_config: None):  # type: ignore
        def decorator(f: Callable) -> Callable:
            return f

        return decorator

    help_config = None  # type: ignore


from click import Context, Option, Parameter

from execenv import dotenv
from execenv.verbose import VerboseInfo


def _no_traceback_excepthook(
    exctype: Type[BaseException],
    value: BaseException,
    traceback: Optional[TracebackType],
    /,
):
    pass


def cwd_callback(ctx: Context, param: Union[Option, Parameter], value: str):
    return os.path.abspath(value) if value else None


def env_callback(
    ctx: Context, param: Union[Option, Parameter], values: Tuple[Tuple[str, str]]
):
    env = {}
    for value in values:
        var_name, var_val = value
        env[var_name] = var_val
    return env


def env_file_callback(
    ctx: Context, param: Union[Option, Parameter], values: Tuple[TextIOWrapper]
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
    help="Whether to keep the current environment. True by default.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Run with verbose mode. Log out necessary info.",
)
@click.option(
    "-e",
    "--env",
    multiple=True,
    type=(str, str),
    callback=env_callback,
    help='Environment variable pair in the format of "NAME val".',
)
@click.option(
    "-f",
    "--env-file",
    multiple=True,
    type=click.File("r"),
    callback=env_file_callback,
    help=".env file with environment variable pairs.",
)
@click.option(
    "-c",
    "--cwd",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    callback=cwd_callback,
    help="Current working directory.",
)
@click.version_option(
    None, "--version", "-V", prog_name=__name__, message="%(prog)s v%(version)s"
)
@click.help_option("-h", "--help")
@rich_config(help_config)
def execenv(
    command: Tuple[str],
    env: Dict[str, str],
    keep: bool,
    cwd: Optional[str],
    verbose: Optional[int],
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
