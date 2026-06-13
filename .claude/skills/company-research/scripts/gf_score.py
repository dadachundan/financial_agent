#!/usr/bin/env python3
"""
gf_score.py — render a GuruFocus-style "GF Score" radar/pentagon as INLINE SVG
plus a markdown scorecard table, for embedding directly in a research report.

Why inline SVG (not matplotlib, not a Mermaid radar):
  * matplotlib PNG generation was disabled project-wide on 2026-06-03 to cut the
    per-agent memory footprint — this helper imports only the stdlib (math /
    argparse), so it adds ~0 MB resident and is safe to run inside a report agent.
  * The report viewer (reports_viewer.py → marked.js, no sanitization) injects raw
    markdown into innerHTML, so a literal <svg> block renders verbatim — the same
    untouched-raw-HTML path the Step-10 <details> verification logs already ride on
    in hundreds of reports. Mermaid's `radar-beta` is unproven on the unpinned
    mermaid@11 CDN import, so we do not depend on it.

What it emits:
  * a single-company filled pentagon (scores 0–10 on five axes), OR
  * an overlaid radar for 2–4 companies (compare-companies), with a legend, AND
  * the markdown scorecard table (per-dimension 0–10 + the composite 0–100 band).

The five dimensions (canonical input order — matches references/gf_score.md):
    financial_strength, profitability, growth, value (GF Value), momentum

The data-source annotation (`--source`) is a REQUIRED argument and is baked into a
<text> footer inside the SVG, per the project-wide chart rule that the source must
travel inside the image (charts get screenshotted / iframe-embedded without their
caption). The composite 0–100 and every sub-score are the analyst's own rubric
output — label them `*Analyst view:*` in the report; every underlying metric must
carry its own inline citation in the surrounding prose. This script does NOT fetch
GuruFocus's proprietary number; it renders the independently-computed scorecard.

Usage
-----
Single company:
    gf_score.py --name NVDA --scores 8,10,9,4,8 \
        --source "10-K FY25 · Yahoo Finance · indicators.db, as of 2026-06-13"

Compare (2–4 companies, overlaid):
    gf_score.py \
        --series "NVDA:8,10,9,4,8" \
        --series "AMD:6,7,8,6,5" \
        --source "FY25 10-Ks · Yahoo Finance, as of 2026-06-13"

Options:
    --scores fs,prof,growth,value,mom   five 0–10 scores (with --name)
    --series "Label:fs,prof,growth,value,mom"   repeatable; one company per flag
    --name LABEL                        label for the single-series form
    --source "..."                      REQUIRED data-source footer annotation
    --weights 20,25,25,15,15            composite weights (%, must sum to 100)
    --title "GF Score (GuruFocus-style)"  heading shown above the table
    --emit svg|table|both               default both
    --lang en|zh|bi                     table column language (default bi)
"""

import argparse
import math
import sys

# canonical dimension order (input order) → display names + fixed pentagon angle.
# Angles (degrees, SVG convention: 0=east, +clockwise because SVG y grows down)
# are chosen to mirror the GuruFocus widget: Profitability on top, then clockwise
# GF Value (right), Momentum (lower-right), Financial Strength (lower-left),
# Growth (upper-left).
DIMS = [
    ("financial_strength", "Financial Strength", "财务实力", 126.0),
    ("profitability",      "Profitability",      "盈利能力", -90.0),
    ("growth",             "Growth",             "成长性",   198.0),
    ("value",              "GF Value",           "估值",     -18.0),
    ("momentum",           "Momentum",           "动量",      54.0),
]

PALETTE = ["#2e8b57", "#2563eb", "#d97706", "#7c3aed"]  # green, blue, amber, violet
RING_BG = "#e9f5ec"   # light-green "target" backdrop, GuruFocus-style
GRID = "#c5d3cb"      # concentric ring outlines
AXIS = "#cfdad3"      # faint radial spokes
INK = "#1f2933"
MUTED = "#52606d"
MAX_V = 10.0

