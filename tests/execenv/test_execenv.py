import os
import platform
from pathlib import Path

import pytest

from execenv import dotenv, execenv, get_shell_env_varref_format
from tests.conftest import CliTester

CURRENT_DIR = Path(__file__).parent


@pytest.mark.parametrize("option", ["-e", "--env"])
def test_env_option(tester: CliTester, option: str):
    (
        tester.run_command(execenv)
        .with_option(option, "SHELL", "overwritten")
        .with_option(option, "KEY", "VAL")
        .with_end_of_options()
        .with_arguments("execenv-echo", "SHELL", "KEY")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout("SHELL=overwritten\nKEY=VAL\n")
    )


@pytest.mark.parametrize("option", ["-f", "--file"])
def test_file_option(tester: CliTester, option: str):
    (
        tester.run_command(execenv)
        .with_option(option, (CURRENT_DIR / "file.env").absolute())
        .with_end_of_options()
        .with_arguments("execenv-echo", "KEY")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout("KEY=VAL\n")
    )


@pytest.mark.parametrize("option", ["-c", "--clear"])
def test_clear_option(tester: CliTester, option: str):
    if (
        platform.system() == "Windows"
        and int(platform.python_version().split(".")[1]) <= 10
    ):
        # Skip for Windows with Python 3.10 and earlier
        # Check python/cpython#105436 for further information
        return

    path = os.environ["PATH"]
    os.environ["TEST_VAR"] = "VAL"
    (
        tester.run_command(execenv)
        .with_option(option)
        .with_option("-e", "PATH", path)
        .with_end_of_options()
        .with_arguments("execenv-echo", "TEST_VAR")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout("TEST_VAR=NOT FOUND\n")
    )


@pytest.mark.parametrize("option", ["-a", "--append-env"])
def test_append_option(tester: CliTester, option: str):
    TEST_PATH = "execenv-test-path"
    (
        tester.run_command(execenv)
        .with_option(option, "PATH", TEST_PATH)
        .with_end_of_options()
        .with_arguments("execenv-echo", "PATH")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout_contains(TEST_PATH)
    )


def test_append_separator_option(tester: CliTester):
    TEST_PATH = "execenv-test-path"
    SEPARATOR = ":"
    (
        tester.run_command(execenv)
        .with_option("--append-separator", SEPARATOR)
        .with_option("-a", "PATH", TEST_PATH)
        .with_end_of_options()
        .with_arguments("execenv-echo", "PATH")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout_contains(SEPARATOR + TEST_PATH)
    )


@pytest.mark.parametrize("option", ["-s", "--shell"])
def test_shell_option(tester: CliTester, option: str):
    (
        tester.run_command(execenv)
        .with_option("-e", "PATH", "overwritten")
        .with_option("-e", "KEY", "VAL")
        .with_option(option)
        .with_end_of_options()
        .with_arguments("echo", "EXECENV_PATH", get_shell_env_varref_format("KEY"))
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout("overwritten VAL\n")
    )


@pytest.mark.parametrize("option", ["-C", "--cwd"])
def test_cwd_option(tester: CliTester, option: str):
    target_cwd = CURRENT_DIR / "cwd"
    system = platform.system()

    tester.run_command(execenv).with_option(option, target_cwd.absolute())

    if system == "Windows":
        (
            tester.with_option("-s")
            .with_end_of_options()
            .with_arguments("echo", "EXECENV_CD")
        )
    else:
        (tester.with_end_of_options().with_arguments("pwd"))

    (
        tester.execute_and_its_result()
        .should_pass()
        .should_have_stdout(f"{target_cwd}\n")
    )


@pytest.mark.parametrize("level", list(range(1, 3)))
def test_verbose_option(tester: CliTester, level: int):
    (
        tester.run_command(execenv)
        .with_option("-e", "KEY", "VAL")
        .with_option(f"-{'v' * level}")
        .with_end_of_options()
        .with_arguments("execenv-echo", "KEY")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout_contains("KEY=VAL\n")
        .should_have_stdout_contains("= execenv =")
    )


def test_config_option(tester: CliTester):
    # TODO: will be changed in 0.2.0
    # with the new `dotenv.dump` function to generate the .env file in-place
    TEST_PATH = "execenv-test-path"
    CONFIG_FILE = CURRENT_DIR / "config.env"
    config = dotenv.parse(CONFIG_FILE.read_text())
    (
        tester.run_command(execenv)
        .with_option("--config", (CURRENT_DIR / "config.env").absolute())
        .with_option("-a", "PATH", TEST_PATH)
        .with_option("-s")
        .with_end_of_options()
        .with_arguments("echo", f"{config['env_varref_prefix']}PATH")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout_contains(config["append_separator"] + TEST_PATH)
    )
