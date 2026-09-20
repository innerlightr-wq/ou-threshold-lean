# Zotero: library structure for this project, and what still has to be done by hand

**Status as of 19 September 2026.** Zotero is installed and holds an existing library for this
project, built during the September 2026 literature/provenance audit. This extension **did not
write to Zotero**: at the time of writing Zotero was **not running**, its local API was
unreachable, and **Better BibTeX is not installed**. Everything below that is marked *verified*
was read from a **copy** of `~/Zotero/zotero.sqlite` taken while the application was closed;
nothing in the live database, and no file inside `~/Zotero/`, was modified.

The authoritative bibliographic record for the repository is
[`../references.bib`](../references.bib), which is complete and validated (§6). The Zotero-side
actions in §5 remain **outstanding**.

## 1. Installation and access (verified)

| | |
|---|---|
| Zotero | installed as an extracted upstream Linux archive (Zotero 10.x), same installation used by the other research repositories |
| data directory | `~/Zotero/`, database `~/Zotero/zotero.sqlite` (5.3 MB, last modified 18 Sept 2026) |
| process state | **not running** at the time of this work (`pgrep zotero` → nothing) |
| local API | **unreachable** (`GET http://127.0.0.1:23119/api/` → no response) |
| Better BibTeX | **not installed** — no extension directory, no `better-bibtex.sqlite` |

The local-API procedure itself is unchanged from the other repositories and is documented in
`strain-vorticity-comparator-dynamics/docs/ZOTERO_SETUP.md` §§2–3: enable
`extensions.zotero.httpServer.localAPI.enabled`, read `Zotero-Server-ID` from `GET /api/`,
`POST /api/local/authorize` — **which blocks on a GUI approval dialog** — then send
`Zotero-API-Key` on writes. Because that dialog needs a human, the write steps below cannot be
completed from a non-interactive session, and are therefore listed as instructions rather than
reported as done.

`zotero.sqlite` must never be edited directly, and must not be copied or read while Zotero is
running.

## 2. Existing library for this project (verified, read-only)

Parent collection **`OU Threshold — Heterogeneity and Coupling`** (key `SXXMUAZA`), with
**16 subcollections** and **12 distinct items** — matching the 12 original entries of
`references.bib` one-for-one.

| subcollection | items |
|---|---|
| `00 — Reviews & Orientation` | 3 |
| `01 — Ornstein–Uhlenbeck Processes` | 2 |
| `02 — Multivariate OU & Lyapunov Equations` | 3 |
| `03 — Coupled Linear Langevin Systems` | 2 |
| `04 — Stochastic Synchronization` | 2 |
| `05 — Heterogeneous Noise` | 3 |
| `06 — Generalized Variance & Covariance Volume` | 1 |
| `07 — Gaussian Entropy` | 1 |
| `08 — Network Coherence & Consensus` | 1 |
| `09 — Control / H2 / Gramians` | 2 |
| `10 — Nonequilibrium Linear Systems` | 2 |
| `11 — Brownian Gyrator` | 1 |
| `12 — Exact Threshold Search` | 8 |
| `13 — Lean / Formalization Context` | **0** (deliberately empty: no Lean/mathlib formalization of OU processes or continuous Lyapunov equations was located) |
| `14 — Directly Cited in Repository` | 12 |
| `15 — Closest Prior Art / Novelty Checks` | 6 |

This numbering is the convention already established for this project and is **preserved**. The
generic `00–14` scheme proposed for new projects is *not* applied here, because renumbering an
existing library would break the mapping recorded in the September audit.

## 3. Subcollections to add for this extension

Seven new subcollections continue the existing numbering. They cover the topics the
residual-threshold, cross-threshold and active-plane results actually draw on:

| new subcollection | intended items (citation keys) |
|---|---|
| `16 — Low-Rank Forcing & Gramian Determinants` | `SummersEtAl2016`, `Simoncini2016`, `Antoulas2005` |
| `17 — Covariance Shape & Sphericity` | `Mauchly1940`, `Muirhead1982`, `WolkowiczStyan1980` |
| `18 — Conditional / Residual Variance` | `Lauritzen1996` |
| `19 — Modal Covariance & Heterogeneous Temperatures` | `Barucca2014`, `GodrecheLuck2019`, `FerreiraMetzBarucca2025` |
| `20 — Matrix-Analytic Machinery` | `HornJohnson2012`, `TownsendWilber2018` |
| `21 — Reconstruction / Invariant Context` | `DeJesus2026dual` |
| `22 — Reciprocal & Palindromic Algebra` | `Vieira2019` |

