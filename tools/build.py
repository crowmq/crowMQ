#!/usr/bin/env python3
"""Build the CrowMQ site.

Pages ship as self-contained HTML so GitHub Pages can serve them with no build
step. This script keeps the shell, styles, logo and figures in one place.

    python3 tools/build.py

Content lives in tools/pages/*.html, styles in tools/site.css, and the shell,
navigation, logo and figures below.
"""

import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

SITE_NAME = "CrowMQ"
TAGLINE = "An intelligent messaging protocol for agentic systems."
INSTITUTION = "Department of Computer and Systems Sciences, Stockholm University"
GITHUB = "https://github.com/your-username/crowmq"          # <- change me
BASE_URL = "https://your-username.github.io/crowmq-site"    # <- change me
CONTACT = "your-email@dsv.su.se"                            # <- change me

INK, ACCENT, PAPER, HALO = "#12151C", "#4F46E5", "#FFFFFF", "#818CF8"

# ---------------------------------------------------------------------------
# logo
#
# Geometry is taken verbatim from the brand source (anim.py / brand notes).
# The W/M ligature sits on a 42-unit grid with vertices every 10.5; offsetting
# M by 31.5 makes the two letters share one diagonal, giving a set width of
# 73.5. The Q is a crow head drawn bill-horizontal, then rotated 45 degrees.
# ---------------------------------------------------------------------------

V = [(0, 0), (10.5, 32), (21, 6), (31.5, 32), (42, 0), (52.5, 26), (63, 0), (73.5, 32)]
R = [4.2, 3.2, 2.2, 4.2, 3.2, 4.2, 2.2, 3.2]
EDGES = [(i, i + 1) for i in range(7)]
# staggered so channels fire independently rather than in sequence
DELAY = [0.0, -2.1, -0.7, -3.0, -1.4, -2.6, -0.35]

HEAD = ("M32,-18 C26,-36 10,-44 -6,-43 C-28,-42 -44,-26 -44,-4 C-44,8 -40,18 -33,25 "
        "L-28,17 C-24,29 -20,35 -10,36 C8,39 26,26 32,8 C34,0 34,-10 32,-18 Z")
CROWN = ("M32,-18 C26,-36 10,-44 -6,-43 C-28,-42 -44,-26 -44,-4 C-43,4 -41,10 -38,15 "
         "C-34,0 -24,-12 -8,-19 C6,-25 24,-24 32,-18 Z")
BILL = "M32,-20 L40,-18 C54,-16 66,-10 76,0 L72,6 C56,10 42,11 30,10 C30,0 31,-10 32,-20 Z"
GAPE = "M31,-2 C45,0 60,1 73,3"


def crow_head(transform, ink=INK, accent=ACCENT, counter=PAPER, detail=True):
    o = [f'<g transform="{transform}">',
         f'<path d="{HEAD}" fill="{ink}"/>',
         f'<path d="{CROWN}" fill="{accent}"/>',
         f'<path d="{BILL}" fill="{ink}"/>']
    if detail:
        o.append(f'<path d="{GAPE}" fill="none" stroke="{counter}" stroke-width="2.5" '
                 f'stroke-linecap="round"/>')
    o.append(f'<circle cx="4" cy="-10" r="12" fill="{counter}"/>')
    o.append(f'<circle cx="4" cy="-10" r="8.5" fill="{accent}"/>')
    o.append(f'<circle cx="4" cy="-10" r="{3.8 if detail else 4.4}" fill="{ink}"/>')
    if detail:
        o.append(f'<circle cx="7.5" cy="-13.5" r="1.8" fill="{counter}"/>')
    o.append("</g>")
    return "".join(o)


def wordmark(ink=INK, accent=ACCENT, counter=PAPER, aria="CrowMQ"):
    """Full lockup. 'Cro' is live text — convert to outlines before print use."""
    o = [f'<svg viewBox="6 4 220 74" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="{aria}">',
         f'<text x="92" y="52" text-anchor="end" font-family="IBM Plex Sans, sans-serif" '
         f'font-size="45.5" font-weight="500" fill="{ink}">Cro</text>',
         '<g transform="translate(96,20)">',
         f'<path d="M0,0 L10.5,32 L21,6 L31.5,32 L36.75,16" fill="none" stroke="{ink}" stroke-width="1.9"/>',
         f'<path d="M36.75,16 L42,0 L52.5,26 L63,0 L73.5,32" fill="none" stroke="{accent}" stroke-width="1.9"/>']
    for i, (x, y) in enumerate(V):
        o.append(f'<circle cx="{x}" cy="{y}" r="{R[i]}" fill="{ink if i < 4 else accent}"/>')
    o.append(f'<circle cx="36.75" cy="16" r="3.3" fill="{counter}" stroke="{ink}" stroke-width="1.5"/>')
    o.append("</g>")
    o.append(crow_head("translate(191,37.9) rotate(45) scale(0.48)", ink, accent, counter))
    o.append("</svg>")
    return "".join(o)


