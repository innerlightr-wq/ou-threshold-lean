# Literature provenance audit — inertial OU reciprocity theorem

**Publication status**: the manuscript this audit supports is published.
Elias De Jesús. (2026). *Reciprocal Covariance Pencils and
Equal-Specific-Damping Symmetry in Two-Mode Inertial
Ornstein–Uhlenbeck Systems.* Zenodo. DOI:
[10.5281/zenodo.22866116](https://doi.org/10.5281/zenodo.22866116).

Targeted literature and provenance audit performed to make
`paper/inertial/main.tex` ready for public deposition. This is not an
exhaustive systematic review; it is a targeted search sufficient to
identify classical background, close model precedents, and known
mathematical tools, and to flag anything requiring attribution or
framing changes before deposit. See §"Search strategy" below for exactly
what was and was not searched.

## Search strategy

Web search (general search engine results, no restricted database access)
was used with combinations of the terms in each Literature Question of
the audit brief. Sources were filtered to original research articles,
arXiv preprints, SIAM/IEEE-class venues, and standard textbooks;
Wikipedia and similar tertiary sources were used only to locate
terminology and were not cited in the manuscript. No paywalled source was
read beyond its abstract/search-result summary except where a full-text
mirror (PMC) was available. This audit does not constitute a systematic
literature review and does not claim completeness; absence of a source in
this audit is reported as "no exact match identified in literature
searched," never as proof of novelty.

## Prior-art matrix

| Claim / ingredient | Closest source | Year | What source actually proves | Relation to this manuscript | Classification |
|---|---|---|---|---|---|
| Stationary covariance of a stable linear system solves a continuous Lyapunov equation; controllability determines positive definiteness | Kailath, *Linear Systems*, Prentice-Hall | 1980 | Standard linear-systems-theory treatment of the Lyapunov equation, controllability Gramian, and the Kalman rank criterion | Used directly for Lemma 1 (Model/Pencil section); routine background, not specific to OU or to this model | CLASSICAL BACKGROUND |
| Stationary covariance of an Ornstein–Uhlenbeck process via $\Sigma=\int_0^\infty e^{At}Qe^{A^Tt}dt$ / Lyapunov equation | Standard stochastic-processes treatment (e.g. as surveyed on Wikipedia's Ornstein–Uhlenbeck process page and standard SDE texts) | — | Same Lyapunov-equation fact specialized to the OU/Langevin setting | Used directly, Section 2–3 of the manuscript | CLASSICAL BACKGROUND |
| Two coupled damped harmonic oscillators, each with its own position/momentum, each driven by an independent heat bath at its own temperature, stationary covariance via the Lyapunov equation | Boffi, T. & De Gregorio, P., "Variance Resonance in Weakly Coupled Harmonic Oscillators Driven by Thermal Gradients," *Entropy* 26(12), 1087 (2024), DOI: 10.3390/e26121087 | 2024 | Solves the exact same class of model (4×4 inertial state, two independent baths, Lyapunov equation for the stationary covariance) with **uniform** damping $\gamma$ fixed as a modeling choice; studies a resonance phenomenon in the covariance entries as coupling strength varies, not palindromicity, reciprocal spectra, or damping-ratio criteria | Closest identified model precedent for the underlying inertial two-bath Langevin setup (Section 2–3); does not address this manuscript's central question | MODEL-SPECIFIC PRECEDENT |
| Palindromic/self-reciprocal polynomials; reduction of an even-degree self-reciprocal polynomial via $w=x+1/x$ to a polynomial of half the degree; roots pair as $x,1/x$ | Classical theory of reciprocal equations (19th-century algebra; covered in standard polynomial-algebra references) | — | The substitution and the reciprocal-root pairing fact are classical | Used directly, Section 11 of the manuscript | CLASSICAL BACKGROUND |
| Structured ("T-palindromic") matrix pencils $A+zA^{\mathsf T}$ and their reciprocal eigenvalue pairing | Mackey, D.S., Mackey, N., Mehl, C., Mehrmann, V., "Structured Polynomial Eigenvalue Problems: Good Vibrations from Good Linearizations," SIAM J. Matrix Anal. Appl. 28(4), 1029–1051 (2006) | 2006 | Establishes the general theory of palindromic/structured matrix polynomials and their linearizations, where reciprocal eigenvalue pairing follows from an explicit structural relation between the pencil's two matrices (e.g. $B=A^{\mathsf T}$) | **Important distinction**: this manuscript's pencil $sC_1+C_2$ has no such a priori structural relation between $C_1,C_2$ (they are independently obtained from two different Lyapunov equations); palindromicity here is a *derived, parameter-dependent, coefficient-level* condition ($c_4=c_0,c_3=c_1$), not an imposed structural (T-palindromic) one. The classical theory explains *why* reciprocal eigenvalue pairing and coefficient palindromicity are equivalent once palindromicity holds (Section 10), but does not predict *when* it holds for this specific two-bath model | KNOWN TOOL / REPARAMETERIZATION |
| Log-determinant ratio of two covariance/Gramian matrices as a scalar comparator; its monotonicity in a system parameter | General log-determinant literature (differential entropy estimation, information geometry, matrix-monotonicity results) | various | Established general facts about log-determinants of covariance matrices in unrelated contexts (entropy estimation, sample covariance asymptotics) | No source found studying $\log(\det C_2/\det C_1)$ specifically as a function of a damping-ratio parameter for a two-bath linear oscillator pencil | NO EXACT MATCH IDENTIFIED IN SEARCHED LITERATURE |
| Equal specific damping ($\gamma_1/m_1=\gamma_2/m_2$) as a criterion for covariance-determinant/spectral symmetry in coupled damped oscillators | — | — | Searches for "equal specific damping," "equal damping rate," "friction-to-mass ratio," "proportional damping," and related terms returned only generic coupled-oscillator/vibration-engineering literature (frequency tuning, modal damping design), none addressing a mass-normalized damping-ratio criterion for stationary-covariance reciprocal symmetry | Central criterion of Theorem 2; not found elsewhere in the searched literature | NO EXACT MATCH IDENTIFIED IN SEARCHED LITERATURE |
| $P(s)=\det(sC_1+C_2)$ palindromic iff $\gamma_1/m_1=\gamma_2/m_2$, for this exact two-mode inertial OU model | — | — | Not located in any source searched | Central theorem (Theorem 2) of this manuscript | NO EXACT MATCH IDENTIFIED IN SEARCHED LITERATURE |
| Global monotonicity $\partial_{\delta_1}\log(\det C_2/\det C_1)<0$ | General Lyapunov-sensitivity / Gramian-monotonicity theory exists (e.g. monotonicity of controllability Gramians under parameter changes is a known general theme in control theory) | — | General sensitivity results exist in the literature, but a search for a directly applicable general theorem yielding this specific determinant-ratio monotonicity for this pencil did not locate one | Related to known general theory (Lyapunov/Gramian sensitivity analysis) but not a direct instance of a located general theorem; classified conservatively | B: RELATED TO KNOWN GENERAL THEORY, NOT DIRECTLY IMPLIED (see manuscript wording) |
| Universal balance slope $F'|_{\delta_1=\delta_2=\delta}=-4/\delta$ | — | — | Not located in any source searched; no general theorem found explaining the exact frequency/coupling cancellation outside this manuscript's own structural derivation (Section 6) | Proposition 1 of this manuscript | NO EXACT MATCH IDENTIFIED IN SEARCHED LITERATURE |
| First-order OU heterogeneity-threshold companion result | De Jesús, E., "Heterogeneity-Driven Expansion and Synchronization Collapse in Coupled Ornstein–Uhlenbeck Systems," Zenodo (2026), DOI: 10.5281/zenodo.22059089 | 2026 | Same author's related but distinct first-order (2×2 covariance) result, already cited | Companion reference, Section 1 and 12.1 of the manuscript | CLASSICAL BACKGROUND (self-citation, already present) |

## Summary judgment

No exact prior formulation of the central theorem (Theorem 2), the
oriented comparator (Theorem 1), or the balance-slope proposition
(Proposition 1) was identified in the literature searched. The underlying
*machinery* — Lyapunov-equation stationary covariances, controllability-
implies-positive-definiteness, palindromic/reciprocal polynomial algebra,
and structured matrix-pencil eigenvalue theory — is classical or a known
tool, and is cited as such. The closest identified model precedent
(Boffi & De Gregorio 2024) studies the same general class of two-bath
inertial Langevin system but a different phenomenon (variance resonance
under fixed uniform damping, not a damping-ratio reciprocity criterion),
and is cited to correctly situate the model rather than to claim
independence from all related work.

This audit did **not** find grounds to reopen, weaken, or restrict any
mathematical claim in the manuscript. It found grounds to (a) add
citations for classical background and known tools, (b) add one model-
precedent citation and an explicit paragraph distinguishing this
manuscript's model and question from it, and (c) tighten a few phrases
that could be read as implying the reciprocal-coordinate or palindromic-
pencil machinery itself is introduced here, when it is classical/known.
See the manuscript diff for exact wording changes.