Add the 13 new items to `14 — Directly Cited in Repository` as well, bringing it to 25 —
`references.bib` and that subcollection are meant to agree exactly.

`15 — Closest Prior Art / Novelty Checks` should gain `SummersEtAl2016`, `Barucca2014`,
`GodrecheLuck2019` and `Mauchly1940`, bringing it to 10: these four are the sources whose
relationship to the new results most directly constrains how they may be worded.

## 4. Controlled tags

The project's existing nine tags are kept (`directly-cited`, `classical`, `closest-prior-art`,
`lyapunov-standard`, `ou-standard`, `control-theory-prior-art`, `uncertain-more-search`,
`interpretation`, `known-reparameterized`). A tag records the role a *source* plays in the
provenance matrix, not a judgement about the source.

Four further tags are proposed, and only four, to keep the vocabulary small:

| tag | meaning | items |
|---|---|---|
| `low-rank-forcing` | source bears on rank-one/low-rank forcing of a Lyapunov system | `SummersEtAl2016`, `Simoncini2016` |
| `covariance-determinant` | source bears on `det Σ`, generalized variance or log-det | `Wilks1932`, `SummersEtAl2016` |
| `sphericity` | source bears on trace/determinant shape statistics | `Mauchly1940`, `Muirhead1982`, `WolkowiczStyan1980` |
| `reciprocal-polynomial` | source bears on palindromic/self-reciprocal algebra or reciprocal invariants | `Vieira2019`, `DeJesus2026dual` |

Tags not created, deliberately: `apparently-distinct` (no *source* earns it; the classification
belongs to a repository claim, and lives in the provenance table),
`new-derivation-known-ingredients` and `formalized-known-result` (likewise claim-level), and any
per-topic synonym of the subcollection names.

## 5. Outstanding Zotero-side actions (NOT performed)

With Zotero running and the local API enabled and authorized:

1. Import only the 13 new entries, into the parent collection — **not** the whole file, which
   would duplicate the 12 items already present:
   `python3 $Z/scripts/zotero.py import-bibtex --file <subset>.bib --yes`, where `<subset>.bib`
   contains the keys listed in §3. Each Connector import creates new items, so importing
   `references.bib` wholesale would produce 37 items instead of 25.
2. Create the seven subcollections of §3 in one batched `POST /api/users/0/collections` with
   `parentCollection: SXXMUAZA`.
3. `PATCH /api/users/0/items/<key>` with `{"collections":[…]}` and the item's
   `If-Unmodified-Since-Version` to file each item. Patching **adds** membership; it does not
   copy items.
4. Apply the tags of §4 the same way.
5. Re-check: 25 distinct top-level items under the parent, no duplicates, `14 — Directly Cited`
   equal to the key list of `references.bib`.

**Do not report any of this as done until it has been done.** This file records it as
outstanding precisely because the approval dialog could not be answered from the session that
prepared the bibliography.

## 6. Bibliography export

Better BibTeX is not installed, so there is **no auto-export** and none is claimed.
`references.bib` was assembled directly from registry metadata rather than exported from Zotero:

```bash
curl -LH 'Accept: application/x-bibtex' https://doi.org/<DOI>
curl -LH 'Accept: application/vnd.citationstyles.csl+json' https://doi.org/<DOI>   # cross-check
curl -s https://zenodo.org/api/records/<id>                                        # Zenodo records
```

Validated with a throwaway document compiled outside the repository:
`pdflatex` → `bibtex` → `pdflatex` ×2 over all 25 keys — **25 `\bibitem`s, zero BibTeX
warnings**, no duplicate keys, balanced braces, every entry carrying a DOI.

If Better BibTeX is installed later, the intended configuration is: citation-key formula
`auth.capitalize + year` (which reproduces the existing keys), export of
`14 — Directly Cited in Repository` to `references.bib`, "keep updated" enabled, and
"pin citation keys" on so that keys never change silently across exports. Until then the file is
maintained by hand and the keys are fixed by this document.

## 6a. Citation policy

