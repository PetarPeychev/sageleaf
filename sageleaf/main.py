import argparse
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from sageleaf.codegen.codegen import CodeGenerator
from sageleaf.parse.lexer import Lexer
from sageleaf.parse.parser import Parser
from sageleaf.typecheck.typechecker import TypeChecker


def compile_sageleaf_file(file_path: Path) -> str:
    with open(file_path) as f:
        source = f.read()

    lexer = Lexer(source, file_path)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    typechecker = TypeChecker(ast)
    typechecker.check()
    codegen = CodeGenerator(ast)
    c_code = codegen.generate()
    return c_code


def cmd_build(args: argparse.Namespace) -> None:
    file_path = Path(args.file)

    try:
        c_code = compile_sageleaf_file(file_path)
    except Exception:
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        c_file = temp_path / "program.c"
        exe_file = temp_path / "program"

        with open(c_file, "w") as f:
            f.write(c_code)

        try:
            subprocess.run(
                ["cc", "-std=c99", "-o", str(exe_file), str(c_file)],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e.stderr.decode()}", file=sys.stderr)
            sys.exit(1)

        output_exe = file_path.with_suffix("")
        subprocess.run(["cp", str(exe_file), str(output_exe)], check=True)


def cmd_run(args: argparse.Namespace) -> None:
    file_path = Path(args.file)

    try:
        c_code = compile_sageleaf_file(file_path)
    except Exception:
        sys.exit(1)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        c_file = temp_path / "program.c"
        exe_file = temp_path / "program"

        with open(c_file, "w") as f:
            f.write(c_code)

        try:
            subprocess.run(
                ["cc", "-std=c99", "-o", str(exe_file), str(c_file)],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e.stderr.decode()}", file=sys.stderr)
            sys.exit(1)

        try:
            p = subprocess.run([str(exe_file)], check=True)
            print(f"Exit code: {p.returncode}")
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)


def cmd_check(args: argparse.Namespace) -> None:
    file_path = Path(args.file)
    with open(file_path) as f:
        source = f.read()
    try:
        lexer = Lexer(source, file_path)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        typechecker = TypeChecker(ast)
        typechecker.check()
    except Exception:
        sys.exit(1)


def cmd_emit_c(args: argparse.Namespace) -> None:
    file_path = Path(args.file)
    try:
        c_code = compile_sageleaf_file(file_path)
        output_file = file_path.with_suffix(".c")
        with open(output_file, "w") as f:
            f.write(c_code)
    except Exception:
        sys.exit(1)


def setup_emit_parser(subparsers: Any) -> None:
    emit_parser = subparsers.add_parser("emit", help="Emit code in various formats")
    emit_subparsers = emit_parser.add_subparsers(
        dest="emit_format", help="Output format"
    )
    emit_subparsers.required = True

    c_parser = emit_subparsers.add_parser("c", help="Emit C code")
    c_parser.add_argument("file", help="Sageleaf source file (.sl)")
    c_parser.set_defaults(func=cmd_emit_c)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sage", description="Sageleaf programming language compiler"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.required = True

    build_parser = subparsers.add_parser("build", help="Build a Sageleaf program")
    build_parser.add_argument("file", help="Sageleaf source file (.sl)")
    build_parser.set_defaults(func=cmd_build)

    run_parser = subparsers.add_parser("run", help="Run a Sageleaf program")
    run_parser.add_argument("file", help="Sageleaf source file (.sl)")
    run_parser.set_defaults(func=cmd_run)

    check_parser = subparsers.add_parser(
        "check", help="Parse and typecheck a Sageleaf program"
    )
    check_parser.add_argument("file", help="Sageleaf source file (.sl)")
    check_parser.set_defaults(func=cmd_check)

    setup_emit_parser(subparsers)

    args = parser.parse_args()

    if hasattr(args, "file"):
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        if file_path.suffix != ".sl":
            print(f"Error: Expected .sl file, got '{args.file}'", file=sys.stderr)
            sys.exit(1)

    args.func(args)
