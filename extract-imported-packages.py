#!/usr/bin/env python
"""
Extract what (unique) packages/modules are imported from given Python files,
e.g. to inform what the dependencies are.

To do and ideas:
- ignore standard library packages
- support recursive directory scan
- usage histogram
- only collect top-level packages
- skip files that fail to parse
- ignore packages that are conditionally imported or guarded with `except ImportError`
"""

import ast
import os
import sys
from typing import Iterator, Union


class Extractor:
    def collect_from_code(self, code: str) -> Iterator[str]:
        """Collect imported packages from code string."""
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Handle: import x
                yield from (alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                # Handle: from x import y
                if node.module:
                    yield node.module

    def collect_from_file(self, filepath: Union[str, os.PathLike]) -> Iterator[str]:
        """Collect imported packages from a Python file."""
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        return self.collect_from_code(code)

    def main(self, argv):
        collected = set()
        for filepath in argv[1:]:
            collected.update(self.collect_from_file(filepath))

        for package in sorted(collected):
            print(package)


if __name__ == "__main__":
    extractor = Extractor()
    extractor.main(sys.argv)
