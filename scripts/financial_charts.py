#!/usr/bin/env python3
"""
financial_charts.py — stockanalysis.com-style financial-statement visuals as
INLINE SVG, for embedding directly in a research report.

Subcommands (one chart each):
  income    Income-statement Sankey   (revenue → COGS/gross profit → opex/operating
                                        income → tax/net income, with revenue sources)
  balance   Balance-sheet Sankey      (asset components → current/LT → total assets →
                                        liabilities + equity → line items)
  cashflow  Cash-flow Sankey          (operating/investing/financing in/out-flows →
                                        CFO/CFI/CFF → free cash flow / ending cash)
  donut     Revenue donut             (by business segment OR by geography)
  dupont    5-step DuPont ROE tree    (ROE = net-margin × asset-turnover × equity-mult)

Why inline SVG (the same reasoning as scripts/gf_score.py):
  * matplotlib PNG generation was disabled project-wide on 2026-06-03 to cut the
    per-agent memory footprint — this helper imports only the stdlib (math /
    argparse), adds ~0 MB resident, and is safe inside a report agent.
  * The report viewer (reports_viewer.py → marked.js, no sanitization) injects raw
    markdown into innerHTML, so a literal <svg> block renders verbatim — the same
    untouched-raw-HTML path gf_score.py and the Step-10 <details> logs ride on.
    Paste the emitted <svg> into the report UN-FENCED (no ```), so it renders.

Sourcing discipline (load-bearing — read before use):
  * EVERY number you pass is YOUR responsibility to have read in the company's own
    10-K / 10-Q / 20-F / 年度报告 / IR deck. The helper does not fetch anything; it
    only lays out the numbers you give it. This keeps the project rule intact: every
    figure traces to a filing the agent actually read and cites in the surrounding
    prose.
  * --source is REQUIRED and is baked into a <text> footer inside the SVG, per the
    project-wide chart rule that the source must travel inside the image (charts get
    screenshotted / iframe-embedded without their caption). Cite the exact statement:
    e.g. "ISRG FY2025 10-K, Consolidated Statements of Operations + Note 4 Segment".
  * Prefer the company's OWN statements (10-K/10-Q income statement, balance sheet,
    cash-flow statement, segment note) — NOT a third-party data vendor's reshaped
    numbers. If a line item is not disclosed, omit it rather than invent it.

Values & units:
  * Pass values in whatever unit you choose with --unit {raw,k,m,b} (default m =
    millions of the reporting currency). The helper auto-formats labels to
    $X.XB / $XXXM / $X.XK so a chart can mix scales like the screenshots.
  * --currency sets the symbol (default "$"). Negatives render with a leading minus
    (cash-flow uses/outflows).

Examples
--------
Income (ISRG FY2025, US$ millions):
  financial_charts.py income \\
    --segment "Instruments & Accessories:6000" --segment "Systems:2487" \\
    --segment "Service:1576" \\
    --revenue 10063 --cogs 3423 --gross-profit 6640 \\
    --sga 2387 --rd 1308 --operating-income 2945 \\
    --net-interest 366 --pretax 3311 --tax 435 --minority 21 --net-income 2856 \\
    --title "How Intuitive Surgical (ISRG) Makes Its Money — FY2025" \\
    --source "ISRG FY2025 10-K, Consolidated Statements of Operations + Note 4 Segments"

Donut (revenue by segment):
  financial_charts.py donut --title "FY2025 Revenue by Business Segment" \\
    --center ISRG \\
    --slice "Instruments & Accessories:6000" --slice "Systems:2487" \\
    --slice "Service:1576" \\
    --source "ISRG FY2025 10-K, Note 4 — Revenue by product/service"

DuPont (annualized from 2026-Q1):
  financial_charts.py dupont \\
    --net-income 3300 --pretax 3777 --operating-income 3436 --revenue 11136 \\
    --begin-assets 20500 --end-assets 20100 \\
    --begin-equity 17800 --end-equity 17500 \\
    --note "annualized from 2026-Q1 (quarterly × 4)" \\
    --source "ISRG 2026-Q1 10-Q, Statements of Operations + Balance Sheets"
"""

import argparse
import json
import math
import sys

# ── palette ──────────────────────────────────────────────────────────────────
INK = "#1f2933"
MUTED = "#52606d"
FAINT = "#8a97a3"
WHITE = "#ffffff"
# node fills
C_IN = "#2563eb"      # blue   — revenue sources / cash inflows
C_HUB = "#1e3a8a"     # navy   — the central total node (Revenue / Total Assets / CFO)
C_PROFIT = "#15803d"  # green  — profit / equity / retained cash
C_COST = "#dc2626"    # red    — costs / liabilities / cash uses
C_NEUT = "#64748b"    # slate  — neutral intermediate
# ribbon fills (lighter; drawn with opacity)
R_IN = "#93c5fd"
R_PROFIT = "#86efac"
R_COST = "#fca5a5"
R_NEUT = "#cbd5e1"
RIBBON_OP = "0.55"

NODE_FILL = {"in": C_IN, "hub": C_HUB, "profit": C_PROFIT, "cost": C_COST, "neutral": C_NEUT}
RIBBON_FILL = {"in": R_IN, "profit": R_PROFIT, "cost": R_COST, "neutral": R_NEUT}
# donut / dupont
DONUT_PALETTE = ["#2563eb", "#15803d", "#d97706", "#7c3aed", "#dc2626", "#0891b2",
                 "#db2777", "#65a30d", "#9333ea", "#ea580c"]
DUPONT_FILL = "#2563eb"
DUPONT_INK = "#ffffff"
FONT = "Helvetica,Arial,sans-serif"


