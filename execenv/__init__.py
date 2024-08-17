import os
import subprocess
import sys
from importlib.metadata import metadata
from io import TextIOWrapper
from pathlib import Path
from textwrap import dedent, indent
from types import TracebackType
from typing import Callable, Dict, List, Optional, Tuple, Type, Union, cast

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


from auto_click_auto import enable_click_shell_completion
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
    enable_click_shell_completion(__name__)

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


def clink_completion(command: click.Command, completions_path: Path):
    flags: List[str] = []
    descriptions: List[str] = []

    for param in command.params:
        if not isinstance(param, Option):
            continue

        opts = tuple(map(lambda opt: f"'{opt}'", param.opts))
        flags += opts
        if param.help:
            for opt in opts:
                descriptions.append(f"[{opt}] = '{param.help}'")

    flags_str = ", ".join(flags)
    description_str = ",\n".join(descriptions)
    description_str_indented = indent(
        description_str,
        " " * 12,
        lambda line: not description_str.startswith(line),
    )

    script = dedent(f"""\
        local matcher = clink.argmatcher('{command.name}')
        matcher:addflags({flags_str})

        local function adddescriptions_helper(matcher, ...)
            if matcher and matcher.adddescriptions then
                matcher:adddescriptions(...)
            end
        end

        adddescriptions_helper(matcher, {{
            {description_str_indented}
        }})
    """)

    file_path = completions_path / f"{command.name}.lua"

    if file_path.exists():
        click.confirm(
            f"File {f'{command.name}.lua'} already exists. Overwrite?",
            abort=True,
            default=False,
            prompt_suffix=" ",
        )
        click.echo()

    with open(file_path, "w") as f:
        f.write(script)

    click.echo(
        f"Completion script saved to {click.style(str(file_path), fg='yellow', bold=True)}."
    )


@click.command(
    help="Command to manually setup tab completion for execenv.", no_args_is_help=True
)
@click.option(
    "-s",
    "--shell",
    type=click.Choice(["clink"]),
    required=True,
    help="Shell to setup tab completion.",
)
@click.option(
    "-p",
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),  # type: ignore
    default=Path.cwd(),
    help="Path where the completion script will be saved. Current directory by default.",
)
@click.version_option(
    None, "--version", "-V", prog_name=__name__, message="%(prog)s v%(version)s"
)
@click.help_option("-h", "--help")
@rich_config(help_config)
def execenv_completion(shell: str, path: Path):
    enable_click_shell_completion(execenv_completion.name)

    if shell == "clink":
        completions_path = path / "completions"
        if not completions_path.exists():
            click.confirm(
                f"Directory does not exist.\nWill create at {click.style(str(completions_path), fg='yellow', bold=True)}.\nContinue?",
                default=True,
                abort=True,
                prompt_suffix=" ",
            )
            click.echo()
            completions_path.mkdir()

        clink_completion(execenv, completions_path)
        clink_completion(execenv_echo, completions_path)
        clink_completion(execenv_completion, completions_path)

        click.echo("\nRun following to install auto-completion:")
        click.secho(f'\nclink installscripts "{path}"\n', fg="yellow", bold=True)
        click.echo("Restart your shell to load the completion script.")
    else:
        raise click.BadParameter("Shell is not supported.")



if __name__ == "__main__":
    execenv()
