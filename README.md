# Open Symbolic Rules (OSR) - Specification

This repository contains the core specification, JSON schemas, and documentation for the **Open Symbolic Rules (OSR)** standard.

## Overview

The OSR standard defines a universal, language-agnostic JSON format for representing symbolic mathematics rewriting rules. It separates mathematical knowledge from specific Computer Algebra System (CAS) implementations.

By relying on [OpenMath](https://openmath.org/) Content Dictionaries (CDs) for function semantics, OSR ensures that rules are mathematically rigorous and unambiguous, while remaining easily readable by humans and machines.

## Architecture

The OSR ecosystem is federated into specific domain repositories that consume this core specification:
- [Integration](https://github.com/OpenSymbolicRules/Integration) - Formal integration rules (derived from RUBI)
- *Algebra (Coming soon)* - Algebraic simplifications and logic

## Contents

- `schemas/`: The JSON Schema definitions that all OSR rule bases must follow.
- `docs/`: Technical documentation and RFCs.
