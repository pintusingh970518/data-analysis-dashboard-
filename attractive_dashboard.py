"""
Modern Attractive Sales Dashboard - Pandas + Matplotlib
==========================================================
Dark theme, KPI cards, gradient styling
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ---------------------------------------------------------
# STEP 1: DATA LOAD & PREPARE
# ---------------------------------------------------------
df = pd.read_csv("sales_data.csv", parse_dates=["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

region_revenue = df.groupby("region")["revenue"].sum().sort_values(ascending=False)
product_units = df.groupby("product")["units_sold"].sum().sort_values(ascending=False)
monthly_revenue = df.groupby("month")["revenue"].sum()
pivot = df.pivot_table(index="region", columns="product", values="revenue", aggfunc="sum")

total_revenue = df["revenue"].sum()
total_units = df["units_sold"].sum()
avg_order_value = df["revenue"].mean()
top_region = region_revenue.index[0]

# ---------------------------------------------------------
# STEP 2: COLOR THEME (dark, modern, gradient-friendly)
# ---------------------------------------------------------
BG = "#0f1117"
CARD_BG = "#1a1d29"
ACCENT1 = "#00d4ff"   # cyan
ACCENT2 = "#7c5cff"   # purple
ACCENT3 = "#ff6b9d"   # pink
ACCENT4 = "#00e5a0"   # green
TEXT_COLOR = "#e8e9ed"
SUBTEXT_COLOR = "#8b8fa3"
GRID_COLOR = "#2a2e3d"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": TEXT_COLOR,
    "axes.labelcolor": TEXT_COLOR,
    "xtick.color": SUBTEXT_COLOR,
    "ytick.color": SUBTEXT_COLOR,
})

# ---------------------------------------------------------
# STEP 3: FIGURE + GRID LAYOUT (KPI row + 4 charts)
# ---------------------------------------------------------
fig = plt.figure(figsize=(16, 11), facecolor=BG)
gs = fig.add_gridspec(3, 4, height_ratios=[0.6, 1.2, 1.2], hspace=0.55, wspace=0.35,
                       left=0.05, right=0.97, top=0.90, bottom=0.06)

fig.suptitle("SALES ANALYTICS DASHBOARD", fontsize=24, fontweight="bold",
             color=TEXT_COLOR, x=0.05, ha="left", y=0.97)
fig.text(0.05, 0.935, "Yearly performance overview • 2025", fontsize=11, color=SUBTEXT_COLOR)

# ---- KPI CARDS ----
kpis = [
    ("TOTAL REVENUE", f"₹{total_revenue/1e7:.2f} Cr", ACCENT1),
    ("UNITS SOLD", f"{total_units:,}", ACCENT2),
    ("AVG ORDER VALUE", f"₹{avg_order_value:,.0f}", ACCENT3),
    ("TOP REGION", top_region, ACCENT4),
]

for i, (label, value, color) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.set_facecolor(CARD_BG)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    # rounded card background
    ax.add_patch(FancyBboxPatch((0.02, 0.1), 0.96, 0.8, boxstyle="round,pad=0.02,rounding_size=0.08",
                                 transform=ax.transAxes, facecolor=CARD_BG, edgecolor=color, linewidth=1.5))
    ax.text(0.5, 0.62, value, transform=ax.transAxes, fontsize=19, fontweight="bold",
            color=color, ha="center", va="center")
    ax.text(0.5, 0.28, label, transform=ax.transAxes, fontsize=9.5,
            color=SUBTEXT_COLOR, ha="center", va="center", fontweight="medium")

# ---- CHART 1: Region-wise Revenue (Horizontal gradient bar) ----
ax1 = fig.add_subplot(gs[1, 0:2])
ax1.set_facecolor(CARD_BG)
colors_bar = [ACCENT1, ACCENT2, ACCENT3, ACCENT4]
bars = ax1.barh(region_revenue.index[::-1], region_revenue.values[::-1],
                 color=colors_bar[::-1], height=0.55, edgecolor="none")
for bar, val in zip(bars, region_revenue.values[::-1]):
    ax1.text(val + total_revenue*0.005, bar.get_y() + bar.get_height()/2, f"₹{val/1e6:.1f}M",
              va="center", fontsize=10, color=TEXT_COLOR, fontweight="bold")
ax1.set_title("Revenue by Region", fontsize=13, fontweight="bold", color=TEXT_COLOR, loc="left", pad=12)
ax1.grid(axis="x", color=GRID_COLOR, linewidth=0.7)
ax1.set_axisbelow(True)
for spine in ["top", "right", "left"]:
    ax1.spines[spine].set_visible(False)
ax1.spines["bottom"].set_color(GRID_COLOR)
ax1.tick_params(left=False)

# ---- CHART 2: Product Share (Donut chart) ----
ax2 = fig.add_subplot(gs[1, 2:4])
ax2.set_facecolor(CARD_BG)
wedges, texts, autotexts = ax2.pie(
    product_units.values, labels=None, autopct="%1.0f%%", startangle=90,
    colors=[ACCENT1, ACCENT2, ACCENT3, ACCENT4],
    wedgeprops=dict(width=0.42, edgecolor=CARD_BG, linewidth=3),
    pctdistance=0.79, textprops={"fontsize": 10, "fontweight": "bold", "color": BG}
)
ax2.legend(wedges, product_units.index, loc="center left", bbox_to_anchor=(1.0, 0.5),
           frameon=False, labelcolor=TEXT_COLOR, fontsize=10)
ax2.text(0, 0, f"{total_units:,}\nunits", ha="center", va="center",
          fontsize=13, fontweight="bold", color=TEXT_COLOR)
ax2.set_title("Product-wise Units Sold", fontsize=13, fontweight="bold", color=TEXT_COLOR, loc="left", pad=12)

# ---- CHART 3: Monthly Trend (area + line, glow effect) ----
ax3 = fig.add_subplot(gs[2, 0:3])
ax3.set_facecolor(CARD_BG)
x = range(len(monthly_revenue))
y = monthly_revenue.values
ax3.plot(x, y, color=ACCENT1, linewidth=2.5, marker="o", markersize=5,
          markerfacecolor=BG, markeredgecolor=ACCENT1, markeredgewidth=2, zorder=3)
ax3.fill_between(x, y, min(y)*0.9, color=ACCENT1, alpha=0.15, zorder=1)
ax3.set_xticks(list(x))
ax3.set_xticklabels(monthly_revenue.index, rotation=40, fontsize=9)
ax3.set_title("Monthly Revenue Trend", fontsize=13, fontweight="bold", color=TEXT_COLOR, loc="left", pad=12)
ax3.grid(axis="y", color=GRID_COLOR, linewidth=0.7)
ax3.set_axisbelow(True)
for spine in ["top", "right", "left"]:
    ax3.spines[spine].set_visible(False)
ax3.spines["bottom"].set_color(GRID_COLOR)
ax3.tick_params(left=False)
ax3.set_yticklabels([])

# ---- CHART 4: Region vs Product Heatmap (compact) ----
ax4 = fig.add_subplot(gs[2, 3])
ax4.set_facecolor(CARD_BG)
im = ax4.imshow(pivot.values, cmap="magma", aspect="auto")
ax4.set_xticks(range(len(pivot.columns)))
ax4.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=8)
ax4.set_yticks(range(len(pivot.index)))
ax4.set_yticklabels(pivot.index, fontsize=8)
ax4.set_title("Region × Product", fontsize=13, fontweight="bold", color=TEXT_COLOR, loc="left", pad=12)
for spine in ax4.spines.values():
    spine.set_visible(False)

fig.savefig("attractive_dashboard.png", dpi=160, facecolor=BG, bbox_inches="tight")
print("Saved: attractive_dashboard.png")
