#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: an editorial infographic summing up
Thursday 19 November 2026's world news in one 1024x1024 PNG.

Stories verified from reporting published on 19 Nov 2026 (White House /
Al Jazeera, Bloomberg, Reuters, CNN, NASA, TradingView). No network needed.
Run: python3 make_image.py  ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 241, 230)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
GOLD = (233, 196, 106)
RED = (178, 34, 34)
GREY = (90, 90, 84)
CARD = (255, 255, 255)
BORDER = (216, 210, 192)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 38)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_TAG = font("DejaVuSans-Bold.ttf", 19)
F_KICK = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 20)
F_SRC = font("DejaVuSans.ttf", 15)
F_FOOT = font("DejaVuSans-Bold.ttf", 18)
F_FOOT2 = font("DejaVuSans.ttf", 14)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_globe(d, cx, cy, r, color, w=3):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=color, width=2)


def draw_radar(d, x, y, s, color):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r / 2, cy - r / 2, cx + r / 2, cy + r / 2],
              outline=color, width=2)
    d.line([cx, cy, cx + r * 0.8, cy - r * 0.6], fill=color, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)
    for bx, by in ((cx - r * 0.55, cy + r * 0.3), (cx + r * 0.5, cy + r * 0.55)):
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=color)


def draw_flags(d, x, y, s, color):
    for i, fc in enumerate(((220, 60, 60), (40, 120, 200), (40, 160, 90))):
        px = x + (0.14 + 0.28 * i) * s
        d.line([px, y + 0.2 * s, px, y + 0.85 * s], fill=color, width=4)
        d.polygon([(px, y + 0.2 * s), (px + 0.22 * s, y + 0.3 * s),
                   (px, y + 0.42 * s)], fill=fc)


def draw_parliament(d, x, y, s, color):
    d.polygon([(x + 0.08 * s, y + 0.38 * s), (x + 0.5 * s, y + 0.08 * s),
               (x + 0.92 * s, y + 0.38 * s)], fill=color)
    for i in range(3):
        cx = x + (0.22 + 0.28 * i) * s
        d.rectangle([cx - 0.05 * s, y + 0.44 * s, cx + 0.05 * s, y + 0.78 * s],
                    fill=color)
    d.rectangle([x + 0.08 * s, y + 0.78 * s, x + 0.92 * s, y + 0.88 * s],
                fill=color)


def draw_chart(d, x, y, s, color):
    # ascending bars + trend arrow
    base = y + 0.85 * s
    for i, h in enumerate((0.22, 0.38, 0.52, 0.72)):
        bx = x + (0.10 + 0.22 * i) * s
        d.rectangle([bx, base - h * s, bx + 0.14 * s, base], fill=color)
    d.line([x + 0.08 * s, base - 0.18 * s, x + 0.9 * s, base - 0.78 * s],
           fill=color, width=4)
    d.polygon([(x + 0.9 * s, base - 0.78 * s), (x + 0.72 * s, base - 0.78 * s),
               (x + 0.9 * s, base - 0.58 * s)], fill=color)


def draw_city(d, x, y, s, color):
    # skyline with a sun over the towers
    d.ellipse([x + 0.62 * s, y + 0.06 * s, x + 0.88 * s, y + 0.32 * s],
              fill=(230, 180, 40))
    for bx, bw, bh in ((0.06, 0.20, 0.55), (0.30, 0.18, 0.75),
                       (0.52, 0.22, 0.45), (0.76, 0.16, 0.62)):
        d.rectangle([x + bx * s, y + (0.9 - bh) * s, x + (bx + bw) * s,
                     y + 0.9 * s], fill=color)
    d.line([x + 0.05 * s, y + 0.9 * s, x + 0.95 * s, y + 0.9 * s],
           fill=color, width=3)


def draw_dish(d, x, y, s, color):
    # satellite dish on a mount, beaming skyward
    d.arc([x + 0.08 * s, y + 0.10 * s, x + 0.92 * s, y + 0.95 * s],
          180, 360, fill=color, width=5)
    d.line([x + 0.5 * s, y + 0.55 * s, x + 0.5 * s, y + 0.92 * s],
           fill=color, width=5)
    d.line([x + 0.28 * s, y + 0.92 * s, x + 0.72 * s, y + 0.92 * s],
           fill=color, width=5)
    d.line([x + 0.62 * s, y + 0.32 * s, x + 0.88 * s, y + 0.06 * s],
           fill=color, width=3)
    d.ellipse([x + 0.84 * s, y + 0.02 * s, x + 0.94 * s, y + 0.12 * s],
              fill=color)


ICONS = {"flags": draw_flags, "chart": draw_chart, "city": draw_city,
         "radar": draw_radar, "parliament": draw_parliament,
         "dish": draw_dish}

