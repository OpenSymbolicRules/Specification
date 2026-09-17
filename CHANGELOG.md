# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Restored the mandatory stable identity in the quantifier rule example so the
  specification validation workflow passes.

### Added
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

### Changed
- Expanded the roadmap with a transform-analysis workstream covering Laplace,
  inverse Laplace, Z, inverse Z, Fourier, and inverse Fourier transforms.
- Made ecosystem discovery a normative specification requirement.
- Describe OSR as a specification and interchange format rather than an institutional standard.

- Allow alphanumeric leaf components in section identifiers, preserving source
  taxonomies such as `1.1.2.x` and `7.1.4a`.
- Require non-empty OpenMath semantic declarations for rule files.