# ── small helpers ──────────────────────────────────────────────────────────────
def _xml(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _f(x):
    return f"{x:.2f}"


def _unit_mult(unit):
    return {"raw": 1.0, "k": 1e3, "m": 1e6, "b": 1e9}[unit]


def fmt_money(value_abs, currency="$"):
    """value_abs: an absolute (already unit-scaled) figure. Returns e.g. $10.1B, -$1.3B, $851.1M."""
    sign = "-" if value_abs < 0 else ""
    v = abs(float(value_abs))
    if v >= 1e12:
        body = f"{v/1e12:.1f}T"
    elif v >= 1e9:
        body = f"{v/1e9:.1f}B"
    elif v >= 1e6:
        body = f"{v/1e6:.1f}M"
    elif v >= 1e3:
        body = f"{v/1e3:.1f}K"
    elif v == 0:
        body = "0"
    else:
        body = f"{v:.0f}"
    return f"{sign}{currency}{body}"


def fmt_pct(value, ref):
    if ref == 0:
        return ""
    p = value / ref * 100.0
    return f"{p:.1f}%" if abs(p) >= 1 else f"{p:.2f}%"


def _txt(x, y, s, size=12, fill=INK, weight="400", anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{_f(x)}" y="{_f(y)}" text-anchor="{anchor}" '
            f'font-family="{FONT}" font-size="{size}" font-weight="{weight}"{st} '
            f'fill="{fill}">{_xml(s)}</text>')


def _svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{_xml(label)}">'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{WHITE}"/>')


def _footer(w, h, source, note=None):
    out = []
    y = h - 16
    if note:
        out.append(_txt(w / 2, h - 30, note, size=10, fill=FAINT, anchor="middle", italic=True))
    out.append(_txt(w / 2, y, f"Source: {source}", size=10, fill=MUTED, anchor="middle"))
    return out


# ── generic layered-Sankey engine ──────────────────────────────────────────────
class Node:
    __slots__ = ("id", "label", "value", "kind", "col", "side", "x", "y", "h",
                 "lcur", "rcur")

    def __init__(self, nid, label, value, kind, col, side=None):
        self.id = nid
        self.label = label
        self.value = float(value)
        self.kind = kind
        self.col = col
        self.side = side  # 'left'|'right'|'top'|None (None → auto by column)
        self.x = self.y = self.h = 0.0
        self.lcur = self.rcur = 0.0


def render_sankey(columns, flows, ref_value, title, source, currency="$",
                  width=1000, height=560, note=None, aria="financial Sankey"):
    """columns: list[list[Node]] ordered left→right, each inner list top→bottom.
    flows: list of (src_id, dst_id, value, kind). ref_value: denominator for %.
    Node heights ∝ value; ribbon thickness ∝ value; non-conserving flows allowed
    (a node's height is its own value; ribbons stack from the top of each edge)."""
    ncol = len(columns)
    by_id = {n.id: n for col in columns for n in col}

    M_TOP, M_BOT = 64, 46
    M_LEFT, M_RIGHT = 188, 176
    NODE_W = 16
    GAP = 14          # vertical gap between stacked nodes in a column
    LABEL_GAP = 25    # minimum vertical spacing between adjacent labels

    # adaptive height: guarantee the densest column has room to de-collide labels
    densest = max((len(c) for c in columns), default=1)
    height = max(height, M_TOP + M_BOT + densest * LABEL_GAP + 10)

    plot_h = height - M_TOP - M_BOT
    plot_w = width - M_LEFT - M_RIGHT

    # vertical scale from the fullest column (sum of node values + gaps must fit)
    col_total = max(sum(n.value for n in col) for col in columns if col)
    max_nodes = max(len(col) for col in columns)
    avail = plot_h - GAP * (max_nodes - 1)
    scale = avail / col_total if col_total else 1.0
    MIN_H = 2.0

    # x per column
    if ncol > 1:
        step = (plot_w - NODE_W) / (ncol - 1)
    else:
        step = 0
    for c, col in enumerate(columns):
        cx = M_LEFT + c * step
        total_h = sum(max(MIN_H, n.value * scale) for n in col) + GAP * (len(col) - 1)
        y = M_TOP + (plot_h - total_h) / 2.0  # vertically center each column
        for n in col:
            n.x = cx
            n.h = max(MIN_H, n.value * scale)
            n.y = y
            n.lcur = n.y
            n.rcur = n.y
            y += n.h + GAP

    out = [_svg_open(width, height, aria)]
    if title:
        out.append(_txt(20, 30, title, size=15, weight="700", fill=INK))

    # ribbons first (under nodes). sort to reduce crossings: by src.y then dst.y
    fsorted = sorted(flows, key=lambda fl: (by_id[fl[0]].y, by_id[fl[1]].y))
    for src_id, dst_id, val, kind in fsorted:
        s, d = by_id[src_id], by_id[dst_id]
        t = max(MIN_H, float(val) * scale)
        x0, y0 = s.x + NODE_W, s.rcur
        x1, y1 = d.x, d.lcur
        s.rcur += t
        d.lcur += t
        dx = x1 - x0
        cx0 = x0 + dx * 0.5
        cx1 = x1 - dx * 0.5
        path = (f"M {_f(x0)},{_f(y0)} "
                f"C {_f(cx0)},{_f(y0)} {_f(cx1)},{_f(y1)} {_f(x1)},{_f(y1)} "
                f"L {_f(x1)},{_f(y1+t)} "
                f"C {_f(cx1)},{_f(y1+t)} {_f(cx0)},{_f(y0+t)} {_f(x0)},{_f(y0+t)} Z")
        out.append(f'<path d="{path}" fill="{RIBBON_FILL.get(kind, R_NEUT)}" '
                   f'fill-opacity="{RIBBON_OP}"/>')

    # node rectangles
    for c, col in enumerate(columns):
        for n in col:
            out.append(f'<rect x="{_f(n.x)}" y="{_f(n.y)}" width="{NODE_W}" '
                       f'height="{_f(n.h)}" rx="1.5" fill="{NODE_FILL.get(n.kind, C_NEUT)}"/>')

    # ── labels with per-(column,side) vertical de-collision ──
    specs = []  # (col_idx, side, node, name, valline)
    for c, col in enumerate(columns):
        for n in col:
            side = n.side or ("left" if c == 0 else ("right" if c == ncol - 1 else "top"))
            pct = fmt_pct(n.value, ref_value)
            val_line = f"{fmt_money(n.value, currency)}  ({pct})" if pct else fmt_money(n.value, currency)
            specs.append((c, side, n, n.label, val_line))

    groups = {}
    for s in specs:
        groups.setdefault((s[0], s[1]), []).append(s)

    y_lo, y_hi = M_TOP + 12, height - M_BOT - 12
    for (c, side), items in groups.items():
        items.sort(key=lambda s: s[2].y)
        # greedy push-down from each label's natural anchor
        prev = -1e9
        placed = []
        for _, _, n, name, val in items:
            natural = (n.y - 6) if side == "top" else (n.y + n.h / 2 - 3)
            y = max(natural, prev + LABEL_GAP)
            placed.append([n, name, val, y, natural])
            prev = y
        # if the group overflowed the bottom, shift it up (bounded by the top)
        overflow = (placed[-1][3] + 12) - y_hi
        if overflow > 0:
            shift = min(overflow, placed[0][3] - y_lo)
            if shift > 0:
                for p in placed:
                    p[3] -= shift
        for n, name, val, y, natural in placed:
            if side == "left":
                lx = n.x - 9
                if abs(y - (n.y + n.h / 2)) > 6:  # displaced → leader line
                    out.append(f'<line x1="{_f(n.x)}" y1="{_f(n.y + n.h/2)}" '
                               f'x2="{_f(lx + 3)}" y2="{_f(y - 3)}" stroke="#cbd5e1" stroke-width="1"/>')
                out.append(_txt(lx, y, name, size=11.5, weight="700", fill=INK, anchor="end"))
                out.append(_txt(lx, y + 13, val, size=10, fill=MUTED, anchor="end"))
            elif side == "right":
                rx = n.x + NODE_W + 9
                if abs(y - (n.y + n.h / 2)) > 6:
                    out.append(f'<line x1="{_f(n.x + NODE_W)}" y1="{_f(n.y + n.h/2)}" '
                               f'x2="{_f(rx - 3)}" y2="{_f(y - 3)}" stroke="#cbd5e1" stroke-width="1"/>')
                out.append(_txt(rx, y, name, size=11.5, weight="700", fill=INK, anchor="start"))
                out.append(_txt(rx, y + 13, val, size=10, fill=MUTED, anchor="start"))
            else:  # top — white halo so the label stays readable over ribbons
                tx = n.x + NODE_W + 6
                wdt = max(len(name), len(val)) * 6.3 + 6
                out.append(f'<rect x="{_f(tx - 3)}" y="{_f(y - 12)}" width="{_f(wdt)}" '
                           f'height="26" rx="2" fill="{WHITE}" fill-opacity="0.72"/>')
                out.append(_txt(tx, y, name, size=11.5, weight="700", fill=INK, anchor="start"))
                out.append(_txt(tx, y + 13, val, size=10, fill=MUTED, anchor="start"))

    out += _footer(width, height, source, note)
    out.append("</svg>")
    return "\n".join(out)


# ── presets ─────────────────────────────────────────────────────────────────────
def _parse_pairs(items, n_min=2, n_max=3):
    """'Label:value[:group]' → list of tuples (label, float, group_or_None)."""
    res = []
    for s in items:
        parts = s.split(":")
        if len(parts) < n_min or len(parts) > n_max:
            raise ValueError(f"expected 'Label:value[:group]', got {s!r}")
        label = parts[0].strip()
        val = float(parts[1])
        grp = parts[2].strip().lower() if len(parts) > 2 else None
        res.append((label, val, grp))
    return res


def build_income(a):
    u = _unit_mult(a.unit)
    rev = a.revenue * u
    cogs = (a.cogs if a.cogs is not None else (a.revenue - a.gross_profit)) * u
    gp = (a.gross_profit if a.gross_profit is not None else (a.revenue - a.cogs)) * u
    sga = (a.sga or 0) * u
    rd = (a.rd or 0) * u
    other_opex = (a.other_opex or 0) * u
    opex = sga + rd + other_opex
    opinc = (a.operating_income if a.operating_income is not None else (a.revenue - a.cogs - (a.sga or 0) - (a.rd or 0) - (a.other_opex or 0))) * u
    net_int = (a.net_interest or 0) * u
    tax = (a.tax or 0) * u
    minority = (a.minority or 0) * u
    pretax = (a.pretax if a.pretax is not None else (opinc / u + net_int / u + (a.other_income or 0))) * u
    other_income = (a.other_income or 0) * u
    ni = (a.net_income if a.net_income is not None else (pretax / u - (a.tax or 0) - (a.minority or 0))) * u

    cols = [[] for _ in range(6)]
    flows = []
    # col0 segments → col1 Revenue
    segs = _parse_pairs(a.segment) if a.segment else []
    if segs:
        for i, (lbl, v, _) in enumerate(segs):
            cols[0].append(Node(f"seg{i}", lbl, v * u, "in", 0))
            flows.append((f"seg{i}", "rev", v * u, "in"))
    cols[1].append(Node("rev", "Revenue", rev, "hub", 1, side="top"))
    # col2: gross profit (continuing) + COGS (cost)
    cols[2].append(Node("gp", "Gross Profit", gp, "profit", 2))
    cols[2].append(Node("cogs", "Cost of Revenue (COGS)", cogs, "cost", 2))
    flows.append(("rev", "gp", gp, "profit"))
    flows.append(("rev", "cogs", cogs, "cost"))
    # col3: operating income + total operating expense (+ net interest feeder)
    cols[3].append(Node("opinc", "Operating Income", opinc, "profit", 3))
    cols[3].append(Node("opex", "Total Operating Expense", opex, "cost", 3))
    flows.append(("gp", "opinc", opinc, "profit"))
    flows.append(("gp", "opex", opex, "cost"))
    if net_int > 0:
        cols[3].append(Node("nint", "Net Interest / Other Income", net_int, "in", 3, side="left"))
        flows.append(("nint", "pretax", net_int, "in"))
    # col4: pretax + opex children (SG&A, R&D, other)
    cols[4].append(Node("pretax", "Pretax Income", pretax, "profit", 4))
    flows.append(("opinc", "pretax", opinc, "profit"))
    if sga > 0:
        cols[4].append(Node("sga", "SG&A", sga, "cost", 4, side="top"))
        flows.append(("opex", "sga", sga, "cost"))
    if rd > 0:
        cols[4].append(Node("rd", "R&D", rd, "cost", 4, side="top"))
        flows.append(("opex", "rd", rd, "cost"))
    if other_opex > 0:
        cols[4].append(Node("oopex", "Other OpEx", other_opex, "cost", 4, side="top"))
        flows.append(("opex", "oopex", other_opex, "cost"))
    # col5: net income + tax + minority
    cols[5].append(Node("ni", "Net Income", ni, "profit", 5))
    flows.append(("pretax", "ni", ni, "profit"))
    if tax != 0:
        cols[5].append(Node("tax", "Income Tax", tax, "cost", 5))
        flows.append(("pretax", "tax", tax, "cost"))
    if minority != 0:
        cols[5].append(Node("min", "Minority Interest", minority, "cost", 5))
        flows.append(("pretax", "min", minority, "cost"))

    cols = [c for c in cols if c]
    return cols, flows, rev


def build_balance(a):
    u = _unit_mult(a.unit)
    assets = _parse_pairs(a.asset, n_min=3, n_max=3) if a.asset else []
    liabs = _parse_pairs(a.liability, n_min=3, n_max=3) if a.liability else []
    equities = _parse_pairs(a.equity, n_min=2, n_max=2) if a.equity else []
    minority = (a.minority or 0) * u

    cur_a = sum(v for _, v, g in assets if g == "current") * u
    lt_a = sum(v for _, v, g in assets if g == "lt") * u
    total_a = cur_a + lt_a
    cur_l = sum(v for _, v, g in liabs if g == "current") * u
    lt_l = sum(v for _, v, g in liabs if g == "lt") * u
    total_l = cur_l + lt_l
    sh_eq = sum(v for _, v, _ in equities) * u
    total_eq = sh_eq + minority

    cols = [[] for _ in range(6)]
    flows = []
    # col0 components → col1 groupings
    for i, (lbl, v, g) in enumerate(assets):
        nid = f"a{i}"
        cols[0].append(Node(nid, lbl, v * u, "in", 0))
        flows.append((nid, "cur_a" if g == "current" else "lt_a", v * u, "in"))
    if cur_a > 0:
        cols[1].append(Node("cur_a", "Total Current Assets", cur_a, "profit", 1, side="top"))
        flows.append(("cur_a", "ta", cur_a, "profit"))
    if lt_a > 0:
        cols[1].append(Node("lt_a", "Total Non-Current Assets", lt_a, "profit", 1, side="top"))
        flows.append(("lt_a", "ta", lt_a, "profit"))
    # col2 hub
    cols[2].append(Node("ta", "Total Assets", total_a, "hub", 2, side="top"))
    # col3 liabilities + equity
    cols[3].append(Node("tl", "Total Liabilities", total_l, "cost", 3, side="top"))
    cols[3].append(Node("te", "Total Equity", total_eq, "profit", 3, side="top"))
    flows.append(("ta", "tl", total_l, "cost"))
    flows.append(("ta", "te", total_eq, "profit"))
    # col4 sub-groupings
    if cur_l > 0:
        cols[4].append(Node("cur_l", "Current Liabilities", cur_l, "cost", 4, side="top"))
        flows.append(("tl", "cur_l", cur_l, "cost"))
    if lt_l > 0:
        cols[4].append(Node("lt_l", "Non-Current Liabilities", lt_l, "cost", 4, side="top"))
        flows.append(("tl", "lt_l", lt_l, "cost"))
    cols[4].append(Node("she", "Shareholders' Equity", sh_eq, "profit", 4, side="top"))
    flows.append(("te", "she", sh_eq, "profit"))
    if minority > 0:
        cols[4].append(Node("mi", "Minority Interest", minority, "profit", 4, side="right"))
        flows.append(("te", "mi", minority, "profit"))
    # col5 line items
    for i, (lbl, v, g) in enumerate(liabs):
        nid = f"l{i}"
        cols[5].append(Node(nid, lbl, v * u, "cost", 5))
        flows.append(("cur_l" if g == "current" else "lt_l", nid, v * u, "cost"))
    for i, (lbl, v, _) in enumerate(equities):
        nid = f"e{i}"
        cols[5].append(Node(nid, lbl, v * u, "profit", 5))
        flows.append(("she", nid, v * u, "profit"))

    cols = [c for c in cols if c]
    return cols, flows, total_a


def build_cashflow(a):
    """Flow-CONSERVING cash-flow Sankey. Every node's value equals the sum of its
    inbound ribbons (and, for hubs, its outbound ribbons too) — so nothing overflows
    the node rectangle. Structure:
        operating(+) items → Operating Inflow → working-capital uses + CFO
        CFO + Beginning Cash + non-operating inflows → Cash Available
        Cash Available → investing/financing uses + Ending Cash
    The cash identity holds by construction: Begin + CFO + ΣInflows = ΣUses + End.
    CapEx is just one investing use — pass it inside --investing as a negative item;
    --capex is used ONLY to print the Free-Cash-Flow figure in the footer note, never
    as a flow node (that double-counted capex and broke the balance in the old model)."""
    u = _unit_mult(a.unit)
    op  = _parse_pairs(a.operating, n_min=2, n_max=2) if a.operating else []
    inv = _parse_pairs(a.investing, n_min=2, n_max=2) if a.investing else []
    fin = _parse_pairs(a.financing, n_min=2, n_max=2) if a.financing else []
    begin = (a.begin_cash or 0) * u
    fx = (a.fx or 0) * u

    cfo = sum(v for _, v, _ in op) * u
    cfi = sum(v for _, v, _ in inv) * u
    cff = sum(v for _, v, _ in fin) * u
    net = cfo + cfi + cff + fx
    end = begin + net
    ref = abs(cfo) if cfo else max(abs(net), 1.0)

    cols = [[] for _ in range(5)]
    flows = []

    # ── Stage A — operating(+) items → Operating Inflow → working-capital uses + CFO
    op_pos = [(lbl, v * u) for lbl, v, _ in op if v > 0]
    op_neg = [(lbl, -v * u) for lbl, v, _ in op if v < 0]
    opin = sum(v for _, v in op_pos)
    for i, (lbl, v) in enumerate(op_pos):
        cols[0].append(Node(f"op{i}", lbl, v, "in", 0))
        flows.append((f"op{i}", "opin", v, "in"))
    if op_pos:
        cols[1].append(Node("opin", "Operating Inflow", opin, "in", 1, side="top"))
        for j, (lbl, v) in enumerate(op_neg):     # working-capital / non-cash uses
            cols[2].append(Node(f"opu{j}", lbl, v, "cost", 2, side="top"))
            flows.append(("opin", f"opu{j}", v, "cost"))
        cols[2].append(Node("cfo", "Cash Flow from Operations", abs(cfo), "hub", 2, side="top"))
        flows.append(("opin", "cfo", abs(cfo), "in"))
    else:
        cols[2].append(Node("cfo", "Cash Flow from Operations", abs(cfo), "hub", 2, side="top"))

    # ── Stage B — CFO + Beginning Cash + non-operating inflows → Cash Available
    avail = abs(cfo)
    flows.append(("cfo", "avail", abs(cfo), "in"))
    if begin > 0:
        cols[2].append(Node("begin", "Beginning Cash", begin, "in", 2, side="top"))
        flows.append(("begin", "avail", begin, "in")); avail += begin
    inv_in  = [(lbl, v * u) for lbl, v, _ in inv if v > 0]
    inv_use = [(lbl, -v * u) for lbl, v, _ in inv if v < 0]
    fin_in  = [(lbl, v * u) for lbl, v, _ in fin if v > 0]
    fin_use = [(lbl, -v * u) for lbl, v, _ in fin if v < 0]
    for i, (lbl, v) in enumerate(inv_in):
        cols[2].append(Node(f"ivin{i}", lbl, v, "in", 2, side="top"))
        flows.append((f"ivin{i}", "avail", v, "in")); avail += v
    for i, (lbl, v) in enumerate(fin_in):
        cols[2].append(Node(f"fnin{i}", lbl, v, "in", 2, side="top"))
        flows.append((f"fnin{i}", "avail", v, "in")); avail += v
    if fx > 0:
        cols[2].append(Node("fxin", "FX effect", fx, "in", 2, side="top"))
        flows.append(("fxin", "avail", fx, "in")); avail += fx
    cols[3].append(Node("avail", "Cash Available", avail, "hub", 3, side="top"))

    # ── Stage C — Cash Available → investing/financing uses + Ending Cash
    for i, (lbl, v) in enumerate(inv_use):
        cols[4].append(Node(f"ivu{i}", lbl, v, "cost", 4, side="top"))
        flows.append(("avail", f"ivu{i}", v, "cost"))
    for i, (lbl, v) in enumerate(fin_use):
        cols[4].append(Node(f"fnu{i}", lbl, v, "cost", 4, side="top"))
        flows.append(("avail", f"fnu{i}", v, "cost"))
    if fx < 0:
        cols[4].append(Node("fxu", "FX effect", -fx, "cost", 4, side="top"))
        flows.append(("avail", "fxu", -fx, "cost"))
    cols[4].append(Node("end", "Ending Cash", abs(end), "hub", 4, side="right"))
    flows.append(("avail", "end", abs(end), "profit"))

    cols = [c for c in cols if c]
    return cols, flows, ref


# ── donut ────────────────────────────────────────────────────────────────────
def _arc(cx, cy, r, a0, a1):
    x0 = cx + r * math.cos(a0)
    y0 = cy + r * math.sin(a0)
    x1 = cx + r * math.cos(a1)
    y1 = cy + r * math.sin(a1)
    return x0, y0, x1, y1


def render_donut(slices, title, source, center="", currency="$", note=None,
                 width=720, height=460):
    total = sum(v for _, v in slices)
    out = [_svg_open(width, height, "revenue donut")]
    if title:
        out.append(_txt(20, 30, title, size=15, weight="700", fill=INK))
    cx, cy, r_out, r_in = width * 0.40, height * 0.52, 132, 78
    ang = -math.pi / 2  # start at 12 o'clock
    label_pts = []
    for i, (lbl, v) in enumerate(slices):
        frac = v / total if total else 0
        a1 = ang + frac * 2 * math.pi
        color = DONUT_PALETTE[i % len(DONUT_PALETTE)]
        large = 1 if (a1 - ang) > math.pi else 0
        ox0, oy0, ox1, oy1 = _arc(cx, cy, r_out, ang, a1)
        ix0, iy0, ix1, iy1 = _arc(cx, cy, r_in, ang, a1)
        path = (f"M {_f(ox0)},{_f(oy0)} A {r_out} {r_out} 0 {large} 1 {_f(ox1)},{_f(oy1)} "
                f"L {_f(ix1)},{_f(iy1)} A {r_in} {r_in} 0 {large} 0 {_f(ix0)},{_f(iy0)} Z")
        out.append(f'<path d="{path}" fill="{color}"/>')
        mid = (ang + a1) / 2
        label_pts.append((mid, color, lbl, v, frac))
        ang = a1
    # center text
    if center:
        out.append(_txt(cx, cy - 4, center, size=18, weight="800", fill=INK, anchor="middle"))
    out.append(_txt(cx, cy + (16 if center else 4), fmt_money(total, currency),
                    size=13, weight="600", fill=MUTED, anchor="middle"))
    out.append(_txt(cx, cy + (32 if center else 20), "total", size=10, fill=FAINT, anchor="middle"))
    # leader-line labels around the ring
    for mid, color, lbl, v, frac in label_pts:
        lx = cx + (r_out + 6) * math.cos(mid)
        ly = cy + (r_out + 6) * math.sin(mid)
        on_right = math.cos(mid) >= 0
        ex = lx + (16 if on_right else -16)
        anchor = "start" if on_right else "end"
        out.append(f'<line x1="{_f(lx)}" y1="{_f(ly)}" x2="{_f(ex)}" y2="{_f(ly)}" '
                   f'stroke="{color}" stroke-width="1.4"/>')
        out.append(_txt(ex + (4 if on_right else -4), ly - 2, lbl, size=11, weight="700",
                        fill=INK, anchor=anchor))
        out.append(_txt(ex + (4 if on_right else -4), ly + 12,
                        f"{fmt_money(v, currency)}  ({frac*100:.1f}%)", size=10,
                        fill=MUTED, anchor=anchor))
    out += _footer(width, height, source, note)
    out.append("</svg>")
    return "\n".join(out)


# ── historical stacked revenue bars ─────────────────────────────────────────────
def render_revbars(years, series, title, source, currency="$", unit_mult=1.0,
                   mode="value", note=None, width=860, height=470):
    """years: list[str]; series: list[(label, [abs values per year])]. Stacked bars."""
    n = len(years)
    M_L, M_R, M_T, M_B = 70, 26, 78, 58
    pw = width - M_L - M_R
    ph = height - M_T - M_B
    totals = [sum(s[1][i] for s in series) for i in range(n)]
    if mode == "pct":
        ymax = 100.0
    else:
        ymax = (max(totals) if totals else 1) * 1.08 or 1
    gap = pw / n
    bar_w = gap * 0.58

    out = [_svg_open(width, height, "historical revenue bars")]
    if title:
        out.append(_txt(20, 30, title, size=15, weight="700", fill=INK))

    # legend (top, under title)
    lx = 20
    for j, (lbl, _) in enumerate(series):
        color = DONUT_PALETTE[j % len(DONUT_PALETTE)]
        out.append(f'<rect x="{_f(lx)}" y="44" width="11" height="11" rx="2" fill="{color}"/>')
        out.append(_txt(lx + 16, 53, lbl, size=10.5, fill=INK, anchor="start"))
        lx += 30 + 6.6 * len(lbl)

    # y gridlines + labels
    for k in range(6):
        v = ymax * k / 5
        y = M_T + ph * (1 - k / 5)
        out.append(f'<line x1="{M_L}" y1="{_f(y)}" x2="{M_L + pw}" y2="{_f(y)}" '
                   f'stroke="#eceff2" stroke-width="1"/>')
        lab = f"{v:.0f}%" if mode == "pct" else fmt_money(v, currency)
        out.append(_txt(M_L - 6, y + 3, lab, size=9.5, fill=MUTED, anchor="end"))

    # stacked bars
    for i, yr in enumerate(years):
        x = M_L + gap * i + (gap - bar_w) / 2
        cursor = M_T + ph
        for j, (lbl, vals) in enumerate(series):
            v = vals[i]
            disp = v if mode == "value" else (v / totals[i] * 100 if totals[i] else 0)
            h = ph * (disp / ymax) if ymax else 0
            cursor -= h
            color = DONUT_PALETTE[j % len(DONUT_PALETTE)]
            out.append(f'<rect x="{_f(x)}" y="{_f(cursor)}" width="{_f(bar_w)}" '
                       f'height="{_f(max(0, h))}" fill="{color}"/>')
        out.append(_txt(x + bar_w / 2, M_T + ph + 16, str(yr), size=10, fill=MUTED, anchor="middle"))

    out += _footer(width, height, source, note)
    out.append("</svg>")
    return "\n".join(out)


# ── DuPont 5-step tree ──────────────────────────────────────────────────────────
def _box(x, y, w, h, title, value, sub=None, fill=DUPONT_FILL):
    out = [f'<rect x="{_f(x)}" y="{_f(y)}" width="{w}" height="{h}" rx="7" fill="{fill}"/>']
    out.append(_txt(x + w / 2, y + (20 if sub else h / 2 - 2), title, size=11.5, weight="700",
                    fill=DUPONT_INK, anchor="middle"))
    out.append(_txt(x + w / 2, y + (38 if sub else h / 2 + 14), value, size=13, weight="800",
                    fill=DUPONT_INK, anchor="middle"))
    if sub:
        out.append(_txt(x + w / 2, y + h - 6, sub, size=8.5, fill="#dbeafe", anchor="middle"))
    return out


def _conn(x0, y0, x1, y1, out):
    out.append(f'<line x1="{_f(x0)}" y1="{_f(y0)}" x2="{_f(x1)}" y2="{_f(y1)}" '
               f'stroke="#94a3b8" stroke-width="1.4"/>')


def _op(x, y, sym, out):
    out.append(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="11" fill="#ffffff" stroke="#94a3b8" stroke-width="1.2"/>')
    out.append(_txt(x, y + 5, sym, size=14, weight="800", fill=MUTED, anchor="middle"))


def render_dupont(a):
    u = _unit_mult(a.unit)
    ni = a.net_income * u
    pretax = a.pretax * u
    opinc = a.operating_income * u
    rev = a.revenue * u
    avg_assets = (a.begin_assets + a.end_assets) / 2 * u
    avg_equity = (a.begin_equity + a.end_equity) / 2 * u
    cur = a.currency

    net_margin = ni / rev
    asset_turn = rev / avg_assets
    equity_mult = avg_assets / avg_equity
    roe = net_margin * asset_turn * equity_mult
    op_margin = opinc / rev
    tax_burden = ni / pretax
    int_burden = pretax / opinc

    W, H = 1240, 540
    out = [_svg_open(W, H, "DuPont ROE decomposition")]
    title = a.title or "5-Step DuPont Decomposition of Return on Equity (ROE)"
    out.append(_txt(20, 30, title, size=15, weight="700", fill=INK))

    BW, BH = 150, 56
    # L0 ROE (centered top)
    roe_x = W / 2 - BW / 2
    out += _box(roe_x, 56, BW, BH, "ROE", f"{roe*100:.2f}%",
                sub=f"= Net Income / Avg Equity", fill="#1e3a8a")
    # L1: three factors
    l1y = 168
    l1_centers = [W * 0.215, W * 0.5, W * 0.785]
    l1 = [
        ("Net Margin", f"{net_margin*100:.2f}%", "Net Income / Revenue"),
        ("Asset Turnover", f"{asset_turn:.2f}", "Revenue / Avg Assets"),
        ("Equity Multiplier", f"{equity_mult:.2f}", "Avg Assets / Avg Equity"),
    ]
    roe_cx, roe_by = W / 2, 56 + BH
    for cxc, (t, v, s) in zip(l1_centers, l1):
        bx = cxc - BW / 2
        out += _box(bx, l1y, BW, BH, t, v, sub=s)
        _conn(roe_cx, roe_by, cxc, l1y, out)
    # operators between L1 boxes
    _op((l1_centers[0] + l1_centers[1]) / 2, l1y + BH / 2, "×", out)
    _op((l1_centers[1] + l1_centers[2]) / 2, l1y + BH / 2, "×", out)

    # L2 children
    l2y = 300
    BW2 = 118
    # under Net Margin: op margin × tax burden × interest burden
    nm_children_cx = [W * 0.10, W * 0.215, W * 0.33]
    nm_kids = [
        ("Operating Margin", f"{op_margin*100:.2f}%", "Op Inc / Revenue"),
        ("Tax Burden", f"{tax_burden:.4f}", "Net Inc / Pretax"),
        ("Interest Burden", f"{int_burden:.4f}", "Pretax / Op Inc"),
    ]
    for cxc, (t, v, s) in zip(nm_children_cx, nm_kids):
        out += _box(cxc - BW2 / 2, l2y, BW2, BH, t, v, sub=s)
        _conn(l1_centers[0], l1y + BH, cxc, l2y, out)
    _op((nm_children_cx[0] + nm_children_cx[1]) / 2, l2y + BH / 2, "×", out)
    _op((nm_children_cx[1] + nm_children_cx[2]) / 2, l2y + BH / 2, "×", out)

    # under Asset Turnover: revenue ÷ avg assets
    at_children_cx = [W * 0.5 - 82, W * 0.5 + 82]
    at_kids = [("Revenue", fmt_money(rev, cur), ""),
               ("Avg Total Assets", fmt_money(avg_assets, cur), "(begin+end)/2")]
    for cxc, (t, v, s) in zip(at_children_cx, at_kids):
        out += _box(cxc - BW2 / 2, l2y, BW2, BH, t, v, sub=s)
        _conn(l1_centers[1], l1y + BH, cxc, l2y, out)
    _op(W * 0.5, l2y + BH / 2, "÷", out)

    # under Equity Multiplier: avg assets ÷ avg equity
    em_children_cx = [W * 0.785 - 82, W * 0.785 + 82]
    em_kids = [("Avg Total Assets", fmt_money(avg_assets, cur), "(begin+end)/2"),
               ("Avg Total Equity", fmt_money(avg_equity, cur), "(begin+end)/2")]
    for cxc, (t, v, s) in zip(em_children_cx, em_kids):
        out += _box(cxc - BW2 / 2, l2y, BW2, BH, t, v, sub=s)
        _conn(l1_centers[2], l1y + BH, cxc, l2y, out)
    _op(W * 0.78, l2y + BH / 2, "÷", out)

    # L3 raw inputs under the net-margin children (the $ figures)
    l3y = 420
    BW3 = 110
    l3 = [
        (nm_children_cx[0], "Operating Income", fmt_money(opinc, cur)),
        (nm_children_cx[1], "Net Income", fmt_money(ni, cur)),
        (nm_children_cx[2], "Pretax Income", fmt_money(pretax, cur)),
    ]
    for cxc, t, v in l3:
        out += _box(cxc - BW3 / 2, l3y, BW3, 48, t, v, fill="#3b82f6")
        _conn(cxc, l2y + BH, cxc, l3y, out)

    note = a.note
    out += _footer(W, H, a.source, note)
    out.append("</svg>")
    return "\n".join(out)


# ── CLI ──────────────────────────────────────────────────────────────────────
# ── money-flow (supply-chain) diagram ───────────────────────────────────────────
# A 3-stage "follow the dollars" map in the dark gold-ribbon style: who pays →
# what they buy → where the money pools. NOT a flow-conserving Sankey — ribbon
# thickness is rough relative scale (as the legend states), so node heights are
# text-driven and ribbons are stroked gold paths (solid = paid directly, dashed =
# money embedded inside a finished part bought from someone else).
MF_BG = "#0b0f1a"
MF_PANEL = "#0e1320"
MF_INK = "#e8ecf5"
MF_MUT = "#8a93a8"
MF_MUT2 = "#646d82"
MF_GOLD = "#e9b658"
MF_GOLD_SOFT = "#f4d58a"
MF_GRID = "#222a3a"
MF_MONO = "'JetBrains Mono',ui-monospace,Menlo,monospace"
MF_SANS = "'Space Grotesk',system-ui,-apple-system,'Segoe UI',sans-serif"

# kind → (accent stroke/bar, dark node fill, sub-label colour, legend label)
MF_KIND = {
    "buyer":   ("#f2655f", "#15101a", "#c98c87", "buyer"),
    "buyer2":  ("#7fa8f5", "#0f1622", "#8ca6d6", "buyer"),
    "compute": ("#56c6e6", "#141a2a", "#8a93a8", "compute"),
    "silicon": ("#f2655f", "#15101a", "#d49b96", "in-house silicon"),
    "inhouse": ("#f2655f", "#15101a", "#d49b96", "in-house silicon"),
    "power":   ("#d9a05b", "#141a2a", "#bcae98", "power / analog"),
    "rf":      ("#7fa8f5", "#0f1622", "#9bb3df", "RF / wireless"),
    "custom":  ("#7fa8f5", "#0f1622", "#9bb3df", "custom modules"),
    "foundry": ("#34d399", "#101d1a", "#7fd9bf", "foundry"),
    "memory":  ("#a78bfa", "#15121f", "#b9a6f5", "memory"),
    "neutral": ("#e9b658", "#141a2a", "#8a93a8", "supplier"),
}


def _mf_kind(n):
    k = n.get("kind", "neutral")
    acc, fill, sub, lbl = MF_KIND.get(k, MF_KIND["neutral"])
    return (n.get("color", acc), n.get("fill", fill), n.get("sub_color", sub), lbl)


def _mf_wrap(text, max_chars):
    out, cur = [], ""
    for w in str(text).split():
        if cur and len(cur) + 1 + len(w) > max_chars:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        out.append(cur)
    return out


def _mf_text(x, y, s, size, fill, *, weight="400", anchor="start", font=None,
             ls=None, halo=None):
    f = font or MF_SANS
    extra = f' letter-spacing="{ls}"' if ls else ""
    if halo:
        extra += (f' paint-order="stroke" stroke="{halo}" stroke-width="3.2" '
                  f'stroke-linejoin="round"')
    return (f'<text x="{_f(x)}" y="{_f(y)}" text-anchor="{anchor}" '
            f'font-family="{f}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}"{extra}>{_xml(s)}</text>')


def render_moneyflow(spec, source=None, width=1180, note=None):
    """spec: dict with keys
        eyebrow, title, thesis (str), stages (list of stage labels),
        nodes  (list of {id, stage, label, sub:[..], kind, color?, fill?, h?}),
        flows  (list of {from, to, weight, style:'direct'|'embedded', label?}),
        legend (optional list of {type:'direct'|'embedded'|'scale'|'chip', label, kind?}),
        source.
    Emits one self-contained dark inline <svg> for embedding un-fenced in a report."""
    stages = spec.get("stages") or ["who pays", "what they buy", "where it pools"]
    nodes = spec.get("nodes") or []
    flows = spec.get("flows") or []
    N = len(stages)
    by_id = {n["id"]: n for n in nodes}

    PAD = 42
    W_NODE = 214
    GAP = 16

    # ── header (eyebrow + title + thesis) ──
    title_lines = _mf_wrap(spec.get("title", ""), max(18, int((width - 2 * PAD) / 17)))
    thesis_lines = _mf_wrap(spec.get("thesis", ""), max(40, int((width - 2 * PAD) / 8.3)))
    y = 40
    head = []
    if spec.get("eyebrow"):
        y += 16
        head.append(_mf_text(PAD, y, spec["eyebrow"].upper(), 11.5, MF_GOLD,
                             weight="600", font=MF_MONO, ls="3"))
    ty = y + 44
    for ln in title_lines:
        head.append(_mf_text(PAD, ty, ln, 32, MF_INK, weight="700"))
        ty += 38
    thy = ty + 4
    for ln in thesis_lines:
        head.append(_mf_text(PAD, thy, ln, 15, MF_MUT, weight="400"))
        thy += 22
    flow_top = thy + 34

    # ── column x positions (col0 left-aligned, last col right-aligned) ──
    left0 = PAD
    left_last = width - PAD - W_NODE
    if N > 1:
        step = (left_last - left0) / (N - 1)
        col_x = [left0 + i * step for i in range(N)]
    else:
        col_x = [left0]

    # ── node heights (text-driven) & per-column vertical layout ──
    def node_h(n):
        if n.get("h"):
            return float(n["h"])
        return 60 + 17 * len(n.get("sub") or [])

    cols = [[n for n in nodes if n.get("stage", 0) == c] for c in range(N)]
    col_total = []
    for col in cols:
        tot = sum(node_h(n) for n in col) + GAP * max(0, len(col) - 1)
        col_total.append(tot)
    flow_h = max(col_total) if col_total else 200

    pos = {}  # id → (x, y, w, h, cy)
    for c, col in enumerate(cols):
        ys = flow_top + (flow_h - col_total[c]) / 2.0
        for n in col:
            h = node_h(n)
            pos[n["id"]] = (col_x[c], ys, W_NODE, h, ys + h / 2.0)
            ys += h + GAP

    flow_bot = flow_top + flow_h
    legend_y = flow_bot + 30
    height = legend_y + 54

    # ── ribbon thickness & per-node attach bands (centered bundles) ──
    maxw = max((float(f.get("weight", 1)) for f in flows), default=1) or 1
    wscale = 24.0 / maxw

    def thick(f):
        return max(5.0, float(f.get("weight", 1)) * wscale)

    out_cur, in_cur = {}, {}
    for nid in by_id:
        outs = [f for f in flows if f["from"] == nid]
        outs.sort(key=lambda f: pos.get(f["to"], (0, 0, 0, 0, 0))[4])
        tot = sum(thick(f) for f in outs)
        cy = pos[nid][4] - tot / 2.0
        for f in outs:
            t = thick(f)
            out_cur[id(f)] = cy + t / 2.0
            cy += t
        ins = [f for f in flows if f["to"] == nid]
        ins.sort(key=lambda f: pos.get(f["from"], (0, 0, 0, 0, 0))[4])
        tot = sum(thick(f) for f in ins)
        cy = pos[nid][4] - tot / 2.0
        for f in ins:
            t = thick(f)
            in_cur[id(f)] = cy + t / 2.0
            cy += t

    # ── assemble SVG ──
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {int(height)}" '
         f'width="{width}" height="{int(height)}" role="img" '
         f'aria-label="{_xml(spec.get("title", "money flow diagram"))}" '
         f'font-family="{MF_SANS}">']
    o.append('<defs>'
             f'<linearGradient id="mfgold" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{width}" y2="0">'
             '<stop offset="0" stop-color="#f6dc97"/>'
             '<stop offset="0.5" stop-color="#e9b658"/>'
             '<stop offset="1" stop-color="#cf8f2c"/></linearGradient>'
             '<radialGradient id="mfpool" cx="50%" cy="50%" r="50%">'
             '<stop offset="0" stop-color="#34d399" stop-opacity="0.16"/>'
             '<stop offset="1" stop-color="#34d399" stop-opacity="0"/></radialGradient>'
             '</defs>')
    o.append(f'<rect x="0" y="0" width="{width}" height="{int(height)}" rx="16" fill="{MF_BG}"/>')
    o += head

    # gravity glow behind the last column
    if N > 1 and cols[-1]:
        gx = col_x[-1] + W_NODE / 2
        gy = (pos[cols[-1][0]["id"]][1] + pos[cols[-1][-1]["id"]][1] + pos[cols[-1][-1]["id"]][3]) / 2
        o.append(f'<ellipse cx="{_f(gx)}" cy="{_f(gy)}" rx="190" ry="150" fill="url(#mfpool)"/>')

    # stage dividers + eyebrows
    for c in range(N - 1):
        dx = (col_x[c] + W_NODE + col_x[c + 1]) / 2
        o.append(f'<line x1="{_f(dx)}" y1="{_f(flow_top - 10)}" x2="{_f(dx)}" '
                 f'y2="{_f(flow_bot + 6)}" stroke="{MF_GRID}" stroke-dasharray="2 8"/>')
    for c in range(N):
        ex = col_x[c]
        o.append(_mf_text(ex, flow_top - 26, f"STAGE {c + 1:02d}", 12, MF_GOLD,
                          font=MF_MONO, ls="3"))
        o.append(_mf_text(ex, flow_top - 10, stages[c], 11.5, MF_MUT2, font=MF_MONO))

    # ribbons (under nodes): solid first, then dashed
    for want_dashed in (False, True):
        for f in flows:
            dashed = f.get("style", "direct") == "embedded"
            if dashed != want_dashed:
                continue
            if f["from"] not in pos or f["to"] not in pos:
                continue
            sx, _sy, sw, _sh, _scy = pos[f["from"]]
            dx, _dy, _dw, _dh, _dcy = pos[f["to"]]
            x0, y0 = sx + sw, out_cur[id(f)]
            x1, y1 = dx, in_cur[id(f)]
            gx = (x0 + x1) / 2
            t = thick(f)
            dash = ' stroke-dasharray="0.1 11"' if dashed else ""
            op = "0.78" if dashed else "0.9"
            o.append(f'<path d="M {_f(x0)} {_f(y0)} C {_f(gx)} {_f(y0)}, '
                     f'{_f(gx)} {_f(y1)}, {_f(x1)} {_f(y1)}" fill="none" '
                     f'stroke="url(#mfgold)" stroke-width="{_f(t)}" '
                     f'stroke-linecap="round" opacity="{op}"{dash}/>')
    # ribbon labels
    for f in flows:
        if not f.get("label") or f["from"] not in pos or f["to"] not in pos:
            continue
        sx, _a, sw, _b, _c2 = pos[f["from"]]
        dx, _d, _e, _g, _h2 = pos[f["to"]]
        gx = (sx + sw + dx) / 2
        my = (out_cur[id(f)] + in_cur[id(f)]) / 2 - 6
        o.append(_mf_text(gx, my, f["label"], 11.5, MF_GOLD_SOFT, anchor="middle",
                          font=MF_MONO, halo=MF_BG))

    # nodes
    for n in nodes:
        if n["id"] not in pos:
            continue
        x, ny, w, h, _cy = pos[n["id"]]
        acc, fill, subc, _lbl = _mf_kind(n)
        o.append(f'<rect x="{_f(x)}" y="{_f(ny)}" width="{w}" height="{_f(h)}" '
                 f'rx="12" fill="{fill}" stroke="{acc}" stroke-opacity="0.5"/>')
        o.append(f'<rect x="{_f(x)}" y="{_f(ny)}" width="3" height="{_f(h)}" rx="2" fill="{acc}"/>')
        lsize = 21 if len(n.get("label", "")) <= 7 else (17 if len(n["label"]) <= 16 else 14)
        o.append(_mf_text(x + 18, ny + 33, n.get("label", ""), lsize, "#ffffff", weight="700"))
        sy = ny + 54
        for s in (n.get("sub") or []):
            o.append(_mf_text(x + 18, sy, s, 11, subc, font=MF_MONO))
            sy += 17

    # legend
    legend = spec.get("legend")
    if legend is None:
        kinds_present = []
        for n in nodes:
            if n.get("stage", 0) == 0:
                continue
            k = n.get("kind", "neutral")
            if k not in kinds_present:
                kinds_present.append(k)
        legend = [{"type": "direct", "label": "money paid directly"},
                  {"type": "embedded", "label": "money embedded in a finished chip"},
                  {"type": "scale", "label": "thickness ≈ rough scale"}]
        for k in kinds_present:
            legend.append({"type": "chip", "kind": k, "label": MF_KIND.get(k, MF_KIND["neutral"])[3]})
    lx = PAD
    ly = legend_y
    for item in legend:
        typ = item.get("type", "chip")
        lbl = item.get("label", "")
        if typ == "direct":
            o.append(f'<rect x="{_f(lx)}" y="{_f(ly - 4)}" width="26" height="4" rx="2" fill="{MF_GOLD}"/>')
            adv = 26 + 10
        elif typ == "embedded":
            for i in range(4):
                o.append(f'<circle cx="{_f(lx + 4 + i * 7)}" cy="{_f(ly - 2)}" r="2" fill="{MF_GOLD}"/>')
            adv = 28 + 10
        elif typ == "scale":
            adv = 0
        else:  # chip
            acc = MF_KIND.get(item.get("kind", "neutral"), MF_KIND["neutral"])[0]
            o.append(f'<rect x="{_f(lx)}" y="{_f(ly - 9)}" width="11" height="11" rx="3" fill="{acc}"/>')
            adv = 11 + 8
        tx = lx + adv
        o.append(_mf_text(tx, ly, lbl, 11.5, MF_MUT, font=MF_MONO))
        lx = tx + len(lbl) * 7.2 + 24
        if lx > width - PAD - 120:  # wrap to a second legend row
            lx = PAD
            ly += 20
            height = max(height, ly + 40)

    # footer
    fy = ly + 30
    if note:
        o.append(_mf_text(width / 2, fy - 16, note, 10.5, MF_MUT2, anchor="middle"))
    if source:
        o.append(_mf_text(width / 2, fy, f"Source: {source}", 10.5, MF_MUT2,
                          anchor="middle", font=MF_MONO))
    height = max(height, fy + 18)

    # patch viewBox/height now that legend wrap / footer may have grown it
    o[0] = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {int(height)}" '
            f'width="{width}" height="{int(height)}" role="img" '
            f'aria-label="{_xml(spec.get("title", "money flow diagram"))}" '
            f'font-family="{MF_SANS}">')
    o[2] = f'<rect x="0" y="0" width="{width}" height="{int(height)}" rx="16" fill="{MF_BG}"/>'
    o.append("</svg>")
    return "\n".join(o)


