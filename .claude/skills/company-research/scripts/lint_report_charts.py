#!/usr/bin/env python3
"""Lint the inline charts in a research report for *visual* breakage.

Step 10 of company-research string-matches chart NUMBERS against sources, but a
chart can carry perfectly correct numbers and still render broken — nodes drawn
off-canvas, bars taller than the viewBox, labels clipped past the left/right
edge, a degenerate single-ribbon layout. That is exactly how the Black Sesame
(HKEX:2533) FY2025 income Sankey shipped broken: opex was 2.2x revenue, the
generator placed nodes at negative Y and drew a 900px bar inside a 560px
viewBox, and because nothing rendered it, "verification" passed.

This linter parses every inline <svg> in a report and flags geometry that falls
outside its own viewBox (the deterministic half of the Step-10 render check).
It does NOT replace the browser screenshot pass in Step 10.7 — Mermaid blocks
are rendered by JS at view time and can only be checked in the browser — but it
catches the off-canvas/overflow class of bug for free, before you even start the
server.

Usage:
    /opt/anaconda3/bin/python3 lint_report_charts.py <report.md> [--tol 2] [--verbose]

Exit code 0 = all inline SVGs render within bounds; 1 = at least one is broken.
"""
import argparse
import re
import sys

NUM = re.compile(r'-?\d+(?:\.\d+)?')


def viewbox(svg_open_tag):
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', svg_open_tag)
    if m:
        p = [float(x) for x in NUM.findall(m.group(1))]
        if len(p) == 4:
            minx, miny, w, h = p
            return minx, miny, minx + w, miny + h
    # fall back to width/height
    mw = re.search(r'\bwidth\s*=\s*"([\d.]+)"', svg_open_tag)
    mh = re.search(r'\bheight\s*=\s*"([\d.]+)"', svg_open_tag)
    if mw and mh:
        return 0.0, 0.0, float(mw.group(1)), float(mh.group(1))
    return None


def attr(tag, name):
    m = re.search(rf'\b{name}\s*=\s*"(-?[\d.]+)"', tag)
    return float(m.group(1)) if m else None


def translate_of(tag):
    """Return (dx, dy) from a transform="translate(dx[,dy])" on a tag (0,0 if none).
    Reports a scale() if present so the caller can relax strictness."""
    m = re.search(r'transform\s*=\s*"([^"]*)"', tag)
    if not m:
        return 0.0, 0.0, False
    tf = m.group(1)
    has_scale = 'scale(' in tf or 'matrix(' in tf or 'rotate(' in tf
    t = re.search(r'translate\(\s*(-?[\d.]+)[ ,]+(-?[\d.]+)\s*\)', tf)
    if t:
        return float(t.group(1)), float(t.group(2)), has_scale
    t1 = re.search(r'translate\(\s*(-?[\d.]+)\s*\)', tf)
    if t1:
        return float(t1.group(1)), 0.0, has_scale
    return 0.0, 0.0, has_scale


def path_points(d):
    """Yield (x, y) control/anchor points from a path 'd' (abs coords only — our
    generators emit absolute M/C/L, which is what matters for bounds)."""
    nums = [float(x) for x in NUM.findall(d)]
    for i in range(0, len(nums) - 1, 2):
        yield nums[i], nums[i + 1]


# matches any leaf element we bounds-check, plus <g ...> / </g> for the transform stack
TOKEN = re.compile(r'<g\b[^>]*>|</g>|<rect\b[^>]*?/?>|<line\b[^>]*?/?>|'
                   r'<text\b[^>]*>|<path\b[^>]*?/?>', re.S)