LOGO = wordmark()
LOGO_REVERSE = wordmark(ink="#FFFFFF", accent=HALO, counter=INK)

MARK = ('<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CrowMQ">'
        + crow_head("translate(28.7,26.6) rotate(45) scale(0.52)", detail=False)
        + "</svg>")

TICK = ('<svg class="tick" viewBox="0 0 46 22" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        '<path d="M4,18 L12,5 L20,18 L28,5 L36,18" stroke-linecap="round"/>'
        '<circle cx="4" cy="18" r="2.8"/><circle cx="20" cy="18" r="2.2"/>'
        '<circle cx="36" cy="18" r="2.8"/><circle cx="28" cy="5" r="2"/>'
        "</svg>")


def ligature_live(scale=1.0):
    """The network ligature with channel activity, used as the hero graphic.

    Each channel lights on its own schedule: the edge glows, a packet crosses
    it, and the endpoint nodes swell. Nothing runs left to right, so the mark
    reads as load spread across devices rather than a pipeline.
    """
    o = ['<svg class="ligature" viewBox="-14 -14 102 60" xmlns="http://www.w3.org/2000/svg" '
         'role="img" aria-label="A network of eight nodes with messages crossing several '
         'channels at once">']
    for e, (a, b) in enumerate(EDGES):                    # glow under the wire
        (x1, y1), (x2, y2) = V[a], V[b]
        o.append(f'<line class="lig-glow" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke-width="5" style="animation-delay:{DELAY[e]}s"/>')
    o.append(f'<path class="lig-wire-ink" d="M0,0 L10.5,32 L21,6 L31.5,32 L36.75,16"/>')
    o.append(f'<path class="lig-wire-accent" d="M36.75,16 L42,0 L52.5,26 L63,0 L73.5,32"/>')
    for i, (x, y) in enumerate(V):                        # node halo + node
        o.append(f'<circle class="lig-halo" cx="{x}" cy="{y}" r="{R[i]}" '
                 f'style="animation-delay:{DELAY[i % 7]}s"/>')
        o.append(f'<circle class="lig-node-{"ink" if i < 4 else "accent"}" cx="{x}" cy="{y}" r="{R[i]}"/>')
    o.append('<circle class="lig-hollow" cx="36.75" cy="16" r="3.3"/>')
    for e, (a, b) in enumerate(EDGES):                    # packet in flight
        (x1, y1), (x2, y2) = V[a], V[b]
        o.append(f'<circle class="lig-packet" r="2.4" style="animation-delay:{DELAY[e]}s">'
                 f'<animateMotion dur="3.6s" begin="{DELAY[e]}s" repeatCount="indefinite" '
                 f'path="M{x1},{y1} L{x2},{y2}"/></circle>')
    o.append("</svg>")
    return "".join(o)


LIGATURE = ligature_live()

# ---------------------------------------------------------------------------
# figure helpers
# ---------------------------------------------------------------------------


