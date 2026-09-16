# Open Symbolic Rules (OSR) - Roadmap

This document outlines the strategic vision and upcoming milestones for the Open Symbolic Rules standard and its surrounding ecosystem.

## Phase 1: Foundation (Current)
*Establish the universal format and the first massive dataset.*

- [x] Define a universal JSON Schema for symbolic rewriting rules (`osr-expr.schema.json`, `rule-file.schema.json`).
- [x] Anchor the semantics using **OpenMath Content Dictionaries (CDs)** to resolve mathematical ambiguity.
- [x] Port the RUBI (Rule-Based Integration) dataset (~6,000 rules, ~72,000 tests) to the OSR JSON format.
- [x] Federate the architecture into `Specification` (schemas) and `Integration` (data) repositories.

## Phase 2: Host CAS Adoption
*Build the first generation of native parsers and clients in major Computer Algebra Systems.*

- [ ] **Julia / Symbolics.jl**: Build a macro-based compiler (`@load_osr`) that parses OSR JSON at compile-time into zero-overhead `SymbolicUtils.jl` rewrite rules.
- [ ] **Julia / Assumptions**: Merge metadata enhancements (e.g., `VariableDomain`) into Symbolics.jl to support OSR constraints (positive, real, integer).
- [ ] **Python / SymPy**: Develop an adapter to load OSR rules into SymPy's pattern matching engine.
- [ ] **Rust / CAS**: Prototype a standalone Rust engine capable of evaluating OSR rules with high performance.

## Phase 3: Domain Expansion
*Extend the standard beyond integration into general algebra.*

- [ ] Create the **`Algebra`** repository to host rules for polynomial expansion, factoring, and simplification.
- [ ] Create the **`Trigonometry`** repository to host rules for trigonometric identities and simplifications.
- [ ] Extend the OSR schemas to support conditional branching and loop-based rewrites (if necessary for algebraic limits).

## Phase 4: Hybrid Architecture (SMT Solvers)
*Combine rule-based rewriting with formal constraint solvers.*

- [ ] Define the architectural interface between OSR rule engines and SMT solvers (like Microsoft Z3).
- [ ] Use OSR rules to rewrite transcendental constraints (e.g., logarithms, exponentials) into piecewise polynomial constraints.
- [ ] Delegate the validation of these algebraic constraints to the underlying SMT solver (e.g., via `SymbolicSMT.jl` in Julia).
