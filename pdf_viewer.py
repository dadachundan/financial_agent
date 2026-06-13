"""In-browser PDF viewer with selection-anchored markdown comments.

Mirrors the UX of /claude-reports/view/<md> (right-rail cards anchored to
selected text via TextQuoteSelector) but for any PDF library on disk.

Renders the PDF client-side with PDF.js so text selection, quote
extraction (prefix + selected + suffix) and `<mark>` wrapping work the
same way as the markdown viewer. For scanned pages where PDF.js's text
layer is empty, the user can Shift+drag a rectangle; the rect goes to
the backend, which runs ocrmac (Apple Vision) on the cropped image and
returns the OCR'd text as the quote — so quote-based anchoring is
unified across vector and scanned PDFs.

Routes registered on the parent blueprint (URL prefix becomes the
viewer's namespace, e.g. /zsxq, /sec, /cn, /manual-report):

  GET    /pdf-viewer/<file_id>             — viewer page
  GET    /pdf-viewer-pdf/<file_id>         — raw PDF bytes (used by PDF.js)
  GET    /pdf-inline-comments              — list  (?file_id=N)
  POST   /pdf-inline-comments              — create
  PATCH  /pdf-inline-comments/<id>         — update body
  DELETE /pdf-inline-comments/<id>         — delete
  POST   /pdf-page-ocr                     — OCR a full page (cached)
  POST   /pdf-ocr-region                   — OCR a rect on a page

Storage: `pdf_inline_comments` and `pdf_page_ocr` in db/notes.db. Both
tables namespace rows by (source, file_id) so the four PDF libraries
share storage cleanly. See pdf_inline_comments.py + pdf_page_ocr.py.

`register(bp, *, source, path_provider)`:
- bp: Flask Blueprint to attach routes to. The blueprint's URL prefix
  becomes the viewer's namespace.
- source: one of 'zsxq' | 'sec' | 'cn' | 'manual'.
- path_provider: callable (file_id: int) -> dict | None returning the
  PDF's metadata: {local_path: str, name: str, title: str}. Each
  parent app (zsxq_viewer, fetch_financial_report, fetch_cninfo_report,
  notes_app) wires this to its own DB lookup.
"""
from __future__ import annotations

import io
from pathlib import Path

from flask import Blueprint, abort, jsonify, render_template_string, request, send_file

import pdf_inline_comments as _pic
import pdf_page_ocr as _ppo


def register(bp: Blueprint, *, source: str, path_provider) -> None:
    """Attach all PDF-viewer routes to the given blueprint.

    See module docstring for parameter semantics.
    """
    if source not in {"zsxq", "sec", "cn", "manual"}:
        raise ValueError(f"unknown source: {source!r}")

    def _meta(file_id: int) -> dict | None:
        info = path_provider(file_id)
        if not info:
            return None
        # Tolerate provider returning Row-like or dict-like objects.
        return {
            "local_path": info["local_path"] if "local_path" in info else None,
            "name": info["name"] if "name" in info else "",
            "title": info["title"] if "title" in info else "",
        }

    @bp.route("/pdf-viewer/<int:file_id>")
    def pdf_viewer(file_id: int):
        m = _meta(file_id)
        if not m or not m["local_path"]:
            abort(404, "No local file recorded for this PDF.")
        if not Path(m["local_path"]).exists():
            abort(404, f"File not found on disk: {m['local_path']}")
        return render_template_string(
            _VIEWER_TMPL,
            file_id=file_id,
            name=m["name"] or "",
            title=m["title"] or m["name"] or f"PDF {file_id}",
        )

    @bp.route("/pdf-viewer-pdf/<int:file_id>")
    def pdf_viewer_pdf(file_id: int):
        """Serve the raw PDF bytes for PDF.js to fetch. The template uses
        this URL (not the parent app's own PDF route) so pdf_viewer stays
        self-contained — different parent apps use different naming
        (zsxq /pdf/<id>, sec /file/<id>, cn /open/<id>, manual /pdf/<id>)."""
        m = _meta(file_id)
        if not m or not m["local_path"]:
            abort(404, "No local file recorded for this PDF.")
        path = Path(m["local_path"])
        if not path.exists():
            abort(404, f"File not found on disk: {path}")
        return send_file(path, mimetype="application/pdf")

    # ── CRUD ────────────────────────────────────────────────────────────
    @bp.route("/pdf-inline-comments", methods=["GET"])
    def pdf_ic_list():
        try:
            file_id = int(request.args.get("file_id", "0"))
        except (TypeError, ValueError):
            return jsonify(error="invalid file_id"), 400
        if not file_id:
            return jsonify(error="missing file_id"), 400
        return jsonify(comments=_pic.list_for_file(source, file_id))

    @bp.route("/pdf-inline-comments", methods=["POST"])
    def pdf_ic_create():
        data = request.get_json(silent=True) or {}
        try:
            file_id = int(data.get("file_id") or 0)
            page = int(data.get("page") or 0)
        except (TypeError, ValueError):
            return jsonify(error="file_id/page must be int"), 400
        quote = (data.get("quote") or "").strip()
        # body may be empty — that's a highlight-only entry (no comment).
        # We still require a quote (or rect) so there's something to anchor.
        body = (data.get("body") or "")
        rect = data.get("rect")  # {x,y,w,h} in PDF page CSS px at scale=1, or None
        if not file_id or not page:
            return jsonify(error="file_id, page required"), 400
        if not quote and not rect:
            return jsonify(error="quote or rect required"), 400
        row = _pic.create(
            source=source,
            file_id=file_id,
            page=page,
            quote=quote,
            prefix=(data.get("prefix") or "")[:64],
            suffix=(data.get("suffix") or "")[:64],
            rect=rect,
            body=body,
        )
        return jsonify(comment=row), 201

    @bp.route("/pdf-inline-comments/<int:cid>", methods=["PATCH"])
    def pdf_ic_update(cid: int):
        data = request.get_json(silent=True) or {}
        # body may be empty (downgrading a comment to a plain highlight).
        body = (data.get("body") or "")
        row = _pic.update(cid, body)
        if not row:
            return jsonify(error="not found"), 404
        return jsonify(comment=row)

    @bp.route("/pdf-inline-comments/<int:cid>", methods=["DELETE"])
    def pdf_ic_delete(cid: int):
        ok = _pic.delete(cid)
        if not ok:
            return jsonify(error="not found"), 404
        return "", 204

    # ── Per-page OCR (synthetic text layer for scanned pages) ──────────
    @bp.route("/pdf-page-ocr", methods=["POST"])
    def pdf_page_ocr_route():
        data = request.get_json(silent=True) or {}
        try:
            file_id = int(data.get("file_id") or 0)
            page = int(data.get("page") or 0)
        except (TypeError, ValueError):
            return jsonify(error="bad payload"), 400
        if not file_id or not page:
            return jsonify(error="file_id/page required"), 400
        cached = _ppo.get(source, file_id, page)
        if cached is not None:
            return jsonify(words=cached, cached=True)
        m = _meta(file_id)
        if not m or not m["local_path"] or not Path(m["local_path"]).exists():
            return jsonify(error="pdf not found"), 404
        try:
            words = _ppo.compute(source, file_id, page, m["local_path"])
        except Exception as e:
            return jsonify(error=f"OCR failed: {e}"), 500
        return jsonify(words=words, cached=False)

    # ── On-demand region OCR (for scanned pages) ────────────────────────
    @bp.route("/pdf-ocr-region", methods=["POST"])
    def pdf_ocr_region():
        data = request.get_json(silent=True) or {}
        try:
            file_id = int(data.get("file_id") or 0)
            page = int(data.get("page") or 0)
            x = float(data.get("x") or 0)
            y = float(data.get("y") or 0)
            w = float(data.get("w") or 0)
            h = float(data.get("h") or 0)
        except (TypeError, ValueError):
            return jsonify(error="bad payload"), 400
        if not file_id or not page or w <= 1 or h <= 1:
            return jsonify(error="file_id/page/rect required"), 400
        m = _meta(file_id)
        if not m or not m["local_path"] or not Path(m["local_path"]).exists():
            return jsonify(error="pdf not found"), 404

        try:
            import fitz  # type: ignore
        except ImportError:
            return jsonify(error="PyMuPDF not installed"), 500

        try:
            doc = fitz.open(m["local_path"])
        except Exception as e:
            return jsonify(error=f"fitz open failed: {e}"), 500
        try:
            if page < 1 or page > doc.page_count:
                return jsonify(error="page out of range"), 400
            pg = doc[page - 1]
            # Caller sends coords in CSS px at PDF.js scale=1, which equals
            # PDF points (1 CSS px @ scale=1 == 1 PDF user-space unit when
            # viewport.scale==1). Clip the rect to the page bounds.
            pw, ph = pg.rect.width, pg.rect.height
            x0 = max(0.0, min(pw, x))
            y0 = max(0.0, min(ph, y))
            x1 = max(0.0, min(pw, x + w))
            y1 = max(0.0, min(ph, y + h))
            if x1 - x0 < 2 or y1 - y0 < 2:
                return jsonify(error="rect too small"), 400
            clip = fitz.Rect(x0, y0, x1, y1)

            # Fast path: native text (vector PDF) inside the rect. fitz already
            # returns reading-order text for a clipping rect, so no OCR needed.
            native = (pg.get_text("text", clip=clip) or "").strip()
            if len(native) >= 4:
                doc.close()
                return jsonify(text=native, source="native")

            # Slow path: render the crop and OCR with Apple Vision.
            try:
                from ocrmac import ocrmac  # type: ignore
                from PIL import Image  # type: ignore
            except ImportError:
                doc.close()
                return jsonify(error="ocrmac/Pillow not installed"), 500
            pix = pg.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), clip=clip)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            anns = ocrmac.OCR(
                img,
                recognition_level="accurate",
                language_preference=["en-US", "zh-Hans"],
            ).recognize()

            def _sort_key(a):
                _t, _c, bbox = a
                bx, by, bw, bh = bbox
                return (round((1 - by - bh) * 100), round(bx * 100))
            anns.sort(key=_sort_key)
            text = " ".join(t for t, _c, _b in anns if t.strip())
        finally:
            try:
                doc.close()
            except Exception:
                pass
        return jsonify(text=text, source="ocr")

    # ── On-demand region screenshot (PNG crop of a rect) ────────────────
    @bp.route("/pdf-region-image/<int:file_id>")
    def pdf_region_image(file_id: int):
        """Render a rectangular crop of a PDF page as a PNG.

        A region-style comment stores its box in `pdf_inline_comments.
        rect_json` ({x,y,w,h} in PDF points). The /comments/ feed points an
        <img> at this route to show a screenshot of the region instead of
        just its OCR'd text. Stateless — nothing is persisted; the crop is
        re-rendered from the PDF + rect on each request, so no write ever
        touches the (Tier-1, read-only) comments DB.
        """
        try:
            page = int(request.args.get("page") or 0)
            x = float(request.args.get("x") or 0)
            y = float(request.args.get("y") or 0)
            w = float(request.args.get("w") or 0)
            h = float(request.args.get("h") or 0)
        except (TypeError, ValueError):
            abort(400, "bad rect params")
        if not page or w <= 1 or h <= 1:
            abort(400, "page/rect required")
        m = _meta(file_id)
        if not m or not m["local_path"] or not Path(m["local_path"]).exists():
            abort(404, "pdf not found")
        try:
            import fitz  # type: ignore
        except ImportError:
            abort(500, "PyMuPDF not installed")
        try:
            doc = fitz.open(m["local_path"])
        except Exception as e:
            abort(500, f"fitz open failed: {e}")
        try:
            if page < 1 or page > doc.page_count:
                abort(400, "page out of range")
            pg = doc[page - 1]
            pw, ph = pg.rect.width, pg.rect.height
            # A few points of padding so the crop isn't flush against the text.
            pad = 3.0
            x0 = max(0.0, min(pw, x - pad))
            y0 = max(0.0, min(ph, y - pad))
            x1 = max(0.0, min(pw, x + w + pad))
            y1 = max(0.0, min(ph, y + h + pad))
            if x1 - x0 < 2 or y1 - y0 < 2:
                abort(400, "rect too small")
            clip = fitz.Rect(x0, y0, x1, y1)
            # 3× supersample so the crop stays crisp when displayed at the
            # full width of the comments column (charts are near page-width).
            pix = pg.get_pixmap(matrix=fitz.Matrix(3.0, 3.0), clip=clip)
            png = pix.tobytes("png")
        finally:
            try:
                doc.close()
            except Exception:
                pass
        resp = send_file(io.BytesIO(png), mimetype="image/png")
        # Deterministic for a given (file_id, page, rect) — cache aggressively.
        resp.headers["Cache-Control"] = "public, max-age=86400"
        return resp


