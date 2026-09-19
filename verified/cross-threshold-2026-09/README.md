# Verification snapshot — cross-threshold extension (September 2026)

This directory is a **separate, later** verification record for the residual-threshold and
cross-threshold extension. It does not replace the original record in `verified/`, whose files
(`Threshold.lean`, `MainTheorem.lean`, `verification-log.txt`, `SHA256SUMS.txt`, and the
environment files) are left untouched and describe the earlier proof state.

## Commits

| | commit |
|---|---|
| base (state before this extension) | `93c961d67d14a26f1f305c98c69a61adc571f7da` |
| verified sources (this snapshot) | `910ce1cf3b0ab18e67cb22113ec000f7b924df73` |

The commit that adds this directory is the child of the verified-sources commit. The snapshot
therefore records the commit whose sources were built, not its own commit id.

## Contents

- `OUCorridor/` — copies of all six library modules built for this record:
  `Basic.lean`, `Threshold.lean`, `MainTheorem.lean`, `Covariance.lean`,
  `ResidualThreshold.lean`, `CrossThreshold.lean`.
- `OUCorridor.lean` — the root module.
- `lakefile.toml`, `lake-manifest.json`, `lean-toolchain` — the pinned build environment. The
  toolchain and dependency pins are unchanged from the base commit; no `lake update` was run.
- `print-axioms.lean` — the `#print axioms` / `#check` script used for the kernel-level audit.
  It is a checking script, not part of the library, and is not built by `lakefile.toml`.
- `verification-log.txt` — Lean and Lake versions, the mathlib revision, the full `lake build`
  output with all project modules rebuilt from source, the unfinished-proof grep, and the output
  of the axiom check.
- `SHA256SUMS.txt` — fingerprints of the files in this directory.

## Environment

```text
Lean 4.33.1
x86_64-unknown-linux-gnu
Lean commit: 819816b2e0a3bf405af45ae5c7af2491d8f5bee6
mathlib:     0df444a360eaa60ab8c11dca51a86af692955474
```

The original record was produced on `arm64-apple-darwin24.6.0` with the same Lean commit.

## Result

```text
Build completed successfully (8713 jobs).
```

The unfinished-proof grep returned no matches, and every theorem checked in `print-axioms.lean`
depends only on `propext`, `Classical.choice`, and `Quot.sound` — no `sorryAx` and no custom axiom.

## Checking the hashes

From this directory:

```bash
sha256sum -c SHA256SUMS.txt
```

The copies here are byte-identical to the corresponding files at the verified-sources commit:

```bash
git -C ../.. show 910ce1cf3b0ab18e67cb22113ec000f7b924df73:OUCorridor/CrossThreshold.lean | sha256sum
```
