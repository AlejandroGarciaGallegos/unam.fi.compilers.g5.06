from __future__ import annotations

import argparse
from pathlib import Path

from ast_nodes import ExecutionContext, CompileError
from parser import parse_source


def compile_and_run(source_path: Path) -> None:
    text = source_path.read_text(encoding="utf-8")

    try:
        program = parse_source(text)
        ctx = ExecutionContext()
        program.execute(ctx)
    except CompileError as e:
        # Estilo requerido: error in line n
        print(str(e))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="unam.fi.compilers.g5.00",
        description="Mini compiler/interpreter for a simple typed language (int/float/print).",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="source code file to compile and execute",
    )
    args = parser.parse_args()
    compile_and_run(args.file)


if __name__ == "__main__":
    main()
