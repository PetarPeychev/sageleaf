#!/usr/bin/python3

import os
import subprocess

programs = [
    (
        "main_no_return",
        """
        fn main() {}
        """,
        0,
    ),
    (
        "main_empty_return",
        """
        fn main() {
            return;
        }
        """,
        0,
    ),
    (
        "main_return_i64",
        """
        fn main(): i64 {
            return 42;
        }
        """,
        42,
    ),
    (
        "main_return_single_add",
        """
        fn main(): i64 {
            return 28 + 9;
        }
        """,
        37,
    ),
    (
        "main_return_multiple_add",
        """
        fn main(): i64 {
            return 28 + 9 + 5;
        }
        """,
        42,
    ),
]

failures: list[str] = []
for name, code, expected_exit_code in programs:
    try:
        with open(name + ".sl", "w") as f:
            f.write(code)

        os.system("./sage build " + name + ".sl")

        exit_code = subprocess.run(["./" + name], capture_output=True).returncode

        if exit_code != expected_exit_code:
            asm = open(name + ".asm").read()
            failures.append(
                "Test "
                + name
                + " failed:\nexpected "
                + str(expected_exit_code)
                + ", got "
                + str(exit_code)
                + " for: "
                + code
                + "\n"
                + "with generated assembly:\n"
                + asm
            )
    except Exception as e:
        failures.append("Test " + name + " failed: " + repr(e))
    finally:
        os.remove(name + ".sl")
        os.remove(name)
        os.remove(name + ".asm")

if len(failures) > 0:
    for failure in failures:
        print(failure)
    print("ERROR: " + str(len(failures)) + "/" + str(len(programs)) + " failed tests.")
    exit(1)
else:
    print("All tests (" + str(len(programs)) + "/" + str(len(programs)) + ") passed.")
