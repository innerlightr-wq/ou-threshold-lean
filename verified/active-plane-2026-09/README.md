# Verification snapshot — two-mode active-plane reduction (September 2026)

A **third**, separate verification record. It does not replace `verified/` (the original record)
or `verified/cross-threshold-2026-09/`; both are left untouched and both still verify against the
live sources.

## Commits

| | commit |
|---|---|
| base (state before this extension) | `3d0d64883759a5107ae68fc0c894d6c7098cb2a1` |
| verified sources (this snapshot) | `cb1059df5e164c088bf03c6275c531e080e14b73` |

The commit that adds this directory is the child of the verified-sources commit, so the snapshot
records the commit whose sources were built rather than its own.

## Contents

- `OUCorridor/` — copies of all eight library modules built for this record: `Basic.lean`,
  `Threshold.lean`, `MainTheorem.lean`, `Covariance.lean`, `ResidualThreshold.lean`,
  `CrossThreshold.lean`, `ActivePlane.lean`, `SpectralShape.lean`.
- `OUCorridor.lean` — the root module.
- `lakefile.toml`, `lake-manifest.json`, `lean-toolchain` — the pinned environment, unchanged
  from the base commit. No `lake update` and no `lake clean` were run.
- `print-axioms.lean` — the `#print axioms` script used for the kernel audit (28 theorems,
  covering the new results and the pre-existing main theorems). Not part of the library.
- `verification-log.txt` — Lean version, mathlib revision, the full `lake build` with the project
  modules rebuilt from source, the unfinished-proof grep, and the axiom-check output.
- `SHA256SUMS.txt` — fingerprints of the files in this directory.

## Environment

```text
Lean 4.33.1
x86_64-unknown-linux-gnu
Lean commit: 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
mathlib:     0df444a360eaa60ab8c11dca51a86af692955474
```

## Result

```text
Build completed successfully (8715 jobs).
```

The unfinished-proof grep returned no matches, and all 28 audited theorems depend only on
`propext`, `Classical.choice` and `Quot.sound` — no `sorryAx`, no custom axiom.

## Checking

From this directory:

```bash
sha256sum -c SHA256SUMS.txt
```
