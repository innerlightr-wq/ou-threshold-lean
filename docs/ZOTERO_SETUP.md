# Zotero: library structure for this project

**Status as of 19 September 2026 (second pass — the library is now filed).** The Zotero-side
actions that §5 previously listed as outstanding **have been carried out**. Zotero 10.0.3 was
running, its local API was enabled, and write access was granted through the
`POST /api/local/authorize` approval dialog, which a human answered. The OU collection now holds
**33 items in 23 subcollections**, matching [`../references.bib`](../references.bib) one-for-one.
Better BibTeX **is now installed** (9.0.64) and every citation key is pinned.

The authoritative bibliographic record for the repository is still
[`../references.bib`](../references.bib), which is **hand-maintained, not generated**. Auto-export
was deliberately **not** configured; §6 records the dry-run comparison that decided this.

*Historical note.* The first pass could not write to Zotero at all — the application was not
running, the local API was unreachable, and everything marked *verified* there was read from a
**copy** of `~/Zotero/zotero.sqlite` taken while the application was closed. That constraint no
longer applies, but the rule below does: `zotero.sqlite` is never edited directly.

## 1. Installation and access (verified)

| | |
|---|---|
| Zotero | **10.0.3** (`zotero-bin 10.0.3-1`), installed from the distribution package |
| data directory | `~/Zotero/` (database `~/Zotero/zotero.sqlite`) |
| profile directory | `~/.zotero/zotero/5lik04lk.default/` — **plugins and the remembered API key live here, not in the data directory** |
| process state | **running** |
| local API | **enabled and writable**; `Zotero-Server-ID: o4GPd5AO2djD` |
| Better BibTeX | **installed and active**, 9.0.64 (`better-bibtex@iris-advies.com`) |
| sync | **not signed in** — `prefs.js` holds no `sync.*` keys, so there is no cloud sync and none is claimed |

The local-API procedure itself is unchanged from the other repositories and is documented in
`strain-vorticity-comparator-dynamics/docs/ZOTERO_SETUP.md` §§2–3: enable
`extensions.zotero.httpServer.localAPI.enabled`, read `Zotero-Server-ID` from `GET /api/`,
`POST /api/local/authorize` — **which blocks on a GUI approval dialog** — then send
`Zotero-API-Key` on writes. Send `Zotero-Server-ID` on **every** request, including reads that
write nothing; without it the write endpoints answer `428 Zotero-Server-ID not provided`, which
is easy to mistake for the API being read-only.

The dialog still needs a human, so issue the authorize request in the background and ask for the
click. It answers `{"key": …, "remember": true}` and the grant is stored in the **profile**
directory as `localAPIKeys.json`, so it survives restarts: a later session should attempt a write
before prompting again.

`zotero.sqlite` must never be edited directly, and must not be copied or read while Zotero is
running.

## 2. Library for this project (verified)

Parent collection **`OU Threshold — Heterogeneity and Coupling`** (key `SXXMUAZA`). It now holds
**23 subcollections** and **33 distinct items**, matching `references.bib` one-for-one (§5).

The table below is the **starting** state recorded by the first pass — 16 subcollections and 12
items, matching the 12 original entries of `references.bib`. It is kept as the baseline that §5's
changes were applied to; for current contents see §5.

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

## 3. Subcollections added for this extension (created — see §5)

Seven new subcollections continue the existing numbering. They cover the topics the
residual-threshold, cross-threshold and active-plane results actually draw on. All seven were
**created on 19 September 2026** and populated exactly as specified here:

| subcollection | items (citation keys) |
|---|---|
| `16 — Low-Rank Forcing & Gramian Determinants` | `SummersEtAl2016`, `Simoncini2016`, `Antoulas2005` |
| `17 — Covariance Shape & Sphericity` | `Mauchly1940`, `Muirhead1982`, `WolkowiczStyan1980` |
| `18 — Conditional / Residual Variance` | `Lauritzen1996` |
| `19 — Modal Covariance & Heterogeneous Temperatures` | `Barucca2014`, `GodrecheLuck2019`, `FerreiraMetzBarucca2025` |
| `20 — Matrix-Analytic Machinery` | `HornJohnson2012`, `TownsendWilber2018` |
| `21 — Reconstruction / Invariant Context` | `DeJesus2026dual` |
| `22 — Reciprocal & Palindromic Algebra` | `Vieira2019` |

The 13 new items were added to `14 — Directly Cited in Repository` as well. That brought it to 25
at the time this section was written; it now stands at **33**, because the eight manuscript
references were filed later in the same pass — `references.bib` and that subcollection are meant
to agree exactly, and they do.