# Connect polygon vertices in clockwise angular order from the top — NOT the
# canonical input order (fs, prof, growth, value, mom). Connecting in input
# order makes the polygon self-intersect into a star (the "line across the
# middle, Profitability→Financial Strength" bug). RENDER_ORDER sorts the five
# axes by their on-screen angle so every edge joins adjacent rim vertices.
RENDER_ORDER = sorted(range(len(DIMS)), key=lambda i: DIMS[i][3])


def band_label(score100):
    """Map a 0–100 composite to the GuruFocus band text."""
    s = score100
    if s >= 91:
        return "91–100 Highest outperformance potential"
    if s >= 81:
        return "81–90 Good outperformance potential"
    if s >= 71:
        return "71–80 Likely average performance"
    if s >= 51:
        return "51–70 Poor future performance potential"
    return "0–50 Worst future performance potential / insufficient data"


def composite(scores, weights):
    """Weighted mean of the five 0–10 sub-scores, scaled to 0–100."""
    wsum = sum(weights)
    avg10 = sum(s * w for s, w in zip(scores, weights)) / wsum
    return int(round(avg10 * 10))


def _f(x):
    return f"{x:.1f}"


def _vertex(cx, cy, r_frac, angle_deg, radius):
    a = math.radians(angle_deg)
    r = radius * r_frac
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def _poly_points(cx, cy, values, radius):
    pts = []
    for i in RENDER_ORDER:
        ang = DIMS[i][3]
        v = values[i]
        x, y = _vertex(cx, cy, max(0.0, min(MAX_V, v)) / MAX_V, ang, radius)
        pts.append(f"{_f(x)},{_f(y)}")
    return " ".join(pts)


