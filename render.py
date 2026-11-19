#!/usr/bin/env python3
"""Render the 1024x1024 newspaper front page for 18 November 2026.
All art is drawn programmatically with Pillow. No external assets."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
MIDBLUE = (58, 110, 165)
LIGHT = (120, 120, 115)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"

def serif_b(sz): return ImageFont.truetype(FL + "LiberationSerif-Bold.ttf", sz)
def serif(sz):   return ImageFont.truetype(FL + "LiberationSerif-Regular.ttf", sz)
def sans_b(sz):  return ImageFont.truetype(FL + "LiberationSans-Bold.ttf", sz)
def sans(sz):    return ImageFont.truetype(FL + "LiberationSans-Regular.ttf", sz)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center(y, text, font, fill=INK):
    d.text((W / 2, y), text, font=font, fill=fill, anchor="ma")

def rule(y, w=2, fill=INK):
    d.rectangle([M, y, W - M, y + w - 1], fill=fill)

# ---------------- masthead ----------------
d.rectangle([M, 12, W - M, 14], fill=INK)
d.rectangle([M, 17, W - M, 17], fill=INK)
d.text((M, 30), "WORLD EDITION", font=sans_b(13), fill=INK)
d.text((W - M, 30), "ONE PAGE  •  FREE", font=sans_b(13), fill=INK, anchor="ra")
center(26, "THE DAILY GLOBE", serif_b(66))
rule(102)
center(110, "WEDNESDAY,  18  NOVEMBER  2026", serif_b(21))
rule(138)

# ---------------- lead story ----------------
y = 152
center(y, "APEC SUMMIT  —  SHENZHEN, CHINA", sans_b(16), RED)
y = 176
for line in ["Trump, Xi and Putin meet in Shenzhen",
             "ahead of first three-way summit"]:
    center(y, line, serif_b(45))
    y += 54
y += 4
for line in wrap("Leaders of the world\u2019s three biggest nuclear powers gather at APEC \u2014 "
                 "Putin shakes Trump\u2019s hand as Thursday\u2019s trilateral talks loom.",
                 sans(19), CW):
    center(y, line, sans(19))
    y += 25

# lead illustration: dusk skyline + three flags, y 330..450
ix0, iy0, ix1, iy1 = M, 330, W - M, 450
# sky gradient (warm dusk)
for yy in range(iy0, iy1):
    t = (yy - iy0) / (iy1 - iy0)
    r = int(232 - 40 * t); g = int(176 - 30 * t); b = int(106 + 60 * t)
    d.line([(ix0, yy), (ix1, yy)], fill=(r, g, b))
# sun
d.ellipse([ix0 + 60, iy0 + 12, ix0 + 116, iy0 + 68], fill=(255, 214, 120), outline=(230, 170, 60), width=2)
# skyline silhouettes
import random
random.seed(18)
bx = ix0 + 8
while bx < ix1 - 60:
    bw = random.randint(34, 62); bh = random.randint(34, 92)
    d.rectangle([bx, iy1 - bh, bx + bw, iy1], fill=(46, 58, 74))
    for wy in range(iy1 - bh + 8, iy1 - 6, 12):
        for wx in range(bx + 6, bx + bw - 4, 11):
            if random.random() < 0.45:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 215, 106))
    bx += bw + random.randint(2, 10)
# three flags on poles, right side above skyline
def flag_us(x, y, w=64, h=40):
    for i in range(7):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(30, 50, 110))
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 4 + c * 7, y + 4 + r * 7, x + 7 + c * 7, y + 7 + r * 7], fill=(255, 255, 255))
def flag_cn(x, y, w=64, h=40):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.text((x + 6, y + 6), "\u2605", font=sans_b(20), fill=(255, 222, 0))
    d.text((x + 34, y + 4), "\u2605", font=sans_b(10), fill=(255, 222, 0))
    d.text((x + 42, y + 14), "\u2605", font=sans_b(10), fill=(255, 222, 0))
    d.text((x + 36, y + 24), "\u2605", font=sans_b(10), fill=(255, 222, 0))
def flag_ru(x, y, w=64, h=40):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)
fx = ix1 - 3 * 78 - 8
for fn, label in [(flag_us, "USA"), (flag_cn, "CHINA"), (flag_ru, "RUSSIA")]:
    d.line([(fx + 32, iy0 + 14), (fx + 32, iy1 - 58)], fill=(60, 60, 60), width=3)
    fn(fx, iy0 + 16)
    lw = d.textlength(label, font=sans_b(11))
    d.rectangle([fx + 32 - lw / 2 - 4, iy0 + 60, fx + 32 + lw / 2 + 4, iy0 + 76],
                fill=(247, 243, 234), outline=(120, 120, 115))
    d.text((fx + 32, iy0 + 61), label, font=sans_b(11), fill=INK, anchor="ma")
    fx += 78
d.rectangle([ix0, iy0, ix1, iy0], outline=INK, width=1)
d.rectangle([ix0, iy1, ix1, iy1], outline=INK, width=1)

rule(464)

# ---------------- row 2: two columns ----------------
COLW = (CW - 20) // 2   # 466
def kicker(x, y, text):
    d.text((x, y), text, font=sans_b(15), fill=RED)

# left: Gulf
x = M; y = 478
kicker(x, y, "MIDDLE EAST  —  GULF CONFLICT")
y = 500
for line in wrap("Iran strikes Kuwait and Bahrain after US hits Qeshm Island", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 4
for line in wrap("Iran says it hit US drone and missile sites in Kuwait overnight; "
                 "Bahrain says it intercepted attacks three times in a week.", sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
# Gulf map, y 648..716
mx0, my0, mx1, my1 = x, 648, x + COLW, 716
d.rectangle([mx0, my0, mx1, my1], fill=(168, 200, 224), outline=INK, width=1)
d.polygon([(mx0, my0), (mx0 + 150, my0), (mx0 + 120, my1), (mx0, my1)], fill=(234, 223, 195))
d.polygon([(mx1 - 170, my1), (mx1, my1), (mx1, my0 + 26), (mx1 - 120, my0 + 40)], fill=(234, 223, 195))
d.text((mx0 + 300, my0 + 34), "GULF", font=sans_b(11), fill=(70, 90, 120))
def burst(cx, cy, r=7):
    for ang in range(0, 360, 30):
        import math
        ex = cx + r * math.cos(math.radians(ang)); ey = cy + r * math.sin(math.radians(ang))
        d.line([(cx, cy), (ex, ey)], fill=RED, width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
burst(mx0 + 120, my0 + 12); d.text((mx0 + 132, my0 + 5), "KUWAIT", font=sans_b(11), fill=INK)
burst(mx0 + 165, my0 + 30); d.text((mx0 + 177, my0 + 23), "BAHRAIN", font=sans_b(11), fill=INK)
burst(mx1 - 90, my1 - 12);  d.text((mx1 - 168, my1 - 19), "QESHM IS.", font=sans_b(11), fill=INK)

# right: US Senate
x = M + COLW + 20; y = 478
kicker(x, y, "UNITED STATES  —  SENATE")
y = 500
for line in wrap("Peltola wins Alaska; Democrats take 56\u201344 Senate majority", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 4
for line in wrap("Democrat Mary Peltola beats two-term Republican Dan Sullivan in the "
                 "last Senate race to be called, AP reports.", sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
# bar chart, y 646..716
bx0, by0 = x, 646
d.text((bx0, by0), "DEMOCRATS", font=sans_b(13), fill=INK)
d.rectangle([bx0 + 108, by0, bx0 + 108 + 280, by0 + 18], fill=MIDBLUE)
d.text((bx0 + 396, by0), "56", font=sans_b(15), fill=INK)
d.text((bx0, by0 + 26), "REPUBLICANS", font=sans_b(13), fill=INK)
d.rectangle([bx0 + 108, by0 + 26, bx0 + 108 + 220, by0 + 44], fill=(178, 34, 52))
d.text((bx0 + 336, by0 + 26), "44", font=sans_b(15), fill=INK)

rule(730)

# ---------------- row 3: two columns ----------------
def stat_chip(x, y, big, label, color=INK):
    d.text((x, y), big, font=serif_b(34), fill=color)
    bw = d.textlength(big, font=serif_b(34))
    d.text((x + bw + 10, y + 8), label, font=sans(14), fill=INK)

x = M; y = 744
kicker(x, y, "TECH & MARKETS")
y = 766
for line in wrap("Anthropic prices IPO at $83; Nvidia tops forecasts", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 2
for line in wrap("Anthropic prices its IPO above its $70\u201378 range; Nvidia beats "
                 "forecasts in its first report since Jensen Huang\u2019s exit.",
                 sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
stat_chip(x, 862, "$83", "a share \u2014 IPO priced\nabove the $70\u201378 range")

x = M + COLW + 20; y = 744
kicker(x, y, "SOUTH ASIA  —  BANGLADESH")
y = 766
for line in wrap("Paramilitary deployed as unrest grows over Hasina return", serif_b(25), COLW):
    d.text((x, y), line, font=serif_b(25), fill=INK); y += 30
y += 2
for line in wrap("Hundreds of troops deploy nationwide as bomb blasts and arson spread "
                 "ahead of Hasina\u2019s planned December return.", sans(16), COLW):
    d.text((x, y), line, font=sans(16), fill=INK); y += 21
stat_chip(x, 862, "28", "districts hit by blasts\nand arson in 10 days", RED)

rule(912)

# ---------------- in brief ticker ----------------
y = 924
d.text((M, y), "IN BRIEF", font=sans_b(15), fill=RED)
tick = ("UK inflation hits a one-year high  \u2022  Brent crude settles at $91.95 a barrel  \u2022  "
        "Cyclone Akvan nears India\u2019s east coast  \u2022  Voyager 1 reaches a light-day from Earth")
lines = wrap(tick, sans(15), CW - 92)
ty = y
for line in lines:
    d.text((M + 92, ty), line, font=sans(15), fill=INK); ty += 19

# ---------------- footer ----------------
rule(968)
center(976, "Wednesday, 18 November 2026  \u2022  The Daily Globe", serif_b(15))
center(996, "Sources: Reuters, Associated Press, BBC News, The New York Times, The Hindu",
       sans(12), LIGHT)

img.save("/home/hatch/workspace/makefun/work-news-image/entry.png", optimize=True)
print("saved")