`15 — Closest Prior Art / Novelty Checks` gained `SummersEtAl2016`, `Barucca2014`,
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

## 5. Zotero-side actions (COMPLETED 19 September 2026)

All of the following were carried out through the authorized local API and then verified by
reading the library back. Item keys are recorded so the work is auditable.

**Seven subcollections created** under `SXXMUAZA`, continuing the existing numbering, exactly as
§3 specifies: `16` (`HPK4TYHX`), `17` (`KY86S9ZC`), `18` (`HDIYMRGC`), `19` (`9S3NMPKX`),
`20` (`A2STA9TV`), `21` (`YDEFLBU9`), `22` (`QU9BJ7J9`). Total 16 → **23**.

**Twenty items created**, 0 failed. Two entries were *filed rather than imported*, which is the
whole point of the DOI/title inventory that precedes any write:

* `WolkowiczStyan1980` already existed as `FZ96K7LK` under *Strain–Vorticity Comparator
  Dynamics*. It was added to `14` and `17`; `PATCH` adds membership, so one item now appears in
  both projects and **no duplicate was created**.
* `Antoulas2005` (`56JA99V6`, already in the OU tree) was added to `16`.

**Thirteen pre-existing items patched** to pin citation keys, plus the §3/§4 memberships and
tags. One metadata repair: `DeJesus2026ou` (`4L5K6XCQ`) carried the malformed DataCite creator
`firstName: ", Elias"`, corrected to `Elias` / `De Jesús`.

**Citation keys are pinned.** Writing an `extra` line `Citation Key: <key>` causes Zotero 10 to
absorb it into a first-class **`citationKey` field** — the `extra` line disappears, which looks
like a failed write but is not. All 33 are pinned, and Better BibTeX reports all 33 unchanged
(its own formula would have produced lowercase `barucca2014` rather than `Barucca2014`, so the
pins are demonstrably being honoured).

**Tags applied** exactly as §4 specifies, and nothing beyond it: `directly-cited` on all 33 (the
established convention — all 12 original items carried it), plus `low-rank-forcing` ×2,
`covariance-determinant` ×2, `sphericity` ×3, `reciprocal-polynomial` ×2. No provenance tag was
assigned by inference: `NOVELTY_AND_PROVENANCE.md` assigns tags at the *claim* level, not per
source, so there was no basis for more.

**Verification.** 33 bib entries ↔ 33 items ↔ 33 in `14 — Directly Cited`, no orphans in either
direction, **no duplicate DOIs, no duplicate citation keys**, and all 33 agree with
`references.bib` on title, year, DOI and author list. `15 — Closest Prior Art` went 6 → **10** as
§3 requires. `13 — Lean / Formalization Context` remains deliberately empty.

### 5a. Still outstanding

1. **Eight references have no topical subcollection.** `PecoraCarroll1998`, `RulkovEtAl1995`,
   `AbarbanelEtAl1996`, `KocarevParlitz1996`, `AronsonEtAl1990`, `Haken1983`, `Aubin1991` and
   `DeJesus2026bjj` are the works cited by the manuscript and by no `docs/` file. They are filed
   in `14 — Directly Cited` only, because §3 predates them and assigns them none, and inventing
   a structure was out of scope. `04 — Stochastic Synchronization` fits the four
   generalized-synchronization papers only loosely — they are deterministic. Decide whether to
   add `23 — Deterministic & Generalized Synchronization` and `24 — Viability & Synergetics
   Context`, or to widen an existing subcollection.
2. **`DeJesus2026ou` is stored as a `journalArticle`.** It is a Zenodo technical note; `preprint`
   would be accurate, and is what the two newer self-citations use. Left unchanged because
   altering an existing record's item type was not authorized. This is the direct cause of the
   `@misc → @article` regression in §6's dry run.
3. **An empty `__audit_write_test__` collection** (`S6UZDBCB`) sits at the library root, left by
   an earlier session. Harmless, deletable, not deleted here.

## 6. Bibliography export

Better BibTeX **is** installed (9.0.64), but there is **no auto-export**, deliberately.
`references.bib` was assembled directly from registry metadata rather than exported from Zotero:

```bash
curl -LH 'Accept: application/x-bibtex' https://doi.org/<DOI>
curl -LH 'Accept: application/vnd.citationstyles.csl+json' https://doi.org/<DOI>   # cross-check
curl -s https://zenodo.org/api/records/<id>                                        # Zenodo records
```