def build_svg(series, source, composites, lang="bi"):
    """series: list of (label, [5 scores]); composites: list of 0–100 ints."""
    W, H = 500, 500
    cx, cy, R = 250, 238, 150
    multi = len(series) > 1
    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" role="img" '
        f'aria-label="GF Score radar">'
    )
    out.append('<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (W, H))

    # title / composite header (single-series only — multi shows per-company in legend)
    if not multi:
        comp = composites[0]
        out.append(
            f'<text x="20" y="24" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="15" font-weight="700" fill="{INK}">'
            f'GF Score (GuruFocus-style): {comp}/100</text>'
        )
        out.append(
            f'<text x="20" y="41" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="11" fill="{MUTED}">{band_label(comp)}</text>'
        )
    else:
        out.append(
            f'<text x="20" y="24" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="14" font-weight="700" fill="{INK}">'
            f'GF Score (GuruFocus-style)</text>'
        )

    # light-green "target" backdrop (outer pentagon) + concentric ring outlines
    out.append(
        f'<polygon points="{_poly_points(cx, cy, [MAX_V] * 5, R)}" '
        f'fill="{RING_BG}" stroke="none"/>'
    )
    for level in (2, 4, 6, 8, 10):
        pts = _poly_points(cx, cy, [level] * 5, R)
        sw = "1.3" if level == 10 else "1"
        out.append(
            f'<polygon points="{pts}" fill="none" stroke="{GRID}" stroke-width="{sw}"/>'
        )

    # radial spokes + axis labels with the per-axis score (single series)
    for idx, (_, en, zh, ang) in enumerate(DIMS):
        ex, ey = _vertex(cx, cy, 1.0, ang, R)
        out.append(
            f'<line x1="{cx}" y1="{cy}" x2="{_f(ex)}" y2="{_f(ey)}" '
            f'stroke="{AXIS}" stroke-width="1"/>'
        )
        lx, ly = _vertex(cx, cy, 1.0, ang, R + 26)
        anchor = "middle"
        if lx > cx + 6:
            anchor = "start"
        elif lx < cx - 6:
            anchor = "end"
        label = en if lang == "en" else (zh if lang == "zh" else en)
        dy = 0
        if ang == -90.0:
            dy = -4
        elif ang in (54.0, 126.0):
            dy = 12
        out.append(
            f'<text x="{_f(lx)}" y="{_f(ly + dy)}" text-anchor="{anchor}" '
            f'font-family="Helvetica,Arial,sans-serif" font-size="11.5" '
            f'font-weight="600" fill="{INK}">{label}</text>'
        )
        if lang == "bi":
            out.append(
                f'<text x="{_f(lx)}" y="{_f(ly + dy + 13)}" text-anchor="{anchor}" '
                f'font-family="Helvetica,Arial,sans-serif" font-size="9.5" '
                f'fill="{MUTED}">{zh}</text>'
            )
        if not multi:
            sv = series[0][1][idx]
            sx, sy = _vertex(cx, cy, min(MAX_V, max(0.0, sv)) / MAX_V, ang, R)
            out.append(
                f'<text x="{_f(sx)}" y="{_f(sy - 6)}" text-anchor="middle" '
                f'font-family="Helvetica,Arial,sans-serif" font-size="10.5" '
                f'font-weight="700" fill="{INK}">{_num(sv)}</text>'
            )

    # score polygons
    for i, (label, scores) in enumerate(series):
        color = PALETTE[i % len(PALETTE)]
        pts = _poly_points(cx, cy, scores, R)
        op = "0.34" if not multi else "0.14"
        out.append(
            f'<polygon points="{pts}" fill="{color}" fill-opacity="{op}" '
            f'stroke="{color}" stroke-width="2"/>'
        )
        for (_, _, _, ang), v in zip(DIMS, scores):
            vx, vy = _vertex(cx, cy, min(MAX_V, max(0.0, v)) / MAX_V, ang, R)
            out.append(f'<circle cx="{_f(vx)}" cy="{_f(vy)}" r="2.6" fill="{color}"/>')

    # legend (multi-series)
    if multi:
        ly0 = H - 74
        out.append(
            f'<text x="20" y="{ly0}" font-family="Helvetica,Arial,sans-serif" '
            f'font-size="10.5" font-weight="700" fill="{MUTED}">Legend</text>'
        )
        x = 20
        for i, (label, _) in enumerate(series):
            color = PALETTE[i % len(PALETTE)]
            comp = composites[i]
            out.append(
                f'<rect x="{x}" y="{ly0 + 6}" width="11" height="11" rx="2" '
                f'fill="{color}"/>'
            )
            txt = f"{label} — {comp}/100"
            out.append(
                f'<text x="{x + 16}" y="{ly0 + 15}" '
                f'font-family="Helvetica,Arial,sans-serif" font-size="10.5" '
                f'fill="{INK}">{_xml(txt)}</text>'
            )
            x += 26 + 7.2 * len(txt)

    # required source footer (baked into the image), on two lines so it never clips
    out.append(
        f'<text x="{W/2:.0f}" y="{H - 30}" text-anchor="middle" '
        f'font-family="Helvetica,Arial,sans-serif" font-size="9.5" '
        f'fill="{MUTED}">Source: {_xml(source)}</text>'
    )
    out.append(
        f'<text x="{W/2:.0f}" y="{H - 15}" text-anchor="middle" '
        f'font-family="Helvetica,Arial,sans-serif" font-size="9" '
        f'fill="{MUTED}">GF Score = independent analyst rubric '
        f'(*Analyst view:*) — not GuruFocus™ official number</text>'
    )
    out.append("</svg>")
    return "\n".join(out)


def _num(v):
    return str(int(v)) if float(v).is_integer() else f"{v:g}"


def _xml(s):
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def build_table(series, composites, weights, lang="bi"):
    multi = len(series) > 1
    rows = []
    if lang == "en":
        head_dim, head = "Dimension", "Score (0–10)"
    elif lang == "zh":
        head_dim, head = "维度", "评分 (0–10)"
    else:
        head_dim, head = "维度 / Dimension", "评分 / Score (0–10)"

    if not multi:
        scores = series[0][1]
        rows.append(f"| {head_dim} | {head} | |")
        rows.append("|---|---|---|")
        for (_, en, zh, _), v in zip(DIMS, scores):
            name = en if lang == "en" else (zh if lang == "zh" else f"{en} ({zh})")
            iv = int(round(min(MAX_V, max(0.0, v))))
            bar = "█" * iv + "░" * (10 - iv)
            rows.append(f"| {name} | {_num(v)} | `{bar}` |")
        comp = composites[0]
        comp_lbl = "**GF Score (composite, *Analyst view:*)**"
        rows.append(f"| {comp_lbl} | **{comp} / 100** | **{band_label(comp)}** |")
    else:
        labels = [s[0] for s in series]
        rows.append("| " + head_dim + " | " + " | ".join(labels) + " |")
        rows.append("|---" * (len(labels) + 1) + "|")
        for j, (_, en, zh, _) in enumerate(DIMS):
            name = en if lang == "en" else (zh if lang == "zh" else f"{en} ({zh})")
            cells = " | ".join(_num(series[k][1][j]) for k in range(len(series)))
            rows.append(f"| {name} | {cells} |")
        comp_cells = " | ".join(f"**{c}/100**" for c in composites)
        rows.append(f"| **GF Score (composite, *Analyst view:*)** | {comp_cells} |")

    wnote = (
        "*Composite weights (*Analyst view:*): Financial Strength "
        f"{weights[0]:g}% · Profitability {weights[1]:g}% · Growth {weights[2]:g}% · "
        f"GF Value {weights[3]:g}% · Momentum {weights[4]:g}% "
        "(transparent reproduction — not GuruFocus's proprietary weighting).*"
    )
    return "\n".join(rows) + "\n\n" + wnote


def _parse_scores(text):
    parts = [p.strip() for p in text.split(",")]
    if len(parts) != 5:
        raise ValueError(f"expected 5 comma-separated scores, got {len(parts)}: {text!r}")
    vals = []
    for p in parts:
        v = float(p)
        if not (0.0 <= v <= 10.0):
            raise ValueError(f"score {v} out of range 0–10 in {text!r}")
        vals.append(v)
    return vals


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render a GuruFocus-style GF Score radar (inline SVG) + scorecard table.")
    ap.add_argument("--series", action="append", default=[],
                    help='"Label:fs,prof,growth,value,mom" — repeatable (2–4 for an overlay).')
    ap.add_argument("--name", help="label for the single-series form (use with --scores).")
    ap.add_argument("--scores", help="five 0–10 scores fs,prof,growth,value,mom (use with --name).")
    ap.add_argument("--source", required=True,
                    help="REQUIRED data-source footer annotation baked into the SVG.")
    ap.add_argument("--weights", default="20,25,25,15,15",
                    help="composite weights %% fs,prof,growth,value,mom (must sum to 100).")
    ap.add_argument("--title", default="GF Score (GuruFocus-style)")
    ap.add_argument("--emit", choices=["svg", "table", "both"], default="both")
    ap.add_argument("--lang", choices=["en", "zh", "bi"], default="bi")
    args = ap.parse_args(argv)

    try:
        weights = [float(x) for x in args.weights.split(",")]
        if len(weights) != 5 or abs(sum(weights) - 100) > 0.01:
            raise ValueError("--weights must be 5 numbers summing to 100")

        series = []
        for s in args.series:
            if ":" not in s:
                raise ValueError(f"--series must be 'Label:fs,prof,growth,value,mom', got {s!r}")
            label, rest = s.split(":", 1)
            series.append((label.strip(), _parse_scores(rest)))
        if args.scores:
            series.append((args.name or "Company", _parse_scores(args.scores)))
        if not series:
            raise ValueError("provide --scores (+--name) or at least one --series")
        if len(series) > 4:
            raise ValueError("at most 4 companies on one radar")
    except ValueError as e:
        ap.error(str(e))

    composites = [composite(sc, weights) for _, sc in series]

    chunks = []
    if args.emit in ("svg", "both"):
        chunks.append(build_svg(series, args.source, composites, lang=args.lang))
    if args.emit in ("table", "both"):
        if args.emit == "both":
            chunks.append("")  # blank line between SVG and table
        chunks.append(build_table(series, composites, weights, lang=args.lang))
    print("\n".join(chunks))


if __name__ == "__main__":
    main()
