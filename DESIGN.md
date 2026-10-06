# Design notes

A record of the decisions behind the site, so later edits stay consistent.

## Starting point

The brand already existed, so the site follows it rather than inventing a second
identity. Everything here comes from `crowmq-brand-notes.md` and the logo
source: the ink, the single accent, the counter, and the rule that the mark's
depth comes from flat overlapping shapes rather than gradients or shadows.

The page background is a very light grey rather than white. It lets white panels
sit on top as distinct surfaces, keeps the ink from vibrating against a pure
white field, and leaves the accent doing one job instead of two.

## Colour

| Token | Value | Use |
| --- | --- | --- |
| `--paper` | `#F2F3F5` | Page background |
| `--surface` | `#FFFFFF` | Panels, tables, alternating bands |
| `--ink` | `#12151C` | Text, dark bands, code blocks |
| `--ink-soft` | `#363C4B` | Lede paragraphs |
| `--muted` | `#646B7C` | Secondary text, captions, figure labels |
| `--line` | `#DCDFE6` | Every border and hairline |
| `--accent` | `#4F46E5` | Links, buttons, live paths in figures |
| `--halo` | `#818CF8` | The accent on dark surfaces, and secondary figure marks |
| `--wash` | `#EEEEFC` | Tinted panels, inline code, highlighted figure boxes |

`#4F46E5` does not carry enough contrast on near-black, so dark bands and the
footer switch to `#818CF8`, exactly as the brand notes specify for reverse use.

## Type

IBM Plex Sans throughout, IBM Plex Mono for figure labels, field names and code.
Plex is a deliberate choice rather than a default: it was drawn for technical
products, and the brand notes tune the ligature stroke to a 500-weight sans,
which Plex Sans Medium matches closely. Using one family in two widths keeps the
pages coherent without a second typeface competing with the mark.

Body text is 17 px at 1.62 line-height, capped at 70 characters. Headings are
600 weight with negative tracking that grows with size.

## Structure

- Left-aligned throughout, in a 1120 px column. No centred text blocks.
- Sections alternate between the grey page, white bands, and occasional ink
  bands. The alternation carries the rhythm, so content does not need to be
  chopped into identical cards.
- Feature blocks are led by a hairline rule rather than a bordered box. Borders
  are reserved for figures, tables and code, so a box means "this is a distinct
  artefact" rather than "this is a paragraph".
- Numbered markers appear only where the content is genuinely a sequence: the
  four stages of the control loop, and the four data-plane components.
- Each section heading is preceded by a small fragment of the wordmark's network
  ligature instead of an all-caps eyebrow label.

## Figures

Redrawn as inline SVG, not exported images, so they inherit the palette, stay
sharp at any size, and can be edited in `tools/build.py` with the rest of the
site. Coordinates are computed in Python where the figure has real data behind
it, so figure 1's fitted curves are the actual functions from the research plan
rather than a traced approximation.

Each figure carries a `role="img"` and an `aria-label` describing what it shows.
Labels inside an SVG are not a substitute for a description of the whole.

## Motion

One animation per figure, and one on the hero. Nothing fades in on scroll, and
nothing animates on hover. The hero reuses the behaviour of the brand's animated
wordmark: channels fire on independent schedules so several are usually live at
once, and none of it runs left to right, which is the point — the mark reads as
load distributed across devices rather than a pipeline.

Every animation is switched off under `prefers-reduced-motion`, with static
states chosen so the figures still read as complete compositions.

## Accessibility floor

Text meets WCAG AA against its background. Focus is visible on every interactive
element. The layout reflows to one column at 920 px and the navigation collapses
to a toggle. Tables scroll horizontally rather than forcing the page to.
