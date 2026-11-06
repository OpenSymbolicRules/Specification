# Open Symbolic Rules — Interchange format v1 (draft)

Status: **draft**, format version `1.0.0-alpha.1`.  Reference implementation:
[`OpenSymbolicRules/Lean`](https://github.com/OpenSymbolicRules/Lean).
Reference consumer: `OpenSymbolicRules.OSRv1` in OpenSymbolicRules.jl.

The key words MUST, MUST NOT, SHOULD and MAY are to be interpreted as in
RFC 2119.

## 1. Scope and principles

OSR v1 distributes symbolic rewrite rules together with machine-checkable
evidence of their correctness.

- **V1-P-001.**  OpenMath content dictionaries give the meaning of every
  operator.  An OSR file MUST NOT invent OpenMath symbols or CDs.  A construct
  without an OpenMath symbol is outside the format.
- **V1-P-002.**  Rule sets are *generated* from Lean 4 sources, where each rule
  is stated and proved against Mathlib.  Hand-written v1 files are not
  conforming unless they reproduce a generated file.
- **V1-P-003.**  The interchange format is independent of any CAS and of Lean.
  A consumer needs Lean only to re-verify a record.
- **V1-P-004.**  Mathematical truth, rewrite soundness and strategy are separate
  properties, reported separately (§6, §7).

v1 is not compatible with v0.1.  The v0.1 specification (`docs/spec.md`) stays
in force for repositories not yet migrated.

## 2. Files

| File | Schema | Content |
|---|---|---|
| `<ruleset>.osr.json` | `schemas/v1/ruleset.schema.json` | Rules, symbols, profiles, verification records |
| `registry.json` | — (subset of the rule-set `symbols` schema) | Every symbol of the semantic registry |
| `<suite>.cases.json` | `schemas/v1/conformance.schema.json` | Engine conformance cases |
| `<ruleset>.report.json`, `<ruleset>.report.md` | — | Verification report: metrics per domain, rules not migrated, termination proofs, strategy runs |

- **V1-F-001.**  A rule-set file MUST validate against
  `schemas/v1/ruleset.schema.json`.
- **V1-F-002.**  Generation MUST be deterministic: the same sources, toolchain
  and dependency revisions produce byte-identical files.  Files MUST NOT
  contain timestamps; they carry a `source_digest` (SHA-256 over the sources)
  instead.

## 3. Expressions

- **V1-E-001.**  Expressions use the OpenMath 2.0 JSON encoding (2019 revision,
  §3.3), with `cdbase` `http://www.openmath.org/cd`.
- **V1-E-002.**  Only `OMS`, `OMV`, `OMI` (JSON integer) and `OMA` with an `OMS`
  applicant are allowed.  Floats, strings, binders, attributions and errors are
  outside the v1 fragment, and consumers MUST reject them.
- **V1-E-003.**  Every `OMS` used by a rule MUST be listed in the rule's
  `symbols` and in the file's `symbols` table.
- **V1-E-004.**  Arity is fixed per symbol in the `symbols` table.  An n-ary CD
  symbol used with a fixed arity (for example binary `arith1#plus`) is noted
  in the symbol's `fragment`; longer sums are left-nested.
- **V1-E-005.**  `arith1#power` takes any expression as exponent, but v1
  interprets it only where the exponent is an integer, with a nonzero base if
  the exponent is negative; elsewhere the power is undefined, so
  `defined_pattern` rules say nothing there.  General real or complex powers
  (`exp(a ln x)`) are outside v1.

## 4. Semantic registry

Each symbol entry relates an OpenMath symbol to a Lean constant, per domain
(`real` with carrier `setname1#R`, `complex` with carrier `setname1#C`).

- **V1-S-001.**  An interpretation records:
  - `lean`: the Lean constant;
  - `assurance`: one of `reviewed`, `formally_related`, `provisional`,
    `unsupported`;
  - `definedness`: where the OpenMath operation is defined, in words;
  - `obligations`: CMPs of the CD, each with the Lean theorem proving it;
  - `unresolved`: open semantic questions.
- **V1-S-002.**  `formally_related` requires at least one proved obligation.
  The generator MUST check that every listed theorem exists and depends only
  on the accepted axioms (§6).
- **V1-S-003.**  The CD of each symbol is identified by version, revision,
  date and SHA-256 of a pinned snapshot (`OpenSymbolicRules/OpenMath`).

## 5. Rules

A rule record has `id`, `legacy_id`, `description`, `variables`, `pattern`,
`replacement`, `conditions`, `orientation`, `applicability`, `profiles`,
`priority`, `symbols`, `provenance`, `verification` and `findings`.

- **V1-R-001.**  `id` is a dotted lower-case identifier, unique in the rule set.
- **V1-R-002.**  Every variable of `pattern`, `replacement` and `conditions` is
  declared in `variables`.  Every variable of `replacement` occurs in
  `pattern`.  `pattern` is not a bare variable.
- **V1-R-003.**  `orientation` is `forward`: the rule rewrites an instance of
  `pattern` into the corresponding instance of `replacement`.
- **V1-R-004.**  `applicability` is `defined_pattern`.  For every assignment of
  the variables that satisfies the conditions, **if every operation in the
  pattern is applied inside its domain of definition** (registry definedness:
  no zero divisor, no `tan` pole, no `arctan` singularity over ℂ, …), then the
  replacement is defined and has the same value.  A rewrite may enlarge the
  domain of definition; it never changes a defined value and never produces an
  undefined expression from a defined one.
- **V1-R-005.**  `conditions` are explicit side conditions (v1:
  `relation1#neq`, `relation1#gt`, and `set1#in` with `setname1#Z` for an
  integer-valued expression), whose operands are required to be defined.  A condition symbol without an interpretation in a domain (v1:
  `relation1#gt` over ℂ) makes the rule unsupported there.  An engine MUST
  NOT apply a rule whose conditions it cannot decide.
- **V1-R-005a.**  A rule set migrated from v0.1 SHOULD report the v0.1 rules
  it does not migrate, with the reason, in its verification report; a rule is
  never dropped silently.
- **V1-R-006.**  `provenance.method` is one of `authored`, `transcribed`,
  `converted` and `derived`; `sources` preserve the original attributions and
  licenses.  A rule migrated from v0.1 carries its v0.1 identity in
  `legacy_id`.
- **V1-R-007.**  `findings` report migration issues (missing hypotheses,
  semantic gaps, strategy problems).  They are informative.

## 6. Verification records and certification

A rule has one verification record per domain.

- **V1-V-001.**  `status` is one of `proved`, `unproved`, `counterexample` and
  `unsupported`.  A `proved` record names the Lean `theorem`, its `statement`
  (`OSR.Rule.Holds <rule> <domain>`), `axioms`, `module`, `lean_toolchain`,
  `mathlib_revision` and `source_digest`.
- **V1-V-002.**  Before export, the generator MUST check, in the elaborated
  Lean environment:
  - that the theorem's type is syntactically the statement for exactly this
    rule and domain;
  - that the rule declaration evaluates to the exported rule;
  - that the theorem's axioms are within `propext`, `Classical.choice` and
    `Quot.sound`.

  `sorryAx`, `Lean.ofReduceBool` and custom axioms MUST make the export fail.
- **V1-V-003.**  `certified` is `true` if and only if:
  - `status` is `proved`;
  - every symbol used by the rule has a `reviewed` or `formally_related`
    interpretation in that domain (`mapping_assurance` reports the weakest).
- **V1-V-004.**  Certification is per domain and MUST NOT be merged across
  domains.
- **V1-V-005.**  A record is a claim.  It is re-checkable by rebuilding the
  sources at `source_digest`, as `OpenSymbolicRules/Verification` does.
- **V1-V-006.**  Imported rules without a proof MAY be distributed with status
  `unproved`.  They MUST NOT carry a `theorem`.

## 7. Profiles and strategy

- **V1-T-001.**  `profiles` maps a profile name to its rule ids, in priority
  order (lower `priority` first).
- **V1-T-002.**  The reference strategy is outermost-leftmost.  At each step it
  tries the root with each unconditional rule of the profile in order, then the
  arguments left to right, applying one rewrite per step.  Matching is
  syntactic: a repeated pattern variable matches equal subterms, and integers
  compare by value.
- **V1-T-003.**  The reference rewriter (`OSR.normalize`) is proved sound in
  Lean: with rules whose records are `proved`, rewriting a defined expression
  yields a defined expression with the same value.
- **V1-T-004.**  The generator MUST run every profile on every rule pattern
  (and further seeds) and fail if a run does not reach a normal form within
  its budget.  This is a test, not a proof of termination.
- **V1-T-004a.**  A generator SHOULD also prove termination of each profile
  under the reference strategy and record the proof in its verification
  report (theorem, statement, axioms).  The Lean generator does so with one
  monotone weight per profile (`OSR.Terminates`); a profile without such a
  record is only known to terminate on the tested seeds.
- **V1-T-005.**  An engine that claims v1 conformance MUST reproduce every case
  of the published conformance suites for the profiles it supports: same
  result, same sequence of rule ids, and a normal form reported exactly when
  the case says `normal`.  Engines MAY implement other strategies outside
  that claim.

## 8. Consumers

- **V1-C-001.**  A consumer MUST reject files with an unsupported
  `osr_format` major version, unknown expression kinds, undeclared symbols,
  or rules violating V1-R-002.
- **V1-C-002.**  By default, a consumer SHOULD apply only rules `certified` in
  the domain of the expression.  Using other rules SHOULD be an explicit
  choice.
- **V1-C-003.**  A consumer SHOULD record, for each applied rewrite, the rule
  id and the theorem of the record used.

## 9. Changes from v0.1

| v0.1 | v1 |
|---|---|
| Hand-written JSON, S-expression-like `["Add", …]` | Generated from Lean, OpenMath 2.0 JSON |
| OpenMath mapping per operator (unsatisfiable for RUBI utilities, OSR-F-003a) | Fragment limited to registry symbols; others are not representable |
| `constraints` strings | Typed `conditions` and `defined_pattern` applicability |
| No proofs; numeric tests | Per-domain Lean proofs, audited, certification policy |
| `meta.json` `load_order` | `profiles` with priorities, termination-checked |
| Integration-specific requirements (taxonomy, 72,000 tests) | Domain-independent contract |
