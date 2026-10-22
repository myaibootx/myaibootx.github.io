#!/usr/bin/env python3
"""Regenerate the approved Week-2 draft visuals for @l.x.ai using the
approved LxAI Fuse brand kit (design/lxai-brand-kit).

Copy, layouts and canvas sizes stay exactly as approved in LXA-126
'week-2-drafts' (board-approved batch, card 6e53a0b0, 2026-10-22). The
layouts extend the Week-1 slide system (../week1/gen_visuals.py) and the
design/instagram template pack: violet cover + Ink-on-Paper body + violet
CTA carousel structure, square-layout extension for the single cards, and
the story layout band rules.

Brand rules applied (from design/lxai-brand-kit/docs/brand-guidelines.md):
  - logo artwork is used as supplied (never redrawn), scaled uniformly
  - colour logo on Paper, white logo on solid Violet, dark variant on Ink
  - body copy is Ink on light backgrounds; White-on-Violet full opacity
  - no text is placed inside the logo area; story content stays inside the
    central band with 200+ px reserved at the top and bottom
Emoji note: DejaVu Sans cannot render colour emoji (they rasterise as
.notdef boxes), so approved slide copy renders without its trailing emoji
glyph; the full approved text including emoji lives in captions.md and the
'week-2-drafts' document.
"""
import os
from PIL import Image

SCRATCH = os.environ.get("PAPERCLIP_RUN_SCRATCH_DIR", "/tmp/opencode")
OUT = os.path.dirname(os.path.abspath(__file__))
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

from PIL import ImageDraw, ImageFont
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


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
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
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


def autosize(draw, text, start, max_w, max_lines, min_size):
    """Largest size <= start that wraps to <= max_lines at max_w."""
    size = start
    while size > min_size:
        f = F(size)
        if len(wrap(draw, text, f, max_w)) <= max_lines:
            return f
        size -= 2
    return F(min_size)


def canvas(w, h, bg):
    return Image.new("RGBA", (w, h), bg + (255,))


def save(img, name):
    rgb = img.convert("RGB")
    p = f"{OUT}/{name}"
    rgb.save(p, "PNG")
    print("wrote", p, rgb.size)


# ---- Thu carousel: "What an API is - in plain words" (7 slides) ------------
SLIDES = [
    ("What an API is - in plain words", "cover"),
    ("Picture a menu at a restaurant. You order from it; the kitchen does the work.", "body"),
    ("An API is that menu for software. One app asks another app for something, and gets an answer back.", "body"),
    ("No jargon needed: request in, answer out. That's the whole trick.", "body"),
    ("Every time an app shows you data from somewhere else - weather, maps, payments - an API carried it.", "body"),
    ("So 'connecting your tools' means letting them order from each other's menus instead of you copy-pasting.", "body"),
    ("Clearer now? Save this post", "cta"),  # approved copy ends with a pin emoji; DejaVu cannot render it
]


def thu_carousel():
    total = len(SLIDES)
    for i, (text, kind) in enumerate(SLIDES, 1):
        counter = f"{i} / {total}"
        if kind == "cover":
            img = canvas(1080, 1080, VIOLET)
            d = ImageDraw.Draw(img)
            f = autosize(d, text, 80, 860, 4, 56)
            draw_lines(d, wrap(d, text, f, 860), f, 540, 560 - f.size, WHITE, 1.3)
            cf = F(30, False)
            d.text((80, 1080 - 84), counter, font=cf, fill=WHITE)
            paste_logo(img, "white", 180, 1080 - 80 - 90, 1080 - 84 + 8)
        elif kind == "body":
            img = canvas(1080, 1080, PAPER)
            d = ImageDraw.Draw(img)
            f = autosize(d, text, 72, 880, 5, 56)
            centered_block(d, text, f, 540, 560, 880, INK, 1.35)
            cf = F(30, False)
            d.text((80, 1080 - 84), counter, font=cf, fill=MUTED)
            paste_logo(img, "color", 180, 1080 - 80 - 90, 1080 - 84 + 8)
        else:  # cta
            img = canvas(1080, 1080, VIOLET)
            d = ImageDraw.Draw(img)
            body = F(80)
            lines = []
            for part in text.split("\n"):
                lines += wrap(d, part, body, 860)
            y = 500 - int(body.size * 1.3 * len(lines) / 2)
            draw_lines(d, lines, body, 540, y, WHITE, 1.3)
            paste_logo(img, "white", 240, 540, 940)
        save(img, f"w2-thu-carousel-slide-{i:02d}-1080x1080.png")