Validated with a throwaway document compiled outside the repository:
`pdflatex` → `bibtex` → `pdflatex` ×2 over all 25 keys — **25 `\bibitem`s, zero BibTeX
warnings**, no duplicate keys, balanced braces, every entry carrying a DOI.

## 6a. Citation policy

`references.bib` is **"directly cited only"**: every entry is cited by key in at least one
citing document, and every key cited there exists in the file. The citing documents are
`docs/LITERATURE_REVIEW.md`, `docs/NOVELTY_AND_PROVENANCE.md` and the manuscript
`paper/zenodo-revision-2026-09/main.tex`. The file holds **33** entries; the two `docs/` files
cite 25 and the manuscript cites 24, and the union is all 33 — checked mechanically, no orphans
in either direction.

> **Branch note.** The 33-entry state and the eight manuscript references were added on
> `revise-zenodo-ou-2026-09`. On *this* branch `references.bib` still has 25 entries, so the
> counts above describe the merged result, not this branch in isolation. Reconcile at merge;
> the two versions do not conflict (the manuscript branch's file is a superset).

Sources consulted during the searches but not bearing on a specific claim are **not** added; the
bibliography is meant to make the provenance traceable, not to look large. If a source is ever
retained for provenance without being cited in prose, that exception must be recorded here.

## 6b. Why auto-export is NOT configured (dry run, 19 September 2026)

The plan recorded here previously was to point a Better BibTeX auto-export of
`14 — Directly Cited in Repository` at `references.bib`. **That plan is rejected.** A dry export
of all 33 entries to `/tmp/ou-zotero-references.bib` was compared field-by-field against the
repository file. It agrees on the things that matter most — **33/33 entries, 33/33 citation
keys, identical DOI set, identical years, identical author lists** (one cosmetic difference:
`Maciołek` vs `Macio{\l}ek`) and identical titles once case and brace protection are
normalized. But it is **not semantically equivalent or better**, and so it must not overwrite a
hand-verified file:

| regression | scope |
|---|---|
| `note` field dropped | 5 entries — including the `Aubin1991` edition mismatch, the `Vieira2019` "Chebyshev transform" naming caution, and both Zenodo self-citation notes. **These are exactly the provenance cautions the bibliography exists to carry.** |
| `url` dropped | all 33 |
| `publisher` dropped | 12 journal articles |
| title re-cased with brace protection | all 33 — e.g. `Barucca2014` becomes `{{Ornstein-Uhlenbeck}}` in Title Case, discarding the published APS wording that the audit specifically corrected to |
| `@misc → @article` | `DeJesus2026ou`, misrepresenting a Zenodo note as a journal article (see §5a.2) |
| `journal` / `issn` dropped | `Haken1983`, `Muirhead1982` (series information) |
| `keywords` added | all 33 — exports internal provenance tags into the bibliography |

`item.export` accepts no display options, so this cannot be tuned over the API; the relevant
switches ("Title case titles", brace protection, URL export, note export) are **global Better
BibTeX preferences** set in the GUI, and they would change every other project's exports too.

**Standing decision:** `references.bib` stays **hand-maintained**. Better BibTeX is kept for what
it is genuinely good at here — stable pinned citation keys and ad-hoc exports — and is not given
write authority over the repository file. If auto-export is ever reconsidered, redo this
comparison first; do not assume a later BBT version fixes it.

## 7. Citation keys

Existing keys are preserved exactly; they are `AuthorYear` or `AuthorEtAlYear`, with a
disambiguating suffix where an author has two entries in the same year (`DeJesus2026ou`,
`DeJesus2026dual`). New keys follow the same rule: `Barucca2014`, `GodrecheLuck2019`,
`FerreiraMetzBarucca2025`, `Mauchly1940`, `Muirhead1982`, `SummersEtAl2016`,
`TownsendWilber2018`, `WolkowiczStyan1980`, `HornJohnson2012`, `Lauritzen1996`,
`Simoncini2016`, `Vieira2019`, `DeJesus2026dual`. No key was changed, and no key is duplicated.

**Keys are now pinned in Zotero itself.** Each item carries its key in Zotero's first-class
`citationKey` field, which is what Better BibTeX treats as a pin, so BBT cannot silently rename
them. To pin a key, write `Citation Key: <key>` as a line in the item's `extra` field; Zotero 10
absorbs it into `citationKey` and the `extra` line vanishes — that is expected, not a failed
write. Verified after installing BBT 9.0.64: all 33 keys reported unchanged, where BBT's own
formula would have produced `barucca2014` rather than `Barucca2014`.

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