STORIES = [
    dict(kick="DIPLOMACY  \u2022  TRILATERAL", color=(37, 99, 235), icon="flags",
         head="Trump, Xi and Putin meet in Shenzhen \u2014 a first",
         body=("The three leaders sat down together for the first time, "
               "at APEC in Shenzhen. Nuclear arms and the Iran war topped "
               "the agenda; no deal was expected."),
         src="White House  \u2022  Al Jazeera"),
    dict(kick="MARKETS  \u2022  IPO", color=(217, 119, 6), icon="chart",
         head="Anthropic debuts on Nasdaq in the biggest IPO ever",
         body=("The Claude maker priced at $83 a share, raising $81.3bn. "
               "Shares start trading Thursday under ANT, valuing it "
               "near $1.5 trillion."),
         src="Bloomberg  \u2022  TradingView"),
    dict(kick="CULTURE  \u2022  GAMING", color=(219, 39, 119), icon="city",
         head="GTA VI begins its global rollout; Vice City opens",
         body=("After 13 years, Rockstar's game unlocked at midnight in "
               "New Zealand and rolled around the world, earning "
               "a 99 on Metacritic."),
         src="Reuters"),
    dict(kick="MIDDLE EAST  \u2022  GULF WAR", color=(220, 38, 38),
         icon="radar",
         head="Iran fires on a US base in Kuwait",
         body=("Iranian drones targeted Ali Al Salem air base, the first "
               "attack on Kuwait since September. Bahrain intercepted "
               "a third attack in a week."),
         src="Reuters  \u2022  BBC"),
    dict(kick="US POLITICS  \u2022  CONGRESS", color=(124, 58, 237),
         icon="parliament",
         head="Democrats nominate Jeffries for Speaker, 251\u201311",
         body=("Hakeem Jeffries won the caucus vote and is in line to "
               "become the first Black Speaker when the new Congress "
               "meets on 3 January."),
         src="CNN  \u2022  Reuters"),
    dict(kick="SCIENCE  \u2022  SPACE", color=(13, 148, 136), icon="dish",
         head="NASA confirms Voyager 1 one light-day away",
         body=("The 1977 probe is the first human-made object a full "
               "light-day from Earth \u2014 16 billion miles. A radio "
               "signal now takes a day to reach it."),
         src="NASA  \u2022  Popular Science"),
]

FOOTER = ("ALSO TODAY  \u2014  Canada adjusts China ties  \u2022  "
          "Amazon pledges $7bn for renewables  \u2022  AI cyber threats "
          "outpace defences")
FOOTER2 = "Sources: Reuters, Bloomberg, CNN, NASA, White House, TradingView"


def draw_panel(d, x, y, w, h, st):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=BORDER, width=1)
    # accent bar
    d.rounded_rectangle([x, y, x + w, y + 7], radius=3, fill=st["color"])
    d.rectangle([x, y + 4, x + w, y + 7], fill=st["color"])
    # icon box top-right (small, clear of the headline below it)
    ix, iy, isz = x + w - 66, y + 14, 48
    d.rounded_rectangle([ix, iy, ix + isz, iy + isz], radius=10,
                        fill=st["color"])
    ICONS[st["icon"]](d, ix + 5, iy + 5, isz - 10, (255, 255, 255))
    # kicker (kept clear of the icon)
    d.text((x + 18, y + 24), st["kick"], font=F_KICK, fill=st["color"])
    # headline (max 2 lines), starting below the icon row
    hl = wrap(d, st["head"], F_HEAD, w - 36)
    hy = y + 72
    for line in hl[:2]:
        d.text((x + 18, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    # body (max 3 lines)
    bl = wrap(d, st["body"], F_BODY, w - 36)
    by = hy + 6
    for line in bl[:3]:
        d.text((x + 18, by), line, font=F_BODY, fill=(51, 51, 51))
        by += 26
    # source
    d.text((x + 18, y + h - 30), st["src"], font=F_SRC, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 124], fill=NAVY)
    draw_globe(d, 968, 62, 30, GOLD)
    d.text((28, 20), "THE WORLD IN ONE PICTURE", font=F_TITLE, fill=(255, 255, 255))
    d.text((28, 76), "THURSDAY, 19 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.text((718, 30), "6 STORIES THAT", font=F_TAG, fill=(200, 205, 220))
    d.text((718, 54), "DEFINED THE DAY", font=F_TAG, fill=(200, 205, 220))
    d.text((718, 84), "ONE DAY \u2022 ONE IMAGE", font=F_TAG, fill=GOLD)
    d.rectangle([0, 124, W, 130], fill=RED)
    # grid of panels
    mx, gap = 16, 12
    pw = (W - 2 * mx - gap) // 2
    top, bot = 146, 946
    ph = (bot - top - 2 * gap) // 3
    for i, st in enumerate(STORIES):
        cx = mx + (i % 2) * (pw + gap)
        cy = top + (i // 2) * (ph + gap)
        draw_panel(d, cx, cy, pw, ph, st)
    # footer (shrink ticker font until it fits)
    d.rectangle([0, 958, W, H], fill=NAVY)
    fsize = 18
    while fsize > 12:
        ff = font("DejaVuSans-Bold.ttf", fsize)
        if d.textlength(FOOTER, font=ff) <= W - 56:
            break
        fsize -= 1
    d.text((28, 968), FOOTER, font=ff, fill=(255, 255, 255))
    d.text((28, 996), FOOTER2, font=F_FOOT2, fill=(180, 185, 200))
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
