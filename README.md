# Open Symbolic Rules (OSR) - Specification

This repository contains the core specification, JSON schemas, and documentation for the **Open Symbolic Rules (OSR)** format.

## Overview

The OSR specification defines a universal, language-agnostic JSON format for representing symbolic mathematics rewriting rules. It separates mathematical knowledge from specific Computer Algebra System (CAS) implementations.

By relying on [OpenMath](https://openmath.org/) Content Dictionaries (CDs) for function semantics, OSR ensures that rules are mathematically rigorous and unambiguous, while remaining easily readable by humans and machines.

## Ecosystem

The ecosystem is also available as the machine-readable
[`ecosystem.json`](ecosystem.json) manifest. Tools can use it to discover rule
sets, clients, their domains, and their dependencies.

| Repository | Role | Domain |
|---|---|---|
| [Specification](https://github.com/OpenSymbolicRules/Specification) | Core schemas and documentation | All domains |
| [Integration](https://github.com/OpenSymbolicRules/Integration) | RUBI-derived symbolic integration rules | Integration |
| [Algebra](https://github.com/OpenSymbolicRules/Algebra) | Simplification, exponent, logarithm, and polynomial rules | Algebra |
| [Calculus](https://github.com/OpenSymbolicRules/Calculus) | Limit and derivative rules | Calculus |
| [Trigonometry](https://github.com/OpenSymbolicRules/Trigonometry) | Identities and simplification rules | Trigonometry |
| [Logic](https://github.com/OpenSymbolicRules/Logic) | Boolean simplification and propositional logic rules | Logic / Boolean algebra |
| [OpenSymbolicRules.jl](https://github.com/OpenSymbolicRules/OpenSymbolicRules.jl) | Julia client and loader | Julia |

All rule-set repositories depend on this specification. The Julia client
consumes the specification and can load the algebra, calculus, and trigonometry
rule sets. Logic is independently discoverable through the ecosystem manifest.

## Contents

- `schemas/`: The JSON Schema definitions that all OSR rule bases must follow.
- `docs/`: Technical documentation and RFCs.
- `ecosystem.json`: Machine-readable catalogue of OSR repositories.

## License

This repository is licensed under the [MIT License](LICENSE). OpenMath
identifiers are referenced for semantic interoperability; see [NOTICE.md](NOTICE.md).
