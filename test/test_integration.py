import contextlib
import subprocess
import tempfile
from pathlib import Path

import pytest

from sageleaf.main import compile_sageleaf_file


def run_sageleaf_file(file_path: Path) -> str:
    """Run a Sageleaf file and return its output, similar to cmd_run."""
    # Compile Sageleaf to C code
    c_code = compile_sageleaf_file(file_path)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        c_file = temp_path / "program.c"
        exe_file = temp_path / "program"

        with open(c_file, "w") as f:
            f.write(c_code)

        result = subprocess.run(
            ["cc", "-std=c99", "-o", str(exe_file), str(c_file)],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"C compilation failed: {result.stderr}")

        result = subprocess.run([str(exe_file)], capture_output=True, text=True)

        output = result.stdout
        if result.stdout and not result.stdout.endswith("\n"):
            output += "\n"
        output += f"Exit code: {result.returncode}"

        return output


def get_testdata_files() -> list[tuple[str, Path, Path]]:
    testdata_dir = Path(__file__).parent / "programs"
    sl_files = list(testdata_dir.glob("*.sl"))

    test_cases: list[tuple[str, Path, Path]] = []
    for sl_file in sl_files:
        txt_file = sl_file.with_suffix(".txt")
        if txt_file.exists():
            test_cases.append((sl_file.name, sl_file, txt_file))

    return test_cases


@pytest.mark.parametrize("test_name,sl_file,expected_output_file", get_testdata_files())
def test_sageleaf_integration(test_name: str, sl_file: Path, expected_output_file: Path):
    try:
        with open(expected_output_file) as f:
            expected_output = f.read().strip()

        actual_output = run_sageleaf_file(sl_file).strip()
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
