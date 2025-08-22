import contextlib
import subprocess
from pathlib import Path

import pytest


def get_testdata_files() -> list[tuple[str, Path, Path]]:
    testdata_dir = Path(__file__).parent.parent / "testdata"
    sl_files = list(testdata_dir.glob("*.sl"))

    test_cases: list[tuple[str, Path, Path]] = []
    for sl_file in sl_files:
        txt_file = sl_file.with_suffix(".txt")
        if txt_file.exists():
            test_cases.append((sl_file.name, sl_file, txt_file))

    return test_cases


@pytest.mark.parametrize("test_name,sl_file,expected_output_file", get_testdata_files())
def test_sageleaf_integration(
    test_name: str, sl_file: Path, expected_output_file: Path
):
    try:
        with open(expected_output_file) as f:
            expected_output = f.read().strip()

        result = subprocess.run(
            ["uv", "run", "sage", "run", str(sl_file)],
            cwd=str(sl_file.parent.parent),
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            pytest.fail(
                f"Failed to run {test_name}:\n"
                f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )

        actual_output = result.stdout.strip()
        assert actual_output == expected_output, (
            f"Output mismatch for {test_name}:\n"
            f"Expected: {expected_output!r}\nActual: {actual_output!r}"
        )

    finally:
        testdata_dir = sl_file.parent
        for cleanup_pattern in ["*.c", "*.exe", "*.out", "a.out"]:
            for cleanup_file in testdata_dir.glob(cleanup_pattern):
                with contextlib.suppress(OSError):
                    cleanup_file.unlink()
