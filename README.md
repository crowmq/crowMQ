# CrowMQ website

The site for **CrowMQ: An Intelligent Messaging Protocol for Agentic Systems**, a
research project at the Department of Computer and Systems Sciences, Stockholm
University. Six pages, no framework, no build step required to deploy — every
page is self-contained HTML that GitHub Pages serves as-is.

```
index.html          Overview: the problem, what CrowMQ changes, goals
protocol.html       Message envelope, bounded action space, interoperability
architecture.html   Control plane, data plane, storage, path separation
adaptive.html       Active Inference, EFE, quality/resource/cost, Markov blanket
plan.html           Tasks, milestones, evaluation design, risks
team.html           People, collaborators, infrastructure, references
404.html            Not-found page
assets/img/         Logo files, favicon, social card, room for team photos
tools/              Source: stylesheet, page bodies, generators
```

## Publish it

All links are relative, so the site works at a domain root or in any
subdirectory.

**A. Its own repository.** Push this folder to a new repo, then open
*Settings → Pages* and set the source to *Deploy from a branch* → `main` →
`/ (root)`. It appears at `https://<username>.github.io/<repo>/`.

**B. A folder inside your existing user site.** If you already publish
`<username>.github.io`, copy this folder into that repo as e.g. `crowmq/`. It
goes live at `https://<username>.github.io/crowmq/` with nothing to configure.
Note that GitHub only uses `404.html` when it sits at the repository root.

For a custom domain, add a `CNAME` file at the repository root containing just
the hostname, and point a `CNAME` DNS record at `<username>.github.io`.

## Before you publish

- [ ] `tools/build.py` — set `GITHUB`, `BASE_URL` and `CONTACT` at the top.
      `CONTACT` is currently `your-email@dsv.su.se`. `BASE_URL` only affects the
      canonical and social-preview tags.
- [ ] `team.html` — confirm with Susanna Pirttikangas, Sasu Tarkoma and
      Schahram Dustdar that they are happy to be listed, before the site is
      public. Add photos by replacing the `<div class="avatar">…</div>` block
      with `<img class="avatar" src="assets/img/people/name.jpg" alt="">` and
      dropping a square image of 320 px or more into that folder.
- [ ] **Funding.** The site does not name a funder anywhere. Add that only once
      the outcome is known and you are permitted to announce it.
- [ ] **Licence.** The research plan keeps the exploitation pathway open —
      IP protection, open-source release or standardisation — so the site makes
      no licence claim. Once you decide, state it in the footer
      (`tools/build.py`) and add a `LICENSE` file. GitHub's *Add file → Create
      new file → LICENSE* picker inserts the full canonical text for you.
- [ ] `protocol.html` — the envelope field names and action names are indicative.
      Replace them with the specification once D1 lands at month 4.
- [ ] Search the built pages for `your-username` and confirm none are left.

Amber-bordered notes on the pages mark anything provisional. Delete each one as
you replace the content around it.

## Editing

```sh
python3 tools/build.py        # regenerate the pages
python3 tools/make-assets.py  # regenerate favicon, logo files, social card
```

| To change | Edit |
| --- | --- |
| Page content | `tools/pages/<page>.html` |
| Colours, type, spacing, animation | `tools/site.css` |
| Navigation, footer, metadata | `tools/build.py` |
| Logo geometry | `V`, `R`, `HEAD`, `CROWN`, `BILL`, `GAPE` in `tools/build.py` |
| Figures 1–4 | `figure1()` … `figure4()` in `tools/build.py` |
| Add a page | a file in `tools/pages/`, plus entries in `PAGES` and `NAV_ITEMS` |

`build.py` needs only the Python standard library and fails loudly if a
`{{PLACEHOLDER}}` is left unresolved. `make-assets.py` needs `cairosvg` for the
PNG social card (`pip install cairosvg`); the SVG assets are written without it.

Commit the generated `*.html` files — they are what gets served.

## Preview locally

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

## The logo

The wordmark is reconstructed from the brand source, so the ligature grid, node
size tiers, and the crow-head Q geometry match `crowmq-mark.svg` exactly. Two
things carried over from `crowmq-brand-notes.md`:

- **"Cro" is live text** set in IBM Plex Sans at weight 500, to match the note
  that the 1.9 ligature stroke is tuned to a 500-weight sans. Convert it to
  outlines, or reset it in the licensed face, before any production use outside
  the web.
- **The accent appears in exactly two places in the mark** — the crown plane and
  the iris. Elsewhere on the site the accent carries links, buttons and live
  paths in the figures; the mark itself is left alone.

`favicon.svg` is the crow head with the gape line and eye highlight removed, as
the notes require below 32 px. `favicon-dark.svg` is the reverse cut for dark
browser chrome; wire it up with a `prefers-color-scheme` media query if you want
it used.

## Figures

The four figures from the research plan are redrawn as inline SVG rather than
exported images, so they stay sharp, inherit the site palette, and carry text
descriptions for screen readers. Each has one animation that earns its place:

| Figure | Page | Animation |
| --- | --- | --- |
| 1 · memory growth vs GPU capacity | `index.html` | Fits draw in, then the gap between them fills |
| 2 · broker architecture | `architecture.html` | A message crosses the data plane; a control signal descends into the queues |
| 3 · observe–infer–evaluate–act | `adaptive.html` | A pulse travels the loop, passing behind each stage |
| 4 · implementation plan | `plan.html` | Task bars grow from their start month |

The hero graphic reuses the wordmark's own network ligature: channels light on
independent schedules, a packet crosses each one, and the endpoint nodes swell —
the same behaviour as `crowmq-wordmark-animated.gif`, rebuilt as SVG so it
scales and follows the theme. All motion is disabled under
`prefers-reduced-motion`.

## Design

See [DESIGN.md](DESIGN.md) for the palette, type scale and layout reasoning.
