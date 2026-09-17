# Open Symbolic Rules (OSR) - Roadmap

This document outlines the strategic vision and upcoming milestones for the Open Symbolic Rules specification and its surrounding ecosystem.

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
*Extend the specification beyond integration into general algebra and logic.*

- [x] Create the **`Algebra`** repository to host rules for polynomial expansion, factoring, and simplification.
- [x] Create the **`Trigonometry`** repository to host rules for trigonometric identities and simplifications.
- [x] Create the **`Logic`** repository to host Boolean simplification and propositional logic rules.
- [ ] Extend the OSR schemas to support conditional branching and loop-based rewrites (if necessary for algebraic limits).

### Transform analysis and operational calculus

- [ ] Define OpenMath-anchored expression forms and rule profiles for the
  **Laplace transform** and its inverse. The design must bind the source and
  transform variables explicitly and carry the region-of-convergence or the
  assumptions needed for inverse-transform rules.
- [ ] Define expression forms and rule profiles for the bilateral and
  unilateral **Z-transform**, together with their inverses. Time-index origin,
  sidedness, and region of convergence must be representable rather than left
  to an implementation convention.
- [ ] Define expression forms and rule profiles for the **Fourier transform**
  and inverse Fourier transform. A selected normalization convention must be
  carried by the profile so that `2π` factors are never implicit.
- [ ] Add transform-pair fixtures, shift/scaling/convolution rules, and
  domain-sensitive conditions. Direct and inverse rules must be selected as
  separate profiles to prevent uncontrolled transform/inverse cycles.
- [ ] Establish a dedicated transform rule-set repository after the above
  semantics, variable binding, normalization, and convergence requirements are
  specified and schema-validated.

## Phase 4: Hybrid Architecture (SMT Solvers)
*Combine rule-based rewriting with formal constraint solvers.*

- [ ] Define the architectural interface between OSR rule engines and SMT solvers (like Microsoft Z3).
- [ ] Use OSR rules to rewrite transcendental constraints (e.g., logarithms, exponentials) into piecewise polynomial constraints.
- [ ] Delegate the validation of these algebraic constraints to the underlying SMT solver (e.g., via `SymbolicSMT.jl` in Julia).

## Known Technical Limitations & Strategic Mitigations
*While OSR specifies interoperable pattern-matching rules, we acknowledge the intrinsic limits of a purely rule-based JSON approach.*

1. **Procedural Algorithms vs. Pattern Matching**
   - **Limitation**: Pure JSON rewrite rules cannot efficiently encode full procedural algorithms like the Risch algorithm (for integration), the full GrÃ¶bner basis algorithm, or Risch-Norman extensions. These algorithms require arbitrary iterative arithmetic over rational function fields, mutable loop states, and complex branching.
   - **Mitigation**: OSR does not aim to replace core procedural CAS algorithms. OSR is designed to sit alongside them as a heuristics engine. A host CAS should use its native procedural algorithms for standard operations, and leverage the OSR dataset for specialized knowledge (like RUBI's deep catalog of transcendental transformations).

2. **Complex Entangled Domain Constraints**
   - **Limitation**: Representing deeply entangled assumptions (e.g., "if $x \in \mathbb{C}$, then $y \in \mathbb{R}$ unless $z > 0$") is extremely verbose and brittle using a rigid JSON constraint array.
   - **Mitigation**: Phase 4 addresses this by delegating heavy domain logic to formal SMT solvers (like Z3). The OSR JSON focuses strictly on mapping local variables to standard OpenMath sets, relying on the host CAS (via interfaces like `SymbolicSMT.jl`) to resolve the complex satisfiability of those constraints.

3. **Performance Overhead of Interpretation**
   - **Limitation**: Dynamically parsing and interpreting 6,000+ JSON rules at runtime in a CAS creates an unacceptable performance bottleneck compared to native code.
   - **Mitigation**: The OSR standard advocates for an **Ahead-Of-Time (AOT) compilation architecture**. Host client implementations (like the planned `OpenSymbolicRules.jl`) must parse the JSON at compile-time (e.g., using Julia macros) and transform the OSR AST directly into native host rules (like `SymbolicUtils.jl` `@rule`s), achieving zero-overhead runtime performance.
