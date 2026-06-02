"""Flask blueprint for the Price Target viewer (mounted at /pt).

Surfaces the contents of ``stock_price_target.db`` — every sell-side PT row
extracted from zsxq broker PDFs. Default sort is by report_date desc. A
text filter narrows on ticker / company name / Chinese name / broker.
Clicking the report URL column opens the source PDF in the ZSXQ viewer.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Blueprint, jsonify, render_template
from markupsafe import Markup

import nav_widget2 as nw2
import sector_map
from db_paths import db_path

DB_PATH: Path = db_path("stock_price_target.db")

pt_bp = Blueprint("pt", __name__, template_folder="templates")


def _query_all_rows() -> list[dict]:
    if not DB_PATH.exists():
        return []
    with sqlite3.connect(DB_PATH) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("""
            SELECT
                id,
                company_ticker,
                company_name,
                research_institute,
                rating,
                price_target,
                target_currency,
                catalyst,
                report_file_id,
                report_pdf_filename,
                report_url,
                report_date,
                report_date_price,
                report_date_market_cap,
                price_currency,
                upside_pct,
                created_at
            FROM price_targets
            ORDER BY report_date DESC, id DESC
        """).fetchall()
        # Enrich each row with the user-maintained sector at runtime (looked
        # up via sector_map.py — change that file and the column updates on
        # the next request, no DB migration needed).
        out = []
        for r in rows:
            d = dict(r)
            d["sector"] = sector_map.sector_for_yfinance(d["company_ticker"])
            out.append(d)
        return out


@pt_bp.route("/")
def index():
    rows = _query_all_rows()
    return render_template(
        "pt.html",
        rows=rows,
        total=len(rows),
        NAV_HTML=Markup(nw2.NAV_HTML),
    )


@pt_bp.route("/api/rows")
def api_rows():
    return jsonify(_query_all_rows())
