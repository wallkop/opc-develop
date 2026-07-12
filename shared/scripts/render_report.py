#!/usr/bin/env python3
"""Render a dependency-free, self-contained HTML companion for human reports."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

REQUIRED_ZH = ("结论", "对用户意味着什么", "证据")


def inline(text: str) -> str:
    value = html.escape(text)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", value)
    return value


def render_markdown(text: str) -> str:
    lines = text.splitlines()
    out, in_code, list_open = [], False, False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("```"):
            if list_open:
                out.append("</ul>"); list_open = False
            out.append("<pre><code>" if not in_code else "</code></pre>")
            in_code = not in_code
            continue
        if in_code:
            out.append(html.escape(line) + "\n")
            continue
        match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if match:
            if list_open:
                out.append("</ul>"); list_open = False
            level = len(match.group(1))
            out.append(f"<h{level}>{inline(match.group(2))}</h{level}>")
        elif line.startswith("- "):
            if not list_open:
                out.append("<ul>"); list_open = True
            out.append(f"<li>{inline(line[2:])}</li>")
        elif not line:
            if list_open:
                out.append("</ul>"); list_open = False
        else:
            if list_open:
                out.append("</ul>"); list_open = False
            out.append(f"<p>{inline(line)}</p>")
    if list_open:
        out.append("</ul>")
    return "\n".join(out)


def render_report(source: Path, output: Path, lang: str = "zh-CN", title: str | None = None) -> Path:
    text = source.read_text(encoding="utf-8")
    digest = hashlib.sha256(text.encode()).hexdigest()
    heading = title or next((line.lstrip("# ") for line in text.splitlines() if line.startswith("# ")), source.stem)
    body = render_markdown(text)
    doc = f"""<!doctype html>
<html lang="{html.escape(lang)}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="opc-source-sha256" content="{digest}"><title>{html.escape(heading)}</title>
<style>:root{{--ink:#172033;--muted:#5e687a;--line:#dfe4ec;--paper:#fff;--accent:#2855d9}}*{{box-sizing:border-box}}body{{margin:0;background:#f4f6fa;color:var(--ink);font:16px/1.72 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}}main{{max-width:76ch;margin:40px auto;padding:40px;background:var(--paper);border:1px solid var(--line);border-radius:16px}}h1,h2,h3{{line-height:1.3}}h2{{margin-top:2em;border-top:1px solid var(--line);padding-top:1em}}code{{background:#eef1f6;padding:.12em .35em;border-radius:4px}}pre{{overflow:auto;background:#111827;color:#e5e7eb;padding:16px;border-radius:10px}}li{{margin:.35em 0}}p{{color:var(--ink)}}@media(max-width:720px){{main{{margin:0;padding:24px;border:0;border-radius:0}}}}</style></head>
<body><main>{body}</main></body></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(doc, encoding="utf-8")
    return output


def lint_report(source: Path, output: Path, terms_path: Path | None = None, lang: str = "zh-CN") -> list[str]:
    errors = []
    if not output.exists():
        return ["html companion missing"]
    src = source.read_text(encoding="utf-8")
    rendered = output.read_text(encoding="utf-8")
    digest = hashlib.sha256(src.encode()).hexdigest()
    if f'opc-source-sha256" content="{digest}"' not in rendered:
        errors.append("source SHA mismatch")
    if f'<html lang="{lang}"' not in rendered:
        errors.append("language attribute mismatch")
    if re.search(r"<(?:link|script)[^>]+(?:src|href)=", rendered, re.I):
        errors.append("external asset detected")
    if lang.lower().startswith("zh"):
        for heading in REQUIRED_ZH:
            if heading not in src:
                errors.append(f"missing plain-language section: {heading}")
        if "下一步" not in src and "需要决定什么" not in src:
            errors.append("missing plain-language section: 下一步/需要决定什么")
    if terms_path and terms_path.exists():
        terms = json.loads(terms_path.read_text(encoding="utf-8"))
        for term in terms.get("terms", []):
            name = term["name"]
            first = src.find(name)
            if first >= 0:
                nearby = src[first + len(name): first + len(name) + 100]
                if not re.match(r"\s*[（(][^）)]+[）)]", nearby):
                    errors.append(f"term lacks first-use explanation: {name}")
                tail = src[first + len(name) + len(nearby):]
                prefix = str(term.get("explanation", ""))[:8]
                if prefix and re.search(re.escape(name) + r"\s*[（(]" + re.escape(prefix), tail):
                    errors.append(f"term explanation repeated: {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    render = sub.add_parser("render")
    render.add_argument("source"); render.add_argument("--out", required=True); render.add_argument("--lang", default="zh-CN")
    lint = sub.add_parser("lint")
    lint.add_argument("source"); lint.add_argument("--html", required=True); lint.add_argument("--terms"); lint.add_argument("--lang", default="zh-CN")
    args = parser.parse_args()
    if args.command == "render":
        render_report(Path(args.source), Path(args.out), args.lang)
        return 0
    errors = lint_report(Path(args.source), Path(args.html), Path(args.terms) if args.terms else None, args.lang)
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
