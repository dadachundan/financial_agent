"""
kg_models.py — Graph data model helpers for the knowledge graph.
"""

import json
import sqlite3


# ── Node / edge colours (declarative config) ──────────────────────────────────

NODE_STYLE = {
    "company": {
        "color": {"background": "#0d6efd", "border": "#084298"},
        "font":  {"color": "#084298"},
        "group": "company",
    },
    "business": {
        "color": {"background": "#fd7e14", "border": "#a04c00"},
        "font":  {"color": "#a04c00"},
        "group": "business",
        "shape": "square",
    },
}

EDGE_STYLE = {
    "bc": {
        "color":  {"color": "#6c757d", "highlight": "#0d6efd"},
        "dashes": False,
    },
    "bb": {
        "color":  {"color": "#e64545", "highlight": "#e64545"},
        "dashes": True,
    },
    "cc": {
        "color":  {"color": "#6f42c1", "highlight": "#6f42c1"},
        "dashes": [4, 3],
    },
}


# ── Graph builder ─────────────────────────────────────────────────────────────

def build_graph_json(conn: sqlite3.Connection) -> str:
    """Return a JSON string suitable for vis-network DataSets."""
    nodes, edges = [], []

    for row in conn.execute("SELECT id, name, description FROM companies"):
        nodes.append({
            "id":    f"c{row['id']}",
            "label": row["name"],
            "title": row["description"],
            **NODE_STYLE["company"],
        })

    for row in conn.execute("SELECT id, name, description FROM businesses"):
        nodes.append({
            "id":    f"b{row['id']}",
            "label": row["name"],
            "title": row["description"],
            **NODE_STYLE["business"],
        })

    for row in conn.execute(
            "SELECT business_id, company_id, comment FROM business_company"):
        edges.append({
            "from":  f"b{row['business_id']}",
            "to":    f"c{row['company_id']}",
            "title": row["comment"],
            **EDGE_STYLE["bc"],
        })

    for row in conn.execute(
            "SELECT business_from, business_to, comment FROM business_business"):
        edges.append({
            "from":  f"b{row['business_from']}",
            "to":    f"b{row['business_to']}",
            "title": row["comment"],
            **EDGE_STYLE["bb"],
        })

    for row in conn.execute(
            "SELECT company_from, company_to, comment FROM company_company"):
        edges.append({
            "from":  f"c{row['company_from']}",
            "to":    f"c{row['company_to']}",
            "title": row["comment"],
            **EDGE_STYLE["cc"],
        })

    return json.dumps({"nodes": nodes, "edges": edges})