# ------------------------------------------------------- Fri BTS timeline
def fri_timeline():
    img = canvas(1080, 1080, PAPER)
    d = ImageDraw.Draw(img)
    t = F(52)
    s = "From ticket to shipped, in a day"
    w = d.textlength(s, font=t)
    d.text(((1080 - w) / 2, 120), s, font=t, fill=INK)
    steps = [("01", "Ticket", "read it twice"),
             ("02", "Map", "every step first"),
             ("03", "Build", "one step at a time"),
             ("04", "Test", "the 5 pm test"),
             ("05", "Ship", "then ship")]
    n = len(steps)
    margin, gap = 56, 26
    bw = (1080 - 2 * margin - (n - 1) * gap) // n
    bh, y = 300, 380
    for i, (num, title, sub) in enumerate(steps):
        x = margin + i * (bw + gap)
        d.rounded_rectangle([x, y, x + bw, y + bh], 24, fill=WHITE,
                            outline=VIOLET, width=4)
        nf = F(24, False)
        w = d.textlength(num, font=nf)
        d.text((x + (bw - w) / 2, y + 30), num, font=nf, fill=LILAC)
        tf = F(38)
        w = d.textlength(title, font=tf)
        d.text((x + (bw - w) / 2, y + 82), title, font=tf, fill=VIOLET)
        sf = F(22, False)
        lines = wrap(d, sub, sf, bw - 32)
        draw_lines(d, lines, sf, x + bw / 2, y + 160, INK, 1.3)
        if i < n - 1:
            ax = x + bw + gap / 2
            d.line([ax - 14, y + bh / 2, ax + 14, y + bh / 2], fill=MUTED, width=6)
            d.polygon([(ax + 14, y + bh / 2 - 13), (ax + 14, y + bh / 2 + 13),
                       (ax + 32, y + bh / 2)], fill=MUTED)
    c = F(32, False)
    s = "No magic - just a boring, repeatable day."
    w = d.textlength(s, font=c)
    d.text(((1080 - w) / 2, 770), s, font=c, fill=MUTED)
    paste_logo(img, "color", 180, 540, 1080 - 84)
    save(img, "w2-fri-timeline-1080x1080.png")


# ---------------------------------------------------------- Sat ask-us card
def sat_ask():
    img = canvas(1080, 1080, PAPER)
    d = ImageDraw.Draw(img)
    t = F(92)
    centered_block(d, "Ask us anything", t, 540, 330, 900, INK, 1.3)
    q = F(40)
    centered_block(d, "Automation, integrations, \"is my spreadsheet situation fixable\" - all fair game.",
                   q, 540, 560, 860, INK, 1.35)
    s = F(36, False)
    centered_block(d, "No tricks, just answers.", s, 540, 780, 800, MUTED, 1.35)
    paste_logo(img, "color", 180, 540, 1080 - 84)
    save(img, "w2-sat-ask-1080x1080.png")


