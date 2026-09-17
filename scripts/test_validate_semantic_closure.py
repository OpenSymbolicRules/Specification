#!/usr/bin/env python3
"""Tests for OpenMath semantic-closure validation."""

import json
from pathlib import Path
import tempfile
import unittest

from validate_semantic_closure import validate_file


class SemanticClosureTests(unittest.TestCase):
    def write_rule_file(self, document: dict) -> Path:
        temporary = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        path = Path(temporary.name)
        temporary.close()
        path.write_text(json.dumps(document), encoding="utf-8")
        self.addCleanup(path.unlink)
        return path

    def test_accepts_declared_expression_heads(self) -> None:
        path = self.write_rule_file({
            "semantics": {"Add": "openmath:arith1#plus"},
            "rules": [{"id": 1, "pattern": ["Add", "x", 0], "result": "x"}],
        })

        self.assertEqual(validate_file(path), [])

    def test_rejects_undeclared_expression_heads(self) -> None:
        path = self.write_rule_file({
            "semantics": {"Add": "openmath:arith1#plus"},
            "rules": [{"id": 1, "pattern": ["Add", "x", 0], "result": ["Multiply", "x", 1]}],
        })

        self.assertIn("Multiply", validate_file(path)[0])

    def test_ignores_binder_variable_lists(self) -> None:
        path = self.write_rule_file({
            "semantics": {"Forall": "openmath:quant1#forall", "Not": "openmath:logic1#not"},
            "rules": [{"id": 1, "pattern": ["Forall", ["x"], ["Not", "P"]], "result": "q"}],
        })

        self.assertEqual(validate_file(path), [])


if __name__ == "__main__":
    unittest.main()