def _add_common(p):
    p.add_argument("--source", required=True, help="REQUIRED data-source footer baked into the SVG.")
    p.add_argument("--title", default="")
    p.add_argument("--unit", choices=["raw", "k", "m", "b"], default="m",
                   help="unit of the values you pass (default m = millions).")
    p.add_argument("--currency", default="$")
    p.add_argument("--note", default=None, help="optional italic caption above the source footer.")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Financial-statement charts as inline SVG (income/balance/cashflow Sankey, donut, DuPont).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("income", help="income-statement Sankey")
    _add_common(pi)
    pi.add_argument("--segment", action="append", default=[], help="'Label:revenue' revenue source — repeatable.")
    pi.add_argument("--revenue", type=float, required=True)
    pi.add_argument("--cogs", type=float, default=None)
    pi.add_argument("--gross-profit", type=float, default=None)
    pi.add_argument("--sga", type=float, default=None)
    pi.add_argument("--rd", type=float, default=None)
    pi.add_argument("--other-opex", type=float, default=None)
    pi.add_argument("--operating-income", type=float, default=None)
    pi.add_argument("--net-interest", type=float, default=None, help="net interest/other income feeding pretax (positive).")
    pi.add_argument("--other-income", type=float, default=None)
    pi.add_argument("--pretax", type=float, default=None)
    pi.add_argument("--tax", type=float, default=None)
    pi.add_argument("--minority", type=float, default=None)
    pi.add_argument("--net-income", type=float, default=None)

    pb = sub.add_parser("balance", help="balance-sheet Sankey")
    _add_common(pb)
    pb.add_argument("--asset", action="append", default=[], help="'Label:value:current|lt' — repeatable.")
    pb.add_argument("--liability", action="append", default=[], help="'Label:value:current|lt' — repeatable.")
    pb.add_argument("--equity", action="append", default=[], help="'Label:value' (shareholders' equity components) — repeatable.")
    pb.add_argument("--minority", type=float, default=None, help="equity-side noncontrolling interest.")

    pc = sub.add_parser("cashflow", help="cash-flow Sankey")
    _add_common(pc)
    pc.add_argument("--operating", action="append", default=[], help="'Label:value' (signed) — repeatable.")
    pc.add_argument("--investing", action="append", default=[], help="'Label:value' (signed) — repeatable.")
    pc.add_argument("--financing", action="append", default=[], help="'Label:value' (signed) — repeatable.")
    pc.add_argument("--capex", type=float, default=None, help="capex (positive magnitude); splits CFO into FCF + CapEx.")
    pc.add_argument("--begin-cash", type=float, default=None)
    pc.add_argument("--fx", type=float, default=None, help="effects of FX on cash.")

    pd = sub.add_parser("donut", help="revenue donut (by segment or geography)")
    _add_common(pd)
    pd.add_argument("--slice", action="append", default=[], required=True, help="'Label:value' — repeatable.")
    pd.add_argument("--center", default="", help="center text (e.g. ticker).")

    pr = sub.add_parser("revbars", help="historical stacked revenue bars (by segment or geography)")
    _add_common(pr)
    pr.add_argument("--years", required=True, help="comma list, e.g. '2021,2022,2023,2024,2025'.")
    pr.add_argument("--series", action="append", default=[], required=True,
                    help="'Label:v1,v2,...' one per segment/region; values align to --years. Repeatable.")
    pr.add_argument("--mode", choices=["value", "pct"], default="value",
                    help="value = absolute stacked $; pct = 100%% stacked share.")

    pm = sub.add_parser("moneyflow", help="3-stage supply-chain money-flow diagram (dark gold-ribbon)")
    pm.add_argument("--spec", required=True, help="path to JSON spec ('-' for stdin). See references/money_flow.md.")
    pm.add_argument("--source", default=None, help="overrides spec.source (one is required).")
    pm.add_argument("--title", default=None, help="overrides spec.title.")
    pm.add_argument("--note", default=None, help="optional italic caption above the source footer.")
    pm.add_argument("--width", type=int, default=None)

    pdu = sub.add_parser("dupont", help="5-step DuPont ROE tree")
    _add_common(pdu)
    pdu.add_argument("--net-income", type=float, required=True)
    pdu.add_argument("--pretax", type=float, required=True)
    pdu.add_argument("--operating-income", type=float, required=True)
    pdu.add_argument("--revenue", type=float, required=True)
    pdu.add_argument("--begin-assets", type=float, required=True)
    pdu.add_argument("--end-assets", type=float, required=True)
    pdu.add_argument("--begin-equity", type=float, required=True)
    pdu.add_argument("--end-equity", type=float, required=True)

    a = ap.parse_args(argv)

    try:
        if a.cmd == "income":
            cols, flows, ref = build_income(a)
            svg = render_sankey(cols, flows, ref, a.title or "Income Statement Breakdown",
                                a.source, currency=a.currency,
                                width=a.width or 1000, height=a.height or 560,
                                note=a.note, aria="income statement Sankey")
        elif a.cmd == "balance":
            cols, flows, ref = build_balance(a)
            svg = render_sankey(cols, flows, ref, a.title or "Balance Sheet Breakdown",
                                a.source, currency=a.currency,
                                width=a.width or 1040, height=a.height or 600,
                                note=a.note, aria="balance sheet Sankey")
        elif a.cmd == "cashflow":
            cols, flows, ref = build_cashflow(a)
            cf_note = a.note
            if a.capex:
                um = _unit_mult(a.unit)
                cfo_v = (sum(v for _, v, _ in _parse_pairs(a.operating, n_min=2, n_max=2))
                         * um) if a.operating else 0.0
                fcf_txt = (f"Free Cash Flow = CFO − CapEx = "
                           f"{fmt_money(cfo_v - abs(a.capex) * um, a.currency)}")
                cf_note = f"{cf_note}  ·  {fcf_txt}" if cf_note else fcf_txt
            svg = render_sankey(cols, flows, ref, a.title or "Cash Flow Breakdown",
                                a.source, currency=a.currency,
                                width=a.width or 1040, height=a.height or 600,
                                note=cf_note, aria="cash flow Sankey")
        elif a.cmd == "donut":
            slices = [(lbl, v) for lbl, v, _ in _parse_pairs(a.slice, n_min=2, n_max=2)]
            slices = [(lbl, v * _unit_mult(a.unit)) for lbl, v in slices]
            svg = render_donut(slices, a.title or "Revenue Breakdown", a.source,
                               center=a.center, currency=a.currency, note=a.note,
                               width=a.width or 720, height=a.height or 460)
        elif a.cmd == "revbars":
            years = [y.strip() for y in a.years.split(",")]
            um = _unit_mult(a.unit)
            series = []
            for s in a.series:
                if ":" not in s:
                    raise ValueError(f"--series must be 'Label:v1,v2,...', got {s!r}")
                lbl, rest = s.split(":", 1)
                vals = [float(x) * um for x in rest.split(",")]
                if len(vals) != len(years):
                    raise ValueError(f"series {lbl!r} has {len(vals)} values but {len(years)} years")
                series.append((lbl.strip(), vals))
            svg = render_revbars(years, series, a.title or "Historical Revenue",
                                 a.source, currency=a.currency, mode=a.mode, note=a.note,
                                 width=a.width or 860, height=a.height or 470)
        elif a.cmd == "moneyflow":
            raw = sys.stdin.read() if a.spec == "-" else open(a.spec, encoding="utf-8").read()
            spec = json.loads(raw)
            if a.title:
                spec["title"] = a.title
            src = a.source or spec.get("source")
            if not src:
                ap.error("moneyflow requires --source or spec.source")
            svg = render_moneyflow(spec, source=src,
                                   width=a.width or spec.get("width") or 1180,
                                   note=a.note or spec.get("note"))
        elif a.cmd == "dupont":
            svg = render_dupont(a)
        else:
            ap.error(f"unknown command {a.cmd}")
    except (ValueError, ZeroDivisionError) as e:
        ap.error(str(e))

    print(svg)


if __name__ == "__main__":
    main()