def lint_svg(idx, svg, tol):
    """Return list of human-readable problem strings for one <svg> blob.

    Transform-aware: accumulates translate() from enclosing <g> groups and from
    each element's own transform, so a node deliberately shifted with
    transform="translate(-180,0)" (the money-flow generator does this) is checked
    at its *rendered* position, not its raw attribute position. Without this the
    linter false-positives on every money-flow chart.
    """
    open_tag = svg[: svg.index('>') + 1]
    vb = viewbox(open_tag)
    problems = []
    if vb is None:
        return [f"svg #{idx}: no viewBox/width-height — cannot bounds-check"]
    minx, miny, maxx, maxy = vb
    lo_x, hi_x = minx - tol, maxx + tol
    lo_y, hi_y = miny - tol, maxy + tol
    scale_seen = [False]

    def oob(x, y, what, ox, oy):
        if x is None or y is None:
            return
        X, Y = x + ox, y + oy
        if X < lo_x or X > hi_x or Y < lo_y or Y > hi_y:
            problems.append(f"svg #{idx}: {what} renders at ({X:.1f},{Y:.1f}) — outside "
                            f"viewBox [{minx:.0f},{miny:.0f} → {maxx:.0f},{maxy:.0f}]")

    gstack = []  # cumulative (dx, dy) per open <g>
    for tok in TOKEN.finditer(svg):
        s = tok.group(0)
        if s.startswith('<g'):
            dx, dy, sc = translate_of(s)
            px, py = (gstack[-1] if gstack else (0.0, 0.0))
            gstack.append((px + dx, py + dy))
            scale_seen[0] |= sc
            continue
        if s == '</g>':
            if gstack:
                gstack.pop()
            continue
        gx, gy = (gstack[-1] if gstack else (0.0, 0.0))
        ex, ey, sc = translate_of(s)
        scale_seen[0] |= sc
        ox, oy = gx + ex, gy + ey
        if s.startswith('<rect'):
            x, y, w, h = attr(s, 'x'), attr(s, 'y'), attr(s, 'width'), attr(s, 'height')
            if None in (x, y, w, h):
                continue
            oob(x, y, "rect top-left", ox, oy)
            oob(x + w, y + h, "rect bottom-right", ox, oy)
            if h > (maxy - miny) + tol:
                problems.append(f"svg #{idx}: rect height {h:.0f}px exceeds viewBox "
                                f"height {maxy - miny:.0f}px (bar taller than canvas)")
        elif s.startswith('<path'):
            md = re.search(r'\bd\s*=\s*"([^"]+)"', s)
            if md:
                for x, y in path_points(md.group(1)):
                    oob(x, y, "path point", ox, oy)
        elif s.startswith('<line'):
            oob(attr(s, 'x1'), attr(s, 'y1'), "line start", ox, oy)
            oob(attr(s, 'x2'), attr(s, 'y2'), "line end", ox, oy)
        elif s.startswith('<text'):
            oob(attr(s, 'x'), attr(s, 'y'), "text anchor", ox, oy)

    if scale_seen[0] and problems:
        problems.append(f"svg #{idx}: note — a scale()/rotate()/matrix() transform is "
                        f"present; bounds shown ignore it, eyeball this one in the browser too")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('report', help='path to the report .md')
    ap.add_argument('--tol', type=float, default=2.0,
                    help='out-of-bounds tolerance in px (default 2)')
    ap.add_argument('--verbose', action='store_true',
                    help='list every SVG checked, even the clean ones')
    a = ap.parse_args()

    text = open(a.report, encoding='utf-8').read()
    svgs = re.findall(r'<svg\b.*?</svg>', text, re.S)
    mermaid = re.findall(r'```mermaid', text)

    if not svgs:
        print(f"no inline <svg> found in {a.report}")
    total_problems = []
    for i, svg in enumerate(svgs, 1):
        probs = lint_svg(i, svg, a.tol)
        label = re.search(r'aria-label\s*=\s*"([^"]+)"', svg)
        name = label.group(1) if label else f"svg #{i}"
        if probs:
            total_problems += probs
            print(f"✗ FAIL  {name}")
            for p in probs:
                print(f"        {p}")
        elif a.verbose:
            print(f"✓ ok    {name}")

    print(f"\n{len(svgs)} inline SVG(s) checked, {len(mermaid)} mermaid block(s) "
          f"present (mermaid renders in-browser — screenshot-verify in Step 10.7).")
    if total_problems:
        print(f"✗ {len(total_problems)} geometry problem(s) — FIX before shipping. "
              f"A bar/label/node outside the viewBox renders clipped or off-canvas.")
        return 1
    print("✓ all inline SVGs render within their viewBox.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
