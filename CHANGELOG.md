# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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
