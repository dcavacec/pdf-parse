"""Thin wrapper CLI.

This file intentionally delegates to the canonical package CLI at
`pdf_parse.cli:main` to avoid duplicating CLI logic in two places.

Keeping a thin wrapper preserves backwards compatibility for users who
run `python cli.py` from the project root while the package entry point
remains `pdf-parse=pdf_parse.cli:main` in `setup.py`.
"""

from __future__ import annotations

import sys


def main() -> None:
    """Delegate to the package CLI implementation."""
    # Import here to avoid importing package internals on module import
    # (only when invoked as a script).
    from pdf_parse.cli import main as package_main

    # Call the package's main() which uses argparse reading from sys.argv.
    package_main()


if __name__ == "__main__":
    main()