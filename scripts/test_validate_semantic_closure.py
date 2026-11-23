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

    def test_local_bindings_are_structural_and_values_are_checked(self) -> None:
        path = self.write_rule_file({
            "semantics": {"Multiply": "openmath:arith1#times", "Denominator": "openmath:osr#Denominator"},
            "rules": [{"id": 1, "pattern": "x", "result": ["With",
                ["List", ["Set", "k", ["Denominator", "m"]]], ["Multiply", "k", "x"]]}],
        })
        self.assertEqual(validate_file(path), [])

    def test_local_binding_does_not_hide_undeclared_value_operator(self) -> None:
        path = self.write_rule_file({
            "semantics": {"Multiply": "openmath:arith1#times"},
            "rules": [{"id": 1, "pattern": "x", "result": ["With",
                ["List", ["Set", "k", ["Mystery", "m"]]], ["Multiply", "k", "x"]]}],
        })
        self.assertTrue(any("Mystery" in error for error in validate_file(path)))

    def test_malformed_local_bindings_are_rejected(self) -> None:
        for binding in (["List", ["Set", "k"]],
                        ["List", ["Set", "k", 1], ["Set", "k", 2]],
                        ["List", ["Set", "k_", 1]]):
            with self.subTest(binding=binding):
                path = self.write_rule_file({"semantics": {"With": "openmath:osr#With", "Set": "openmath:osr#Set"},
                    "rules": [{"id": 1, "pattern": "x", "result": ["With", binding, "k"]}]})
                self.assertTrue(any("invalid With" in error for error in validate_file(path)))

    def test_rubi_star_requires_its_mathematical_projection(self) -> None:
        rule = {"id": 1, "pattern": "x", "result": ["Star", "a", "x"]}
        good = self.write_rule_file({"semantics": {"Star": "openmath:arith1#times"}, "rules": [rule]})
        self.assertEqual(validate_file(good), [])
        bad = self.write_rule_file({"semantics": {"Star": "openmath:transc1#sin"}, "rules": [rule]})
        self.assertTrue(any("Star" in error for error in validate_file(bad)))
        bad_arity = self.write_rule_file({"semantics": {"Star": "openmath:arith1#times"},
            "rules": [{"id": 1, "pattern": "x", "result": ["Star", "a"]}]})
        self.assertTrue(any("invalid Star" in error for error in validate_file(bad_arity)))

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

    def test_checks_expressions_reached_through_a_constraint(self) -> None:
        # A constraint applies predicates to mathematical expressions, and
        # those expressions carry domain vocabulary just as a pattern does.
        path = self.write_rule_file({
            "semantics": {"Add": "openmath:arith1#plus"},
            "rules": [{
                "id": 1,
                "pattern": ["Add", "x", 0],
                "result": "x",
                "constraints": [["NeQ", ["Multiply", "a", "x"], 0]],
            }],
        })

        self.assertIn("Multiply", validate_file(path)[0])

    def test_ignores_predicate_names_and_combinators(self) -> None:
        # A predicate is rule-language vocabulary, not a mathematical operator,
        # and a combinator nests constraints rather than expressions.
        path = self.write_rule_file({
            "semantics": {"Add": "openmath:arith1#plus"},
            "rules": [{
                "id": 1,
                "pattern": ["Add", "x", 0],
                "result": "x",
                "constraints": [["Not", ["And", ["IntegerQ", "x"], ["GtQ", "x", 0]]]],
            }],
        })

        self.assertEqual(validate_file(path), [])

    def test_ignores_structural_heads(self) -> None:
        # `List` collects expressions and `Condition` guards a pattern with a
        # test; both belong to the OSR expression language rather than to a
        # mathematical domain, so neither binds one.
        path = self.write_rule_file({
            "semantics": {"Add": "openmath:arith1#plus"},
            "rules": [{
                "id": 1,
                "pattern": ["Add", "x", 0],
                "result": "x",
                "constraints": [
                    ["FreeQ", ["List", "a", "b"], "x"],
                    ["MatchQ", "u", ["Condition", ["Add", "a", "x"], ["FreeQ", "a", "x"]]],
                ],
            }],
        })

        self.assertEqual(validate_file(path), [])

    def test_reports_an_operator_inside_a_guarded_pattern(self) -> None:
        path = self.write_rule_file({
            "semantics": {"Add": "openmath:arith1#plus"},
            "rules": [{
                "id": 1,
                "pattern": ["Add", "x", 0],
                "result": "x",
                "constraints": [
                    ["MatchQ", "u", ["Condition", ["Divide", "a", "x"], ["FreeQ", "a", "x"]]],
                ],
            }],
        })

        self.assertIn("Divide", validate_file(path)[0])

    def test_ignores_a_wildcard_in_operator_position(self) -> None:
        # OSR-X-004 allows a pattern variable where an operator goes, as in the
        # rules that match any of the six trigonometric heads at once.  It
        # names a binding, not an operation.
        path = self.write_rule_file({
            "semantics": {"Add": "openmath:arith1#plus"},
            "rules": [{
                "id": 1,
                "pattern": ["F_", ["Add", "a", "x"]],
                "result": ["G.", "x"],
            }],
        })

        self.assertEqual(validate_file(path), [])


if __name__ == "__main__":
    unittest.main()