# ── Template ─────────────────────────────────────────────────────────────
_VIEWER_TMPL = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ name }}</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <style>
    body{background:#525659;margin:0;color:#222}
    .topbar{background:#323639;color:#eee;padding:8px 16px;display:flex;
            gap:14px;align-items:center;font-family:-apple-system,sans-serif;
            font-size:.88rem;position:sticky;top:0;z-index:1000;
            box-shadow:0 1px 3px rgba(0,0,0,.3)}
    .topbar a{color:#9ecbff;text-decoration:none}
    .topbar a:hover{text-decoration:underline}
    .topbar .filename{flex:1;color:#bbb;overflow:hidden;text-overflow:ellipsis;
                      white-space:nowrap;font-family:ui-monospace,Menlo,monospace;
                      font-size:.78rem}
    .topbar .zoom-btn{background:#454a4d;color:#eee;border:1px solid #5a5f64;
                      border-radius:3px;padding:3px 9px;cursor:pointer;
                      font-family:inherit;font-size:.84rem}
    .topbar .zoom-btn:hover{background:#555a5d}
    .topbar .zoom-val{min-width:46px;text-align:center;color:#ddd}
    .topbar .page-info{color:#bbb;font-family:ui-monospace,Menlo,monospace;
                       font-size:.78rem}
    .topbar input.page-input{background:#454a4d;color:#fff;border:1px solid #5a5f64;
                             border-radius:3px;padding:3px 6px;width:50px;
                             text-align:center;font-family:inherit;font-size:.84rem}
    .topbar .mode-btn{background:#454a4d;color:#eee;border:1px solid #5a5f64;
                      border-radius:3px;padding:3px 9px;cursor:pointer;
                      font-family:inherit;font-size:.84rem}
    .topbar .mode-btn.active{background:#1F4E78;border-color:#3a6e9a;color:#fff}
    .topbar .mode-btn:hover{background:#555a5d}
    .topbar .mode-btn.active:hover{background:#265d8e}

    .layout{display:flex;align-items:flex-start;gap:0;position:relative;
            min-height:calc(100vh - 44px)}
    .doc{flex:1 1 auto;min-width:0;padding:24px 0 80px;
         display:flex;flex-direction:column;align-items:center}
    .pdf-page{background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.4);
              margin:0 auto 16px;position:relative;
              max-width:100%;line-height:1}
    .pdf-page canvas{display:block;width:100%;height:100%}
    .pdf-page .pageNumber{position:absolute;top:6px;right:8px;font-size:.7rem;
                          color:#999;background:rgba(255,255,255,.7);
                          padding:1px 6px;border-radius:3px;font-family:ui-monospace,
                          Menlo,monospace;pointer-events:none;
                          font-family:-apple-system,sans-serif}
    .pdf-page.loading::before{content:"loading…";position:absolute;top:50%;left:50%;
                              transform:translate(-50%,-50%);color:#999;font-size:.9rem;
                              font-family:-apple-system,sans-serif}

    /* PDF.js text layer — copied from pdfjs-dist css so selection works.
       Spans are absolutely-positioned, transparent text on top of the
       canvas, with the same character metrics so selection rectangles
       align with what's visible. */
    .textLayer{position:absolute;left:0;top:0;right:0;bottom:0;
               overflow:hidden;opacity:0.2;line-height:1;
               text-size-adjust:none;forced-color-adjust:none;
               transform-origin:0 0;z-index:2;cursor:text}
    .textLayer span,.textLayer br{color:transparent;position:absolute;
                                  white-space:pre;cursor:text;
                                  transform-origin:0% 0%}
    .textLayer span.markedContent{top:0;height:0}
    .textLayer ::selection{background:rgba(0,0,255,.25)}
    .textLayer mark.pic-hl{background:#ffe9a3;color:transparent;
                           border-radius:2px;cursor:pointer;
                           opacity:1;mix-blend-mode:multiply;
                           padding:0;display:inline}
    /* Rect-anchored highlights (drawn over the page; no text inside) */
    /* pointer-events:none so a rect overlay never blocks selecting the text
       underneath it. Click-to-activate is re-added via hit-testing on the
       page (see the delegated click handler). */
    .pdf-page .rect-hl{position:absolute;background:rgba(255,225,80,.35);
                       border:1px solid rgba(220,170,30,.5);border-radius:2px;
                       cursor:pointer;z-index:3;pointer-events:none;
                       transition:background .15s}
    .pdf-page .rect-hl:hover{background:rgba(255,225,80,.55)}
    .pdf-page .rect-hl.active{background:rgba(255,205,30,.5);
                              border-color:rgba(190,140,10,.8)}

    /* Region-drag overlay (active when user holds Shift on the page) */
    .pdf-page .region-overlay{position:absolute;inset:0;z-index:4;
                              cursor:crosshair;background:transparent;
                              display:none}
    .pdf-page.region-mode .region-overlay{display:block}
    .pdf-page.region-mode .textLayer{pointer-events:none}
    /* While OCR is in flight on a scanned page, show a small spinner badge.
       Once the synthetic text layer lands, the class is removed and the
       page behaves like any text-selectable page. */
    .pdf-page.ocr-loading::after{content:"⏳ OCR…";
                                 position:absolute;top:6px;left:8px;
                                 background:rgba(255,200,0,.92);color:#5a3a00;
                                 padding:2px 8px;border-radius:3px;font-size:.7rem;
                                 font-family:-apple-system,sans-serif;font-weight:600;
                                 pointer-events:none;letter-spacing:.02em;z-index:5}
    /* Synthetic OCR word spans — transparent, covering the word's bbox, so
       native text selection across them produces the OCR'd string. */
    .textLayer span.ocr-word{color:transparent;position:absolute;
                             white-space:nowrap;cursor:text;
                             transform-origin:0 0;line-height:1;
                             font-family:-apple-system,BlinkMacSystemFont,
                                         "Helvetica Neue",sans-serif}
    .pdf-page .region-rubber{position:absolute;background:rgba(31,78,120,.18);
                             border:1.5px dashed #1F4E78;pointer-events:none}

    /* Floating action toolbar at the selection's right edge: [🖍 highlight | 💬 comment].
       Position-FIXED (viewport-relative) so it stays anchored to the selection
       even as the user scrolls — preserves the toolbar from drifting off-screen. */
    .pic-fab{position:fixed;z-index:1500;background:#fff;
             border:1px solid #cfd6df;border-radius:22px;
             padding:3px;cursor:default;
             box-shadow:0 2px 8px rgba(0,0,0,.22);display:none;
             align-items:center;gap:2px;
             transition:box-shadow .15s}
    .pic-fab.show{display:inline-flex}
    .pic-fab button{background:none;border:none;cursor:pointer;
                    width:32px;height:32px;border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    color:#1F4E78;padding:0;font-size:1rem;
                    transition:background .12s}
    .pic-fab button:hover{background:#eef4fb}
    .pic-fab button.hl:hover{background:#fff3b8;color:#7a5b00}
    .pic-fab button svg{width:18px;height:18px;display:block}

    /* Popover that appears when you click an existing highlight */
    .pic-hl-pop{position:fixed;z-index:1600;background:#fff;
                border:1px solid #cfd6df;border-radius:8px;
                padding:4px;display:none;align-items:center;gap:3px;
                box-shadow:0 3px 10px rgba(0,0,0,.24)}
    .pic-hl-pop.show{display:inline-flex}
    /* Labelled pill buttons (icon + text) so the delete action is obvious —
       a body-less highlight has no rail card, so this popover IS its only UI. */
    .pic-hl-pop button{background:none;border:none;cursor:pointer;
                       height:30px;border-radius:6px;
                       display:inline-flex;align-items:center;gap:5px;
                       color:#1F4E78;padding:0 11px 0 8px;
                       font-size:.82rem;font-weight:600;
                       transition:background .12s}
    .pic-hl-pop button svg{width:16px;height:16px;display:block;flex:none}
    .pic-hl-pop button:hover{background:#eef4fb}
    .pic-hl-pop button.danger{color:#c0392b}
    .pic-hl-pop button.danger:hover{background:#fdecea;color:#c0392b}

    /* Comments rail — clone of /claude-reports/view comments-rail.
       Default width scales with viewport via clamp() so the rail keeps
       proportions on a wide monitor; user can still drag to override
       (the chosen width is persisted to localStorage). */
    .comments-rail{flex:0 0 auto;width:clamp(340px, 28vw, 720px);
                   min-width:240px;max-width:720px;
                   position:relative;min-height:200px;
                   padding:24px 8px 24px 14px;box-sizing:border-box;
                   background:#3a3e41}
    .comments-rail.hidden{display:none}
    .rail-splitter{flex:0 0 6px;align-self:stretch;cursor:col-resize;
                   background:transparent;position:relative;z-index:5}
    .rail-splitter:hover{background:#5a6066}
    .rail-splitter.dragging{background:#1F4E78}
    .rail-splitter.hidden{display:none}
    .pic-card{position:absolute;top:0;left:14px;right:8px;
              background:#fff;border:1px solid #d0d4d8;border-radius:8px;
              padding:10px 12px;box-shadow:0 1px 3px rgba(0,0,0,.2);
              font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
              font-size:.88rem;cursor:pointer;
              transition:box-shadow .15s, border-color .15s, transform .15s}
    .pic-card:hover{box-shadow:0 2px 8px rgba(0,0,0,.28);border-color:#a9bdd1}
    .pic-card.active{box-shadow:0 2px 14px rgba(31,78,120,.4);
                     border-color:#1F4E78;transform:translateX(-4px);z-index:3}
    .pic-card:focus{outline:none;box-shadow:0 2px 16px rgba(31,78,120,.45);
                    border-color:#1F4E78}
    .pic-card.orphan{background:#fffaee;border-color:#f0d8a6}
    /* Body-less highlight cards: a yellow left rail to read as a highlight. */
    .pic-card.highlight-only{border-left:3px solid #f0c14b}
    .pic-card.pending{border-color:#1F4E78;box-shadow:0 3px 14px rgba(31,78,120,.32);
                      cursor:default}
    .pic-page-tag{font-size:.68rem;color:#888;font-family:ui-monospace,Menlo,monospace;
                  margin-bottom:4px;text-transform:uppercase;letter-spacing:.04em}
    .pic-quote{font-size:.74rem;color:#555;font-style:italic;
               border-left:3px solid #ffd966;padding:2px 0 2px 8px;
               margin-bottom:6px;max-height:3.6em;overflow:hidden;line-height:1.4}
    .pic-quote.empty{color:#888;font-style:normal}
    .pic-body{font-size:.88rem;color:#222;line-height:1.45;word-wrap:break-word}
    .pic-body p{margin:0 0 .3em}
    .pic-body p:last-child{margin-bottom:0}
    .pic-body ul,.pic-body ol{padding-left:1.2em;margin:.2em 0}
    .pic-body code{background:#f0f0f0;padding:1px 4px;border-radius:2px;font-size:.85em}
    .pic-body strong{font-weight:600}
    .pic-body.collapsible{position:relative}
    .pic-body.collapsed{max-height:140px;overflow:hidden}
    .pic-body.collapsed::after{content:"";position:absolute;left:0;right:0;bottom:0;
                               height:38px;pointer-events:none;
                               background:linear-gradient(rgba(255,255,255,0),#fff 90%)}
    .pic-expand{font-size:.78rem;color:#0366d6;cursor:pointer;background:none;
                border:none;padding:0;margin-top:4px;font-family:inherit}
    .pic-expand:hover{text-decoration:underline}
    .pic-meta{font-size:.7rem;color:#888;margin-top:6px;
              font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
    .pic-actions{font-size:.78rem;margin-top:6px;display:flex;gap:12px}
    .pic-actions button{background:none;border:none;color:#0366d6;
                        cursor:pointer;padding:0;font-size:.78rem;
                        font-family:inherit}
    .pic-actions button:hover{text-decoration:underline}
    .pic-actions button.danger{color:#c00}

    .pic-editor textarea{width:100%;min-height:64px;max-height:240px;
                         border:1px solid #cfd6df;border-radius:6px;
                         padding:7px 9px;font-family:inherit;font-size:.9rem;
                         resize:vertical;outline:none;box-sizing:border-box;
                         transition:border-color .15s;line-height:1.4}
    .pic-editor textarea:focus{border-color:#1F4E78;
                               box-shadow:0 0 0 2px rgba(31,78,120,.12)}
    .pic-editor-actions{display:flex;gap:6px;justify-content:flex-end;
                        margin-top:8px;align-items:center}
    .pic-editor-actions .cancel{background:none;border:none;color:#555;
                                cursor:pointer;padding:6px 10px;font-size:.85rem;
                                font-family:inherit;border-radius:14px}
    .pic-editor-actions .cancel:hover{background:#f1f3f7;color:#222}
    .pic-editor-actions .save{background:#1F4E78;color:#fff;border:none;
                              border-radius:14px;padding:6px 14px;font-size:.85rem;
                              cursor:pointer;font-family:inherit;font-weight:500}
    .pic-editor-actions .save:disabled{background:#cfd6df;cursor:not-allowed}
    .pic-editor-actions .save:not(:disabled):hover{background:#16395a}
    .pic-editor-hint{font-size:.72rem;color:#888;margin-right:auto;
                     font-style:italic}
    .pic-editor textarea.upl-dragover{border-color:#1F4E78;background:#f0f6ff}
    .pic-body img,.pic-modal-body img{max-width:100%;height:auto;
                                      border-radius:4px;display:block;
                                      margin:.4em 0}

    .pic-expand-btn{display:inline-flex;align-items:center;gap:4px;
                    font-size:.78rem;color:#0366d6;cursor:pointer;
                    background:none;border:none;padding:0;margin-top:6px;
                    font-family:inherit}
    .pic-expand-btn:hover{text-decoration:underline}
    .pic-expand-btn svg{width:13px;height:13px;flex:none}

    dialog.pic-modal{border:none;border-radius:10px;padding:0;
                     width:min(1200px,92vw);min-width:360px;max-width:96vw;
                     resize:horizontal;overflow:hidden;
                     box-shadow:0 16px 48px rgba(0,0,0,.45)}
    dialog.pic-modal::backdrop{background:rgba(0,0,0,.5)}
    .pic-modal-head{display:flex;align-items:center;justify-content:space-between;
                    gap:12px;padding:10px 16px;border-bottom:1px solid #e0e4ea;
                    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    .pic-modal-head .title{font-size:.82rem;color:#555;font-style:italic;
                           overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
                           flex:1;min-width:0;border-left:3px solid #ffd966;
                           padding-left:8px}
    .pic-modal-head .close{background:none;border:none;font-size:1.5rem;
                           color:#666;cursor:pointer;padding:0 4px;line-height:1}
    .pic-modal-head .close:hover{color:#222}
    .pic-modal-body{padding:16px 22px;max-height:min(78vh,720px);overflow:auto;
                    color:#222;background:#fff}
    .pic-modal-body table{display:table;border-collapse:collapse;margin:.5em 0;
                          max-width:100%}
    .pic-modal-body table th,.pic-modal-body table td{border:1px solid #d0d7de;
                                                      padding:6px 10px;text-align:left;
                                                      vertical-align:top}
    .pic-modal-body table th{background:#f6f8fa;font-weight:600}
    .pic-modal-body p:last-child{margin-bottom:0}

    .toast{position:fixed;top:60px;right:24px;background:#fff;color:#222;
           border:1px solid #d0d4d8;border-radius:6px;padding:8px 14px;
           font-family:-apple-system,sans-serif;font-size:.85rem;z-index:5000;
           box-shadow:0 4px 14px rgba(0,0,0,.3);display:none}
    .toast.error{background:#fdecea;border-color:#f5c6cb;color:#7a1a13}
    .toast.show{display:block;animation:toastFade 2.4s ease forwards}
    @keyframes toastFade{
      0%{opacity:0;transform:translateY(-6px)}
      8%{opacity:1;transform:translateY(0)}
      80%{opacity:1}
      100%{opacity:0;transform:translateY(-4px)}
    }

    @media (max-width: 1080px) {
      .comments-rail{display:none}
      .rail-splitter{display:none}
    }
  </style>
</head>
<body>
  <div class="topbar">
    <a href="{{ _base }}/">&larr; back</a>
    <span class="filename">{{ name }}</span>
    <button type="button" class="zoom-btn" id="zoomOut" title="Zoom out">−</button>
    <span class="zoom-val" id="zoomVal">100%</span>
    <button type="button" class="zoom-btn" id="zoomIn" title="Zoom in">+</button>
    <button type="button" class="zoom-btn" id="zoomFit"
            title="Fit page to the available document width">⤢ Fit</button>
    <span class="page-info">
      <input type="number" class="page-input" id="pageInput" min="1" value="1">
      / <span id="pageTotal">?</span>
    </span>
    <button type="button" class="mode-btn" id="regionToggle"
            title="Shift+drag also works; this toggle locks region mode on">▭ Region</button>
  </div>

  <div class="layout">
    <div class="doc" id="doc"></div>
    <div class="rail-splitter hidden" id="railSplitter"
         title="Drag to resize comments column"></div>
    <div class="comments-rail hidden" id="picRail"></div>
  </div>

  <div class="pic-fab" id="picFab" role="toolbar" aria-label="Annotate selection">
    <button type="button" class="hl" id="picFabHighlight"
            title="Highlight only (no comment)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14.5 4.5l5 5M3 21l4-1 11-11-4-4L3 16v5zM12.5 6.5l5 5"/>
      </svg>
    </button>
    <button type="button" class="cm" id="picFabComment" title="Add comment">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7
                 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8
                 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0
                 0 1 8 8v.5z"/>
        <line x1="9" y1="11.5" x2="15" y2="11.5"/>
        <line x1="12" y1="8.5" x2="12" y2="14.5"/>
      </svg>
    </button>
  </div>

  <!-- Popover that appears when a saved highlight is clicked. -->
  <div class="pic-hl-pop" id="picHlPop" role="toolbar" aria-label="Highlight actions">
    <button type="button" class="cm" id="picHlPopComment" title="Add comment">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7
                 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8
                 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0
                 0 1 8 8v.5z"/>
      </svg>
      <span>Comment</span>
    </button>
    <button type="button" class="danger" id="picHlPopDelete" title="Delete highlight">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
           stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="3 6 5 6 21 6"/>
        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
      </svg>
      <span>Delete</span>
    </button>
  </div>

  <div id="toast" class="toast"></div>

  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script>
    // Shared KaTeX rendering — keeps math in comment bodies live just like
    // the markdown viewer. Currency amounts ($5.84B) bypass the regex
    // because they don't contain a backslash command.
    window._katexOpts = {
      delimiters: [
        {left: "$$", right: "$$", display: true},
        {left: "\\[", right: "\\]", display: true},
        {left: "\\(", right: "\\)", display: false},
      ],
      throwOnError: false,
      ignoredTags: ["script","noscript","style","textarea","pre","code"],
      ignoredClasses: ["pic-quote"],
    };
    function _convertDollarLatex(root) {
      const SKIP = new Set(["CODE","PRE","SCRIPT","STYLE","TEXTAREA","A"]);
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
        acceptNode(n) {
          let el = n.parentNode;
          while (el && el !== root) {
            if (SKIP.has(el.tagName)) return NodeFilter.FILTER_REJECT;
            if (el.classList && el.classList.contains("pic-quote")) return NodeFilter.FILTER_REJECT;
            el = el.parentNode;
          }
          return NodeFilter.FILTER_ACCEPT;
        },
      });
      const nodes = [];
      let n;
      while ((n = walker.nextNode())) nodes.push(n);
      const re = /(?<!\$)\$([^$\n]*?\\[A-Za-z]+[^$\n]*?)\$(?!\$)/g;
      const reIdent = /(?<![\$\w])\$([A-Za-z][A-Za-z0-9_^{}]{0,15})\$(?![\$\w])/g;
      for (const node of nodes) {
        if (!node.nodeValue.includes("$")) continue;
        let nv = node.nodeValue.replace(re, "\\($1\\)");
        nv = nv.replace(reIdent, "\\($1\\)");
        if (nv !== node.nodeValue) node.nodeValue = nv;
      }
    }
    window._renderMath = function(el) {
      if (!el) return;
      try { _convertDollarLatex(el); } catch(_) {}
      if (window.renderMathInElement) {
        try { window.renderMathInElement(el, window._katexOpts); } catch(_) {}
      }
    };
  </script>

  <script type="module">
  import * as pdfjsLib from "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.7.76/+esm";
  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.7.76/build/pdf.worker.min.mjs";

  const FILE_ID  = {{ file_id|tojson }};
  const PDF_URL  = {{ (_base + '/pdf-viewer-pdf/' + (file_id|string))|tojson }};
  const API_BASE = {{ _base|tojson }};
  const docEl   = document.getElementById('doc');
  const fab     = document.getElementById('picFab');
  const fabHl   = document.getElementById('picFabHighlight');
  const fabCm   = document.getElementById('picFabComment');
  const hlPop   = document.getElementById('picHlPop');
  const hlPopComment = document.getElementById('picHlPopComment');
  const hlPopDelete  = document.getElementById('picHlPopDelete');
  const rail    = document.getElementById('picRail');
  const splitter = document.getElementById('railSplitter');
  const zoomVal  = document.getElementById('zoomVal');
  const pageInput= document.getElementById('pageInput');
  const pageTotal= document.getElementById('pageTotal');
  const regionToggle = document.getElementById('regionToggle');

  // ── State ────────────────────────────────────────────────────────────
  let pdfDoc       = null;
  let scale        = 1.25;            // user zoom
  let pageDivs     = [];              // per-page placeholder div
  let pageRendered = [];              // bool per page index (0-based)
  let pageTextIndex= [];              // {full, nodes} per page after textlayer
  let comments     = [];              // server rows (with .orphan flag)
  let editingId    = null;
  let activeId     = null;
  let pendingSel   = null;            // {file_id,page,quote,prefix,suffix,rect?}
  let regionMode   = false;           // toggle from topbar

  function showToast(msg, kind) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'toast' + (kind === 'error' ? ' error' : '') + ' show';
    setTimeout(() => t.classList.remove('show'), 2600);
  }

  function api(path, opts) {
    return fetch(API_BASE + path, opts || {}).then(async r => {
      if (!r.ok) {
        let msg = 'HTTP ' + r.status;
        try { const j = await r.json(); if (j && j.error) msg = j.error; } catch(_){}
        throw new Error(msg);
      }
      if (r.status === 204) return null;
      return r.json();
    });
  }

  // ── Rail width persistence ───────────────────────────────────────────
  const RAIL_W_KEY = 'pic-rail-width';
  (function restoreRailWidth(){
    const w = parseInt(localStorage.getItem(RAIL_W_KEY) || '', 10);
    if (w > 0) rail.style.width = Math.max(240, Math.min(700, w)) + 'px';
  })();
  if (splitter) {
    let startX = 0, startW = 0;
    const onMove = (e) => {
      const w = Math.max(240, Math.min(700, startW + (startX - e.clientX)));
      rail.style.width = w + 'px';
    };
    const onUp = () => {
      splitter.classList.remove('dragging');
      document.body.style.userSelect = '';
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      const w = parseInt(rail.style.width, 10);
      if (w > 0) localStorage.setItem(RAIL_W_KEY, String(w));
      layoutCards();
    };
    splitter.addEventListener('mousedown', (e) => {
      e.preventDefault();
      startX = e.clientX;
      startW = rail.getBoundingClientRect().width;
      splitter.classList.add('dragging');
      document.body.style.userSelect = 'none';
      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup', onUp);
    });
  }

  // ── PDF load + page placeholders ─────────────────────────────────────
  async function loadPdf() {
    const task = pdfjsLib.getDocument({ url: PDF_URL });
    pdfDoc = await task.promise;
    pageTotal.textContent = pdfDoc.numPages;
    pageInput.max = pdfDoc.numPages;

    // Build empty page placeholders so the document has the right total
    // height immediately, even before pages render. Sized from each page's
    // intrinsic PDF dimensions × current scale.
    const sizes = [];
    for (let p = 1; p <= pdfDoc.numPages; p++) {
      const pg = await pdfDoc.getPage(p);
      const vp = pg.getViewport({ scale: 1 });
      sizes.push({ w: vp.width, h: vp.height });
      pg.cleanup();
    }
    docEl.innerHTML = '';
    pageDivs = [];
    pageRendered = sizes.map(() => false);
    pageTextIndex = sizes.map(() => null);
    for (let i = 0; i < sizes.length; i++) {
      const d = document.createElement('div');
      d.className = 'pdf-page loading';
      d.dataset.pageNum = (i + 1);
      sizePage(d, sizes[i]);
      const tag = document.createElement('div');
      tag.className = 'pageNumber';
      tag.textContent = (i + 1) + ' / ' + sizes.length;
      d.appendChild(tag);
      docEl.appendChild(d);
      pageDivs.push(d);
    }

    setupLazyRender();
    setupPageInputTracker();

    // Auto-fit page width to the available document panel on first load,
    // so users on wide monitors don't see a tiny page floating in the
    // middle. The user can still zoom in/out from there.
    fitToWidth({ skipRerender: true });

    // Pre-fetch comments and render orphan-able cards immediately.
    await loadAndRender();
  }

  // Compute the scale that makes the median page width fill the doc
  // panel, then apply it. Called from the topbar ⤢ Fit button + once on
  // initial load. `skipRerender` is used during loadPdf to avoid an
  // unnecessary re-render cycle before any page has rendered.
  function fitToWidth(opts) {
    let docW = Math.max(200, docEl.clientWidth - 24);
    // If the rail is currently hidden (no comments yet) but the viewport
    // is wide enough to show it, reserve its CSS-default width so the
    // first comment doesn't shrink the doc panel mid-session.
    if (rail.classList.contains('hidden') && window.innerWidth > 1080) {
      const railDefaultW = Math.min(720, Math.max(340, window.innerWidth * 0.28));
      docW -= railDefaultW + 6;  // splitter width
    }
    const widths = pageDivs.map(d => d._intrinsic && d._intrinsic.w).filter(Boolean);
    if (!widths.length) return;
    widths.sort((a, b) => a - b);
    const medianW = widths[Math.floor(widths.length / 2)];
    const newScale = Math.max(0.5, Math.min(3.0, docW / medianW));
    if (opts && opts.skipRerender) {
      scale = newScale;
      zoomVal.textContent = Math.round(scale * 100) + '%';
      for (const d of pageDivs) sizePage(d, d._intrinsic);
    } else {
      applyScale(newScale);
    }
  }

  function sizePage(div, dims) {
    div.style.width = (dims.w * scale) + 'px';
    div.style.height = (dims.h * scale) + 'px';
    // PDF.js 4.x TextLayer CSS sizes spans via `round(down, var(--scale-factor) * N, ...)`,
    // so the page div MUST publish --scale-factor or text spans render at 0×0.
    div.style.setProperty('--scale-factor', String(scale));
    // Used by some PDF.js CSS too (e.g. total-scale-factor on annotation editors).
    div.style.setProperty('--total-scale-factor', String(scale));
    div._intrinsic = dims;
  }

  // Re-size all placeholders + re-render visible pages on zoom change.
  async function applyScale(newScale) {
    scale = Math.max(0.5, Math.min(3.0, newScale));
    zoomVal.textContent = Math.round(scale * 100) + '%';
    for (const d of pageDivs) sizePage(d, d._intrinsic);
    // Mark all rendered pages as needing re-render at the new scale.
    for (let i = 0; i < pageRendered.length; i++) {
      if (!pageRendered[i]) continue;
      pageRendered[i] = false;
      pageTextIndex[i] = null;
      const d = pageDivs[i];
      // Strip everything except the page-number tag and re-add the loading class.
      const keep = d.querySelector('.pageNumber');
      d.innerHTML = '';
      if (keep) d.appendChild(keep);
      d.classList.add('loading');
    }
    // Trigger fresh renders for whatever's in the viewport.
    triggerVisibleRenders();
    layoutCards();
  }

  // ── Lazy render via IntersectionObserver ─────────────────────────────
  let pageObserver = null;
  function setupLazyRender() {
    if (pageObserver) pageObserver.disconnect();
    pageObserver = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (!e.isIntersecting) continue;
        const pn = parseInt(e.target.dataset.pageNum, 10);
        if (pn) renderPage(pn);
      }
    }, { rootMargin: '400px 0px' });
    pageDivs.forEach(d => pageObserver.observe(d));
  }
  function triggerVisibleRenders() {
    const vh = window.innerHeight;
    for (const d of pageDivs) {
      const r = d.getBoundingClientRect();
      if (r.bottom > -400 && r.top < vh + 400) {
        const pn = parseInt(d.dataset.pageNum, 10);
        if (pn) renderPage(pn);
      }
    }
  }

  async function renderPage(pageNum) {
    const idx = pageNum - 1;
    if (pageRendered[idx]) return;
    pageRendered[idx] = true;  // claim early to prevent double-renders
    const div = pageDivs[idx];
    let page;
    try {
      page = await pdfDoc.getPage(pageNum);
    } catch (e) {
      console.error('getPage failed', pageNum, e);
      pageRendered[idx] = false;
      return;
    }
    const vp = page.getViewport({ scale });
    // Render the canvas backing-store at a *supersampled* resolution so
    // text stays crisp even when:
    //   - DPR=2 (Retina)                              → 2× supersample
    //   - DPR=1 on a HiDPI / scaled external monitor  → still 2× supersample
    //     (Apple Preview / Chrome's built-in PDF viewer do the same; without
    //     this, OS-side display scaling smears the bitmap)
    //   - the user uses browser Cmd+ zoom              → DPR rises above 1
    // We take max(devicePixelRatio, 2) capped at 3 to keep GPU memory sane.
    const dpr = Math.min(3, Math.max(2, window.devicePixelRatio || 1));
    const canvas = document.createElement('canvas');
    canvas.width  = Math.floor(vp.width  * dpr);
    canvas.height = Math.floor(vp.height * dpr);
    canvas.style.width  = vp.width  + 'px';
    canvas.style.height = vp.height + 'px';
    const ctx = canvas.getContext('2d');
    div.classList.remove('loading');
    div.insertBefore(canvas, div.firstChild);

    // Text layer
    const textLayerDiv = document.createElement('div');
    textLayerDiv.className = 'textLayer';
    textLayerDiv.style.width  = vp.width  + 'px';
    textLayerDiv.style.height = vp.height + 'px';
    div.appendChild(textLayerDiv);

    // Region-overlay div for shift-drag (and the global Region-mode toggle)
    const overlay = document.createElement('div');
    overlay.className = 'region-overlay';
    div.appendChild(overlay);
    wireRegionOverlay(div, overlay, pageNum);

    const renderTransform = dpr !== 1 ? [dpr, 0, 0, dpr, 0, 0] : null;
    try {
      await page.render({
        canvasContext: ctx, viewport: vp, canvas, transform: renderTransform,
      }).promise;
    } catch (e) {
      console.error('canvas render failed', pageNum, e);
      pageRendered[idx] = false;
      return;
    }
    let tc;
    try { tc = await page.getTextContent(); } catch (_) { tc = { items: [] }; }
    try {
      // PDF.js 4.x TextLayer ESM API.
      const TL = pdfjsLib.TextLayer || (pdfjsLib.default && pdfjsLib.default.TextLayer);
      if (TL) {
        const tl = new TL({ textContentSource: tc, container: textLayerDiv, viewport: vp });
        await tl.render();
      } else if (pdfjsLib.renderTextLayer) {
        const task = pdfjsLib.renderTextLayer({
          textContentSource: tc, container: textLayerDiv, viewport: vp,
        });
        await task.promise;
      }
    } catch (e) {
      // Text layer rendering can race when the user zooms quickly; not fatal.
      console.warn('textLayer render failed', pageNum, e);
    }
    page.cleanup();

    // Build the per-page text index used for quote-anchored highlights.
    pageTextIndex[idx] = buildIndex(textLayerDiv);

    // Empty / near-empty text layer = scanned page (or CID-encoded fonts
    // PDF.js can't decode). Trigger backend OCR and inject the word boxes
    // as a synthetic text layer so native text selection works — same UX
    // Apple Preview offers via on-demand Vision OCR.
    if ((pageTextIndex[idx].full || '').trim().length < 8) {
      div.classList.add('scanned', 'ocr-loading');
      injectOcrTextLayer(pageNum, textLayerDiv, vp).then(() => {
        // Rebuild the index from the synthetic spans so quote-based
        // anchoring works on this page too.
        pageTextIndex[idx] = buildIndex(textLayerDiv);
        div.classList.remove('ocr-loading');
        // Re-anchor any comments that were waiting on this page.
        anchorCommentsOnPage(pageNum);
        layoutCards();
      }).catch(e => {
        div.classList.remove('ocr-loading');
        console.warn('OCR text-layer failed for page', pageNum, e);
      });
    }

    // Anchor any comments belonging to this page.
    anchorCommentsOnPage(pageNum);
    layoutCards();
  }

  // Fetch OCR'd word boxes for a scanned page and inject them as positioned
  // spans inside the PDF.js text layer div. Spans are transparent + cover
  // each word's bbox, so native text selection picks up the OCR'd text AND
  // Chrome's find-in-page highlights the right region (vs. highlighting the
  // wrong column inside a line-level span when the layout font's metrics
  // don't match the PDF's font).
  //
  // ocrmac returns LINE-level bboxes. We use a hidden canvas to measure
  // each word's pixel width in the layout font, then proportionally
  // allocate the line's CSS width across the words so each word sits
  // approximately where its glyphs appear on the canvas underneath.
  const _measureCanvas = document.createElement('canvas');
  const _measureCtx = _measureCanvas.getContext('2d');
  function _measureTextWidth(text, fontSize) {
    _measureCtx.font = fontSize + 'px -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif';
    return _measureCtx.measureText(text).width;
  }
  async function injectOcrTextLayer(pageNum, textLayerDiv, vp) {
    const resp = await api('/pdf-page-ocr', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ file_id: FILE_ID, page: pageNum }),
    });
    const lines = (resp && resp.words) || [];
    if (!lines.length) return;
    const W = vp.width, H = vp.height;

    let prevRow = -1;
    for (const line of lines) {
      const top   = line.y * H;
      const left  = line.x * W;
      const lineW = line.w * W;
      const lineH = line.h * H;
      const fontSize = Math.max(4, lineH);

      // Row separator: an inserted <br> between visually-distinct rows
      // produces '\n' in copy-paste output and matches the line breaks the
      // user would expect across a paragraph.
      const rowKey = Math.round(top / 8);
      if (rowKey !== prevRow && prevRow !== -1) {
        textLayerDiv.appendChild(document.createElement('br'));
      }
      prevRow = rowKey;

      // Split the line text into tokens, KEEPING whitespace so we can
      // accumulate offsets correctly. Emit a span per non-empty token.
      const tokens = (line.t || '').split(/(\s+)/);
      const fullW = Math.max(0.0001, _measureTextWidth(line.t, fontSize));
      const k = lineW / fullW;  // scale from layout-font pixels → OCR bbox CSS pixels
      let cumLayoutW = 0;
      for (const tok of tokens) {
        const tokW = _measureTextWidth(tok, fontSize);
        if (tok && tok.trim()) {
          const span = document.createElement('span');
          span.className = 'ocr-word';
          span.style.left     = (left + cumLayoutW * k) + 'px';
          span.style.top      = top + 'px';
          span.style.width    = Math.max(2, tokW * k) + 'px';
          span.style.height   = lineH + 'px';
          span.style.fontSize = fontSize + 'px';
          // Trailing space → adjacent word selections include a space when
          // copied. Browser also positions a real space glyph that helps
          // selection extension across word boundaries.
          span.textContent = tok + ' ';
          textLayerDiv.appendChild(span);
        }
        cumLayoutW += tokW;
      }
    }
  }

  // ── Selection capture (text-layer, parallel to /claude-reports) ──────
  function buildIndex(root) {
    const nodes = [];
    let full = '';
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(n) {
        const p = n.parentNode && n.parentNode.tagName;
        if (p === 'SCRIPT' || p === 'STYLE') return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    let n;
    while ((n = walker.nextNode())) {
      if (!n.nodeValue) continue;
      const start = full.length;
      // Use a single space to join adjacent text spans so words pulled from
      // different positioned <span>s don't run together in prefix/suffix.
      if (full && !/\s$/.test(full) && !/^\s/.test(n.nodeValue)) full += ' ';
      const realStart = full.length;
      full += n.nodeValue;
      nodes.push({ node: n, start: realStart, end: full.length });
    }
    return { full, nodes };
  }

  function findPageNumFromNode(node) {
    let el = node.nodeType === 1 ? node : node.parentNode;
    while (el && el !== document.body) {
      if (el.classList && el.classList.contains('pdf-page')) {
        return parseInt(el.dataset.pageNum, 10);
      }
      el = el.parentNode;
    }
    return null;
  }

  function getTextSelectionInfo() {
    const sel = window.getSelection();
    if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return null;
    const range = sel.getRangeAt(0);
    const startEl = range.startContainer.nodeType === 1
      ? range.startContainer : range.startContainer.parentNode;
    const pageNum = findPageNumFromNode(startEl);
    if (!pageNum) return null;
    const idx = pageTextIndex[pageNum - 1];
    if (!idx) return null;

    const quote = sel.toString();
    if (!quote || !quote.trim()) return null;
    let startOff = -1, endOff = -1;
    for (const e of idx.nodes) {
      if (e.node === range.startContainer) startOff = e.start + range.startOffset;
      if (e.node === range.endContainer)   endOff   = e.start + range.endOffset;
    }
    if (startOff < 0 || endOff < 0 || endOff <= startOff) return null;
    const prefix = idx.full.slice(Math.max(0, startOff - 32), startOff);
    const suffix = idx.full.slice(endOff, endOff + 32);
    const rect = range.getBoundingClientRect();
    // Page-space rect (CSS px at scale=1) — stable across reload/rescale, so
    // we can use it as a fallback overlay anchor when quote+prefix+suffix
    // re-location fails (e.g. PDFs whose text layer has no inter-word
    // whitespace, so the selected "Taiwan has the…" never matches
    // "Taiwanhasthe…" in the normalised index).
    const pageDiv = pageDivs[pageNum - 1];
    let pageRect = null;
    if (pageDiv) {
      const pb = pageDiv.getBoundingClientRect();
      pageRect = {
        x: (rect.left - pb.left) / scale,
        y: (rect.top  - pb.top)  / scale,
        w: rect.width  / scale,
        h: rect.height / scale,
      };
    }
    return {
      page: pageNum, quote, prefix, suffix,
      start_off: startOff, end_off: endOff,
      rect: { top: rect.top, left: rect.left, right: rect.right, bottom: rect.bottom,
              width: rect.width, height: rect.height },
      pageRect,
    };
  }

  // ── Floating action toolbar anchored at selection right-edge ─────────
  // Position is viewport-relative (.pic-fab is position:fixed). Keeping it
  // in sync with the LIVE selection via selectionchange + scroll listeners
  // means the toolbar follows the selection as you scroll, instead of
  // sticking at the original document position and silently going off-screen.
  function showFab(rect) {
    fab.classList.add('show');
    fab.style.top  = (rect.top - 6) + 'px';
    fab.style.left = (rect.right + 8) + 'px';
  }
  function hideFab() { fab.classList.remove('show'); }
  function hideHlPop() { hlPop.classList.remove('show'); hlPop._cid = null; }

  function refreshFabFromSelection() {
    const info = getTextSelectionInfo();
    if (!info) { hideFab(); pendingSel = null; return; }
    pendingSel = { kind: 'text', ...info };
    // Re-read the rect from the LIVE range so scroll / DOM mutations don't
    // freeze the fab at a stale position.
    const sel = window.getSelection();
    const r = sel.rangeCount ? sel.getRangeAt(0).getBoundingClientRect() : info.rect;
    // Hide cleanly when the selection is fully outside the viewport — the
    // toolbar lurking just above/below the visible area is confusing.
    const vh = window.innerHeight;
    if (r.bottom < 4 || r.top > vh - 4) { hideFab(); return; }
    showFab(r);
  }
  // selectionchange fires per-character during drag-select — debounce to
  // ~90ms so we don't thrash on every mousemove.
  let _fabDebounce = null;
  document.addEventListener('selectionchange', () => {
    clearTimeout(_fabDebounce);
    _fabDebounce = setTimeout(refreshFabFromSelection, 90);
  });
  // Keep the fab pinned to its selection while the user scrolls.
  window.addEventListener('scroll', () => {
    if (!fab.classList.contains('show')) return;
    refreshFabFromSelection();
  }, { passive: true, capture: true });

  // Mousedown elsewhere closes the highlight popover (a click on a mark or
  // inside the fab/rail/popover itself preserves its state).
  document.addEventListener('mousedown', function(e) {
    if (fab.contains(e.target))   return;
    if (hlPop.contains(e.target)) return;
    if (rail.contains(e.target))  return;
    if (e.target && e.target.classList && (e.target.classList.contains('pic-hl') ||
                                            e.target.classList.contains('rect-hl'))) return;
    hideHlPop();
  });

  // rect-hl overlays are pointer-events:none (so they never block selecting
  // the text beneath them), so their own click handler can't fire. Re-add
  // click-to-activate by hit-testing on a PLAIN click: a text-selecting drag
  // leaves a non-collapsed selection and is ignored; a simple click in a
  // rect activates its comment (rail card for noted ones, [💬 🗑] popover for
  // bare highlights). Marks stopPropagation on their own click, so a click on
  // a text highlight never reaches here.
  document.addEventListener('click', function(e) {
    const sel = window.getSelection();
    if (sel && !sel.isCollapsed) return;            // user was selecting text
    if (fab.contains(e.target) || hlPop.contains(e.target) || rail.contains(e.target)) return;
    let hit = null, hitArea = Infinity;
    document.querySelectorAll('.rect-hl').forEach(r => {
      const b = r.getBoundingClientRect();
      if (e.clientX >= b.left && e.clientX <= b.right &&
          e.clientY >= b.top  && e.clientY <= b.bottom) {
        const area = b.width * b.height;            // prefer the smallest enclosing rect
        if (area < hitArea) { hitArea = area; hit = r; }
      }
    });
    if (!hit) return;
    const cid = parseInt(hit.dataset.cid, 10);
    if (!cid) return;
    const c = comments.find(x => x.id === cid);
    if (!c) return;
    if (c.body && c.body.trim()) setActive(c.id, false);
    else                         showHlPop(hit, c.id);
  });

  // Prevent fab button mousedown from stealing focus / collapsing selection.
  // Without preventDefault, clicking the button can shift focus out of the
  // text layer and the browser drops the selection before our click handler
  // reads it — fab vanishes mid-click.
  [fabHl, fabCm, hlPopComment, hlPopDelete].forEach(b => {
    b.addEventListener('mousedown', (ev) => ev.preventDefault());
  });

  // 💬 fab → full comment editor (current behaviour)
  fabCm.addEventListener('click', function(ev) {
    ev.stopPropagation();
    if (!pendingSel) return;
    hideFab();
    editingId = null;
    openNewCommentCard(pendingSel);
  });
  // 🖍 fab → instant highlight save, no editor, no rail card
  fabHl.addEventListener('click', async function(ev) {
    ev.stopPropagation();
    if (!pendingSel) return;
    hideFab();
    await saveHighlightOnly(pendingSel);
    window.getSelection().removeAllRanges();
    pendingSel = null;
  });

  async function saveHighlightOnly(info) {
    try {
      // Region selections: info.rect is already page-space ({x,y,w,h}).
      // Text selections: info.pageRect carries the page-space rect for
      // fallback re-anchoring when quote re-location fails on reload.
      const persistedRect = (info.kind === 'region' && info.rect)
        ? info.rect
        : (info.pageRect || null);
      await api('/pdf-inline-comments', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
          file_id: FILE_ID, page: info.page,
          quote: info.quote || '', prefix: info.prefix || '', suffix: info.suffix || '',
          rect: persistedRect, body: '',
        }),
      });
      await loadAndRender();
    } catch (e) { showToast('Highlight save failed: ' + e.message, 'error'); }
  }

  // Show the highlight popover at a mark's right edge. Viewport-relative
  // coords (popover is position:fixed) so it tracks the mark even on scroll.
  function showHlPop(targetEl, cid) {
    const r = targetEl.getBoundingClientRect();
    hlPop.classList.add('show');
    hlPop._cid = cid;
    hlPop._anchor = targetEl;
    hlPop.style.top  = (r.top - 6) + 'px';
    hlPop.style.left = (r.right + 8) + 'px';
  }
  // Keep the highlight popover pinned to its mark on scroll.
  window.addEventListener('scroll', () => {
    if (!hlPop.classList.contains('show')) return;
    const a = hlPop._anchor;
    if (!a || !a.isConnected) { hideHlPop(); return; }
    const r = a.getBoundingClientRect();
    hlPop.style.top  = (r.top - 6) + 'px';
    hlPop.style.left = (r.right + 8) + 'px';
  }, { passive: true, capture: true });
  hlPopDelete.addEventListener('click', async (ev) => {
    ev.stopPropagation();
    const cid = hlPop._cid; if (!cid) return;
    hideHlPop();
    try {
      await api('/pdf-inline-comments/' + cid, { method: 'DELETE' });
      await loadAndRender();
    } catch (e) { showToast('Delete failed: ' + e.message, 'error'); }
  });
  hlPopComment.addEventListener('click', (ev) => {
    ev.stopPropagation();
    const cid = hlPop._cid; if (!cid) return;
    hideHlPop();
    const c = comments.find(x => x.id === cid);
    if (!c) return;
    // Open the rail editor pre-populated for THIS row. Save will PATCH the
    // existing row (no new id), upgrading it from highlight to comment.
    openEditCard(c);
  });

  // ── Region-drag selection (Shift+drag, or "Region mode" toggle) ─────
  function wireRegionOverlay(pageDiv, overlay, pageNum) {
    let startX = 0, startY = 0, rubber = null;
    let dragging = false;
    overlay.addEventListener('mousedown', (e) => {
      e.preventDefault();
      const r = pageDiv.getBoundingClientRect();
      startX = e.clientX - r.left;
      startY = e.clientY - r.top;
      dragging = true;
      rubber = document.createElement('div');
      rubber.className = 'region-rubber';
      rubber.style.left = startX + 'px';
      rubber.style.top  = startY + 'px';
      rubber.style.width = '0';
      rubber.style.height= '0';
      pageDiv.appendChild(rubber);
    });
    overlay.addEventListener('mousemove', (e) => {
      if (!dragging || !rubber) return;
      const r = pageDiv.getBoundingClientRect();
      const x = e.clientX - r.left;
      const y = e.clientY - r.top;
      rubber.style.left   = Math.min(x, startX) + 'px';
      rubber.style.top    = Math.min(y, startY) + 'px';
      rubber.style.width  = Math.abs(x - startX) + 'px';
      rubber.style.height = Math.abs(y - startY) + 'px';
    });
    overlay.addEventListener('mouseup', async (e) => {
      if (!dragging || !rubber) return;
      dragging = false;
      const cssX = parseFloat(rubber.style.left)   || 0;
      const cssY = parseFloat(rubber.style.top)    || 0;
      const cssW = parseFloat(rubber.style.width)  || 0;
      const cssH = parseFloat(rubber.style.height) || 0;
      rubber.remove();
      if (cssW < 4 || cssH < 4) return;
      // Convert CSS px (at current scale) to PDF user-space units (scale=1).
      const rect = {
        x: cssX / scale, y: cssY / scale,
        w: cssW / scale, h: cssH / scale,
      };
      // OCR the region (server runs ocrmac on a fitz-rendered crop, or
      // returns native text if the PDF is vector-text inside the rect).
      let text = '';
      try {
        const r2 = await api('/pdf-ocr-region', {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({ file_id: FILE_ID, page: pageNum, ...rect }),
        });
        text = (r2 && r2.text) ? r2.text.trim() : '';
      } catch (err) {
        showToast('OCR failed: ' + err.message, 'error');
        return;
      }
      pendingSel = {
        kind: 'region',
        page: pageNum,
        quote: text,
        prefix: '',
        suffix: '',
        rect,  // page-space units; renderer will scale up by current scale
      };
      editingId = null;
      openNewCommentCard(pendingSel);
    });
  }

  // Shift held → enable region overlay on every page; Toggle button locks it.
  function setRegionMode(on) {
    regionMode = !!on;
    regionToggle.classList.toggle('active', regionMode);
    document.querySelectorAll('.pdf-page').forEach(d => {
      d.classList.toggle('region-mode', regionMode);
    });
  }
  regionToggle.addEventListener('click', () => setRegionMode(!regionMode));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Shift' && !regionMode) {
      document.querySelectorAll('.pdf-page').forEach(d => d.classList.add('region-mode'));
    }
    if (e.key === 'Escape') { hideFab(); hideHlPop(); }
  });
  document.addEventListener('keyup', (e) => {
    if (e.key === 'Shift' && !regionMode) {
      document.querySelectorAll('.pdf-page').forEach(d => d.classList.remove('region-mode'));
    }
  });

  // ── Anchor existing comments to pages ────────────────────────────────
  // Collapse all whitespace runs into a single space so prefix/quote/suffix
  // captured from a selection (which preserves '\n' between text-layer spans)
  // can match the index (which joins spans with a single space). We also
  // build a position map so the matched offsets can be projected back to
  // the original-text offsets that wrapRange operates in.
  function _normWs(s) { return (s || '').replace(/\s+/g, ' ').trim(); }
  function _buildPosMap(full) {
    // Mirror the same collapsing rules as _normWs, but also record the
    // original index that each normalised char originated from. After
    // we find a match in the normalised string we can map [n0, n1] back
    // to [orig0, orig1] for wrapRange.
    const map = [];
    let out = '';
    let prevSpace = true;  // emulate .trim() leading
    for (let i = 0; i < full.length; i++) {
      const c = full[i];
      if (/\s/.test(c)) {
        if (!prevSpace) { out += ' '; map.push(i); prevSpace = true; }
      } else {
        out += c; map.push(i); prevSpace = false;
      }
    }
    // Trim trailing space (mirrors .trim())
    while (out.length && out[out.length-1] === ' ') {
      out = out.slice(0, -1); map.pop();
    }
    return { norm: out, map };
  }
  function findInIndex(idx, c) {
    if (!idx._norm) idx._norm = _buildPosMap(idx.full);
    const NORM = idx._norm.norm;
    const MAP  = idx._norm.map;
    const quoteN  = _normWs(c.quote);
    if (!quoteN) return null;
    const prefixN = _normWs(c.prefix);
    const suffixN = _normWs(c.suffix);
    const candidates = [];
    if (prefixN || suffixN) {
      const sep1 = prefixN && quoteN ? ' ' : '';
      const sep2 = quoteN && suffixN ? ' ' : '';
      candidates.push({ needle: prefixN + sep1 + quoteN + sep2 + suffixN,
                        off: prefixN.length + (sep1 ? 1 : 0) });
    }
    candidates.push({ needle: quoteN, off: 0 });
    for (const t of candidates) {
      if (!t.needle) continue;
      const i = NORM.indexOf(t.needle);
      if (i < 0) continue;
      const nStart = i + t.off;
      const nEnd   = nStart + quoteN.length;
      const origStart = MAP[nStart];
      // MAP[nEnd] points to the char AFTER the last char of the quote in
      // the original; if nEnd is past the end of the normalised string
      // we fall back to full.length.
      const origEnd = (nEnd < MAP.length) ? MAP[nEnd] : idx.full.length;
      return { start: origStart, end: origEnd };
    }

    // Endpoint fallback — the exact full-quote match failed. A long or
    // multi-paragraph selection accumulates tiny text-layer differences
    // (a missing inter-word space at a line break — "through a" + "series"
    // rendered "aseries" — a ligature, a footnote superscript), and a
    // single mismatched char anywhere breaks the contiguous indexOf. So
    // anchor the span by its ENDPOINTS instead: find the quote's head and
    // its tail and wrap everything between them. This keeps long text
    // highlights as selectable marks instead of dropping to a rect overlay.
    //
    // Gate on prefix/suffix so this only fires for TEXT selections (which
    // always carry text-layer context). A region comment (drawn box, OCR'd
    // quote, empty prefix+suffix) must keep falling back to its rect overlay
    // — otherwise its OCR text, if it happens to match native page text
    // (e.g. a chart title), would wrongly re-anchor as a thin text mark.
    if (quoteN.length >= 24 && (prefixN || suffixN)) {
      const HEAD = quoteN.slice(0, 20);
      const TAIL = quoteN.slice(-20);
      const hi = NORM.indexOf(HEAD);
      if (hi >= 0) {
        const ti = NORM.indexOf(TAIL, hi + HEAD.length);
        if (ti >= 0) {
          const nStart = hi;
          const nEnd   = ti + TAIL.length;
          // Reject runaway matches (head and tail both common, far apart):
          // the matched span must be close to the quote's own length.
          if (nEnd - nStart <= quoteN.length * 1.3 + 8) {
            const origStart = MAP[nStart];
            const origEnd = (nEnd < MAP.length) ? MAP[nEnd] : idx.full.length;
            return { start: origStart, end: origEnd };
          }
        }
      }
    }
    return null;
  }

  function wrapRange(idx, oStart, oEnd, cid) {
    const segs = [];
    for (const e of idx.nodes) {
      if (e.end <= oStart) continue;
      if (e.start >= oEnd) break;
      const ls = Math.max(0, oStart - e.start);
      const le = Math.min(e.node.nodeValue.length, oEnd - e.start);
      if (ls >= le) continue;
      segs.push({ node: e.node, start: ls, end: le });
    }
    const marks = [];
    for (const seg of segs) {
      const n = seg.node;
      if (!n.parentNode) continue;
      const before = n.nodeValue.slice(0, seg.start);
      const middle = n.nodeValue.slice(seg.start, seg.end);
      const after  = n.nodeValue.slice(seg.end);
      const mk = document.createElement('mark');
      mk.className = 'pic-hl';
      mk.dataset.cid = String(cid);
      mk.textContent = middle;
      const frag = document.createDocumentFragment();
      if (before) frag.appendChild(document.createTextNode(before));
      frag.appendChild(mk);
      if (after)  frag.appendChild(document.createTextNode(after));
      n.parentNode.replaceChild(frag, n);
      marks.push(mk);
    }
    return marks;
  }

  function anchorCommentsOnPage(pageNum) {
    const div = pageDivs[pageNum - 1];
    if (!div) return;
    // Strip any prior anchors (rect overlays + marks) for this page.
    div.querySelectorAll('.rect-hl').forEach(el => el.remove());
    div.querySelectorAll('mark.pic-hl').forEach(m => {
      const t = document.createTextNode(m.textContent);
      m.parentNode.replaceChild(t, m);
    });
    const tl = div.querySelector('.textLayer');
    if (tl) tl.normalize();
    // The stored pageTextIndex may point at text nodes that got replaced
    // when an earlier pending <mark> was painted in. Rebuild from the
    // (now-clean) text layer so node references and offsets line up.
    const idx = tl ? buildIndex(tl) : null;
    pageTextIndex[pageNum - 1] = idx;
    if (!idx) return;

    for (const c of comments) {
      if (c.page !== pageNum) continue;
      let anchored = false;
      const hasBody = !!(c.body && c.body.trim());
      // Every highlight (noted or bare) now has a rail card, so a click
      // activates that card — its Delete button is always on-screen, unlike
      // the inline popover which could land off-screen at high zoom.
      const onClick = (m) => (ev) => {
        ev.stopPropagation();
        setActive(c.id, false);
      };
      if (c.quote && c.quote.trim()) {
        const found = findInIndex(idx, c);
        if (found) {
          const marks = wrapRange(idx, found.start, found.end, c.id);
          marks.forEach(m => m.addEventListener('click', onClick(m)));
          anchored = true;
        }
      }
      if (!anchored && c.rect) {
        // Rect fallback — draw an overlay div in page-space coords.
        const r = document.createElement('div');
        r.className = 'rect-hl';
        r.dataset.cid = c.id;
        r.style.left   = (c.rect.x * scale) + 'px';
        r.style.top    = (c.rect.y * scale) + 'px';
        r.style.width  = (c.rect.w * scale) + 'px';
        r.style.height = (c.rect.h * scale) + 'px';
        r.title = hasBody ? (c.quote || 'comment') : 'highlight';
        r.addEventListener('click', onClick(r));
        div.appendChild(r);
        anchored = true;
      }
      c.orphan = !anchored;
    }
  }

  // ── Card rendering (clone of /claude-reports/view) ───────────────────
  function fmtTime(s) {
    // Timestamps are stored as UTC ISO (e.g. "2026-06-13T10:32:46Z").
    // Render them in the viewer's LOCAL timezone — otherwise a UTC+2 user
    // sees 10:32 for a comment they made at 12:32.
    if (!s) return '';
    const d = new Date(s);
    if (isNaN(d.getTime())) return s.replace('T', ' ').replace('Z', '');
    const p = n => String(n).padStart(2, '0');
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) +
           ' ' + p(d.getHours()) + ':' + p(d.getMinutes()) + ':' + p(d.getSeconds());
  }

  function buildCardEl(c) {
    const hasBody = !!(c.body && c.body.trim());
    const div = document.createElement('div');
    div.className = 'pic-card' + (c.orphan ? ' orphan' : '') + (hasBody ? '' : ' highlight-only');
    div.dataset.id = c.id;
    div.dataset.anchored = c.orphan ? '0' : '1';
    div.tabIndex = -1;

    const tag = document.createElement('div');
    tag.className = 'pic-page-tag';
    tag.textContent = 'Page ' + c.page + (c.orphan ? '  ⚠ orphan' : '')
                    + (hasBody ? '' : '  ·  🖍 highlight');

    const q = document.createElement('div');
    q.className = 'pic-quote' + (c.quote ? '' : ' empty');
    q.textContent = c.quote
      ? (c.quote.length > 140 ? c.quote.slice(0, 140) + '…' : c.quote)
      : '(region selection — no text)';

    const meta = document.createElement('div');
    meta.className = 'pic-meta';
    meta.textContent = fmtTime(c.updated_at || c.created_at);

    const actions = document.createElement('div');
    actions.className = 'pic-actions';
    const eBtn = document.createElement('button');
    eBtn.type = 'button'; eBtn.textContent = hasBody ? 'Edit' : 'Add note';
    eBtn.addEventListener('click', (ev) => { ev.stopPropagation(); openEditCard(c); });
    const dBtn = document.createElement('button');
    dBtn.type = 'button'; dBtn.textContent = 'Delete'; dBtn.className = 'danger';
    dBtn.addEventListener('click', (ev) => { ev.stopPropagation(); deleteOne(c.id); });
    const jBtn = document.createElement('button');
    jBtn.type = 'button'; jBtn.textContent = 'Go to page';
    jBtn.addEventListener('click', (ev) => { ev.stopPropagation(); scrollToPage(c.page); });
    actions.append(jBtn, eBtn, dBtn);

    // A body-less highlight has no note to render or expand — just the quote.
    if (hasBody) {
      const b = document.createElement('div');
      b.className = 'pic-body';
      b.innerHTML = window.marked ? marked.parse(c.body || '') : (c.body || '');
      if (window._renderMath) window._renderMath(b);

      const viewBtn = document.createElement('button');
      viewBtn.type = 'button';
      viewBtn.className = 'pic-expand-btn';
      viewBtn.innerHTML =
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
        '<path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>' +
        '<span>Expand</span>';
      viewBtn.addEventListener('click', (ev) => {
        ev.stopPropagation();
        openCommentModal(c);
      });
      div.append(tag, q, b, viewBtn, meta, actions);
    } else {
      div.append(tag, q, meta, actions);
    }
    div.addEventListener('click', () => setActive(c.id, true));
    return div;
  }

  let _modalSingleton = null;
  function ensureCommentModal() {
    if (_modalSingleton) return _modalSingleton;
    const dlg = document.createElement('dialog');
    dlg.className = 'pic-modal';
    const head = document.createElement('div');
    head.className = 'pic-modal-head';
    const title = document.createElement('div');
    title.className = 'title';
    const close = document.createElement('button');
    close.type = 'button'; close.className = 'close';
    close.setAttribute('aria-label', 'Close');
    close.textContent = '×';
    close.addEventListener('click', () => dlg.close());
    head.append(title, close);
    const body = document.createElement('div');
    body.className = 'pic-modal-body markdown-body';
    dlg.append(head, body);
    document.body.appendChild(dlg);
    dlg.addEventListener('click', (ev) => {
      if (ev.target !== dlg) return;
      const r = dlg.getBoundingClientRect();
      const inside = ev.clientX >= r.left && ev.clientX <= r.right &&
                     ev.clientY >= r.top  && ev.clientY <= r.bottom;
      if (!inside) dlg.close();
    });
    const STORAGE_KEY = 'pic-modal-width';
    const savedW = parseInt(localStorage.getItem(STORAGE_KEY) || '', 10);
    if (savedW > 0) dlg.style.width = Math.min(savedW, Math.round(window.innerWidth * 0.96)) + 'px';
    new ResizeObserver(() => {
      if (!dlg.open) return;
      const w = Math.round(dlg.getBoundingClientRect().width);
      if (w > 0) localStorage.setItem(STORAGE_KEY, String(w));
    }).observe(dlg);
    _modalSingleton = { dlg, title, body };
    return _modalSingleton;
  }
  function openCommentModal(c) {
    const { dlg, title, body } = ensureCommentModal();
    title.textContent = c.quote ? (c.quote.length > 140 ? c.quote.slice(0, 140) + '…' : c.quote) : ('Page ' + c.page);
    body.innerHTML = window.marked ? marked.parse(c.body || '') : (c.body || '');
    if (window._renderMath) window._renderMath(body);
    if (typeof dlg.showModal === 'function') dlg.showModal();
    else dlg.setAttribute('open', '');
  }

  function buildEditorEl({ id, page, quote, body, onSave, onCancel }) {
    const div = document.createElement('div');
    div.className = 'pic-card pending';
    if (id) div.dataset.id = id;
    else    div.dataset.pending = '1';

    const tag = document.createElement('div');
    tag.className = 'pic-page-tag';
    tag.textContent = 'Page ' + page;

    const q = document.createElement('div');
    q.className = 'pic-quote' + (quote ? '' : ' empty');
    q.textContent = quote
      ? (quote.length > 140 ? quote.slice(0, 140) + '…' : quote)
      : '(region selection — no text)';

    const ed = document.createElement('div');
    ed.className = 'pic-editor';
    const ta = document.createElement('textarea');
    ta.placeholder = 'Add a comment… markdown supported';
    ta.value = body || '';
    const row = document.createElement('div');
    row.className = 'pic-editor-actions';
    const cancel = document.createElement('button');
    cancel.type = 'button'; cancel.className = 'cancel'; cancel.textContent = 'Cancel';
    const save = document.createElement('button');
    save.type = 'button'; save.className = 'save';
    save.textContent = id ? 'Save' : 'Comment';
    save.disabled = !ta.value.trim();

    ta.addEventListener('input', () => { save.disabled = !ta.value.trim(); });
    ta.addEventListener('keydown', (ev) => {
      if ((ev.metaKey || ev.ctrlKey) && ev.key === 'Enter' && !save.disabled) {
        ev.preventDefault();
        onSave(ta.value.trim());
      } else if (ev.key === 'Escape') {
        ev.preventDefault();
        onCancel();
      }
    });

    async function uploadImageFile(file) {
      const token = `__upl_${Date.now()}_${Math.random().toString(36).slice(2,8)}__`;
      const placeholder = `![${token}]()`;
      const s = ta.selectionStart, e = ta.selectionEnd;
      ta.value = ta.value.slice(0, s) + placeholder + ta.value.slice(e);
      ta.selectionStart = ta.selectionEnd = s + placeholder.length;
      save.disabled = !ta.value.trim();
      try {
        const fd = new FormData();
        const subtype = (file.type.split('/')[1] || 'png').toLowerCase();
        const ext = subtype === 'jpeg' ? 'jpg' : subtype;
        fd.append('image', file, `pasted-${Date.now()}.${ext}`);
        const r = await fetch('/upload-image', { method: 'POST', body: fd });
        if (!r.ok) throw new Error('HTTP ' + r.status);
        const j = await r.json();
        const url = j && j.data && j.data.filePath;
        if (!url) throw new Error('no filePath in response');
        ta.value = ta.value.replace(placeholder, `![](${url})`);
      } catch (err) {
        ta.value = ta.value.replace(placeholder, '');
        showToast('Image upload failed: ' + (err && err.message ? err.message : err), 'error');
      }
      save.disabled = !ta.value.trim();
    }
    ta.addEventListener('paste', (ev) => {
      const cd = ev.clipboardData;
      if (!cd || !cd.items) return;
      for (const it of cd.items) {
        if (it.kind === 'file' && it.type.startsWith('image/')) {
          const f = it.getAsFile();
          if (f) { ev.preventDefault(); uploadImageFile(f); return; }
        }
      }
    });
    ta.addEventListener('dragover', (ev) => {
      if (ev.dataTransfer && Array.from(ev.dataTransfer.items || [])
          .some(i => i.kind === 'file' && i.type.startsWith('image/'))) {
        ev.preventDefault();
        ta.classList.add('upl-dragover');
      }
    });
    ta.addEventListener('dragleave', () => ta.classList.remove('upl-dragover'));
    ta.addEventListener('drop', (ev) => {
      ta.classList.remove('upl-dragover');
      const files = ev.dataTransfer && ev.dataTransfer.files;
      if (!files || !files.length) return;
      const imgs = Array.from(files).filter(f => f.type.startsWith('image/'));
      if (!imgs.length) return;
      ev.preventDefault();
      imgs.forEach(uploadImageFile);
    });

    cancel.addEventListener('click', (ev) => { ev.stopPropagation(); onCancel(); });
    save.addEventListener('click',   (ev) => { ev.stopPropagation();
                                               if (!save.disabled) onSave(ta.value.trim()); });
    const hint = document.createElement('span');
    hint.className = 'pic-editor-hint';
    hint.textContent = 'paste / drop image';
    row.append(hint, cancel, save);
    ed.append(ta, row);
    div.append(tag, q, ed);
    div._textarea = ta;
    return div;
  }

  function openNewCommentCard(info) {
    closeAnyEditor();
    rail.classList.remove('hidden');
    if (splitter) splitter.classList.remove('hidden');
    // Paint a real <mark> on the selection so the user can see what's being commented on.
    if (info.kind === 'text' && typeof info.start_off === 'number') {
      const idx = pageTextIndex[info.page - 1];
      if (idx) {
        const marks = wrapRange(idx, info.start_off, info.end_off, 'pending');
        marks.forEach(m => m.classList.add('active'));
      }
    } else if (info.kind === 'region' && info.rect) {
      const div = pageDivs[info.page - 1];
      if (div) {
        const r = document.createElement('div');
        r.className = 'rect-hl';
        r.dataset.cid = 'pending';
        r.style.left   = (info.rect.x * scale) + 'px';
        r.style.top    = (info.rect.y * scale) + 'px';
        r.style.width  = (info.rect.w * scale) + 'px';
        r.style.height = (info.rect.h * scale) + 'px';
        div.appendChild(r);
      }
    }
    const card = buildEditorEl({
      page: info.page,
      quote: info.quote,
      body: '',
      onSave: async (body) => {
        try {
          // Region selections: info.rect is already page-space ({x,y,w,h}).
          // Text selections: info.pageRect is the page-space conversion of
          // the live selection rect (the viewport info.rect is unusable
          // post-reload). Persisting it gives the page renderer a fallback
          // overlay anchor when quote+prefix+suffix re-location fails.
          const persistedRect = (info.kind === 'region' && info.rect)
            ? info.rect
            : (info.pageRect || null);
          const payload = {
            file_id: FILE_ID,
            page: info.page,
            quote: info.quote || '',
            prefix: info.prefix || '',
            suffix: info.suffix || '',
            rect: persistedRect,
            body,
          };
          const resp = await api('/pdf-inline-comments', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify(payload),
          });
          card.remove();
          clearPendingHighlights();
          window.getSelection().removeAllRanges();
          pendingSel = null;
          await loadAndRender();
          const newId = resp && resp.comment && resp.comment.id;
          if (newId) focusSavedCard(newId);
        } catch (e) { showToast('Save failed: ' + e.message, 'error'); }
      },
      onCancel: () => {
        card.remove();
        clearPendingHighlights();
        pendingSel = null;
        updateRailVisibility();
        layoutCards();
      },
    });
    rail.appendChild(card);
    layoutCards();
    setTimeout(() => { card._textarea.focus(); }, 50);
  }

  function clearPendingHighlights() {
    document.querySelectorAll('mark.pic-hl[data-cid="pending"]').forEach(m => {
      const t = document.createTextNode(m.textContent);
      m.parentNode.replaceChild(t, m);
    });
    document.querySelectorAll('.rect-hl[data-cid="pending"]').forEach(r => r.remove());
    document.querySelectorAll('.textLayer').forEach(tl => tl.normalize && tl.normalize());
  }

  function focusSavedCard(cid) {
    setActive(cid, false);
    const card = rail.querySelector('.pic-card[data-id="' + cid + '"]');
    if (!card) return;
    const r = card.getBoundingClientRect();
    if (r.top < 80 || r.bottom > window.innerHeight - 40) {
      card.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
    try { card.focus({ preventScroll: true }); } catch (_) {}
  }

  function openEditCard(c) {
    closeAnyEditor();
    editingId = c.id;
    setActive(c.id, false);
    const existing = rail.querySelector('.pic-card[data-id="' + c.id + '"]');
    const card = buildEditorEl({
      id: c.id,
      page: c.page,
      quote: c.quote,
      body: c.body || '',
      onSave: async (body) => {
        try {
          await api('/pdf-inline-comments/' + c.id, {
            method: 'PATCH',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({ body }),
          });
          editingId = null;
          await loadAndRender();
          focusSavedCard(c.id);
        } catch (e) { showToast('Save failed: ' + e.message, 'error'); }
      },
      onCancel: () => {
        editingId = null;
        renderCards(comments);
        layoutCards();
      },
    });
    if (existing) {
      // Editing an existing comment-bearing card in place.
      card.style.top = existing.style.top;
      existing.replaceWith(card);
    } else {
      // Highlight → comment conversion: no rail card exists yet, append one.
      rail.classList.remove('hidden');
      if (splitter) splitter.classList.remove('hidden');
      rail.appendChild(card);
    }
    layoutCards();
    setTimeout(() => { card._textarea.focus(); }, 50);
  }

  function closeAnyEditor() {
    const p = rail.querySelector('.pic-card.pending[data-pending="1"]');
    if (p) p.remove();
    clearPendingHighlights();
    if (editingId) { editingId = null; renderCards(comments); }
  }

  async function deleteOne(id) {
    if (!confirm('Delete this comment?')) return;
    try {
      await api('/pdf-inline-comments/' + id, { method: 'DELETE' });
      await loadAndRender();
    } catch (e) { showToast('Delete failed: ' + e.message, 'error'); }
  }

  function setActive(cid, scrollDoc) {
    activeId = cid;
    let activeCard = null;
    let layoutDirty = false;
    rail.querySelectorAll('.pic-card').forEach(c => {
      const isActive = c.dataset.id === String(cid);
      c.classList.toggle('active', isActive);
      if (isActive) activeCard = c;
      const body = c.querySelector('.pic-body');
      if (!body || !body.classList.contains('collapsible')) return;
      const btn = c.querySelector('.pic-expand');
      const wasCollapsed = body.classList.contains('collapsed');
      if (isActive && wasCollapsed) {
        body.classList.remove('collapsed');
        if (btn) btn.textContent = 'Show less';
        layoutDirty = true;
      } else if (!isActive && !wasCollapsed) {
        body.classList.add('collapsed');
        if (btn) btn.textContent = 'Show more';
        layoutDirty = true;
      }
    });
    if (layoutDirty) layoutCards();
    document.querySelectorAll('mark.pic-hl').forEach(m => {
      m.classList.toggle('active', m.dataset.cid === String(cid));
    });
    document.querySelectorAll('.rect-hl').forEach(r => {
      r.classList.toggle('active', r.dataset.cid === String(cid));
    });
    if (scrollDoc) {
      const target = document.querySelector('mark.pic-hl[data-cid="' + cid + '"]')
                  || document.querySelector('.rect-hl[data-cid="' + cid + '"]');
      if (target) {
        const r = target.getBoundingClientRect();
        if (r.top < 80 || r.bottom > window.innerHeight - 40) {
          target.scrollIntoView({ block: 'center', behavior: 'smooth' });
        }
      } else {
        // Comment is on an unrendered page — scroll to the page placeholder.
        const c = comments.find(x => x.id === cid);
        if (c) scrollToPage(c.page);
      }
    }
  }

  function scrollToPage(pageNum) {
    const d = pageDivs[pageNum - 1];
    if (!d) return;
    d.scrollIntoView({ block: 'start', behavior: 'smooth' });
  }

  function renderCards(items) {
    rail.querySelectorAll('.pic-card').forEach(el => {
      if (el.classList.contains('pending') && !el.dataset.id) return;
      el.remove();
    });
    for (const c of items) {
      if (c.id === editingId) continue;
      // Every annotation — including body-less highlights — gets a rail card
      // so it has an always-visible Delete button. (Clicking the highlight on
      // the page still pops the inline [💬 Delete] toolbar too.)
      const card = buildCardEl(c);
      rail.appendChild(card);
    }
    updateRailVisibility();
    rail.querySelectorAll('.pic-card').forEach(applyAutoCollapse);
  }

  function applyAutoCollapse(card) {
    const body = card.querySelector('.pic-body');
    if (!body) return;
    const oldBtn = card.querySelector('.pic-expand');
    if (oldBtn) oldBtn.remove();
    body.classList.remove('collapsible', 'collapsed');
    if (body.scrollHeight <= 180) return;
    body.classList.add('collapsible', 'collapsed');
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'pic-expand';
    btn.textContent = 'Show more';
    btn.addEventListener('click', (ev) => {
      ev.stopPropagation();
      const nowCollapsed = body.classList.toggle('collapsed');
      btn.textContent = nowCollapsed ? 'Show more' : 'Show less';
      layoutCards();
    });
    body.parentNode.insertBefore(btn, body.nextSibling);
  }

  function updateRailVisibility() {
    const hasCards = rail.querySelectorAll('.pic-card').length > 0;
    rail.classList.toggle('hidden', !hasCards);
    if (splitter) splitter.classList.toggle('hidden', !hasCards);
  }

  // Position cards relative to their anchors (mark or rect overlay).
  function layoutCards() {
    const cards = Array.from(rail.querySelectorAll('.pic-card'));
    if (!cards.length) return;
    const railRect = rail.getBoundingClientRect();

    const slots = cards.map(card => {
      let desiredTop;
      let isOrphan = false;
      if (card.classList.contains('pending') && card.dataset.pending === '1') {
        const pendingMk = document.querySelector('mark.pic-hl[data-cid="pending"]')
                       || document.querySelector('.rect-hl[data-cid="pending"]');
        if (pendingMk) {
          desiredTop = pendingMk.getBoundingClientRect().top - railRect.top;
        } else if (pendingSel && pendingSel.rect && pendingSel.kind === 'text') {
          desiredTop = pendingSel.rect.top - railRect.top;
        } else {
          desiredTop = 0;
        }
      } else if (card.dataset.anchored === '0') {
        // Anchor failed (quote couldn't be re-located and no rect overlay
        // was drawn). Position the card next to its source page anyway —
        // banishing to the rail bottom landed it at top:0px when no other
        // anchored cards were present, which on a deep page = top of the
        // document, so the card visually "jumped to the beginning".
        const cid = card.dataset.id;
        const c = comments.find(x => x.id === parseInt(cid, 10));
        const pd = c ? pageDivs[c.page - 1] : null;
        if (pd) {
          desiredTop = pd.getBoundingClientRect().top - railRect.top;
        } else {
          desiredTop = Number.MAX_SAFE_INTEGER;
          isOrphan = true;
        }
      } else {
        const cid = card.dataset.id;
        const mk = document.querySelector('mark.pic-hl[data-cid="' + cid + '"]')
                || document.querySelector('.rect-hl[data-cid="' + cid + '"]');
        if (!mk) {
          // Page not yet rendered — anchor to the page placeholder.
          const c = comments.find(x => x.id === parseInt(cid, 10));
          if (c) {
            const pd = pageDivs[c.page - 1];
            if (pd) desiredTop = pd.getBoundingClientRect().top - railRect.top;
            else    desiredTop = Number.MAX_SAFE_INTEGER;
          } else {
            desiredTop = Number.MAX_SAFE_INTEGER; isOrphan = true;
          }
        } else {
          desiredTop = mk.getBoundingClientRect().top - railRect.top;
        }
      }
      return { card, desiredTop, isOrphan };
    });

    slots.sort((a, b) => a.desiredTop - b.desiredTop);

    const GAP = 10;
    const activeIdx = activeId
      ? slots.findIndex(s => !s.isOrphan && s.card.dataset.id === String(activeId))
      : -1;
    let bottomCursor = 0;
    if (activeIdx === -1) {
      for (const s of slots) {
        if (s.isOrphan) continue;
        const top = Math.max(s.desiredTop, bottomCursor);
        s.card.style.top = top + 'px';
        bottomCursor = top + s.card.offsetHeight + GAP;
      }
    } else {
      const active = slots[activeIdx];
      const activeTop = Math.max(0, active.desiredTop);
      active.card.style.top = activeTop + 'px';
      const activeBot = activeTop + active.card.offsetHeight;
      let upCursor = activeTop - GAP;
      for (let i = activeIdx - 1; i >= 0; i--) {
        const s = slots[i];
        if (s.isOrphan) continue;
        const h = s.card.offsetHeight;
        const top = (s.desiredTop + h <= upCursor) ? s.desiredTop : (upCursor - h);
        s.card.style.top = top + 'px';
        upCursor = top - GAP;
      }
      let cursor = activeBot + GAP;
      for (let i = activeIdx + 1; i < slots.length; i++) {
        const s = slots[i];
        if (s.isOrphan) continue;
        const top = Math.max(s.desiredTop, cursor);
        s.card.style.top = top + 'px';
        cursor = top + s.card.offsetHeight + GAP;
      }
      bottomCursor = Math.max(cursor, activeBot + GAP);
    }
    for (const s of slots) {
      if (!s.isOrphan) continue;
      s.card.style.top = bottomCursor + 'px';
      bottomCursor += s.card.offsetHeight + GAP;
    }
    rail.style.minHeight = (bottomCursor + 40) + 'px';
  }

  async function loadAndRender() {
    let resp;
    try {
      resp = await api('/pdf-inline-comments?file_id=' + encodeURIComponent(FILE_ID));
    } catch (e) {
      showToast('Failed to load comments: ' + e.message, 'error');
      return;
    }
    comments = (resp && resp.comments) || [];
    // Anchor on any pages that are already rendered.
    const renderedPages = new Set();
    for (const c of comments) {
      if (pageRendered[c.page - 1]) renderedPages.add(c.page);
    }
    renderedPages.forEach(p => anchorCommentsOnPage(p));
    // Mark unanchored on unrendered pages as not-yet-orphan so the card
    // shows at the page placeholder; they get re-anchored when their page renders.
    for (const c of comments) {
      if (!pageRendered[c.page - 1]) c.orphan = false;
    }
    renderCards(comments);
    layoutCards();
  }

  // ── Zoom controls + page input ──────────────────────────────────────
  document.getElementById('zoomIn').addEventListener('click', () => applyScale(scale + 0.1));
  document.getElementById('zoomOut').addEventListener('click', () => applyScale(scale - 0.1));
  document.getElementById('zoomFit').addEventListener('click', () => fitToWidth());
  pageInput.addEventListener('change', () => {
    const n = parseInt(pageInput.value, 10);
    if (n >= 1 && n <= (pdfDoc && pdfDoc.numPages || 1)) scrollToPage(n);
  });
  function setupPageInputTracker() {
    // Update page-input as user scrolls — uses the page whose midline is
    // closest to the viewport midline.
    const update = () => {
      const midY = window.scrollY + window.innerHeight / 2;
      let best = 1, bestDist = Infinity;
      for (const d of pageDivs) {
        const r = d.getBoundingClientRect();
        const top = r.top + window.scrollY;
        const mid = top + r.height / 2;
        const dist = Math.abs(mid - midY);
        if (dist < bestDist) { bestDist = dist; best = parseInt(d.dataset.pageNum, 10); }
      }
      pageInput.value = best;
    };
    let raf = 0;
    window.addEventListener('scroll', () => {
      if (raf) return;
      raf = requestAnimationFrame(() => { raf = 0; update(); layoutCards(); });
    }, { passive: true });
    window.addEventListener('resize', () => { update(); layoutCards(); });
  }

  loadPdf().catch(e => {
    docEl.innerHTML = '<div style="color:#ddd;padding:48px;text-align:center;font-family:sans-serif">' +
                      'Failed to load PDF: ' + (e && e.message ? e.message : e) + '</div>';
  });
  </script>
</body>
</html>
"""
