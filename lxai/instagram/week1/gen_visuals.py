#!/usr/bin/env python3
"""Regenerate the approved Week-1 draft visuals for @l.x.ai using the
approved LxAI Fuse brand kit (design/lxai-brand-kit).

Copy, layouts and canvas sizes stay exactly as approved in LXA-126
'week-1-drafts'. Only the identity changes: supplied logo artwork plus the
approved Fuse palette replace the placeholder wordmark and blue accent.

Brand rules applied (from design/lxai-brand-kit/docs/brand-guidelines.md):
  - logo artwork is used as supplied (never redrawn), scaled uniformly
  - colour logo on White/Paper, white logo on solid Violet, dark logo on Ink
  - body copy is Ink on light backgrounds; Violet is reserved for the logo
    and large headings (Violet-on-Paper is 4.194:1)
  - White-on-Violet stays at full opacity (4.509:1)
  - the supplied canvases carry their own clear space; no text is placed
    inside the logo area
"""
import os
from PIL import Image

SCRATCH = os.environ.get("PAPERCLIP_RUN_SCRATCH_DIR", "/tmp/opencode")
OUT = SCRATCH + "/visuals-brand"
BRAND = os.environ.get(
    "LXAI_BRANDKIT",
    "/home/x/work/startup/lxai/design/lxai-brand-kit/digital/png",
)
os.makedirs(OUT, exist_ok=True)

# ---- approved Fuse palette -------------------------------------------------
PAPER = (247, 246, 251)   # #F7F6FB
INK = (24, 21, 34)        # #181522
VIOLET = (109, 94, 252)   # #6D5EFC
LILAC = (169, 154, 255)   # #A99AFF
LILAC_SOFT = (231, 228, 254)  # tint of Dark Lilac for quiet option fields
WHITE = (255, 255, 255)
MUTED = (105, 101, 122)   # quiet label grey derived from Ink
LINE_SOFT = (226, 224, 238)
PANEL_EDGE = LILAC

try:
    from PIL import ImageDraw, ImageFont
    BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
except ImportError:  # pragma: no cover
    raise

def F(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)

LOGOS = {
    "color": BRAND + "/lxai-horizontal-color-2048.png",
    "white": BRAND + "/lxai-horizontal-white-2048.png",
    "dark": BRAND + "/lxai-horizontal-dark-2048.png",
}
LOGO_RATIO = 2048 / 1008.0

def paste_logo(img, variant, width, cx, cy):
    """Place supplied horizontal logo, centred on (cx, cy), at `width` px."""
    logo = Image.open(LOGOS[variant]).convert("RGBA")
    h = int(round(width / LOGO_RATIO))
    logo = logo.resize((int(width), h), Image.LANCZOS)
    x = int(cx - width / 2)
    y = int(cy - h / 2)
    img.alpha_composite(logo, (x, y))
    return y + h

# ---- text helpers ----------------------------------------------------------
def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_lines(draw, lines, font, cx, y, fill, line_gap=1.25):
    for ln in lines:
        w = draw.textlength(ln, font=font)
        draw.text((cx - w / 2, y), ln, font=font, fill=fill)
        y += int(font.size * line_gap)
    return y

def centered_block(draw, text, font, cx, cy, max_w, fill, line_gap=1.25):
    lines = wrap(draw, text, font, max_w)
    total = int(font.size * line_gap * len(lines))
    return draw_lines(draw, lines, font, cx, cy - total / 2, fill, line_gap)

def canvas(w, h, bg):
    return Image.new("RGBA", (w, h), bg + (255,))

def save(img, name):
    rgb = img.convert("RGB")
    p = f"{OUT}/{name}"
    rgb.save(p, "PNG")
    print("wrote", p, rgb.size)

# ---------------------------------------------------------------- Mon hero
def mon_hero():
    img = canvas(1080, 1350, PAPER)
    d = ImageDraw.Draw(img)
    eb = F(34, False)
    t = "YOUR AI INTEGRATOR"
    w = d.textlength(t, font=eb)
    d.text(((1080 - w) / 2, 320), t, font=eb, fill=MUTED)
    paste_logo(img, "color", 620, 540, 540)
    ol = F(60)
    lines = wrap(d, "We connect your tools so you don't have to.", ol, 880)
    yb = 1350 - 170 - int(ol.size * 1.3 * len(lines))
    draw_lines(d, lines, ol, 540, yb, INK, 1.3)
    yend = yb + int(ol.size * 1.3 * len(lines)) + 26
    d.rectangle([540 - 60, yend, 540 + 60, yend + 12], fill=VIOLET)
    save(img, "w1-mon-hero-1080x1350.png")

