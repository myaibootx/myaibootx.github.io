#!/usr/bin/env python3
"""Generate Week-1 draft visual assets for @l.x.ai per the approved specs
in LXA-126 'week-1-drafts' document. Drafts for board review only."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.environ.get("PAPERCLIP_RUN_SCRATCH_DIR", "/tmp/opencode") + "/visuals"
os.makedirs(OUT, exist_ok=True)

BG = (246, 241, 233)        # warm off-white
INK = (28, 28, 40)          # near-black ink
MUTED = (107, 107, 123)
ACCENT = (47, 107, 255)     # electric blue
ACCENT_SOFT = (230, 237, 255)
PANEL = (255, 252, 247)

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
if not os.path.exists(BOLD):
    BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def F(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)

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

def draw_lines(draw, lines, font, cx, y, fill, line_gap=1.25, anchor_center=True):
    for ln in lines:
        w = draw.textlength(ln, font=font)
        x = cx - w/2 if anchor_center else cx
        draw.text((x, y), ln, font=font, fill=fill)
        y += int(font.size * line_gap)
    return y

def centered_block(draw, text, font, cx, cy, max_w, fill, line_gap=1.25):
    lines = wrap(draw, text, font, max_w)
    total = int(font.size * line_gap * len(lines))
    return draw_lines(draw, lines, font, cx, cy - total/2, fill, line_gap)

def save(img, name):
    p = f"{OUT}/{name}"
    img.save(p, "PNG")
    print("wrote", p, img.size)

# ---------------------------------------------------------------- Mon hero
def mon_hero():
    img = Image.new("RGB", (1080, 1350), BG)
    d = ImageDraw.Draw(img)
    # top: small eyebrow
    eb = F(34, False)
    t = "YOUR AI INTEGRATOR"
    w = d.textlength(t, font=eb)
    d.text(((1080-w)/2, 300), t, font=eb, fill=MUTED)
    # wordmark centered with bolt mark
    wm = F(190)
    t = "LxAI"
    w = d.textlength(t, font=wm)
    mark = 130
    total = w + 34 + mark
    x = (1080 - total)/2
    y = 430
    # lightning bolt (polygon) in accent
    bx = x + w + 34
    by = y + 30
    pts = [(bx+55,by), (bx+8,by+120), (bx+58,by+120), (bx+28,by+215), (bx+112,by+88), (bx+62,by+88), (bx+100,by)]
    d.polygon(pts, fill=ACCENT)
    d.text((x, y), t, font=wm, fill=INK)
    # bottom one-liner
    ol = F(64)
    lines = wrap(d, "We connect your tools so you don't have to.", ol, 880)
    yb = 1350 - 140 - int(ol.size*1.3*len(lines))
    draw_lines(d, lines, ol, 540, yb, INK, 1.3)
    # accent bar under it
    d.rectangle([540-60, yb + int(ol.size*1.3*len(lines)) + 26, 540+60, yb + int(ol.size*1.3*len(lines)) + 38], fill=ACCENT)
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
        img = Image.new("RGB", (1080, 1080), ACCENT if cta else BG)
        d = ImageDraw.Draw(img)
        if cta:
            body = F(88)
            lines = []
            for part in text.split("\n"):
                lines += wrap(d, part, body, 860)
            y = 540 - int(body.size*1.3*len(lines)/2)
            draw_lines(d, lines, body, 540, y, (255,255,255), 1.3)
            small = F(40, False)
            t = "LxAI"
            w = d.textlength(t, font=small)
            d.text(((1080-w)/2, 1080-110), t, font=small, fill=(255,255,255))
        else:
            if tag:
                nf = F(150)
                d.text((80, 64), tag, font=nf, fill=ACCENT_SOFT if False else (203, 213, 245))
            body = F(72)
            centered_block(d, text, body, 540, 560, 880, INK, 1.35)
            # slide counter + brand
            cf = F(30, False)
            cnt = f"{i} / 7"
            d.text((80, 1080-90), cnt, font=cf, fill=MUTED)
            t = "LxAI"
            w = d.textlength(t, font=cf)
            d.text((1080-80-w, 1080-90), t, font=cf, fill=MUTED)
        save(img, f"w1-tue-slide-{i:02d}-1080x1080.png")

# -------------------------------------------------------------- Sat meme
def sat_meme():
    img = Image.new("RGB", (1080, 1080), BG)
    d = ImageDraw.Draw(img)
    m = 40
    pw = (1080 - 3*m) // 2
    ph = 730
    # panel 1: tired person at desk
    x1 = m
    d.rounded_rectangle([x1, m, x1+pw, m+ph], 28, fill=PANEL, outline=(226, 219, 206), width=3)
    cx = x1 + pw/2
    # desk
    d.rectangle([x1+60, m+ph-190, x1+pw-60, m+ph-172], fill=(196, 186, 168))
    d.rectangle([x1+90, m+ph-172, x1+112, m+ph-60], fill=(196, 186, 168))
    d.rectangle([x1+pw-112, m+ph-172, x1+pw-90, m+ph-60], fill=(196, 186, 168))
    # laptop
    d.rounded_rectangle([x1+pw/2-110, m+ph-310, x1+pw/2+110, m+ph-190], 10, fill=(214, 220, 232), outline=(150,158,175), width=3)
    # head
    hx, hy, hr = cx, m+230, 92
    # body (torso)
    d.rounded_rectangle([hx-70, hy+hr-10, hx+70, hy+hr+150], 30, fill=(158, 180, 214))
    d.ellipse([hx-hr, hy-hr, hx+hr, hy+hr], fill=(250, 226, 200), outline=(60,60,70), width=4)
    # tired eyes: half-lidded
    d.line([hx-46, hy-16, hx-16, hy-16], fill=(60,60,70), width=6)
    d.line([hx+16, hy-16, hx+46, hy-16], fill=(60,60,70), width=6)
    d.ellipse([hx-40, hy-14, hx-22, hy+2], fill=(60,60,70))
    d.ellipse([hx+22, hy-14, hx+40, hy+2], fill=(60,60,70))
    # flat mouth + sweat drop
    d.line([hx-30, hy+48, hx+30, hy+48], fill=(60,60,70), width=6)
    d.polygon([(hx+70, hy-70), (hx+58, hy-40), (hx+82, hy-40)], fill=(120, 170, 240))
    cap1 = F(36)
    lines = wrap(d, "me, moving data between apps by hand (47th time this week)", cap1, pw-60)
    draw_lines(d, lines, cap1, cx, m+ph+30, INK, 1.3)
    # panel 2: shiny unused automation button
    x2 = 2*m + pw
    d.rounded_rectangle([x2, m, x2+pw, m+ph], 28, fill=PANEL, outline=(226, 219, 206), width=3)
    cx2 = x2 + pw/2
    br = 185
    by = m + 320
    # dust arcs
    for r in (br+46, br+78):
        d.arc([cx2-r, by-r, cx2+r, by+r], 200, 340, fill=(200, 192, 176), width=5)
    d.ellipse([cx2-br, by-br, cx2+br, by+br], fill=ACCENT)
    d.ellipse([cx2-br+26, by-br+26, cx2+br-26, by+br-26], outline=(255,255,255), width=5)
    bl = F(44)
    t = "automation"
    w = d.textlength(t, font=bl)
    d.text((cx2-w/2, by-34), t, font=bl, fill=(255,255,255))
    # dust pile
    d.ellipse([cx2-br-30, by+br-16, cx2-40, by+br+18], fill=(222, 214, 198))
    d.ellipse([cx2+20, by+br-10, cx2+br+26, by+br+20], fill=(222, 214, 198))
    cap2 = F(36)
    lines = wrap(d, "the button that's been there the whole time", cap2, pw-60)
    draw_lines(d, lines, cap2, cx2, m+ph+30, INK, 1.3)
    # brand strip
    bf = F(30, False)
    t = "LxAI"
    w = d.textlength(t, font=bf)
    d.text(((1080-w)/2, 1080-64), t, font=bf, fill=MUTED)
    save(img, "w1-sat-meme-1080x1080.png")

# ----------------------------------------------------------- Sun story
def sun_story():
    img = Image.new("RGB", (1080, 1920), ACCENT)
    d = ImageDraw.Draw(img)
    # soft card
    d.rounded_rectangle([70, 330, 1010, 1590], 48, fill=(255, 255, 255))
    t = "LxAI"
    bf = F(44)
    w = d.textlength(t, font=bf)
    d.text(((1080-w)/2, 170), t, font=bf, fill=(255,255,255))
    q = F(76)
    centered_block(d, "Which app do you open first every morning?", q, 540, 560, 800, INK, 1.3)
    opts = ["Email", "Chat (Slack / Teams...)", "Calendar", "Coffee first"]
    of = F(58)
    y = 830
    for o in opts:
        d.rounded_rectangle([180, y, 900, y+120], 24, fill=ACCENT_SOFT)
        w = d.textlength(o, font=of)
        d.text(((1080-w)/2, y+28), o, font=of, fill=INK)
        y += 150
    hint = F(36, False)
    t = "Results land in Monday's post"
    w = d.textlength(t, font=hint)
    d.text(((1080-w)/2, 1660), t, font=hint, fill=(255,255,255))
    save(img, "w1-sun-story-1080x1920.png")

# ------------------------------------------------- Wed fallback diagram
def wed_diagram():
    img = Image.new("RGB", (1080, 1080), BG)
    d = ImageDraw.Draw(img)
    t = F(54)
    s = "How every integration starts"
    w = d.textlength(s, font=t)
    d.text(((1080-w)/2, 130), s, font=t, fill=INK)
    steps = [("Map", "where data lives now,\nand where it needs to go"),
             ("Build", "connect the steps,\none at a time"),
             ("Test", "prove it works\nbefore it ships")]
    bw, bh = 260, 300
    gap = (1080 - 3*bw - 160) / 2
    y = 380
    for i, (title, sub) in enumerate(steps):
        x = 80 + i*(bw+gap)
        d.rounded_rectangle([x, y, x+bw, y+bh], 28, fill=PANEL, outline=ACCENT, width=4)
        tf = F(56)
        w = d.textlength(title, font=tf)
        d.text((x+(bw-w)/2, y+46), title, font=tf, fill=ACCENT)
        sf = F(27, False)
        lines = []
        for part in sub.split("\n"):
            lines += wrap(d, part, sf, bw-44)
        draw_lines(d, lines, sf, x+bw/2, y+140, INK, 1.3)
        if i < 2:
            ax = x + bw + gap/2
            d.line([ax-26, y+bh/2, ax+26, y+bh/2], fill=MUTED, width=8)
            d.polygon([(ax+26, y+bh/2-18), (ax+26, y+bh/2+18), (ax+48, y+bh/2)], fill=MUTED)
    cf = F(30, False)
    t = "LxAI"
    w = d.textlength(t, font=cf)
    d.text(((1080-w)/2, 1080-90), t, font=cf, fill=MUTED)
    save(img, "w1-wed-diagram-fallback-1080x1080.png")

# ------------------------------------------------- Fri fallback card
def fri_card():
    img = Image.new("RGB", (1080, 1080), BG)
    d = ImageDraw.Draw(img)
    t = F(72)
    centered_block(d, "Happy Friday!", t, 540, 330, 900, ACCENT, 1.3)
    q = F(64)
    centered_block(d, "What's one small thing you automated this week - or wish you had?", q, 540, 560, 880, INK, 1.35)
    s = F(48, False)
    centered_block(d, "Brag below. No automation is too small.", s, 540, 800, 800, MUTED, 1.35)
    cf = F(30, False)
    t = "LxAI"
    w = d.textlength(t, font=cf)
    d.text(((1080-w)/2, 1080-90), t, font=cf, fill=MUTED)
    save(img, "w1-fri-fallback-1080x1080.png")

mon_hero()
tue_carousel()
sat_meme()
sun_story()
wed_diagram()
fri_card()
print("ALL DONE ->", OUT)
