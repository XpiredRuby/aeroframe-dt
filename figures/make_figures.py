"""
Figure generator for the F12 correlation lug sweep (AeroFrame-DT).

Regenerates the three figures used in the F12 write-up directly from the solved
sweep results, so the figures cannot drift from the numbers recorded in
docs/F12_FE_RESULTS_AF-DT-1000.md.

Outputs (SVG and PNG):
    fig1_margin_vs_eD            margin of safety vs e/D, all three failure modes
    fig2_fe_response             deformation scaling law, and bearing flatline
    fig3_plastic_strain_check    the open consistency item, section 9

Margins are computed in closed form here rather than pasted, so the plotted
curves are derived from the same expressions given in the write-up. The FE
values are the recorded solve outputs.

Requires matplotlib and numpy. Run:  python make_figures.py

SYNTHETIC_TEST_ONLY. Educational / representative / portfolio only.
Non-OEM, non-certified.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# Specimen constants
# ----------------------------------------------------------------------------
D = 26.8          # bore diameter, mm
T = 25.0          # thickness, mm
P = 284686.0      # applied load, N
SHANK = 160.8     # straight shank length below hole centre, mm
E_MOD = 71000.0   # Young's modulus, MPa
FSU = 303.0       # shear allowable, MPa
FTU = 517.0       # tensile ultimate, MPa
YIELD = 469.0     # bilinear yield, MPa
E_TAN = 760.0     # bilinear tangent modulus, MPa

# ----------------------------------------------------------------------------
# Solved sweep data - recorded FE outputs
# ----------------------------------------------------------------------------
eD = np.array([1.0, 1.2, 1.5, 1.8, 2.0])
peak_vm = np.array([750.23, 521.47, 490.45, 506.34, 503.49])    # MPa
deform = np.array([7.655, 0.896, 0.632, 0.526, 0.4817])         # mm
eps_p = np.array([0.37211, 0.03107, np.nan, 0.00888, 0.00795])  # m/m

# e/D = 1.0 peak stress requires 37% plastic strain and is not physical.
VALID = np.array([False, True, True, True, True])

# ----------------------------------------------------------------------------
# Closed-form margins
# ----------------------------------------------------------------------------
def shear_area(r):
    """Shear-out area, mm^2. Equals net area exactly, because w = 2e here."""
    return (2.0 * r * D - D) * T


def ms_shear(r):
    return FSU / (P / shear_area(r)) - 1.0


def ms_net(r):
    return FTU / (P / shear_area(r)) - 1.0


# Bearing area is D*t, independent of e/D, so this margin is constant.
MS_BEARING = FTU / (P / (D * T)) - 1.0

r_fine = np.linspace(0.95, 2.05, 2000)
cross = r_fine[np.argmin(np.abs(ms_shear(r_fine) - MS_BEARING))]
zero_cross = r_fine[np.argmin(np.abs(ms_shear(r_fine)))]

# ----------------------------------------------------------------------------
# Style
# ----------------------------------------------------------------------------
INK, RED, BLU, GRY = "#1a1a1a", "#c0392b", "#2c6fbb", "#8a8a8a"

plt.rcParams.update({
    "font.size": 10,
    "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})

CAPTION = "SYNTHETIC_TEST_ONLY - educational / representative only. Non-OEM, non-certified."
OUT = ""


def finish(fig, stem):
    fig.text(0.5, 0.005, CAPTION, ha="center", fontsize=7, color=GRY)
    fig.savefig(OUT + stem + ".svg", bbox_inches="tight")
    fig.savefig(OUT + stem + ".png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ----------------------------------------------------------------------------
# Figure 1 - margin of safety vs e/D
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.6))

ax.axhspan(-0.45, 0.0, color=RED, alpha=0.07, zorder=0)
ax.axhline(0.0, color=INK, lw=0.9, ls="--", zorder=1)

ax.plot(r_fine, ms_shear(r_fine), color=RED, lw=2.2,
        label="Shear-out (Fsu = 303 MPa)", zorder=3)
ax.axhline(MS_BEARING, color=BLU, lw=2.2,
           label="Bearing (Ftu = 517 MPa)", zorder=3)
ax.plot(r_fine, ms_net(r_fine), color=GRY, lw=1.4, ls=":",
        label="Net section (Ftu)", zorder=2)
ax.plot(eD, ms_shear(eD), "o", color=RED, ms=6, mec="white", mew=1.2, zorder=5)

ax.plot(cross, MS_BEARING, "o", ms=11, mfc="none", mec=INK, mew=1.8, zorder=6)
ax.annotate("mode crossover\ne/D = %.3f" % cross,
            xy=(cross, MS_BEARING), xytext=(cross + 0.10, MS_BEARING - 0.62),
            fontsize=9, arrowprops=dict(arrowstyle="-", color=INK, lw=0.9))
ax.annotate("zero margin\ne/D = %.3f" % zero_cross,
            xy=(zero_cross, 0.0), xytext=(zero_cross - 0.02, 0.55),
            fontsize=9, ha="center",
            arrowprops=dict(arrowstyle="-", color=INK, lw=0.9))

ax.text(1.08, -0.33, "specimen fails", color=RED, fontsize=9, style="italic")
ax.text(1.72, 0.30, "bearing governs\nmargin independent of e/D",
        color=BLU, fontsize=8.5, ha="center")

ax.set_xlim(0.95, 2.05)
ax.set_ylim(-0.45, 2.8)
ax.set_xlabel("Edge distance ratio  e / D")
ax.set_ylabel("Margin of safety")
ax.set_title("Margin of safety vs edge distance ratio\n"
             "7075-T651 straight lug, D = 26.8 mm, t = 25 mm, P = 284,686 N",
             fontsize=11, loc="left")
ax.legend(frameon=False, fontsize=9, loc="upper left")
ax.grid(alpha=0.13)
finish(fig, "fig1_margin_vs_eD")

# ----------------------------------------------------------------------------
# Figure 2 - FE response
# ----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.3))

w = 2.0 * eD * D
shank_stretch = P * SHANK / (w * T * E_MOD)
SCALE = 1.97

ax1.semilogy(eD, deform, "o-", color=RED, lw=2.0, ms=6, mec="white", mew=1.2,
             label="FE total deformation", zorder=4)
ax1.semilogy(eD, SCALE * shank_stretch, "s--", color=BLU, lw=1.6, ms=5,
             label="1.97 x shank stretch  PL/(AE)", zorder=3)
ax1.axvspan(0.95, zero_cross, color=RED, alpha=0.07, zorder=0)
ax1.text(1.09, 3.4, "plastically\ndominated", fontsize=8.5, color=RED, ha="center")

for r, d in zip(eD[2:], deform[2:]):
    ax1.annotate("%.3f" % d, xy=(r, d), xytext=(0, -15),
                 textcoords="offset points", ha="center", fontsize=8)

ax1.set_xlim(0.95, 2.05)
ax1.set_xlabel("e / D")
ax1.set_ylabel("Max total deformation  (mm)")
ax1.set_title("Elastic scaling law holds to 1.7%", fontsize=10.5, loc="left")
ax1.legend(frameon=False, fontsize=8.5, loc="upper right")
ax1.grid(alpha=0.13, which="both")

ax2.plot(eD[VALID], peak_vm[VALID], "o-", color=BLU, lw=2.0, ms=6,
         mec="white", mew=1.2, label="FE peak von Mises", zorder=4)
ax2.plot(eD[~VALID], peak_vm[~VALID], "x", color=RED, ms=9, mew=2.2,
         label="discarded, exceeds ductility", zorder=4)
ax2.axhline(YIELD, color=GRY, lw=1.3, ls="--", zorder=2)
ax2.text(1.98, YIELD - 22, "yield 469 MPa", fontsize=8.5, color=GRY, ha="right")

band = peak_vm[VALID]
ax2.axhspan(band.min(), band.max(), color=BLU, alpha=0.09, zorder=1)
ax2.annotate("flat within 6% while shear-out margin\nswings from -0.002 to +1.14",
             xy=(1.65, 540), fontsize=8.5, ha="center", color=BLU)

ax2.set_xlim(0.95, 2.05)
ax2.set_ylim(430, 800)
ax2.set_xlabel("e / D")
ax2.set_ylabel("Peak von Mises stress  (MPa)")
ax2.set_title("Bearing governs above e/D = 1.35", fontsize=10.5, loc="left")
ax2.legend(frameon=False, fontsize=8.5, loc="upper right")
ax2.grid(alpha=0.13)

fig.tight_layout()
finish(fig, "fig2_fe_response")

# ----------------------------------------------------------------------------
# Figure 3 - plastic strain consistency, open item
# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.4))

implied = (peak_vm - YIELD) / E_TAN
mask = ~np.isnan(eps_p)

ax.plot(eD[mask], implied[mask], "s--", color=BLU, lw=1.7, ms=6,
        label="implied by material card:  (sigma - 469) / 760", zorder=3)
ax.plot(eD[mask], eps_p[mask], "o-", color=RED, lw=2.0, ms=6, mec="white",
        mew=1.2, label="measured, averaged nodal result", zorder=4)
ax.set_yscale("log")

for r, a, b in zip(eD[mask], implied[mask], eps_p[mask]):
    ax.annotate("", xy=(r, b), xytext=(r, a),
                arrowprops=dict(arrowstyle="<->", color=GRY, lw=1.0))
    ax.annotate("%.2fx" % (b / a), xy=(r, np.sqrt(a * b)), xytext=(7, 0),
                textcoords="offset points", fontsize=8.5, color=GRY, va="center")

ax.set_xlim(0.95, 2.05)
ax.set_xlabel("e / D")
ax.set_ylabel("Equivalent plastic strain  (m/m)")
ax.set_title("OPEN ITEM - plastic strain vs peak stress consistency\n"
             "Agreement is near-exact where the plastic zone is large, and "
             "degrades as it shrinks",
             fontsize=10.5, loc="left")
ax.legend(frameon=False, fontsize=9, loc="lower left")
ax.grid(alpha=0.13, which="both")
finish(fig, "fig3_plastic_strain_check")

# ----------------------------------------------------------------------------
# Console summary - these are the numbers quoted in the write-up
# ----------------------------------------------------------------------------
print("crossover   e/D = %.4f" % cross)
print("zero margin e/D = %.4f" % zero_cross)
print("MS bearing      = %+.4f" % MS_BEARING)
print()
print("%-6s %10s %10s %12s %10s" % ("e/D", "MS_shear", "MS_net", "stretch_mm", "ratio"))
for r, d in zip(eD, deform):
    st = P * SHANK / (2.0 * r * D * T * E_MOD)
    print("%-6.1f %10.4f %10.4f %12.4f %10.3f" % (r, ms_shear(r), ms_net(r), st, d / st))