def box(x, y, w, h, title, subs=(), cls="box", rx=8, pad=11, tcls="t"):
    o = [f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>']
    ty = y + pad + 11
    for line in ([title] if isinstance(title, str) else title):
        o.append(f'<text class="{tcls}" x="{x + pad}" y="{ty}">{line}</text>')
        ty += 15
    ty += 2
    for line in subs:
        o.append(f'<text class="t-sm" x="{x + pad}" y="{ty}">{line}</text>')
        ty += 13
    return "".join(o)


ARROWS = ('<defs>'
          '<marker id="a1" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" '
          'markerHeight="6.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#B9BFCB"/></marker>'
          '<marker id="a2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" '
          f'markerHeight="6.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>'
          '</defs>')

# ---------------------------------------------------------------------------
# figure 1 — model memory against single-accelerator capacity
# ---------------------------------------------------------------------------

X0, X1, Y0, Y1 = 78, 866, 46, 384
LO, HI = math.log10(30), math.log10(30000)


def fx(year):
    return X0 + (year - 2020) * (X1 - X0) / 6


def fy(v):
    return Y1 - (math.log10(v) - LO) / (HI - LO) * (Y1 - Y0)


def _fit_pts(f):
    return [(fx(2020 + t), fy(f(t))) for t in range(7)]


def figure1():
    mfit = _fit_pts(lambda t: 526.2 * math.exp(0.435 * t))
    hfit = _fit_pts(lambda t: 40.3 + 40.7 * t)
    mpath = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in mfit)
    hpath = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in hfit)
    gap = (mpath + " L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in reversed(hfit)) + " Z")

    o = [f'<svg class="fig" viewBox="0 0 900 470" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Log-scale chart, 2020 to 2026. Representative model weight memory rises '
         f'exponentially from about 500 gigabytes to several terabytes, while single-GPU memory '
         f'rises roughly linearly from 80 to 288 gigabytes. The gap between the two trends widens '
         f'every year.">', ARROWS]

    for v in (30, 100, 300, 1000, 3000, 10000, 30000):
        y = fy(v)
        o.append(f'<line class="grid" x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}"/>')
        o.append(f'<text class="t-sm" x="{X0 - 10}" y="{y + 3.5:.1f}" text-anchor="end">'
                 f'{v:,}</text>')
    for t in range(7):
        x = fx(2020 + t)
        o.append(f'<line class="grid" x1="{x:.1f}" y1="{Y1}" x2="{x:.1f}" y2="{Y1 + 6}"/>')
        o.append(f'<text class="t-sm" x="{x:.1f}" y="{Y1 + 22}" text-anchor="middle">{2020 + t}</text>')
    o.append(f'<line class="axis" x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}"/>')
    o.append(f'<line class="axis" x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}"/>')
    o.append(f'<text class="t-sm" transform="translate(24,{(Y0 + Y1) / 2:.0f}) rotate(-90)" '
             f'text-anchor="middle">memory (GB)</text>')
    o.append(f'<text class="t-sm" x="{(X0 + X1) / 2:.0f}" y="{Y1 + 44}" text-anchor="middle">year</text>')

    o.append(f'<path class="f1-gap" d="{gap}"/>')
    o.append(f'<path class="f1-fit-h" d="{hpath}"/>')
    o.append(f'<path class="f1-fit-m" d="{mpath}"/>')

    models = [(2020, 350, "GPT-3", "up"), (2021, 1000, "", ""), (2022, 1150, "", ""),
              (2023, 1600, "", ""), (2024, 2700, "", ""), (2025, 3400, "", ""),
              (2026, 9000, "Kimi K3 · 2.8T", "left")]
    gpus = [(2020, 80, "A100", "down"), (2021, 80, "", ""), (2022, 80, "", ""),
            (2023, 141, "", ""), (2024, 192, "", ""), (2025, 288, "", ""),
            (2026, 288, "B300 · 288 GB", "left")]
    others = [(2026, 6400, "DeepSeek V4 Pro / LongCat 2.0 · 1.6T"),
              (2026, 2976, "GLM-5 · 744B")]

    d = 0.0
    for year, v, label, pos in models:
        x, y = fx(year), fy(v)
        o.append(f'<path class="f1-pt" style="animation-delay:{1.5 + d:.2f}s" '
                 f'd="M{x:.1f},{y - 5.4:.1f} L{x + 5:.1f},{y + 3.6:.1f} L{x - 5:.1f},{y + 3.6:.1f} Z" '
                 f'fill="{ACCENT}"/>')
        d += 0.07
    for year, v, label, pos in gpus:
        x, y = fx(year), fy(v)
        o.append(f'<rect class="f1-pt" style="animation-delay:{1.5 + d:.2f}s" '
                 f'x="{x - 4.4:.1f}" y="{y - 4.4:.1f}" width="8.8" height="8.8" rx="1.5" fill="#5A6170"/>')
        d += 0.07
    for year, v, label in others:
        x, y = fx(year), fy(v)
        o.append(f'<circle class="f1-pt" style="animation-delay:{1.5 + d:.2f}s" cx="{x:.1f}" '
                 f'cy="{y:.1f}" r="4.6" fill="none" stroke="{HALO}" stroke-width="2"/>')
        d += 0.07

    o.append(f'<text class="f1-lab" x="{fx(2020) + 10:.0f}" y="{fy(350) - 9:.0f}" fill="{ACCENT}">GPT-3</text>')
    o.append(f'<text class="f1-lab" x="{fx(2020) + 10:.0f}" y="{fy(80) + 16:.0f}" fill="#5A6170">A100 · 80 GB</text>')
    o.append(f'<text class="f1-lab" x="{fx(2026) - 18:.0f}" y="{fy(9000) - 10:.0f}" fill="{ACCENT}" '
             f'text-anchor="end">Kimi K3 · 2.8T parameters</text>')
    o.append(f'<text class="f1-lab" x="{fx(2026) - 18:.0f}" y="{fy(6400) + 3:.0f}" fill="{HALO}" '
             f'text-anchor="end">DeepSeek V4 Pro / LongCat 2.0 · 1.6T</text>')
    o.append(f'<text class="f1-lab" x="{fx(2026) - 18:.0f}" y="{fy(2976) + 3:.0f}" fill="{HALO}" '
             f'text-anchor="end">GLM-5 · 744B</text>')
    o.append(f'<text class="f1-lab" x="{fx(2026) - 18:.0f}" y="{fy(288) + 20:.0f}" fill="#5A6170" '
             f'text-anchor="end">B300 · 288 GB</text>')
    o.append(f'<text class="f1-lab" x="{fx(2023.1):.0f}" y="{fy(600):.0f}" fill="{ACCENT}" '
             f'text-anchor="middle">widening gap between the fitted trends</text>')

    lx, ly = X0 + 14, Y0 + 6
    o.append(f'<rect class="box" x="{lx}" y="{ly}" width="248" height="76" rx="8"/>')
    o.append(f'<line x1="{lx + 14}" y1="{ly + 20}" x2="{lx + 40}" y2="{ly + 20}" stroke="{ACCENT}" stroke-width="2.2"/>')
    o.append(f'<text class="t-sm" x="{lx + 48}" y="{ly + 23.5}">exponential fit  M(t) = 526.2 e^0.435t</text>')
    o.append(f'<line x1="{lx + 14}" y1="{ly + 39}" x2="{lx + 40}" y2="{ly + 39}" stroke="#7A8394" stroke-width="2" stroke-dasharray="7 5"/>')
    o.append(f'<text class="t-sm" x="{lx + 48}" y="{ly + 42.5}">linear fit  H(t) = 40.3 + 40.7t</text>')
    o.append(f'<path d="M{lx + 20},{ly + 62} L{lx + 25},{ly + 53} L{lx + 30},{ly + 62} Z" fill="{ACCENT}"/>')
    o.append(f'<rect x="{lx + 44}" y="{ly + 53}" width="8.8" height="8.8" rx="1.5" fill="#5A6170"/>')
    o.append(f'<circle cx="{lx + 72}" cy="{ly + 57.5}" r="4.6" fill="none" stroke="{HALO}" stroke-width="2"/>')
    o.append(f'<text class="t-sm" x="{lx + 86}" y="{ly + 61}">model · GPU · other 2026 models</text>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------------------
# figure 2 — protocol architecture
# ---------------------------------------------------------------------------


def figure2():
    o = [f'<svg class="fig" viewBox="0 0 1000 560" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="Publishers send messages through an input interface into the CrowMQ broker. '
         f'The broker has a control plane holding the runtime observation layer, the Active '
         f'Inference controller and the policy manager; a data plane holding admission and '
         f'validation, adaptive message queues, the delivery engine and acknowledgement handling, '
         f'and persistent storage. Messages leave through an output interface to subscribers, and '
         f'the control plane issues control signals down into the data plane.">', ARROWS]

    # publishers and subscribers
    o.append(f'<text class="t-sm" x="18" y="212">agentic AI systems</text>')
    o.append(box(18, 220, 120, 160, ["Publishers"],
                 ["Agent-1", "Agent-2", "Other agents"], cls="box-accent"))
    o.append(f'<text class="t-sm" x="890" y="212">agentic AI systems</text>')
    o.append(box(890, 220, 108, 160, ["Subscribers"],
                 ["Agent-1", "Agent-2", "Other agents"], cls="box-accent"))

    o.append(box(150, 220, 100, 160, ["Input", "interface"],
                 ["Publish API", "Parsing", "Auth", "Validation"]))
    o.append(box(762, 220, 100, 160, ["Output", "interface"],
                 ["Subscribe API", "Delivery", "Acks", "Events"]))

    # broker container
    o.append('<rect class="group-accent" x="264" y="40" width="478" height="470" rx="16"/>')
    o.append('<text class="t-lg" x="284" y="66">CrowMQ broker</text>')
    o.append('<text class="t-sm" x="284" y="84">adaptive message queue</text>')

    # control plane
    o.append('<rect class="group" x="276" y="96" width="454" height="120" rx="12"/>')
    o.append(f'<text class="t-key" x="290" y="114">control plane · adaptive communication control</text>')
    o.append(box(288, 122, 140, 82, ["Runtime", "observation"],
                 ["queue state, arrivals,", "deliveries, resources"]))
    o.append(box(440, 122, 136, 82, ["Active Inference", "controller"],
                 ["belief update, EFE,", "action selection"], cls="box-accent"))
    o.append(box(588, 122, 130, 82, ["Policy", "manager"],
                 ["protocol constraints,", "safety fallback"]))
    o.append('<path class="wire" marker-end="url(#a1)" d="M428,163 L436,163"/>')
    o.append('<path class="wire" marker-end="url(#a1)" d="M576,163 L584,163"/>')

    # control signal path into the data plane
    o.append('<path class="wire-accent" marker-end="url(#a2)" stroke-dasharray="5 4" '
             'd="M650,204 L650,232 L452,232 L452,256"/>')
    o.append('<text class="t-key" x="290" y="226">control signals · priority, buffering, batching, replacement</text>')

    # data plane
    o.append('<rect class="group" x="276" y="236" width="454" height="124" rx="12"/>')
    o.append(f'<text class="t-key" x="290" y="254">data plane · message execution</text>')
    o.append(box(286, 262, 100, 86, ["Admission", "&amp; validation"], ["envelope checks"]))
    o.append(box(400, 262, 104, 86, ["Adaptive", "queues"], ["per topic"], cls="box-accent"))
    o.append(box(518, 262, 100, 86, ["Delivery", "engine"], ["subscriber match"]))
    o.append(box(624, 262, 104, 86, ["Ack &amp; retry"], ["settle, retry"]))
    o.append('<path class="wire" marker-end="url(#a1)" d="M386,305 L396,305"/>')
    o.append('<path class="wire" marker-end="url(#a1)" d="M504,305 L514,305"/>')
    o.append('<path class="wire" marker-end="url(#a1)" d="M618,305 L620,305"/>')

    # observation feedback
    o.append('<path class="wire" stroke-dasharray="4 4" marker-end="url(#a1)" '
             'd="M286,300 L272,300 L272,163 L284,163"/>')
    o.append('<text class="t" x="18" y="58">Publishers attach an envelope</text>')
    o.append('<text class="t-sm" x="18" y="78">topic, priority, deadline,</text>')
    o.append('<text class="t-sm" x="18" y="91">dependencies, supersession</text>')
    o.append('<text class="t" x="982" y="58" text-anchor="end">Subscribers receive</text>')
    o.append('<text class="t-sm" x="982" y="78" text-anchor="end">delivery, acknowledgements,</text>')
    o.append('<text class="t-sm" x="982" y="91" text-anchor="end">event notifications</text>')

    # persistent storage
    o.append('<rect class="group" x="276" y="380" width="454" height="116" rx="12"/>')
    o.append(f'<text class="t-key" x="290" y="398">persistent storage</text>')
    o.append(box(288, 406, 104, 78, ["Queue &amp;", "metadata"], ["state, expiry"]))
    o.append(box(402, 406, 100, 78, ["Runtime", "statistics"], ["telemetry"]))
    o.append(box(512, 406, 100, 78, ["Adaptation", "logs"], ["decisions"]))
    o.append(box(622, 406, 96, 78, ["Config"], ["constraints"]))
    o.append('<path class="wire" stroke-dasharray="4 4" d="M452,348 L452,402"/>')
    o.append('<path class="wire" stroke-dasharray="4 4" d="M650,204 L740,204 L740,444 L722,444"/>')

    # connecting arrows across the whole path
    for a, b in [(138, 148), (250, 262), (742, 760), (862, 888)]:
        o.append(f'<path class="wire-accent" marker-end="url(#a2)" d="M{a},300 L{b},300"/>')

    # travelling pulses
    o.append('<g class="f2-msg"><circle class="pulse" r="5"/>'
             '<circle class="pulse-halo" r="9" opacity=".25"/></g>')
    o.append('<g class="f2-ctrl"><circle class="pulse-halo" r="4.5"/></g>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------------------
# figure 3 — the observe / infer / evaluate / act loop
# ---------------------------------------------------------------------------


def figure3():
    cx, cy, rr = 450, 236, 150
    o = [f'<svg class="fig" viewBox="0 0 900 500" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="A closed loop around the CrowMQ Active Inference controller: observe, '
         f'infer, evaluate, act, and back to observe. A dashed Markov blanket separates the '
         f'controller from publishers, subscribers, agent goals and application workflows, which '
         f'all sit outside it.">', ARROWS]

    o.append(f'<ellipse class="group-accent" cx="{cx}" cy="{cy}" rx="272" ry="216"/>')
    o.append(f'<text class="t-key" x="{cx}" y="{cy + 246}" text-anchor="middle">Markov blanket · '
             f'what the controller may observe and what it may influence</text>')

    for x, y, label in [(40, 70, "Publishers"), (700, 70, "Subscribers"),
                        (40, 372, "Agent goals and reasoning"), (700, 372, "Application workflows")]:
        w = 176 if len(label) > 14 else 150
        o.append(box(x, y, w, 52, [label], ["outside the blanket"]))

    o.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="{ACCENT}"/>')
    o.append(f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" font-family="IBM Plex Sans, sans-serif" '
             f'font-size="14" font-weight="600" fill="#fff">CrowMQ</text>')
    o.append(f'<text x="{cx}" y="{cy + 13}" text-anchor="middle" font-family="IBM Plex Sans, sans-serif" '
             f'font-size="14" font-weight="600" fill="#fff">controller</text>')

    stages = [
        (cx - 92, cy - rr - 30, 184, 72, "1 · Observe",
         ["queue state, message age,", "arrivals, subscriber state"]),
        (cx + rr - 44, cy - 36, 188, 72, "2 · Infer",
         ["update beliefs about", "a partly observable state"]),
        (cx - 92, cy + rr - 42, 184, 72, "3 · Evaluate",
         ["estimate expected free", "energy, select a policy"]),
        (cx - rr - 144, cy - 36, 188, 72, "4 · Act",
         ["prioritise, defer, batch,", "replace, drop, buffer"]),
    ]
    o.append(f'<g class="f3-orbit"><circle class="pulse" cx="{cx}" cy="{cy - 118}" r="6"/></g>')
    for x, y, w, h, title, subs in stages:
        o.append(box(x, y, w, h, [title], subs, cls="box-accent"))

    arc = ('M{:.0f},{:.0f} A{},{} 0 0 1 {:.0f},{:.0f}')
    o.append(f'<path class="wire-accent" marker-end="url(#a2)" d="'
             f'M{cx + 96},{cy - rr + 12} A118,118 0 0 1 {cx + rr - 6},{cy - 46}"/>')
    o.append(f'<path class="wire-accent" marker-end="url(#a2)" d="'
             f'M{cx + rr - 6},{cy + 46} A118,118 0 0 1 {cx + 96},{cy + rr - 12}"/>')
    o.append(f'<path class="wire-accent" marker-end="url(#a2)" d="'
             f'M{cx - 96},{cy + rr - 12} A118,118 0 0 1 {cx - rr + 6},{cy + 46}"/>')
    o.append(f'<path class="wire-accent" marker-end="url(#a2)" d="'
             f'M{cx - rr + 6},{cy - 46} A118,118 0 0 1 {cx - 96},{cy - rr + 12}"/>')

    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------------------
# figure 4 — implementation plan
# ---------------------------------------------------------------------------


def figure4():
    left, right, top = 280, 880, 62
    cw = (right - left) / 12
    rows = [
        ("T1", "Protocol and system design", 1, 4, ACCENT),
        ("T2", "Adaptive communication intelligence", 2, 7, ACCENT),
        ("T3", "Prototype and integration", 4, 9, ACCENT),
        ("T4", "Benchmarking and validation", 6, 12, ACCENT),
    ]
    marks = [(4, 0, "D1 / MS1"), (7, 1, "D2"), (9, 2, "D3 / MS2"),
             (10, 3, "D4"), (12, 3, "D5 / MS3")]

    o = [f'<svg class="fig" viewBox="0 0 900 300" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="A twelve month plan. Task 1 runs months 1 to 4, task 2 months 2 to 7, '
         f'task 3 months 4 to 9 and task 4 months 6 to 12. Milestones fall at months 4, 9 and 12.">']

    o.append(f'<text class="t-sm" x="{left - 12}" y="{top - 20}" text-anchor="end">month</text>')
    for m in range(13):
        x = left + m * cw
        o.append(f'<line class="grid" x1="{x:.1f}" y1="{top - 14}" x2="{x:.1f}" y2="248"/>')
        if m:
            o.append(f'<text class="t-sm" x="{x - cw / 2:.1f}" y="{top - 20}" text-anchor="middle">{m}</text>')

    for i, (tid, label, a, b, col) in enumerate(rows):
        y = top + 6 + i * 46
        x = left + (a - 1) * cw
        w = (b - a + 1) * cw
        o.append(f'<text class="t" x="18" y="{y + 20}">{tid}</text>')
        o.append(f'<text class="t-sm" x="46" y="{y + 20}">{label}</text>')
        o.append(f'<rect class="f4-bar" style="animation-delay:{0.15 * i:.2f}s;transform-origin:{x:.1f}px {y + 14}px" '
                 f'x="{x:.1f}" y="{y}" width="{w:.1f}" height="28" rx="7" fill="{col}" opacity="0.14"/>')
        o.append(f'<rect class="f4-bar" style="animation-delay:{0.15 * i:.2f}s;transform-origin:{x:.1f}px {y + 14}px" '
                 f'x="{x:.1f}" y="{y}" width="{w:.1f}" height="28" rx="7" fill="none" stroke="{col}" stroke-width="1.4"/>')
        o.append(f'<text class="t-key" x="{x + 12:.1f}" y="{y + 18}">M{a}–M{b}</text>')

    for m, row, label in marks:
        x = left + m * cw
        y = top + 6 + row * 46 + 14
        anchor, lx = ("end", x + 8) if m == 12 else ("middle", x)
        o.append(f'<path d="M{x:.1f},{y - 8} L{x + 8:.1f},{y} L{x:.1f},{y + 8} L{x - 8:.1f},{y} Z" '
                 f'fill="{INK}"/>')
        o.append(f'<text class="t-sm" x="{lx:.1f}" y="{y + 26}" text-anchor="{anchor}">{label}</text>')

    o.append(f'<line class="axis" x1="{left}" y1="248" x2="{right}" y2="248"/>')
    o.append(f'<text class="t-sm" x="{left}" y="272">start: February 2027</text>')
    o.append(f'<text class="t-sm" x="{right}" y="272" text-anchor="end">MS1 protocol · MS2 integrated system · MS3 validation</text>')
    o.append("</svg>")
    return "".join(o)


FIG1, FIG2, FIG3, FIG4 = figure1(), figure2(), figure3(), figure4()

# ---------------------------------------------------------------------------
# shell
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    ("index.html", "Overview"),
    ("protocol.html", "Protocol"),
    ("architecture.html", "Architecture"),
    ("adaptive.html", "Adaptive control"),
    ("plan.html", "Research plan"),
    ("team.html", "Team"),
]


def nav(page):
    links = "".join(
        f'<a href="{href}"{' class="on"' if href == page else ""}>{label}</a>'
        for href, label in NAV_ITEMS
    )
    return f"""<header class="nav">
  <div class="nav-in">
    <a class="brand" href="index.html">{LOGO}</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">Menu</button>
    <nav class="nav-links" id="nav-links">{links}</nav>
  </div>
</header>"""


FOOTER = f"""<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html">{LOGO_REVERSE}</a>
        <p class="small" style="margin-top:16px;max-width:36ch">{TAGLINE}</p>
        <p class="small" style="max-width:36ch">{INSTITUTION}.</p>
      </div>
      <div>
        <h4>Project</h4>
        <ul>
          <li><a href="index.html">Overview</a></li>
          <li><a href="protocol.html">Protocol</a></li>
          <li><a href="architecture.html">Architecture</a></li>
          <li><a href="adaptive.html">Adaptive control</a></li>
        </ul>
      </div>
      <div>
        <h4>Project</h4>
        <ul>
          <li><a href="plan.html">Research plan</a></li>
          <li><a href="plan.html#evaluation">Evaluation</a></li>
          <li><a href="team.html">Team</a></li>
          <li><a href="team.html#references">References</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:{CONTACT}">{CONTACT}</a></li>
          <li><a href="{GITHUB}">Source</a></li>
          <li><a href="team.html#position">Open position</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-note">
      <span>© 2026 CrowMQ. {INSTITUTION}.</span>
      <span class="mono">protocol specification in progress</span>
    </div>
  </div>
</footer>"""


SCRIPT = """<script>
(function () {
  var t = document.querySelector('.nav-toggle');
  var l = document.getElementById('nav-links');
  if (t && l) {
    t.addEventListener('click', function () {
      var open = l.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  document.querySelectorAll('.code').forEach(function (block) {
    var b = document.createElement('button');
    b.className = 'copy';
    b.type = 'button';
    b.textContent = 'copy';
    b.addEventListener('click', function () {
      navigator.clipboard.writeText(block.querySelector('pre').innerText).then(function () {
        b.textContent = 'copied';
        setTimeout(function () { b.textContent = 'copy'; }, 1600);
      });
    });
    block.appendChild(b);
  });
})();
</script>"""

SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<meta name="theme-color" content="#F2F3F5">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{{BASE}}/{{PAGE}}">
<meta property="og:type" content="website">
<meta property="og:title" content="{{TITLE}}">
<meta property="og:description" content="{{DESC}}">
<meta property="og:image" content="{{BASE}}/assets/img/og-image.png">
<meta property="og:url" content="{{BASE}}/{{PAGE}}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;display=swap" rel="stylesheet">
<style>
{{CSS}}
</style>
</head>
<body>
{{NAV}}
<main>
{{BODY}}
</main>
{{FOOTER}}
{{SCRIPT}}
</body>
</html>
"""

PAGES = [
    ("index.html", "CrowMQ — an intelligent messaging protocol for agentic systems",
     "CrowMQ makes the message broker an adaptive component of agentic AI communication: "
     "agent-aware message context, a bounded action space, and an Active Inference controller."),
    ("protocol.html", "Protocol — CrowMQ",
     "The CrowMQ publish–subscribe model: the message envelope, the bounded broker action space, "
     "delivery semantics, and how it sits alongside MQTT, AMQP, MCP and A2A."),
    ("architecture.html", "Architecture — CrowMQ",
     "Input interface, control plane, data plane and persistent storage, and the separation "
     "between the high-frequency message path and the adaptive control path."),
    ("adaptive.html", "Adaptive control — CrowMQ",
     "Active Inference in the broker: hidden communication states, Expected Free Energy policy "
     "selection, the quality–resource–cost equilibrium, and the Markov blanket boundary."),
    ("plan.html", "Research plan — CrowMQ",
     "A twelve-month plan: five goals, four technical tasks, three milestones, the evaluation "
     "design, and the project risk register."),
    ("team.html", "Team — CrowMQ",
     "The CrowMQ team at Stockholm University, scientific collaborators, computing "
     "infrastructure and references."),
    ("404.html", "Page not found — CrowMQ",
     "That page does not exist on the CrowMQ site."),
]


def build():
    css = (TOOLS / "site.css").read_text()
    art = {
        "{{LOGO}}": LOGO,
        "{{MARK}}": MARK,
        "{{TICK}}": TICK,
        "{{LIGATURE}}": LIGATURE,
        "{{FIG1}}": FIG1,
        "{{FIG2}}": FIG2,
        "{{FIG3}}": FIG3,
        "{{FIG4}}": FIG4,
        "{{GITHUB}}": GITHUB,
        "{{CONTACT}}": CONTACT,
        "{{INSTITUTION}}": INSTITUTION,
    }

    for page, title, desc in PAGES:
        html = SHELL
        html = html.replace("{{CSS}}", css)
        html = html.replace("{{NAV}}", nav(page))
        html = html.replace("{{FOOTER}}", FOOTER)
        html = html.replace("{{SCRIPT}}", SCRIPT)
        html = html.replace("{{BODY}}", (TOOLS / "pages" / page).read_text())
        html = html.replace("{{TITLE}}", title)
        html = html.replace("{{DESC}}", desc)
        html = html.replace("{{BASE}}", BASE_URL)
        html = html.replace("{{PAGE}}", page)
        for k, v in art.items():
            html = html.replace(k, v)
        leftover = set(re.findall(r"\{\{[A-Z_0-9]+\}\}", html))
        if leftover:
            raise SystemExit(f"{page}: unresolved placeholders {sorted(leftover)}")
        (ROOT / page).write_text(html)
        print(f"wrote {page} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    build()
