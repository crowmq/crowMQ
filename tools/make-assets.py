#!/usr/bin/env python3
"""Regenerate the static image assets from the brand geometry in build.py.

    python3 tools/make-assets.py

Needs cairosvg only for the PNG social card:  pip install cairosvg
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build  # noqa: E402

OUT = build.ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "people").mkdir(exist_ok=True)

INK, ACCENT, PAPER, HALO = build.INK, build.ACCENT, build.PAPER, build.HALO
NS = 'xmlns="http://www.w3.org/2000/svg"'


def write(name, body):
    (OUT / name).write_text(body + "\n")
    print("wrote assets/img/" + name)


# --- favicon: the crow head Q, fine detail removed for small sizes -----------
def favicon(bg, ink, accent, counter):
    return (f'<svg {NS} viewBox="0 0 64 64" width="64" height="64">'
            f'<rect width="64" height="64" rx="14" fill="{bg}"/>'
            + build.crow_head("translate(28.7,26.6) rotate(45) scale(0.52)",
                              ink=ink, accent=accent, counter=counter, detail=False)
            + "</svg>")


write("favicon.svg", favicon(PAPER, INK, ACCENT, PAPER))
write("favicon-dark.svg", favicon(INK, PAPER, HALO, INK))

# --- standalone mark and wordmarks ------------------------------------------
write("crowmq-mark.svg",
      f'<svg {NS} viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="CrowMQ">'
      + build.crow_head("translate(28.7,26.6) rotate(45) scale(0.52)") + "</svg>")
write("crowmq-wordmark.svg", build.wordmark())
write("crowmq-wordmark-reverse.svg", build.wordmark(ink=PAPER, accent=HALO, counter=INK))

# --- social card -------------------------------------------------------------
inner = build.wordmark().replace(
    f'<svg viewBox="6 4 220 74" {NS} role="img" aria-label="CrowMQ">',
    '<svg x="88" y="64" width="430" height="145" viewBox="6 4 220 74">')

og = (f'<svg {NS} viewBox="0 0 1200 630" width="1200" height="630">'
      f'<rect width="1200" height="630" fill="#F2F3F5"/>'
      f'<g stroke="#D3D7E0" stroke-width="1.6" fill="none">'
      f'<path d="M0,556 L150,470 L300,556 L450,470 L600,556 L750,470 L900,556 L1050,470 L1200,556"/>'
      f'</g>'
      f'<g fill="#C6CBD6">'
      + "".join(f'<circle cx="{x}" cy="{y}" r="5"/>'
                for x, y in [(150, 470), (300, 556), (450, 470), (600, 556)])
      + f'</g><g fill="{HALO}">'
      + "".join(f'<circle cx="{x}" cy="{y}" r="5"/>'
                for x, y in [(750, 470), (900, 556), (1050, 470)])
      + "</g>"
      + inner
      + f'<text x="90" y="300" font-family="IBM Plex Sans, sans-serif" font-size="47" '
        f'font-weight="600" fill="{INK}">An intelligent messaging protocol</text>'
      + f'<text x="90" y="356" font-family="IBM Plex Sans, sans-serif" font-size="47" '
        f'font-weight="600" fill="{INK}">for agentic systems</text>'
      + f'<text x="92" y="410" font-family="IBM Plex Mono, monospace" font-size="21" '
        f'fill="#646B7C">adaptive publish–subscribe · Active Inference control</text>'
      + f'<text x="92" y="444" font-family="IBM Plex Mono, monospace" font-size="21" '
        f'fill="#646B7C">Department of Computer and Systems Sciences, Stockholm University</text>'
      + "</svg>")
write("og-image.svg", og)

try:
    import cairosvg
    cairosvg.svg2png(bytestring=og.encode(), write_to=str(OUT / "og-image.png"),
                     output_width=1200, output_height=630)
    print("wrote assets/img/og-image.png")
except ImportError:
    print("cairosvg not installed — og-image.png not regenerated")