# ---------------------------------------------------------- Tue carousel
SLIDES = [
    ("5 signs your team is drowning in copy-paste between apps", None),
    ("The same data lives in 3 places - and none of them match.", "1"),
    ("A 'quick question' takes 20 minutes of tab-switching to answer.", "2"),
    ("Someone's real job is quietly becoming 'moving data between apps.'", "3"),
    ("You built a spreadsheet to track your spreadsheets.", "4"),
    ("Every new tool gets bought... then abandoned. 'The old way was easier.'", "5"),
    ("Nodded at one?\nSave this post", "cta"),
]

def tue_carousel():
    for i, (text, tag) in enumerate(SLIDES, 1):
        cta = tag == "cta"
        img = canvas(1080, 1080, VIOLET if cta else PAPER)
        d = ImageDraw.Draw(img)
        if cta:
            body = F(88)
            lines = []
            for part in text.split("\n"):
                lines += wrap(d, part, body, 860)
            y = 500 - int(body.size * 1.3 * len(lines) / 2)
            draw_lines(d, lines, body, 540, y, WHITE, 1.3)
            paste_logo(img, "white", 240, 540, 940)
        else:
            if tag:
                nf = F(150)
                d.text((80, 56), tag, font=nf, fill=LILAC_SOFT if False else LILAC)
            body = F(72)
            centered_block(d, text, body, 540, 560, 880, INK, 1.35)
            cf = F(30, False)
            d.text((80, 1080 - 84), f"{i} / 7", font=cf, fill=MUTED)
            paste_logo(img, "color", 180, 1080 - 80 - 90, 1080 - 84 + 8)
        save(img, f"w1-tue-slide-{i:02d}-1080x1080.png")

# -------------------------------------------------------------- Sat meme
def sat_meme():
    img = canvas(1080, 1080, PAPER)
    d = ImageDraw.Draw(img)
    m = 40
    pw = (1080 - 3 * m) // 2
    ph = 730
    # panel 1: tired person at desk
    x1 = m
    d.rounded_rectangle([x1, m, x1 + pw, m + ph], 28, fill=WHITE,
                        outline=PANEL_EDGE, width=3)
    cx = x1 + pw / 2
    d.rectangle([x1 + 60, m + ph - 190, x1 + pw - 60, m + ph - 172], fill=LILAC_SOFT)
    d.rectangle([x1 + 90, m + ph - 172, x1 + 112, m + ph - 60], fill=LILAC_SOFT)
    d.rectangle([x1 + pw - 112, m + ph - 172, x1 + pw - 90, m + ph - 60], fill=LILAC_SOFT)
    d.rounded_rectangle([x1 + pw / 2 - 110, m + ph - 310, x1 + pw / 2 + 110,
                         m + ph - 190], 10, fill=LILAC_SOFT, outline=LILAC, width=3)
    hx, hy, hr = cx, m + 230, 92
    d.rounded_rectangle([hx - 70, hy + hr - 10, hx + 70, hy + hr + 150], 30, fill=LILAC)
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=WHITE, outline=INK, width=4)
    d.line([hx - 46, hy - 16, hx - 16, hy - 16], fill=INK, width=6)
    d.line([hx + 16, hy - 16, hx + 46, hy - 16], fill=INK, width=6)
    d.ellipse([hx - 40, hy - 14, hx - 22, hy + 2], fill=INK)
    d.ellipse([hx + 22, hy - 14, hx + 40, hy + 2], fill=INK)
    d.line([hx - 30, hy + 48, hx + 30, hy + 48], fill=INK, width=6)
    d.polygon([(hx + 70, hy - 70), (hx + 58, hy - 40), (hx + 82, hy - 40)], fill=LILAC)
    cap1 = F(36)
    lines = wrap(d, "me, moving data between apps by hand (47th time this week)", cap1, pw - 60)
    draw_lines(d, lines, cap1, cx, m + ph + 30, INK, 1.3)
    # panel 2: shiny unused automation button
    x2 = 2 * m + pw
    d.rounded_rectangle([x2, m, x2 + pw, m + ph], 28, fill=WHITE,
                        outline=PANEL_EDGE, width=3)
    cx2 = x2 + pw / 2
    br = 185
    by = m + 320
    for r in (br + 46, br + 78):
        d.arc([cx2 - r, by - r, cx2 + r, by + r], 200, 340, fill=LILAC_SOFT, width=5)
    d.ellipse([cx2 - br, by - br, cx2 + br, by + br], fill=VIOLET)
    d.ellipse([cx2 - br + 26, by - br + 26, cx2 + br - 26, by + br - 26],
              outline=WHITE, width=5)
    bl = F(44)
    t = "automation"
    w = d.textlength(t, font=bl)
    d.text((cx2 - w / 2, by - 34), t, font=bl, fill=WHITE)
    d.ellipse([cx2 - br - 30, by + br - 16, cx2 - 40, by + br + 18], fill=LILAC_SOFT)
    d.ellipse([cx2 + 20, by + br - 10, cx2 + br + 26, by + br + 20], fill=LILAC_SOFT)
    cap2 = F(36)
    lines = wrap(d, "the button that's been there the whole time", cap2, pw - 60)
    draw_lines(d, lines, cap2, cx2, m + ph + 30, INK, 1.3)
    paste_logo(img, "color", 180, 540, 1080 - 56)
    save(img, "w1-sat-meme-1080x1080.png")

