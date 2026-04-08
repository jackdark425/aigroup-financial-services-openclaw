---
description: Debug and audit a financial model for errors
argument-hint: "[path to .xlsx model file]"
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Modified by AIGroup for OpenClaw compatibility and banker workflow packaging. Not an official Anthropic release. -->


Load the `audit-xls` skill with scope **model** and audit the specified financial model for broken formulas, balance sheet imbalances, hardcoded overrides, circular references, and logic errors — including the full model-integrity checks (BS balance, cash tie-out, roll-forwards, model-type-specific bugs).

If a file path is provided, use it. Otherwise ask the user for the model to review.
