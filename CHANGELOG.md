# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Machine-readable `ecosystem.json` manifest and schema for repository discovery.
- README ecosystem catalogue covering the specification, rule sets, and Julia client.
- CI validation of all JSON schema meta-schemas and the ecosystem manifest.
- Logic rule-set entry, including Boolean algebra and propositional logic domains.
- Optional named rule-set profiles, allowing explicit alternate load manifests
  such as `to_cnf` and `to_dnf`.
- Separate inference-file and inference-test schemas, plus explicit inference
  profiles for sound multi-premise derivations such as resolution.

### Changed
- Made ecosystem discovery a normative specification requirement.
- Describe OSR as a specification and interchange format rather than an institutional standard.

- Initial structure for the Open Symbolic Rules Specification repository.
- Foundational README.md describing the specification architecture.
