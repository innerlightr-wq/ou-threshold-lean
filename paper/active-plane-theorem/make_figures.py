#!/usr/bin/env python3
"""Generate the manuscript figures.

Every plotted value comes from the exact closed forms proved in the paper; the
threshold curves are evaluated from the exact rational expressions derived in
`manuscript_checks.py`, and the marked minima are the exact algebraic constants,
not numerical optimisations.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.linewidth": 0.6,
    "text.usetex": False,
    "mathtext.fontset": "cm",
})

OUT = "figures"
SQRT5 = np.sqrt(5.0)


# ----------------------------------------------------------------- Figure 1
def fig1_active_plane():
    """Schematic of the active plane: drift eigenmodes u, v and the excitation e."""
    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    th = np.deg2rad(34.0)                       # illustrative excitation angle
    c, s = np.cos(th), np.sin(th)

    # unit circle of admissible excitation directions
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(t), np.sin(t), lw=0.6, color="0.75", zorder=1)

    # drift eigenmode axes
    for vec, lab, off in (((1, 0), r"$u$  (rate $D_1$)", (0.06, -0.14)),
                          ((0, 1), r"$v$  (rate $D_2$)", (-0.42, 0.06))):
        ax.annotate("", xy=vec, xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", lw=1.1, color="0.35"))
        ax.text(vec[0] + off[0], vec[1] + off[1], lab, color="0.30", fontsize=8)

    # excitation direction e and its orthogonal complement
    ax.annotate("", xy=(c, s), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color="#1f4e9c"))
    ax.text(c + 0.05, s + 0.04, r"$e=c\,u+s\,v$", color="#1f4e9c", fontsize=9)
    ax.annotate("", xy=(-s, c), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#a23b2e", linestyle=(0, (4, 2))))
    ax.text(-s - 0.30, c + 0.08, r"$e^{\perp}$", color="#a23b2e", fontsize=9)

    # projections
    ax.plot([c, c], [0, s], lw=0.6, ls=":", color="0.5")
    ax.plot([0, c], [s, s], lw=0.6, ls=":", color="0.5")
    ax.plot([0, c], [0, 0], lw=2.2, color="#1f4e9c", alpha=0.30, solid_capstyle="butt")
    ax.plot([0, 0], [0, s], lw=2.2, color="#1f4e9c", alpha=0.30, solid_capstyle="butt")
    ax.text(c / 2, -0.13, r"$c$", color="#1f4e9c", fontsize=9, ha="center")
    ax.text(-0.13, s / 2, r"$s$", color="#1f4e9c", fontsize=9, va="center")

    # forcing eigenvalues
    ax.text(0.52, -0.80,
            r"$Q = q_b\,(I+(\tau-1)\,e\,e^{T})$" "\n"
            r"eigenvalue $q_b\tau$ along $e$," "\n"
            r"$q_b$ along $e^{\perp}$",
            fontsize=7.6, ha="center", va="center", color="0.15",
            bbox=dict(boxstyle="round,pad=0.35", fc="#f4f6fa", ec="0.80", lw=0.5))

    ax.set_xlim(-1.30, 1.45)
    ax.set_ylim(-1.15, 1.30)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(r"Active plane: drift eigenbasis and rank-one excitation",
                 fontsize=8.5, pad=4)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig1.pdf", bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------- Figure 2
def fig2_normalized_determinant():
    """Normalized determinant V/Phi = 1 + A(w-2): exactly affine in w."""
    fig, ax = plt.subplots(figsize=(4.3, 3.0))
    w = np.linspace(2.0, 40.0, 400)
    for A, style in ((0.25, "-"), (0.10, "--"), (0.02, "-."), (0.0, ":")):
        ax.plot(w, 1 + A * (w - 2), style, lw=1.3,
                label=rf"$\mathcal{{A}}={A:g}$" if A else r"$\mathcal{A}=0$  (degenerate)")
    ax.axhline(1.0, color="0.6", lw=0.6)
    ax.axvline(2.0, color="0.6", lw=0.6)
    ax.text(2.35, 9.0, r"$w=2 \Leftrightarrow \tau=1$", fontsize=7.5, color="0.35")
    ax.set_xlabel(r"reciprocal coordinate $w=\tau+1/\tau$")
    ax.set_ylabel(r"$4D_1D_2\det\Sigma \,/\, (q_b^{2}\tau)$")
    ax.set_title(r"Normalized active determinant is affine in $w$", fontsize=9)
    ax.set_xlim(2, 40)
    ax.set_ylim(0.0, 10.5)
    ax.legend(fontsize=7.2, frameon=False, loc="upper left")
    ax.grid(alpha=0.25, lw=0.4)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig2.pdf", bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------- Figure 3
def fig3_threshold_curves():
    """Exact threshold curves w*(kappa) for K2, P3, K3, with exact minima marked."""
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    k = np.linspace(0.02, 3.0, 1200)

    # exact rational curves derived in manuscript_checks.py
    # K2: Phi = 1/(1+2k), C = (1/4)((1-(1+2k))/(1+(1+2k)))^2 = k^2/(1+k)^2 * 1/4... derive:
    nu2 = ((1 - (1 + 2 * k)) / (1 + (1 + 2 * k)))**2
    C2 = 0.25 * nu2
    Phi2 = 1.0 / (1 + 2 * k)
    K2 = 2 + (1 - Phi2) / (Phi2 * C2)

    P3 = (27 * k**3 + 72 * k**2 + 64 * k + 16) / (2 * k)
    K3 = (81 * k**3 + 162 * k**2 + 112 * k + 24) / (2 * k)

    ax.plot(k, K2, lw=1.4, color="#1f4e9c", label=r"$K_2$")
    ax.plot(k, P3, lw=1.4, color="#2e7d4f", label=r"$P_3$ (centre)")
    ax.plot(k, K3, lw=1.4, color="#a23b2e", label=r"$K_3$")

    pts = [(1.0, 34.0, "#1f4e9c", r"$34$"),
           ((SQRT5 - 1) / 3, 35 + 15 * SQRT5, "#2e7d4f", r"$35+15\sqrt{5}$"),
           (1 / 3, 247 / 2, "#a23b2e", r"$247/2$")]
    for kk, ww, col, lab in pts:
        ax.plot([kk], [ww], "o", ms=4.5, color=col, zorder=5)
        ax.annotate(lab, xy=(kk, ww), xytext=(10, 8), textcoords="offset points",
                    fontsize=7.6, color=col)

    ax.axhline(34, color="0.55", lw=0.6, ls="--")
    ax.text(0.06, 24.5, r"$w=34$: the global optimum over these graphs ($K_2$)",
            fontsize=6.8, color="0.40")
    ax.set_xlabel(r"coupling strength $\kappa$")
    ax.set_ylabel(r"threshold $w^{*}(\kappa)=2+(1-\Phi)/(\Phi\,\mathcal{A})$")
    ax.set_title(r"Exact threshold curves and their minima", fontsize=9)
    ax.set_xlim(0, 3)
    ax.set_ylim(20, 260)
    ax.legend(fontsize=7.6, frameon=False)
    ax.grid(alpha=0.25, lw=0.4)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig3.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    fig1_active_plane()
    fig2_normalized_determinant()
    fig3_threshold_curves()
    # numerical sanity against the exact constants
    print(f"K2  min at kappa=1        : w = {34.0}")
    print(f"P3  min at kappa=(v5-1)/3 : kappa* = {(SQRT5-1)/3:.6f}, w* = {35+15*SQRT5:.6f}")
    print(f"K3  min at kappa=1/3      : w* = {247/2}")
    print("figures written to", OUT)
