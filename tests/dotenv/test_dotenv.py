import json
from pathlib import Path
from typing import Dict, List, Tuple

import pytest  # type: ignore

from execenv.dotenv import parse


def _test_parse_from_file_data():
    """
    Fixtures from motdotla/dotenv.

    See:
        https://github.com/motdotla/dotenv/blob/master/tests/.env
        https://github.com/motdotla/dotenv/blob/master/tests/.env.multiline
    """
    files: List[Tuple[Path, Path]] = []

    parent_dir = Path(__file__).parent
    input_dir = parent_dir / "input"
    output_dir = parent_dir / "output"

    for input_file in input_dir.iterdir():
        if input_file.suffix == ".env":
            input_path = input_dir / input_file
            output_path = output_dir / input_file.with_suffix(".json").name

            if output_path.exists():
                files.append((input_path, output_path))
            else:
                # Generate output file if it doesn't exist
                output_path.write_text(
                    json.dumps(parse(input_path.read_text()), indent=4)
                )

    return {
        "argnames": ("input_file", "output_file"),
        "argvalues": files,
        "ids": [input_file.stem for input_file, _ in files],
    }


def _test_parse_from_string_data():
    return {
        "argnames": "input",
        "argvalues": [
            "SERVER=localhost\rPASSWORD=password\rDB=tests\r",
            "SERVER=localhost\nPASSWORD=password\nDB=tests\n",
            "SERVER=localhost\r\nPASSWORD=password\r\nDB=tests\r\n",
        ],
        "ids": ["CR", "LF", "CRLF"],
    }


@pytest.mark.parametrize(**_test_parse_from_file_data())
def test_parse_with_data_from_file(input_file: Path, output_file: Path):
    input_data = input_file.read_text()
    parsed_data = parse(input_data)
    expected_output: Dict[str, str] = json.loads(output_file.read_text())
    assert parsed_data == expected_output
    assert "COMMENTS" not in parsed_data


@pytest.mark.parametrize(**_test_parse_from_string_data())
def test_parse_with_data_from_string(input: str):
    expected = {"SERVER": "localhost", "PASSWORD": "password", "DB": "tests"}
    assert parse(input) == expected