# ------------------------------------------------- Sun story: week-one recap
def sun_story():
    img = canvas(1080, 1920, VIOLET)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([70, 330, 1010, 1310], 48, fill=WHITE)
    paste_logo(img, "white", 240, 540, 180)
    h = F(64)
    lines = wrap(d, "One week in - thank you", h, 800)
    y = draw_lines(d, lines, h, 540, 460, INK, 1.3)
    p1 = F(36, False)
    y = draw_lines(d, wrap(d, "From \"what do you even do?\" to \"what's an API, in plain words\" - you showed up for all of it.",
                           p1, 840), p1, 540, y + 60, INK, 1.35)
    p2 = F(36, False)
    y = draw_lines(d, wrap(d, "This week ahead: more plain-words guides, and a direct way to talk to us.",
                           p2, 840), p2, 540, y + 70, INK, 1.35)
    p3 = F(36, False)
    draw_lines(d, wrap(d, "Follow along so you don't miss it", p3, 840), p3,
               540, y + 80, MUTED, 1.35)
    save(img, "w2-sun-story-1080x1920.png")


# ------------------------------------- Mon fallback: start with one workflow
def mon_fallback():
    img = canvas(1080, 1080, PAPER)
    d = ImageDraw.Draw(img)
    t = F(64)
    centered_block(d, "Start smaller than you think.", t, 540, 230, 880, VIOLET, 1.3)
    b = autosize(d, "The best first automation isn't the fancy one - it's the repeated task with clear inputs and a result you can check.",
                 38, 840, 4, 30)
    centered_block(d, "The best first automation isn't the fancy one - it's the repeated task with clear inputs and a result you can check.",
                   b, 540, 420, 840, INK, 1.35)
    y = 590
    for i, label in enumerate(["Sort requests", "Find information", "Prepare drafts"]):
        d.rounded_rectangle([72, y, 1008, y + 64], 18, fill=LILAC_SOFT)
        rf = F(28, False)
        d.text((104, y + 16), f"0{i + 1}   {label}", font=rf, fill=INK)
        y += 80
    c = F(30, False)
    centered_block(d, "Which repeated task would you hand over first?", c, 540, 880, 840, MUTED, 1.35)
    paste_logo(img, "color", 180, 540, 1080 - 84)
    save(img, "w2-mon-fallback-1080x1080.png")


# ------------------------------- Tue fallback: keep a human in the loop (dark)
def tue_fallback():
    img = canvas(1080, 1080, INK)
    d = ImageDraw.Draw(img)
    t = F(64)
    centered_block(d, "Keep a human in the loop.", t, 540, 260, 880, PAPER, 1.3)
    b = F(38)
    centered_block(d, "Build it, test it, review the output together - then let it run.",
                   b, 540, 450, 840, PAPER, 1.35)
    a = F(36)
    centered_block(d, "Expanding fast feels good; working reliably feels better.",
                   a, 540, 640, 840, LILAC, 1.35)
    c = F(34, False)
    centered_block(d, "Where would you want a human to have the final say?",
                   c, 540, 780, 840, PAPER, 1.35)
    paste_logo(img, "dark", 180, 540, 1080 - 84)
    save(img, "w2-tue-fallback-1080x1080.png")


# ------------------------------------------------- Wed offer: intro call (violet)
def wed_offer():
    img = canvas(1080, 1080, VIOLET)
    d = ImageDraw.Draw(img)
    paste_logo(img, "white", 260, 540, 220)
    t = F(72)
    centered_block(d, "Book a free intro call", t, 540, 430, 880, WHITE, 1.3)
    b = autosize(d, "No pitch, no pressure. We'll look at one workflow you'd love to fix and tell you straight whether connecting your tools would help.",
                 36, 820, 5, 28)
    centered_block(d, "No pitch, no pressure. We'll look at one workflow you'd love to fix and tell you straight whether connecting your tools would help.",
                   b, 540, 650, 820, WHITE, 1.35)
    c = F(40)
    centered_block(d, "Comment or DM us \"call\"", c, 540, 930, 820, WHITE, 1.3)
    save(img, "w2-wed-offer-1080x1080.png")


thu_carousel()
fri_timeline()
sat_ask()
sun_story()
mon_fallback()
tue_fallback()
wed_offer()
print("ALL DONE ->", OUT)