# ----------------------------------------------------------- Sun story
def sun_story():
    img = canvas(1080, 1920, VIOLET)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([70, 330, 1010, 1590], 48, fill=WHITE)
    paste_logo(img, "white", 240, 540, 180)
    q = F(76)
    centered_block(d, "Which app do you open first every morning?", q, 540, 560, 800, INK, 1.3)
    opts = ["Email", "Chat (Slack / Teams...)", "Calendar", "Coffee first"]
    y = 830
    for o in opts:
        of = F(58)
        while d.textlength(o, font=of) > 720 - 48:  # keep 24px padding in pill
            of = F(of.size - 2)
        d.rounded_rectangle([180, y, 900, y + 120], 24, fill=LILAC_SOFT)
        w = d.textlength(o, font=of)
        d.text(((1080 - w) / 2, y + (120 - of.size) / 2 - 4), o, font=of, fill=INK)
        y += 150
    hint = F(36, False)
    t = "Results land in Monday's post"
    w = d.textlength(t, font=hint)
    d.text(((1080 - w) / 2, 1660), t, font=hint, fill=WHITE)
    save(img, "w1-sun-story-1080x1920.png")

# ------------------------------------------------- Wed fallback diagram
def wed_diagram():
    img = canvas(1080, 1080, PAPER)
    d = ImageDraw.Draw(img)
    t = F(54)
    s = "How every integration starts"
    w = d.textlength(s, font=t)
    d.text(((1080 - w) / 2, 130), s, font=t, fill=INK)
    steps = [("Map", "where data lives now,\nand where it needs to go"),
             ("Build", "connect the steps,\none at a time"),
             ("Test", "prove it works\nbefore it ships")]
    bw, bh = 260, 300
    gap = (1080 - 3 * bw - 160) / 2
    y = 380
    for i, (title, sub) in enumerate(steps):
        x = 80 + i * (bw + gap)
        d.rounded_rectangle([x, y, x + bw, y + bh], 28, fill=WHITE,
                            outline=VIOLET, width=4)
        tf = F(56)
        w = d.textlength(title, font=tf)
        d.text((x + (bw - w) / 2, y + 46), title, font=tf, fill=VIOLET)
        sf = F(27, False)
        lines = []
        for part in sub.split("\n"):
            lines += wrap(d, part, sf, bw - 44)
        draw_lines(d, lines, sf, x + bw / 2, y + 140, INK, 1.3)
        if i < 2:
            ax = x + bw + gap / 2
            d.line([ax - 26, y + bh / 2, ax + 26, y + bh / 2], fill=MUTED, width=8)
            d.polygon([(ax + 26, y + bh / 2 - 18), (ax + 26, y + bh / 2 + 18),
                       (ax + 48, y + bh / 2)], fill=MUTED)
    paste_logo(img, "color", 180, 540, 1080 - 84)
    save(img, "w1-wed-diagram-fallback-1080x1080.png")

# ------------------------------------------------- Fri fallback card
def fri_card():
    img = canvas(1080, 1080, PAPER)
    d = ImageDraw.Draw(img)
    t = F(72)
    centered_block(d, "Happy Friday!", t, 540, 330, 900, VIOLET, 1.3)
    q = F(64)
    centered_block(d, "What's one small thing you automated this week - or wish you had?",
                   q, 540, 560, 880, INK, 1.35)
    s = F(48, False)
    centered_block(d, "Brag below. No automation is too small.", s, 540, 800, 800, MUTED, 1.35)
    paste_logo(img, "color", 180, 540, 1080 - 84)
    save(img, "w1-fri-fallback-1080x1080.png")

mon_hero()
tue_carousel()
sat_meme()
sun_story()
wed_diagram()
fri_card()
print("ALL DONE ->", OUT)
