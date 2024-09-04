import os
from dataclasses import dataclass, field
from functools import partial
from traceback import format_exception
from typing import IO, Any, Callable, List, Mapping, Optional, Union

import pytest  # type: ignore
from click import BaseCommand
from click.testing import CliRunner, Result


@dataclass
class CliTestResult:
    """
    Wrapper for `click.testing.Result` to make testing of CLI applications more readable.
    """

    result: Result

    def should_pass(self, no_stderr: bool = True, no_exception: bool = True):
        if no_stderr:
            assert self.result.stderr == "", "STDERR: " + self.result.stderr
        if no_exception:
            assert self.result.exception is None, "".join(
                format_exception(
                    None, self.result.exception, self.result.exception.__traceback__
                )
            )
        assert self.result.exit_code == 0, "Exit code: " + str(self.result.exit_code)
        return self

    def should_fail(self, exit_code: int = 1):
        assert self.result.exit_code == exit_code
        return self

    def should_have_stdout(self, expected: str):
        assert self.result.stdout == expected
        return self

    def should_have_stdout_contains(self, expected: str):
        assert expected in self.result.stdout
        return self

    def should_have_stdout_not_contains(self, expected: str):
        assert expected not in self.result.stdout
        return self


@dataclass
class CliTester:
    """
    Wrapper for `click.testing.CliRunner` to make testing of CLI applications more readable.
    """

    runner: CliRunner = field(default_factory=partial(CliRunner, mix_stderr=False))
    command: Optional[BaseCommand] = None
    args: List[str] = field(default_factory=list)

    def _default_init_callback(self):
        self.args.clear()
        self.command = None

    def run_command(
        self,
        command: BaseCommand,
        init_callback: Optional[Callable[["CliTester"], None]] = None,
    ):
        """
        Set the command to be tested.
        """
        if init_callback is not None:
            init_callback(self)
        else:
            self._default_init_callback()

        self.command = command
        return self

    def with_option(self, option: str, *value: str):
        """
        Add an option with value(s) to the command.
        """
        self.args.append(option)
        self.args.extend(value)
        return self

    def with_end_of_options(self):
        """
        Add an end of options marker to the command.
        """
        self.args.append("--")
        return self

    def with_arguments(self, *values: str):
        """
        Add multiple argument to the command.
        """
        self.args.extend(values)
        return self

    def with_poetry_run(self, *values: str):
        """
        Add `poetry run` and multiple argument to the command.
        """
        self.args.extend(["poetry", "run", *values])
        return self

    def execute_and_its_result(
        self,
        input: Optional[Union[str, bytes, IO[Any]]] = None,
        env: Optional[Mapping[str, str]] = None,
        catch_exceptions: bool = True,
        color: bool = False,
        **extra: Any,
    ):
        """
        Execute the command and return the result.
        """
        assert self.command is not None
        result = self.runner.invoke(
            cli=self.command,
            args=self.args,
            input=input,
            env=env,
            catch_exceptions=catch_exceptions,
            color=color,
            **extra,
        )
        return CliTestResult(result)


@pytest.fixture(scope="module")
def tester():
    return CliTester()


@pytest.fixture(scope="session", autouse=True)
def test_mode():
    os.environ["EXECENV_TEST"] = "1"
