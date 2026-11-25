#!/usr/bin/env python3
"""Render the news-image-20261125 entry: a one-page front-page infographic
summing up Tuesday 25 November 2026's world news. Drawn from scratch with
PIL using flat shapes only -- no photos, no copied artwork. The program uses
no network. Output: entry.png, 1024x1024, well under 1 MiB."""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (22, 35, 63)
GOLD = (201, 162, 39)
INK = (24, 28, 36)
GREY = (107, 101, 88)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap: split text into lines no wider than max_w."""
    lines = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def star(draw, cx, cy, r_out, r_in, points, fill):
    """A filled star with the given number of points."""
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        angle = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=fill)


def dashed_circle(draw, cx, cy, r, fill, dash=9, gap=6):
    """A circle drawn as dashes, used to ring a map or globe."""
    step = 2 * math.pi / 96
    run = []
    for i in range(97):
        a = i * step
        p = (cx + r * math.cos(a), cy + r * math.sin(a))
        if (i % (dash + gap)) < dash:
            run.append(p)
        else:
            if len(run) > 1:
                draw.line(run, fill=fill, width=3)
            run = []
    if len(run) > 1:
        draw.line(run, fill=fill, width=3)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- header ----------------
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 116, W, 121], fill=GOLD)
f_date = font(BOLD, 25)
f_title = font(BOLD, 54)
date_line = "WEDNESDAY  -  25 NOVEMBER 2026"
d.text(((W - d.textlength(date_line, font=f_date)) / 2, 14),
       date_line, font=f_date, fill=GOLD)
title = "THE WORLD IN A DAY"
d.text(((W - d.textlength(title, font=f_title)) / 2, 46),
       title, font=f_title, fill=(255, 255, 255))

# ---------------- story cards ----------------
# (accent colour, headline, fact, pictogram key)
STORIES = [
    ((178, 34, 34), "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
     "Sea drones sink corvette Merkury; Moscow calls it terrorism", "sea"),
    ((20, 90, 70), "COP31 COLLAPSES WITHOUT A DEAL",
     "Antalya summit ends in failure; EU calls the outcome 'terrible'", "summit"),
    ((196, 120, 20), "HOUTHI DRONE HITS RIYADH TOWER",
     "Saudi civil defence reports 11 injured in strike on tallest tower", "tower"),
    ((90, 60, 110), "700,000+ RUSSIAN SOLDIERS KILLED",
     "New analysis counts the war's Russian military dead past 700,000", "memorial"),
    ((30, 60, 120), "CIA AND ODNI HIT BY CYBERATTACK",
     "Breach touches non-classified data at two US intelligence agencies", "cyber"),
    ((120, 80, 30), "HUAWEI GUILTY OF TRADE-SECRETS THEFT",
     "US trial convicts Huawei; acquitted of racketeering charges", "court"),
]

CARD_W, CARD_H, GAP, MARGIN = 480, 269, 16, 24
f_head = font(BOLD, 30)
f_fact = font(REGULAR, 20)
f_num = font(BOLD, 22)


def pic_sea(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 28, 54))
    for sx, sy in [(36, 22), (110, 48), (180, 16), (260, 44), (340, 20), (430, 52)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=(255, 255, 255))
    d.ellipse([x0 + w - 84, y0 + 8, x0 + w - 48, y0 + 44], fill=(235, 225, 190))
    # night sea
    d.rectangle([x0, y0 + 66, x0 + w, y0 + h], fill=(24, 68, 110))
    for wx in range(0, w, 52):
        d.arc([x0 + wx, y0 + 76, x0 + wx + 40, y0 + 92], start=0, end=180,
              fill=(160, 200, 230), width=2)
    # warship hull and tower
    d.rectangle([x0 + 130, y0 + 62, x0 + 330, y0 + 88], fill=(38, 42, 52))
    d.polygon([(x0 + 130, y0 + 62), (x0 + 150, y0 + 62), (x0 + 142, y0 + 44),
               (x0 + 130, y0 + 44)], fill=(38, 42, 52))
    d.rectangle([x0 + 230, y0 + 40, x0 + 250, y0 + 62], fill=(38, 42, 52))
    d.line([x0 + 240, y0 + 28, x0 + 240, y0 + 40], fill=(200, 205, 215), width=3)
    # two sea drones skimming the water
    for dx, dy in [(70, 84), (390, 78)]:
        cx, cy = x0 + dx, y0 + dy
        d.rectangle([cx - 13, cy - 3, cx + 13, cy + 3], fill=(210, 214, 222))
        d.line([cx - 20, cy - 8, cx + 20, cy - 8], fill=(210, 214, 222), width=3)
        d.line([cx - 20, cy + 8, cx + 20, cy + 8], fill=(210, 214, 222), width=3)
    # starburst where a drone struck
    ex, ey = x0 + 356, y0 + 52
    star(d, ex, ey, 30, 13, 8, (255, 176, 32))
    star(d, ex, ey, 17, 8, 8, (255, 110, 30))


def pic_summit(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 232, 240))
    # cracked dry earth along the bottom
    d.rectangle([x0, y0 + 82, x0 + w, y0 + h], fill=(188, 148, 96))
    d.line([x0 + 60, y0 + 82, x0 + 90, y0 + 108], fill=(110, 72, 40), width=3)
    d.line([x0 + 90, y0 + 108, x0 + 70, y0 + 108], fill=(110, 72, 40), width=3)
    d.line([x0 + 250, y0 + 82, x0 + 280, y0 + 100, x0 + 320, y0 + 96],
           fill=(110, 72, 40), width=3)
    d.line([x0 + 400, y0 + 82, x0 + 420, y0 + 108], fill=(110, 72, 40), width=3)
    # globe
    gx, gy = x0 + 150, y0 + 48
    d.ellipse([gx - 42, gy - 42, gx + 42, gy + 42], fill=(52, 130, 190))
    d.ellipse([gx - 30, gy - 26, gx - 2, gy + 4], fill=(96, 168, 92))
    d.ellipse([gx + 4, gy + 8, gx + 30, gy + 30], fill=(96, 168, 92))
    d.ellipse([gx + 8, gy - 34, gx + 30, gy - 12], fill=(96, 168, 92))
    dashed_circle(d, gx, gy, 52, (178, 34, 34))
    # three small summit flags
    for fx, col in [(300, (178, 34, 34)), (350, (20, 90, 70)), (400, (30, 60, 120))]:
        d.line([x0 + fx, y0 + 22, x0 + fx, y0 + 66], fill=(60, 60, 60), width=3)
        d.polygon([(x0 + fx, y0 + 22), (x0 + fx + 34, y0 + 30),
                   (x0 + fx, y0 + 38)], fill=col)


def pic_tower(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 210))
    d.ellipse([x0 + 40, y0 + 12, x0 + 84, y0 + 56], fill=(255, 196, 66))
    # tallest tower, tapering
    tx = x0 + 210
    d.polygon([(tx - 34, y0 + h), (tx - 18, y0 + 12), (tx + 18, y0 + 12),
               (tx + 34, y0 + h)], fill=(52, 66, 96))
    for wy in range(22, 100, 14):
        half = 16 - (wy - 22) // 8
        d.rectangle([tx - half, y0 + wy, tx + half, y0 + wy + 6],
                    fill=(255, 214, 90))
    d.line([tx, y0 + 2, tx, y0 + 12], fill=(52, 66, 96), width=3)
    # drone approaching from the right
    cx, cy = x0 + 372, y0 + 36
    d.rectangle([cx - 18, cy - 4, cx + 18, cy + 4], fill=(40, 40, 46))
    d.line([cx - 28, cy - 10, cx + 28, cy - 10], fill=(40, 40, 46), width=3)
    d.line([cx - 28, cy + 10, cx + 28, cy + 10], fill=(40, 40, 46), width=3)
    # warning triangle
    wx, wy = x0 + 76, y0 + 76
    d.polygon([(wx, wy - 20), (wx - 22, wy + 16), (wx + 22, wy + 16)],
              fill=(255, 176, 32), outline=(178, 34, 34), width=2)
    d.rectangle([wx - 2, wy - 10, wx + 2, wy + 4], fill=(178, 34, 34))
    d.ellipse([wx - 2, wy + 8, wx + 2, wy + 12], fill=(178, 34, 34))


def pic_memorial(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(44, 38, 58))
    # row of candles with flames
    for cx in (90, 160, 230, 300, 370):
        d.rectangle([x0 + cx - 8, y0 + 62, x0 + cx + 8, y0 + 100],
                    fill=(240, 234, 220))
        d.ellipse([x0 + cx - 6, y0 + 42, x0 + cx + 6, y0 + 60],
                  fill=(255, 176, 32))
        d.ellipse([x0 + cx - 3, y0 + 48, x0 + cx + 3, y0 + 58],
                  fill=(255, 110, 30))
    # poppies
    for px, py in [(420, 44), (50, 36), (440, 84)]:
        for ox, oy in [(-7, 0), (7, 0), (0, -7), (0, 7)]:
            d.ellipse([x0 + px + ox - 6, y0 + py + oy - 6,
                       x0 + px + ox + 6, y0 + py + oy + 6], fill=(178, 34, 34))
        d.ellipse([x0 + px - 4, y0 + py - 4, x0 + px + 4, y0 + py + 4],
                  fill=(30, 30, 30))
    # bowed-head silhouette between the candles
    d.ellipse([x0 + 265 - 12, y0 + 8, x0 + 265 + 12, y0 + 32], fill=(20, 18, 28))
    d.polygon([(x0 + 247, y0 + 40), (x0 + 283, y0 + 40), (x0 + 291, y0 + 62),
               (x0 + 239, y0 + 62)], fill=(20, 18, 28))


def pic_cyber(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 26, 44))
    # code lines on the left
    for i, (lw, col) in enumerate([(150, (90, 200, 120)), (110, (200, 205, 215)),
                                   (170, (90, 200, 120)), (90, (200, 205, 215))]):
        d.rectangle([x0 + 24, y0 + 18 + i * 20, x0 + 24 + lw, y0 + 26 + i * 20],
                    fill=col)
    # padlock
    lx, ly = x0 + 330, y0 + 54
    d.arc([lx - 26, ly - 34, lx + 26, ly + 6], start=180, end=360,
          fill=GOLD, width=7)
    d.rectangle([lx - 34, ly - 4, lx + 34, ly + 38], fill=GOLD)
    d.ellipse([lx - 6, ly + 6, lx + 6, ly + 18], fill=NAVY)
    d.rectangle([lx - 3, ly + 14, lx + 3, ly + 28], fill=NAVY)
    # red warning slash across the lock
    d.line([lx - 44, ly + 44, lx + 44, ly - 36], fill=(220, 60, 60), width=6)


def pic_court(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(228, 232, 238))
    # courthouse: pediment, columns, steps
    cx = x0 + 190
    d.polygon([(cx - 110, y0 + 34), (cx, y0 + 8), (cx + 110, y0 + 34)],
              fill=(120, 96, 60))
    d.rectangle([cx - 110, y0 + 34, cx + 110, y0 + 42], fill=(90, 72, 44))
    for ox in (-88, -44, 0, 44, 88):
        d.rectangle([cx + ox - 8, y0 + 42, cx + ox + 8, y0 + 92],
                    fill=(245, 244, 238))
    d.rectangle([cx - 118, y0 + 92, cx + 118, y0 + 100], fill=(90, 72, 44))
    # gavel on the right
    gx, gy = x0 + 390, y0 + 58
    d.rectangle([gx - 34, gy - 12, gx + 10, gy + 12], fill=(110, 72, 40))
    d.rectangle([gx + 10, gy - 4, gx + 44, gy + 4], fill=(140, 96, 52))
    d.rectangle([gx - 26, gy + 16, gx + 30, gy + 24], fill=(90, 72, 44))


PICS = {"sea": pic_sea, "summit": pic_summit, "tower": pic_tower,
        "memorial": pic_memorial, "cyber": pic_cyber, "court": pic_court}

for i, (accent, headline, fact, key) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = MARGIN + col * (CARD_W + GAP)
    y0 = 136 + row * (CARD_H + GAP)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + CARD_H], fill=CARD,
                outline=BORDER, width=1)
    d.rectangle([x0, y0, x0 + CARD_W, y0 + 6], fill=accent)
    PICS[key](x0, y0 + 6, CARD_W, 108)
    # number badge
    bx, by = x0 + 14, y0 + 20
    d.ellipse([bx, by, bx + 34, by + 34], fill=accent)
    num = str(i + 1)
    d.text((bx + 17 - d.textlength(num, font=f_num) / 2, by + 4),
           num, font=f_num, fill=(255, 255, 255))
    # headline (max 2 lines) + fact (max 2 lines)
    head_lines = wrap(d, headline, f_head, CARD_W - 32)
    fact_lines = wrap(d, fact, f_fact, CARD_W - 32)
    print(f"card {i + 1}: headline {len(head_lines)} lines, "
          f"fact {len(fact_lines)} lines")
    ty = y0 + 126
    for ln in head_lines[:2]:
        d.text((x0 + 16, ty), ln, font=f_head, fill=INK)
        ty += 37
    ty = y0 + 126 + 76
    for ln in fact_lines[:2]:
        d.text((x0 + 16, ty), ln, font=f_fact, fill=GREY)
        ty += 24

# ---------------- footer ----------------
f_foot = font(REGULAR, 18)
foot = "Six stories, one day - 25 November 2026 - Sources: Reuters, BBC, RFE/RL"
d.text(((W - d.textlength(foot, font=f_foot)) / 2, 988),
       foot, font=f_foot, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
print("bytes:", os.path.getsize("entry.png"))
