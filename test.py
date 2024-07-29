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
    (
        "main_return_add_subtract",
        """
        fn main(): i64 {
            return 28 - 9 + 5;
        }
        """,
        24,
    ),
    (
        "main_return_multiply",
        """
        fn main(): i64 {
            return 28 * 9;
        }
        """,
        252,
    ),
    (
        "main_return_multiply_multiply",
        """
        fn main(): i64 {
            return 3 * 4 * 5;
        }
        """,
        60,
    ),
    (
        "main_return_divide",
        """
        fn main(): i64 {
            return 28 / 4;
        }
        """,
        7,
    ),
    (
        "main_return_multiply_divide",
        """
        fn main(): i64 {
            return 28 * 9 / 4;
        }
        """,
        63,
    ),
    (
        "main_return_divide_divide_remainder",
        """
        fn main(): i64 {
            return 28 / 4 / 2;
        }
        """,
        3,
    ),
    (
        "main_return_precendence_mul_div_sub_add",
        """
        fn main(): i64 {
            return 28 * 9 + 10 / 4 - 28 * 5 + 9;
        }
        """,
        123,
    ),
    (
        "main_return_parenthesized",
        """
        fn main(): i64 {
            return (2 + 3) * 4 - (((3 + 5)) / 2);
        }
        """,
        16,
    ),
]

failures: list[str] = []
for name, code, expected_exit_code in programs:
    try:
        with open(name + ".sl", "w") as f:
            f.write(code)

        os.system("go run sage _build " + name + ".sl")

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
        os.remove(name + ".o")
        os.remove(name + ".asm")

if len(failures) > 0:
    for failure in failures:
        print(failure)
    print("ERROR: " + str(len(failures)) + "/" + str(len(programs)) + " failed tests.")
    exit(1)
else:
    print("All tests (" + str(len(programs)) + "/" + str(len(programs)) + ") passed.")
