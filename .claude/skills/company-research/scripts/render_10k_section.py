#!/usr/bin/env python3
"""Render a section of a locally-cached SEC 10-K HTML file to a PNG image.

Used by the company-research skill's Section 4 (Products & Services), which
embeds the issuer's own product table as an image to anchor the section to
primary disclosure.

The script locates a target HTML element by either:
  - An anchor string that uniquely appears inside the desired <table> (e.g.
    a product family name like "SABRE"), OR
  - A CSS selector you pass explicitly via --selector

…then screenshots that element (with some padding above for the section
header) and saves the PNG.

Requires: pip install playwright && python3 -m playwright install chromium

Usage examples:

  # Render Lam Research 2025 10-K products table (anchored by "SABRE")
  python3 render_10k_section.py \\
      --html financial_reports/LRCX/lrcx-20250629.htm \\
      --anchor SABRE \\
      --output reports/company/LamResearch_NASDAQ_LRCX/charts/lrcx_10k_products_table.png

  # Render a section by CSS selector instead
  python3 render_10k_section.py \\
      --html financial_reports/AAPL/aapl-20240928.htm \\
      --selector "table.products" \\
      --output reports/company/Apple_NASDAQ_AAPL/charts/aapl_10k_products.png

  # Render with extra header padding (default 80px above element)
  python3 render_10k_section.py \\
      --html <path> --anchor <text> --output <png> --pad-top 150

Notes for Chinese 年报 PDFs:
  This script renders HTML. For Chinese A-share PDFs (cninfo), use
  PyMuPDF (fitz) instead — see the project's render_pdf_pages.py pattern.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def render(
    html_path: str,
    output_png: str,
    anchor: str | None = None,
    selector: str | None = None,
    pad_top: int = 80,
    pad_side: int = 20,
    pad_bottom: int = 20,
    viewport_w: int = 1200,
    viewport_h: int = 2400,
    scale: int = 2,
) -> str:
    """Render the located element to PNG. Returns the output path on success."""
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError:
        sys.exit(
            "playwright is not installed. Install with:\n"
            "    pip install playwright && python3 -m playwright install chromium"
        )

    if not anchor and not selector:
        sys.exit("Either --anchor or --selector must be provided.")

    html_abs = Path(html_path).resolve()
    if not html_abs.exists():
        sys.exit(f"HTML file not found: {html_abs}")

    output_abs = Path(output_png).resolve()
    output_abs.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": viewport_w, "height": viewport_h},
            device_scale_factor=scale,
        )
        page.goto(f"file://{html_abs}")

        # Locate the target element
        if selector:
            target = page.locator(selector).first
        else:
            # Find the <table> that contains the anchor string
            target = page.locator("table").filter(has_text=anchor).first

        try:
            target.scroll_into_view_if_needed(timeout=5000)
            bbox = target.bounding_box()
        except Exception as e:
            browser.close()
            sys.exit(
                f"Could not locate element (anchor={anchor!r}, selector={selector!r}): {e}"
            )

        if bbox is None:
            browser.close()
            sys.exit("Element located but has no bounding box (possibly hidden).")

        # Clip the screenshot to the element + padding
        clip = {
            "x": max(0, bbox["x"] - pad_side),
            "y": max(0, bbox["y"] - pad_top),
            "width": min(viewport_w, bbox["width"] + 2 * pad_side),
            "height": min(viewport_h, bbox["height"] + pad_top + pad_bottom),
        }
        page.screenshot(path=str(output_abs), clip=clip)
        browser.close()

    size_kb = output_abs.stat().st_size / 1024
    print(f"Rendered: {output_abs} ({size_kb:.1f} KB)")
    return str(output_abs)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html", required=True, help="Path to the local 10-K HTML file")
    ap.add_argument("--output", required=True, help="Output PNG path")
    ap.add_argument(
        "--anchor",
        help="Unique text string inside the target <table> element (e.g. 'SABRE')",
    )
    ap.add_argument(
        "--selector",
        help="CSS selector for the target element (e.g. 'table.products'). Overrides --anchor.",
    )
    ap.add_argument("--pad-top", type=int, default=80, help="Pixels above element (default 80)")
    ap.add_argument("--pad-side", type=int, default=20, help="Pixels left/right (default 20)")
    ap.add_argument("--pad-bottom", type=int, default=20, help="Pixels below element (default 20)")
    ap.add_argument("--viewport-w", type=int, default=1200, help="Browser viewport width (default 1200)")
    ap.add_argument("--viewport-h", type=int, default=2400, help="Browser viewport height (default 2400)")
    ap.add_argument("--scale", type=int, default=2, help="Device scale factor (default 2 = retina)")
    args = ap.parse_args()

    render(
        html_path=args.html,
        output_png=args.output,
        anchor=args.anchor,
        selector=args.selector,
        pad_top=args.pad_top,
        pad_side=args.pad_side,
        pad_bottom=args.pad_bottom,
        viewport_w=args.viewport_w,
        viewport_h=args.viewport_h,
        scale=args.scale,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
