# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- V1-R-005: derivative rules may have conditions too (a conditional
  derivative rule holds for every assignment satisfying them,
  `OSR.Calculus.DerivHoldsUnder`), so a refuted derivative rule can have a
  strengthened variant (V1-R-005e).
- V1-E-002b: a residual integral may be evaluated at an expression `g` of
  the bound variable, `int(λx. H)(g)` (v0.1 `Subst[Int[H, x], x, g]`);
  V1-R-005c states its meaning (`OSR.Calculus.AntiderivSubstHolds`).
- V1-R-005: `relation1#geq` is a condition symbol (both operands defined, the
  first greater than or equal to the second; no complex interpretation) and
  binary `logic1#or` joins two conditions, so v0.1 `GeQ`, `LeQ`, `Not[LtQ]`,
  `Not[GtQ]` and `Or` conditions can be stated; V1-R-005d decides them.
- V1-R-005e: a strengthened rule may be distributed unproved, with its
  numerical evidence in a `numerical:` finding.
- V1-R-005e: strengthened rules (corrected variants), which append conditions
  to the converted v0.1 conditions under a new `id`, the same `legacy_id` and
  a `strengthened:` finding; the refuted rule as stated is kept.
- V1-R-005: `relation1#eq` is a condition symbol (both operands defined and
  equal), so v0.1 `EqQ` conditions can be stated; V1-R-005d decides it like
  `relation1#neq`.
- V1-R-005d: exact decision of conditions whose operands are closed rational
  expressions after matching; the calculus reference rewriter applies a
  conditional rule when all its conditions are decided true.
- V1-E-002b, V1-R-005c: antiderivative rules and residual integrals
  `int(λx. H)(x)` (an `OMA` whose applicant is `calculus1#int` applied to a
  lambda, the form of the CD's FMP), in the text and in the rule-set schema.
  Engines that cannot continue inside a residual integral must not apply the
  rule.
- V1-R-005b: `independent` matching constraints (v0.1 `FreeQ`) in rules and
  in the rule-set schema.
- V1-E-002, V1-E-002a: `OMBIND` bindings (quantifiers) in the expression
  fragment and in the v1 schemas, with capture-free rule semantics.
- `boolean` domain (carrier `setname2#Boolean`) in the v1 schemas and
  specification, for propositional rule sets.
- V1-R-005: integer conditions `set1#in(e, setname1#Z)`.
- V1-E-005: `arith1#power` takes an expression exponent, interpreted for
  integer values only (previously a natural-number literal).
- V1-R-005: `relation1#gt` conditions; a condition symbol without an
  interpretation in a domain makes the rule unsupported there.
- V1-R-005a: rules not migrated from v0.1 are reported with the reason.
- Per-rule-set verification reports (`<ruleset>.report.json`, `.md`) in the
  file table.
- V1-T-004a: generators should prove termination of each profile and record
  the proof in the verification report.
- Draft of the OSR v1 interchange format (`docs/osr-v1.md`): OpenMath 2.0 JSON
  expressions, semantic registry with assurance levels, `defined_pattern`
  applicability, per-domain Lean verification records and certification,
  termination-checked profiles and engine conformance.
- v1 schemas: `schemas/v1/ruleset.schema.json` and
  `schemas/v1/conformance.schema.json`.
- A `symbol` typed wildcard (OSR-W-003), matching only a symbol. A rule that
  binds a variable of the problem — the variable of an integral, a derivative,
  a sum, or a limit — is valid only when that operand really is a variable, and
  without the restriction such a rule is unsound rather than incomplete.

### Changed
- Semantic closure is now checked over constraint expressions as well as
  patterns and results: a constraint applies its predicates to mathematical
  expressions, and those carry domain vocabulary that must be declared.
- Semantic closure no longer demands an OpenMath binding for a structural head
  of the expression language (`List`, `Condition`), for a constraint predicate
  name, or for a wildcard in operator position (OSR-X-004). None of these
  denotes a mathematical operation, so binding one asserts nothing.

### Fixed
- Restored the mandatory stable identity in the quantifier rule example so the
  specification validation workflow passes.

### Added
- An integration architecture requirement in the roadmap: procedural
  Risch-family methods and ordered OSR rule profiles such as RUBI are
  complementary backends sharing OpenMath semantics, assumptions, and proof
  traces.
- Roadmap requirements for explicit transform-result status, hierarchical
  algorithm proof traces, Laplace fixture coverage, and
  algebraic-structure-specific canonical forms.
- Machine-readable `ecosystem.json` manifest and schema for repository discovery.
- README ecosystem catalogue covering the specification, rule sets, and Julia client.
- CI validation of all JSON schema meta-schemas and the ecosystem manifest.
- Logic rule-set entry, including Boolean algebra and propositional logic domains.
- Optional named rule-set profiles, allowing explicit alternate load manifests
  such as `to_cnf` and `to_dnf`.
- Separate inference-file and inference-test schemas, plus explicit inference
  profiles for sound multi-premise derivations such as resolution.
- Lexically scoped `Forall` and `Exists` OSR-Expr forms with OpenMath `quant1`
  semantics and validation examples.
- Bound-variable sequence wildcards for quantifier rules that preserve an
  arbitrary lexical binder list.
- MIT licensing and an OpenMath attribution notice.
- Canonical rule identities (`identity:id`) derived from mandatory stable
  rule-file identities and mandatory positive rule identifiers.
- Required file-level `identity` values for rule files.
- Optional conversion provenance, predicate catalogues, utility-function
  catalogues, and source taxonomies in manifests.
- Mandatory machine-readable provenance for every rule, including a method and
  stable source locator.
- Semantic-closure validation for all operators used by a rule file, enforced
  in specification CI in addition to JSON Schema validation.

### Changed
- Expanded the roadmap with a transform-analysis workstream covering Laplace,
  inverse Laplace, Z, inverse Z, Fourier, and inverse Fourier transforms.
- Expanded the roadmap with university-level domains including differential
  equations, complex analysis, linear algebra, tensors, distributions,
  discrete mathematics, probability, optimization, abstract algebra, and
  number theory, plus their cross-cutting semantic requirements.
- Made ecosystem discovery a normative specification requirement.
- Describe OSR as a specification and interchange format rather than an institutional standard.

- Allow alphanumeric leaf components in section identifiers, preserving source
  taxonomies such as `1.1.2.x` and `7.1.4a`.
- Require non-empty OpenMath semantic declarations for rule files.
