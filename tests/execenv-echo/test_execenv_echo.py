import os

from execenv import execenv_echo
from tests.conftest import CliTester


def test_echo_with_something_existing(tester: CliTester):
    (
        tester.run_command(execenv_echo)
        .with_arguments("PATH")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout(f"PATH={os.environ['PATH']}\n")
    )


def test_echo_with_something_missing(tester: CliTester):
    (
        tester.run_command(execenv_echo)
        .with_arguments("SOMETHING_THAT_DOES_NOT_EXIST")
        .execute_and_its_result()
        .should_pass()
        .should_have_stdout("SOMETHING_THAT_DOES_NOT_EXIST=NOT FOUND\n")
    )
