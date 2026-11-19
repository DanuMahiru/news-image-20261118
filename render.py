#!/usr/bin/env python3
"""Render v3 of the 18 November 2026 front page: 48 verified stories,
7 regions, UTC timeline, proof tags, world map, date check.
All art drawn programmatically with Pillow. No external assets.
Own design and wording; layout follows the proven dense-front-page form."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
M = 30
CW = W - 2 * M

PAPER = (248, 244, 235)
INK = (16, 16, 16)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
MIDBLUE = (58, 110, 165)
TEAL = (14, 110, 110)
PURPLE = (96, 60, 140)
GREEN = (34, 110, 60)
ORANGE = (190, 100, 20)
DARKRED = (140, 30, 30)
LIGHT = (118, 118, 112)
SKY = (168, 200, 224)
LAND = (234, 223, 195)

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

def vline(x, y0, y1, fill=(150, 150, 143)):
    d.line([(x, y0), (x, y1)], fill=fill, width=1)

def tag(x, y, text, color=RED):
    """small red proof tag, returns width used"""
    f = sans_b(9)
    tw = d.textlength(text, font=f)
    d.rectangle([x, y, x + tw + 8, y + 12], fill=color)
    d.text((x + 4, y + 1), text, font=f, fill=(255, 255, 255))
    return tw + 8

def kicker(x, y, text, color=RED):
    d.text((x, y), text, font=sans_b(10), fill=color)

def headline(x, y, text, size, max_w, leading=None):
    ld = leading or int(size * 1.18)
    for line in wrap(text, serif_b(size), max_w):
        d.text((x, y), line, font=serif_b(size), fill=INK)
        y += ld
    return y

def body(x, y, text, size, max_w, leading=None):
    ld = leading or int(size * 1.3)
    for line in wrap(text, sans(size), max_w):
        d.text((x, y), line, font=sans(size), fill=INK)
        y += ld
    return y

def burst(cx, cy, r=7, color=RED):
    for ang in range(0, 360, 30):
        ex = cx + r * math.cos(math.radians(ang))
        ey = cy + r * math.sin(math.radians(ang))
        d.line([(cx, cy), (ex, ey)], fill=color, width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)

# ---------------- top line ----------------
d.text((M, 8), "THE WORLD'S NEWS OF ONE DAY, ON ONE PAGE", font=sans_b(11), fill=RED)
d.text((W - M, 8), "48 STORIES  \u2022  7 REGIONS  \u2022  9 FIELDS  \u2022  16 DRAWN", font=sans_b(11), fill=INK, anchor="ra")
rule(24)

# ---------------- masthead ----------------
center(28, "Wednesday 18 November 2026", serif_b(52))
rule(86)

# ---------------- region bar (segments + legend line) ----------------
REGIONS = [("ASIA", 10, RED), ("EUROPE", 8, BLUE), ("AMERICAS", 13, TEAL),
           ("MIDDLE EAST", 5, DARKRED), ("GLOBAL", 7, PURPLE), ("AFRICA", 2, GREEN),
           ("OCEANIA", 3, ORANGE)]
x = M
tot = 48
for name, n, color in REGIONS:
    w = CW * n / tot
    d.rectangle([x, 92, x + w - 1, 106], fill=color)
    x += w
rx = M
for name, n, color in REGIONS:
    d.rectangle([rx, 111, rx + 8, 119], fill=color)
    d.text((rx + 11, 110), f"{name} {n}", font=sans_b(10), fill=INK)
    rx += 11 + d.textlength(f"{name} {n}", font=sans_b(10)) + 12
d.text((M, 124), "BY FIELD", font=sans_b(10), fill=RED)
d.text((M + 62, 124), "Diplomacy 4   War & security 11   Economy & markets 13   Politics & courts 2   Culture & sport 5   Business & tech 4   Labour & society 4   Climate & disasters 3   Science & space 2", font=sans(10), fill=INK)
rule(138)

# ---------------- UTC timeline ----------------
d.text((M, 144), "THE DAY IN UTC", font=sans_b(11), fill=RED)
TL = [("Overnight", "Drones over Kuwait, Bahrain"),
      ("07:00", "UK inflation: 3.6%"),
      ("Morning", "Xi greets Trump"),
      ("10:16", "Voyager 1 light-day"),
      ("11:00", "GTA VI in New Zealand"),
      ("14:37", "EU offers Kyiv \u20ac45bn"),
      ("19:00", "Fed minutes: more hikes"),
      ("21:00", "Dow closes down 561")]
tx = M + 118
tw = (CW - 118) / len(TL)
for i, (t, label) in enumerate(TL):
    cx = tx + i * tw
    d.text((cx, 144), t, font=sans_b(10), fill=INK)
    yy = 158
    for line in wrap(label, sans(9), tw - 6):
        d.text((cx, yy), line, font=sans(9), fill=INK)
        yy += 11
        if yy > 169:
            break
    if i:
        vline(cx - 4, 144, 178)
rule(182)

# ---------------- leads: 4 columns ----------------
LEADW = (CW - 3 * 12) // 4   # 232
LY = 186

def flag_us(x, y, w=56, h=35):
    for i in range(7):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(30, 50, 110))

def flag_cn(x, y, w=56, h=35):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.text((x + 5, y + 4), "\u2605", font=sans_b(17), fill=(255, 222, 0))
    d.text((x + 28, y + 3), "\u2605", font=sans_b(9), fill=(255, 222, 0))
    d.text((x + 35, y + 12), "\u2605", font=sans_b(9), fill=(255, 222, 0))
    d.text((x + 29, y + 21), "\u2605", font=sans_b(9), fill=(255, 222, 0))

def flag_ru(x, y, w=56, h=35):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)

def draw_gulf(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=1)
    d.polygon([(x0, y0), (x0 + 78, y0), (x0 + 60, y1), (x0, y1)], fill=LAND)
    d.polygon([(x1 - 90, y1), (x1, y1), (x1, y0 + 16), (x1 - 62, y0 + 22)], fill=LAND)
    d.text((x0 + 150, y0 + 26), "GULF", font=sans_b(10), fill=(70, 90, 120))
    burst(x0 + 62, y0 + 10); d.text((x0 + 72, y0 + 4), "KUWAIT", font=sans_b(9), fill=INK)
    burst(x0 + 86, y0 + 26); d.text((x0 + 96, y0 + 20), "BAHRAIN", font=sans_b(9), fill=INK)
    burst(x1 - 48, y1 - 10); d.text((x1 - 112, y1 - 16), "QESHM IS.", font=sans_b(9), fill=INK)
    d.text((x0 + 6, y0 + 4), "IRAN", font=sans_b(10), fill=(120, 60, 60))
    d.text((x0 + 6, y1 - 16), "SAUDI ARABIA", font=sans_b(9), fill=(90, 90, 80))

def draw_shenzhen(x0, y0, x1, y1):
    for yy in range(y0, y1):
        t = (yy - y0) / (y1 - y0)
        d.line([(x0, yy), (x1, yy)], fill=(int(232 - 40 * t), int(176 - 30 * t), int(106 + 60 * t)))
    d.ellipse([x0 + 4, y0 + 4, x0 + 22, y0 + 22], fill=(255, 214, 120), outline=(230, 170, 60), width=2)
    import random
    random.seed(7)
    bx = x0 + 4
    sky_end = x0 + int((x1 - x0) * 0.52)
    while bx < sky_end:
        bw = random.randint(16, 28); bh = random.randint(18, 44)
        d.rectangle([bx, y1 - bh, bx + bw, y1], fill=(46, 58, 74))
        bx += bw + 3
    fx = x1 - 3 * 66 - 4
    for fn, label in [(flag_us, "USA"), (flag_cn, "CHINA"), (flag_ru, "RUSSIA")]:
        d.line([(fx + 28, y0 + 6), (fx + 28, y1 - 30)], fill=(60, 60, 60), width=2)
        fn(fx, y0 + 8)
        lw = d.textlength(label, font=sans_b(8))
        d.rectangle([fx + 28 - lw / 2 - 3, y0 + 46, fx + 28 + lw / 2 + 3, y0 + 57], fill=PAPER)
        d.text((fx + 28, y0 + 47), label, font=sans_b(8), fill=INK, anchor="ma")
        fx += 66
    d.rectangle([x0, y0, x1, y1], outline=INK, width=1)

def draw_odesa(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(30, 42, 66), outline=INK, width=1)
    for cx, cy, r in [(x0 + 34, y0 + 26, 14), (x0 + 96, y0 + 36, 15), (x0 + 140, y0 + 16, 9)]:
        burst(cx, cy, r, (255, 170, 40))
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 220, 120))
    d.rectangle([x0 + 8, y1 - 22, x0 + 112, y1 - 6], fill=(255, 255, 255))
    d.text((x0 + 11, y1 - 21), "ODESA \u2022 4 KILLED", font=sans_b(10), fill=RED)
    d.text((x1 - 8, y0 + 2), "\u20ac45bn", font=serif_b(20), fill=(255, 214, 120), anchor="ra")
    d.text((x1 - 8, y1 - 14), "EU LOAN OFFER FOR 2027", font=sans_b(8), fill=(255, 255, 255), anchor="ra")

def draw_voyager(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(8, 10, 26), outline=INK, width=1)
    import random
    random.seed(3)
    for _ in range(26):
        sx = random.randint(x0 + 4, x1 - 4); sy = random.randint(y0 + 4, y1 - 4)
        d.ellipse([sx, sy, sx + 1, sy + 1], fill=(255, 255, 255))
    d.ellipse([x0 + 12, y1 - 34, x0 + 44, y1 - 2], fill=(60, 120, 200), outline=(140, 190, 255), width=1)
    d.text((x0 + 12, y0 + 4), "EARTH", font=sans_b(8), fill=(200, 220, 255))
    d.line([(x0 + 52, y1 - 18), (x1 - 34, y0 + 22)], fill=(255, 220, 120), width=1)
    d.rectangle([x1 - 40, y0 + 14, x1 - 26, y0 + 26], fill=(220, 220, 210), outline=(255, 255, 255))
    d.line([(x1 - 40, y0 + 20), (x1 - 52, y0 + 12)], fill=(220, 220, 210), width=2)
    d.text((x0 + 52, y0 + 3), "1 LIGHT-DAY", font=serif_b(17), fill=(255, 214, 120))
    d.rectangle([x0 + 50, y0 + 25, x0 + 208, y0 + 37], fill=(8, 10, 26))
    d.text((x0 + 52, y0 + 27), "25.9 BILLION KM FROM EARTH", font=sans_b(8), fill=(200, 220, 255))

LEADS = [
    ("1  MIDDLE EAST \u2014 IRAN WAR", "Iran hits US base in Kuwait; Bahrain reports new attacks",
     "Kuwait says its air defences engaged \u201chostile drones\u201d. Bahrain says it intercepted attacks, the third time in a week.",
     "CLAIM: IRAN\u2019S ARMY", draw_gulf),
    ("2  ASIA \u2014 APEC SUMMIT", "Xi greets Trump as APEC opens in Shenzhen",
     "A break with protocol. Xi calls for open trade; Putin is in town too. The first Trump\u2013Xi\u2013Putin summit is set for Thursday.",
     "CONFIRMED: AP", draw_shenzhen),
    ("3  EUROPE \u2014 UKRAINE WAR", "Russian strikes kill five; EU offers Kyiv a \u20ac45bn loan",
     "Four die in Odesa\u2019s historic centre. Brussels: Ukraine repays only once Russia pays reparations.",
     "OFFICIALS: KYIV, EU", draw_odesa),
    ("4  GLOBAL \u2014 SPACE", "Voyager 1, one light-day out, a first for humankind",
     "At 10:16 UTC the probe launched in 1977 passed 25.9 billion km. Its signal now takes a full day to arrive.",
     "CONFIRMED: NASA", draw_voyager),
]
for i, (kick, head, summ, t, drawfn) in enumerate(LEADS):
    x = M + i * (LEADW + 12)
    drawfn(x, LY, x + LEADW, LY + 76)
    y = LY + 82
    kicker(x, y, kick); y += 14
    y = headline(x, y, head, 19, LEADW, 22)
    y = body(x, y + 2, summ, 11, LEADW, 14)
    tag(x, LY + 188, t)
    if i < 3:
        vline(x + LEADW + 6, LY, LY + 200)
rule(LY + 206)

# ---------------- mid row: 6 columns ----------------
MIDW = (CW - 5 * 10) // 6   # 152
MY = LY + 214

def draw_gaza(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=LAND, outline=INK, width=1)
    d.rectangle([x0, y0, x1, y0 + 14], fill=SKY)
    d.text((x0 + 4, y0 + 2), "GAZA", font=sans_b(9), fill=INK)
    d.line([(x0 + 20, y0 + 20), (x1 - 10, y1 - 8)], fill=(200, 120, 40), width=2)
    d.text((x0 + 4, y0 + 18), "YELLOW LINE", font=sans_b(8), fill=(160, 90, 20))
    for tx in (x0 + 60, x0 + 92):
        d.rectangle([tx, y1 - 26, tx + 22, y1 - 14], fill=(70, 80, 60))
        d.ellipse([tx + 4, y1 - 12, tx + 9, y1 - 7], fill=INK)
        d.ellipse([tx + 14, y1 - 12, tx + 19, y1 - 7], fill=INK)
    d.text((x0 + 4, y1 - 12), "NUSEIRAT", font=sans_b(8), fill=INK)

def draw_horn(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=LAND, outline=INK, width=1)
    d.polygon([(x0 + 20, y0 + 8), (x0 + 70, y0 + 8), (x0 + 60, y1 - 8), (x0 + 10, y1 - 8)], fill=(200, 170, 120))
    d.polygon([(x1 - 70, y0 + 8), (x1 - 20, y0 + 8), (x1 - 30, y1 - 8), (x1 - 80, y1 - 8)], fill=(170, 140, 100))
    d.line([(x0 + 74, y0 + 30), (x1 - 74, y0 + 30)], fill=RED, width=2)
    d.polygon([(x1 - 74, y0 + 24), (x1 - 74, y0 + 36), (x1 - 62, y0 + 30)], fill=RED)
    d.polygon([(x0 + 74, y0 + 24), (x0 + 74, y0 + 36), (x0 + 62, y0 + 30)], fill=RED)
    d.text((x0 + 4, y0 + 2), "ETHIOPIA", font=sans_b(8), fill=INK)
    d.text((x1 - 4, y1 - 12), "ERITREA", font=sans_b(8), fill=INK, anchor="ra")

def draw_fed(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=1)
    pts = [(x0 + 6, y0 + 12), (x0 + 40, y0 + 16), (x0 + 74, y0 + 12), (x0 + 108, y0 + 26), (x0 + 140, y0 + 40)]
    d.line(pts, fill=RED, width=2)
    d.text((x0 + 6, y1 - 14), "DOW  \u2212561", font=sans_b(11), fill=RED)
    d.text((x1 - 4, y0 + 2), "\u22121.1%", font=sans_b(10), fill=INK, anchor="ra")

def draw_factory(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(230, 225, 215), outline=INK, width=1)
    d.rectangle([x0 + 10, y1 - 26, x0 + 90, y1 - 6], fill=(120, 110, 100))
    d.rectangle([x0 + 16, y1 - 44, x0 + 24, y1 - 26], fill=(120, 110, 100))
    d.rectangle([x0 + 30, y1 - 52, x0 + 38, y1 - 26], fill=(120, 110, 100))
    for wx in range(x0 + 96, x1 - 12, 14):
        d.ellipse([wx, y1 - 22, wx + 7, y1 - 15], fill=(40, 60, 90))
    d.text((x0 + 96, y0 + 4), "30,000", font=serif_b(16), fill=RED)
    d.text((x0 + 96, y0 + 22), "TAKA DEMAND", font=sans_b(8), fill=INK)

def draw_senate(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=1)
    d.text((x0 + 6, y0 + 4), "DEM", font=sans_b(9), fill=INK)
    d.rectangle([x0 + 34, y0 + 4, x0 + 34 + 96, y0 + 16], fill=MIDBLUE)
    d.text((x0 + 134, y0 + 3), "251", font=sans_b(11), fill=INK)
    d.text((x0 + 6, y0 + 22), "REP", font=sans_b(9), fill=INK)
    d.rectangle([x0 + 34, y0 + 22, x0 + 34 + 12, y0 + 34], fill=(178, 34, 52))
    d.text((x0 + 50, y0 + 21), "11", font=sans_b(11), fill=INK)
    d.text((x0 + 6, y1 - 14), "HOUSE VOTE", font=sans_b(9), fill=INK)

def draw_chip(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(20, 30, 50), outline=INK, width=1)
    d.rectangle([x0 + 52, y0 + 12, x0 + 100, y1 - 12], fill=(60, 90, 140), outline=(140, 190, 255), width=1)
    for px in range(x0 + 44, x0 + 108, 16):
        d.line([(px, y0 + 20), (px, y0 + 12)], fill=(140, 190, 255), width=2)
        d.line([(px, y1 - 20), (px, y1 - 12)], fill=(140, 190, 255), width=2)
    d.text((x0 + 6, y0 + 4), "$83", font=serif_b(20), fill=(255, 214, 120))
    d.text((x0 + 6, y0 + 28), "IPO PRICED", font=sans_b(9), fill=(255, 255, 255))

MIDS = [
    ("5  MIDDLE EAST \u2014 GAZA", "Israel makes first ground push in central Gaza since truce",
     "Tanks cross the Yellow Line; Hamas calls it a breach.",
     "CONFIRMED: AL JAZEERA, BBC", draw_gaza),
    ("6  AFRICA \u2014 HORN", "Ethiopia and Eritrea mass troops on their border",
     "Within striking distance, monitors say; Eritrea calls it propaganda.",
     "SOURCES: REUTERS", draw_horn),
    ("7  AMERICAS \u2014 MARKETS", "Fed minutes point to more rate rises; Dow drops 561",
     "Officials expect more hikes; Dow \u22121.1%, Nasdaq +0.4%.",
     "CONFIRMED: REUTERS", draw_fed),
    ("8  ASIA \u2014 LABOUR", "Bangladesh wage protests shut factories; tear gas fired",
     "Workers walk out in Savar-Ashulia; 30 factories halt.",
     "CONFIRMED: DAILY STAR", draw_factory),
    ("9  AMERICAS \u2014 US POLITICS", "House Democrats pick Jeffries for Speaker, 251\u201311",
     "The first Black nominee; the full House votes on 3 January.",
     "CONFIRMED: AP", draw_senate),
    ("10  AMERICAS \u2014 BUSINESS", "Anthropic prices IPO at $83; Nvidia tops forecasts",
     "Anthropic prices above its range; Nvidia revenue doubles.",
     "CONFIRMED: REUTERS", draw_chip),
]
for i, (kick, head, summ, t, drawfn) in enumerate(MIDS):
    x = M + i * (MIDW + 10)
    drawfn(x, MY, x + MIDW, MY + 56)
    y = MY + 62
    kicker(x, y, kick); y += 13
    y = headline(x, y, head, 14, MIDW, 17)
    y = body(x, y + 1, summ, 10, MIDW, 13)
    tag(x, MY + 158, t)
    if i < 5:
        vline(x + MIDW + 5, MY, MY + 170)
rule(MY + 180)

# ---------------- third row: 6 columns ----------------
TY = MY + 188

def draw_peltola(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=1)
    d.text((x0 + 6, y0 + 4), "56\u201344", font=serif_b(22), fill=MIDBLUE)
    d.text((x0 + 6, y0 + 30), "SENATE", font=sans_b(10), fill=INK)
    d.text((x1 - 6, y1 - 14), "ALASKA", font=sans_b(9), fill=INK, anchor="ra")

def draw_akvan(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=1)
    d.polygon([(x0 + 30, y0 + 30), (x0 + 90, y0 + 20), (x0 + 120, y0 + 44), (x0 + 60, y1 - 6), (x0 + 20, y1 - 10)], fill=LAND)
    cx, cy = x0 + 78, y0 + 30
    for r in (22, 15, 8):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    d.text((x0 + 4, y0 + 2), "BAY OF BENGAL", font=sans_b(8), fill=(70, 90, 120))
    d.text((x0 + 4, y1 - 12), "ODISHA", font=sans_b(8), fill=INK)

def draw_gta(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(16, 10, 30), outline=INK, width=1)
    d.text((x0 + 6, y0 + 2), "GTA VI", font=serif_b(20), fill=(255, 80, 200))
    d.text((x0 + 6, y0 + 24), "00:00 THU", font=sans_b(11), fill=(120, 255, 220))
    d.text((x0 + 6, y0 + 37), "NEW ZEALAND FIRST", font=sans_b(8), fill=(255, 255, 255))

def draw_aria(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(60, 20, 80), outline=INK, width=1)
    d.ellipse([x0 + 56, y0 + 8, x0 + 96, y0 + 34], fill=(255, 214, 120), outline=(255, 255, 255), width=1)
    d.rectangle([x0 + 70, y0 + 34, x0 + 82, y0 + 46], fill=(255, 214, 120))
    d.text((x0 + 6, y0 + 6), "7", font=serif_b(24), fill=(255, 255, 255))
    d.text((x0 + 6, y1 - 13), "ARIA WINS", font=sans_b(9), fill=(255, 255, 255))

def draw_uk(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=1)
    for i, h in enumerate((14, 20, 17, 26, 34)):
        d.rectangle([x0 + 10 + i * 26, y1 - 8 - h, x0 + 10 + i * 26 + 18, y1 - 8], fill=MIDBLUE if i < 4 else RED)
    d.text((x0 + 6, y0 + 2), "3.6%", font=serif_b(15), fill=RED)

def draw_quad(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK, width=1)
    flags = [((178, 34, 52), "US"), ((255, 153, 51), "IN"), ((0, 80, 160), "AU"), ((220, 40, 40), "JP")]
    for i, (c, lab) in enumerate(flags):
        fx = x0 + 8 + i * 36
        d.rectangle([fx, y0 + 10, fx + 28, y0 + 26], fill=c)
        d.text((fx + 14, y0 + 28), lab, font=sans_b(9), fill=INK, anchor="ma")

THIRDS = [
    ("11  AMERICAS \u2014 US POLITICS", "Peltola wins Alaska; Dems take Senate 56\u201344",
     "Democrat beats Sullivan in the last race to be called.",
     "CONFIRMED: AP", draw_peltola),
    ("12  ASIA \u2014 WEATHER", "Cyclone Akvan turns towards India\u2019s Odisha coast",
     "Nearly 50,000 moved to safety; landfall due Friday.",
     "FORECAST: PTI", draw_akvan),
    ("13  GLOBAL \u2014 GAMES", "GTA VI\u2019s midnight launch begins in New Zealand",
     "After 13 years, it unlocks time zone by time zone.",
     "CONFIRMED: ANADOLU", draw_gta),
    ("14  OCEANIA \u2014 MUSIC", "Tame Impala sweeps Australia\u2019s ARIA Awards",
     "Seven wins in Sydney, album of the year among them.",
     "CONFIRMED: ABC", draw_aria),
    ("15  EUROPE \u2014 ECONOMY", "UK inflation up to 3.6%, a one-year high",
     "Price rises stay above the Bank\u2019s 2% target.",
     "CONFIRMED: ONS", draw_uk),
    ("16  ASIA \u2014 DIPLOMACY", "QUAD meets in Manila; Trump flies to Shenzhen",
     "Modi, Albanese and Takaichi join Trump before APEC.",
     "SOURCES: REUTERS", draw_quad),
]
for i, (kick, head, summ, t, drawfn) in enumerate(THIRDS):
    x = M + i * (MIDW + 10)
    drawfn(x, TY, x + MIDW, TY + 48)
    y = TY + 54
    kicker(x, y, kick); y += 13
    y = headline(x, y, head, 13, MIDW, 16)
    y = body(x, y + 1, summ, 10, MIDW, 13)
    tag(x, TY + 140, t)
    if i < 5:
        vline(x + MIDW + 5, TY, TY + 152)
rule(TY + 158)

# ---------------- map + briefs ----------------
BY = TY + 160
d.text((M, BY), "WHERE IT HAPPENED", font=sans_b(11), fill=RED)
d.text((M + 316, BY), "ALSO ON WEDNESDAY 18 NOVEMBER", font=sans_b(11), fill=RED)
rule(BY + 16)

MAPX, MAPY, MAPW, MAPH = M, BY + 22, 300, 132
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(210, 228, 240), outline=INK, width=1)
# simplified continents
d.polygon([(MAPX + 18, MAPY + 22), (MAPX + 90, MAPY + 14), (MAPX + 108, MAPY + 44), (MAPX + 70, MAPY + 66), (MAPX + 30, MAPY + 58)], fill=LAND)  # N America
d.polygon([(MAPX + 78, MAPY + 74), (MAPX + 108, MAPY + 72), (MAPX + 104, MAPY + 118), (MAPX + 84, MAPY + 126)], fill=LAND)  # S America
d.polygon([(MAPX + 138, MAPY + 20), (MAPX + 172, MAPY + 16), (MAPX + 178, MAPY + 40), (MAPX + 150, MAPY + 46)], fill=LAND)  # Europe
d.polygon([(MAPX + 140, MAPY + 52), (MAPX + 176, MAPY + 50), (MAPX + 182, MAPY + 96), (MAPX + 160, MAPY + 112), (MAPX + 146, MAPY + 82)], fill=LAND)  # Africa
d.polygon([(MAPX + 182, MAPY + 14), (MAPX + 268, MAPY + 10), (MAPX + 282, MAPY + 52), (MAPX + 240, MAPY + 66), (MAPX + 196, MAPY + 50)], fill=LAND)  # Asia
d.polygon([(MAPX + 258, MAPY + 112), (MAPX + 288, MAPY + 110), (MAPX + 290, MAPY + 128), (MAPX + 264, MAPY + 130)], fill=LAND)  # Oceania
PINS = {1: (200, 58), 2: (258, 44), 3: (168, 30), 4: (288, 22), 5: (184, 64),
        6: (168, 76), 7: (52, 44), 8: (236, 56), 9: (62, 50), 10: (44, 52),
        11: (28, 30), 12: (246, 64), 13: (292, 118), 14: (280, 122), 15: (152, 26), 16: (268, 62)}
for n, (px, py) in PINS.items():
    d.ellipse([MAPX + px - 6, MAPY + py - 6, MAPX + px + 6, MAPY + py + 6], fill=RED, outline=(255, 255, 255), width=1)
    d.text((MAPX + px, MAPY + py - 1), str(n), font=sans_b(7), fill=(255, 255, 255), anchor="mm")
d.text((MAPX, MAPY + MAPH + 4), "Numbered pin = stories 1\u201316  \u2022  dot = a brief from the list",
       font=sans(9), fill=INK)
d.text((MAPX, MAPY + MAPH + 16), "HOW SURE \u2014 CONFIRMED: on the record. CLAIM: one side\u2019s account,",
       font=sans_b(9), fill=INK)
d.text((MAPX, MAPY + MAPH + 27), "not independently verified. SOURCES: monitors, via a news agency.",
       font=sans(9), fill=INK)

BRIEFS = [
    ("Gold falls to $3,770, lowest since Sept 2025", PURPLE),
    ("Brent settles at $91.95 a barrel", PURPLE),
    ("Nvidia revenue doubles to $115.8bn", TEAL),
    ("Nasdaq +0.42% as the Dow falls 561", TEAL),
    ("El Ni\u00f1o drought, fires persist in Amazon", TEAL),
    ("Gopalganj: police station burned in unrest", RED),
    ("Hasina unrest: troops out in 28 districts", RED),
    ("Dhoni retires from the IPL", RED),
    ("Muse privacy flaws alarm Meta staff", PURPLE),
    ("UnitedHealth falls 10%, biggest drag on Dow", TEAL),
    ("WTI crude down 3.2% to $83.26", TEAL),
    ("10-year Treasury yield eases to 5.07%", TEAL),
    ("Dollar hits a 19-month high", PURPLE),
    ("Waller: half-point Dec hike may be needed", TEAL),
    ("Markets put December hike odds near 95%", TEAL),
    ("S&P 500 falls for a fifth straight day", TEAL),
    ("EU: four states opt out of the Ukraine loan", BLUE),
    ("Merz warns he will block the EU budget", BLUE),
    ("Odesa: strikes hit a UNESCO historic centre", BLUE),
    ("Gaza: 5,200 flee as tanks roll onto main road", DARKRED),
    ("Gaza: three killed in separate drone strikes", DARKRED),
    ("Wage board meets 23 Nov; new pay due in Dec", RED),
    ("About 30 factories shut in Savar-Ashulia", RED),
    ("Akvan is the third storm in a month", RED),
    ("Ecca Vandal wins four ARIAs; Owusu shut out", ORANGE),
    ("Alcaraz meets Medvedev at the ATP Finals", BLUE),
    ("Nyala market drone strike kills 21", GREEN),
    ("Houthi strike on Riyadh airport kills 12", DARKRED),
    ("NZ telco braces for 35 PB of GTA downloads", ORANGE),
    ("France: students blockade schools in strikes", BLUE),
    ("Dragon undocking stood down by weather", PURPLE),
    ("ECB top jobs split: Spain, Germany, France", BLUE),
]
BX0 = M + 316
BCOLW = (W - M - BX0 - 16) // 3
for col in range(3):
    x = BX0 + col * (BCOLW + 8)
    y = BY + 24
    for j in range(11):
        idx = col * 11 + j
        if idx >= len(BRIEFS):
            break
        text, color = BRIEFS[idx]
        d.ellipse([x, y + 2, x + 7, y + 9], fill=color)
        d.text((x + 11, y), text, font=sans(9), fill=INK)
        y += 11
rule(BY + 190)

# ---------------- date check ----------------
DY = BY + 198
d.text((M, DY), "DATE CHECK", font=sans_b(11), fill=(255, 255, 255))
d.rectangle([M, DY, M + 78, DY + 14], fill=RED)
d.text((M + 4, DY + 1), "DATE CHECK", font=sans_b(10), fill=(255, 255, 255))
dc = ("Left out on purpose, because they were first reported before Wednesday: the US strike on Qeshm (Tue), "
      "the Crimean Bridge attack (Tue), India beating Pakistan 2\u20131 in the SAFF final (Tue), the Earthshot Prize "
      "in Mumbai (Tue), the US losing measles elimination status (Tue), the Rugby League World Cup final, Australia 32\u201312 NZ (Sun). Not yet reported: the Trump\u2013Xi\u2013Putin "
      "summit, Anthropic\u2019s first trade and GTA VI\u2019s US release (Thu 19 Nov); Akvan\u2019s landfall (Fri 20 Nov).")
y = DY
for line in wrap(dc, sans(10), CW - 88):
    d.text((M + 88, y), line, font=sans(10), fill=INK)
    y += 13

# ---------------- footer ----------------
rule(DY + 44)
center(DY + 50, "Every story here happened or was first reported on Wednesday 18 November 2026; nothing older is shown as the day\u2019s news.", serif_b(12))
center(DY + 68, "Sources: Reuters, AP, AFP, Al Jazeera, BBC, CNBC, NASA, ONS, ABC, ATP.  Original drawings.", sans(10), LIGHT)

img.save("/home/hatch/workspace/makefun/work-news-image-v3/entry.png", optimize=True)
print("saved", img.size)