`references.bib` is **"directly cited only"**: every entry is cited by key in at least one
citing document of this repository, and every key cited there exists in the file. Sources
consulted during the searches but not bearing on a specific claim are **not** added; the
bibliography is meant to make the provenance traceable, not to look large. If a source is ever
retained for provenance without being cited in prose, that exception must be recorded here.

**Updated 19 September 2026 (`revise-zenodo-ou-2026-09`).** The set of citing documents now has
three members, not two: `docs/LITERATURE_REVIEW.md`, `docs/NOVELTY_AND_PROVENANCE.md`, and the
manuscript `paper/zenodo-revision-2026-09/main.tex`. The file holds **33** entries. The 8 added
in that task (`PecoraCarroll1998`, `RulkovEtAl1995`, `AbarbanelEtAl1996`, `KocarevParlitz1996`,
`AronsonEtAl1990`, `Haken1983`, `Aubin1991`, `DeJesus2026bjj`) are the works cited by the
manuscript and by no repository document, and they were verified the same way as the rest — DOI
content negotiation against Crossref/DataCite, cross-checked as CSL-JSON. The manuscript cites
24 of the 33; the remaining 9 are cited by the two `docs/` files, so there are still no orphans
in either direction.

Two entries carry a `note` recording a metadata problem rather than hiding it: `Aubin1991` (the
manuscript cites the 1991 Birkhäuser edition, but the only registered DOI resolves to the 2009
Modern Birkhäuser Classics reprint) and `DeJesus2026bjj` (DataCite returns an `@article` with no
journal and a trailing comma in the author string, which BibTeX rejects; reformatted into the
`@misc` house style used by the other Zenodo entries).

## 7. Citation keys

Existing keys are preserved exactly; they are `AuthorYear` or `AuthorEtAlYear`, with a
disambiguating suffix where an author has two entries in the same year (`DeJesus2026ou`,
`DeJesus2026dual`). New keys follow the same rule: `Barucca2014`, `GodrecheLuck2019`,
`FerreiraMetzBarucca2025`, `Mauchly1940`, `Muirhead1982`, `SummersEtAl2016`,
`TownsendWilber2018`, `WolkowiczStyan1980`, `HornJohnson2012`, `Lauritzen1996`,
`Simoncini2016`, `Vieira2019`, `DeJesus2026dual`; and, from the September revision task,
`PecoraCarroll1998`, `RulkovEtAl1995`, `AbarbanelEtAl1996`, `KocarevParlitz1996`,
`AronsonEtAl1990`, `Haken1983`, `Aubin1991`, `DeJesus2026bjj`. No key was changed, and no key is
duplicated.

## 8. Source-note template

For any source whose relationship to a repository claim is not obvious, attach a child note with
these seven headings (the same template used in the other repositories):

```text
REPOSITORY CLAIM:     what this repository asserts, and where
SOURCE RESULT:        what the source actually proves, with equation/theorem number
ASSUMPTIONS:          the source's hypotheses
CONVENTIONS:          sign/normalization conventions, and how they map onto ours
RELATIONSHIP:         standard theory reused / special case / closest prior art / distinct
EPISTEMIC STATUS:     one of the classifications used in NOVELTY_AND_PROVENANCE.md
RECOMMENDED WORDING:  conservative sentence suitable for the README or a manuscript
```

The per-claim commentary these notes would carry is written out in
[`LITERATURE_REVIEW.md`](LITERATURE_REVIEW.md) and
[`NOVELTY_AND_PROVENANCE.md`](NOVELTY_AND_PROVENANCE.md); no child notes were added to Zotero in
this pass.

## 9. Adding a new paper later

1. Verify the DOI against registry metadata **before** adding anything; never type metadata from
   a search snippet. Two corrections in this pass came from doing so (§6 of
   `LITERATURE_REVIEW.md`).
2. Add the BibTeX entry to `references.bib` with an `AuthorYear` key.
3. File it in the topical subcollection, and in `14 — Directly Cited in Repository` **only if it
   is actually cited** in the repository prose.
4. Tag it with the role it plays, not with its subject.
5. If it bears on a novelty classification, add a row to the provenance table and, if the
   relationship is subtle, write a source note using the §8 template.

## 10. PDFs

No full texts are stored in this repository and none were added to Zotero here. Publisher PDFs,
`storage/`, and `zotero.sqlite` are never committed. The two Zenodo notes are the author's own
and are openly licensed (CC BY 4.0), but even those are cited by DOI rather than copied in.
