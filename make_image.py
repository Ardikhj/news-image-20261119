#!/usr/bin/env python3
"""Draw the 1024x1024 "world news in one image" poster for 19 November 2026.

Run:  python3 make_image.py            # writes entry.png next to this file
The output is deterministic: fixed fonts, fixed layout, same bytes every run.

Layout: a navy masthead, six story cards in a 2 x 3 grid, and a navy footer
strip. Every story is drawn from the STORIES table below; nothing is fetched
from the network.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = Path(__file__).resolve().parent

NAVY = (15, 29, 62)
GOLD = (232, 169, 61)
CREAM = (246, 241, 231)
INK = (24, 33, 51)
BODY = (38, 48, 66)
GREY = (107, 114, 128)
WHITE = (255, 255, 255)
SOFT = (203, 213, 225)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


FONTS = {
    "masthead": font(SERIF_B, 34),
    "date": font(SANS_B, 28),
    "side": font(SANS_B, 23),
    "side_gold": font(SANS_B, 20),
    "kicker": font(SANS_B, 21),
    "headline": font(SERIF_B, 28),
    "body": font(SANS, 20),
    "source": font(SANS, 17),
    "foot": font(SANS_B, 18),
    "foot_src": font(SANS, 15),
}

# (kicker, headline, body, sources, accent colour, icon kind)
STORIES = [
    (
        "DIPLOMACY  \u2022  TRILATERAL",
        "Trump, Xi and Putin meet in Shenzhen \u2014 a first",
        "The three leaders sat down together for the first time, at APEC in "
        "Shenzhen. Nuclear arms and the Iran war topped the agenda; no deal "
        "was expected.",
        "White House  \u2022  Al Jazeera",
        (37, 99, 235),
        "bars",
    ),
    (
        "MARKETS  \u2022  IPO",
        "Anthropic debuts on Nasdaq in the biggest IPO ever",
        "The Claude maker priced at $83 a share, raising $81.3bn. Shares "
        "start trading Thursday under ANT, valuing it near $1.5tn.",
        "Bloomberg  \u2022  TradingView",
        (234, 122, 31),
        "chart",
    ),
    (
        "CULTURE  \u2022  GAMING",
        "GTA VI begins its global rollout; Vice City opens",
        "After 13 years, Rockstar's game unlocked at midnight in New Zealand "
        "and rolled around the world, earning a 99 on Metacritic.",
        "Reuters",
        (219, 39, 119),
        "pad",
    ),
    (
        "MIDDLE EAST  \u2022  GULF WAR",
        "Iran fires on a US base in Kuwait",
        "Iranian drones targeted Ali Al Salem air base, the first attack on "
        "Kuwait since September. Bahrain intercepted a third attack in a week.",
        "Reuters  \u2022  BBC",
        (220, 38, 38),
        "target",
    ),
    (
        "US POLITICS  \u2022  CONGRESS",
        "Democrats nominate Jeffries for Speaker, 251\u201311",
        "Hakeem Jeffries won the caucus vote and is in line to become the "
        "first Black Speaker when the new Congress meets on 3 January.",
        "CNN  \u2022  Reuters",
        (124, 58, 237),
        "capitol",
    ),
    (
        "SCIENCE  \u2022  SPACE",
        "NASA confirms Voyager 1 one light-day away",
        "The 1977 probe is the first human-made object a full light-day from "
        "Earth \u2014 16 billion miles. A radio signal now takes a day to "
        "reach it.",
        "NASA  \u2022  Popular Science",
        (13, 148, 136),
        "planet",
    ),
]

FOOTER_ITEMS = (
    "Canada adjusts China ties",
    "Amazon pledges $7bn for renewables",
    "AI cyber threats outpace defences",
)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def wrap_first_narrow(draw, text, fnt, first_w, rest_w):
    """Wrap with a narrower first line (room for the icon tile), then full
    width; returns every line, never dropping words."""
    lines, current, limit = [], "", first_w
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
            limit = rest_w
    if current:
        lines.append(current)
    return lines


def shrink_to_fit(draw, text, fnt, max_width, min_size=12):
    """Return a font shrunk until the text fits max_width."""
    size = fnt.size
    path = fnt.path
    while draw.textlength(text, font=fnt) > max_width and size > min_size:
        size -= 1
        fnt = ImageFont.truetype(path, size)
    return fnt


def draw_icon(draw, kind, x0, y0, size, colour):
    """A rounded accent tile with a white pictogram drawn from primitives."""
    draw.rounded_rectangle([x0, y0, x0 + size, y0 + size], radius=10,
                           fill=colour)
    cx, cy = x0 + size // 2, y0 + size // 2
    w = WHITE
    if kind == "bars":  # three figures: bars with heads
        for i, hgt in enumerate((16, 26, 20)):
            bx = x0 + 12 + i * 11
            draw.ellipse([bx + 1, y0 + 26 - hgt, bx + 7, y0 + 32 - hgt],
                         fill=w)
            draw.rounded_rectangle([bx, y0 + 32 - hgt + 4, bx + 8,
                                    y0 + 42], radius=3, fill=w)
    elif kind == "chart":  # ascending bars
        for i, hgt in enumerate((10, 17, 24, 31)):
            bx = x0 + 10 + i * 10
            draw.rectangle([bx, y0 + 42 - hgt, bx + 7, y0 + 42], fill=w)
        draw.line([x0 + 9, y0 + 14, x0 + 44, y0 + 14], fill=w, width=2)
    elif kind == "pad":  # game controller
        draw.rounded_rectangle([x0 + 9, y0 + 16, x0 + 45, y0 + 38],
                               radius=8, outline=w, width=3)
        draw.line([x0 + 17, y0 + 27, x0 + 25, y0 + 27], fill=w, width=3)
        draw.line([x0 + 21, y0 + 23, x0 + 21, y0 + 31], fill=w, width=3)
        draw.ellipse([x0 + 31, y0 + 22, x0 + 35, y0 + 26], fill=w)
        draw.ellipse([x0 + 36, y0 + 28, x0 + 40, y0 + 32], fill=w)
    elif kind == "target":  # concentric rings
        for r in (15, 10, 5):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w,
                         width=3)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=w)
    elif kind == "capitol":  # dome, columns, base
        draw.pieslice([cx - 12, cy - 16, cx + 12, cy + 2], start=180,
                      end=360, fill=w)
        draw.rectangle([cx - 13, cy - 2, cx + 13, cy + 1], fill=w)
        for i in (-1, 0, 1):
            draw.rectangle([cx + i * 9 - 2, cy + 4, cx + i * 9 + 2, cy + 13],
                           fill=w)
        draw.rectangle([cx - 15, cy + 14, cx + 15, cy + 17], fill=w)
    elif kind == "planet":  # ringed planet
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=w)
        draw.line([x0 + 6, cy + 8, x0 + 48, cy - 8], fill=w, width=4)
        draw.ellipse([x0 + 40, y0 + 10, x0 + 43, y0 + 13], fill=w)


def draw_card(base, x, y, w, h, story):
    kicker, headline, body, sources, accent, icon = story
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=12,
                        fill=WHITE + (255,))
    d.rectangle([0, 0, w - 1, 7], fill=accent + (255,))
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, w - 1, h - 1], radius=12, fill=255)
    layer.putalpha(mask)

    pad = 20
    text_w = w - 2 * pad
    d.text((pad, 22), kicker, font=FONTS["kicker"], fill=accent + (255,))
    draw_icon(d, icon, w - pad - 54, 16, 54, accent)

    # Headline: try 28pt, then 26pt, until it fits in two lines with the
    # first line narrowed to clear the icon tile.
    head_font, head_lines = FONTS["headline"], []
    for size in (28, 26, 24):
        fnt = font(SERIF_B, size)
        lines = wrap_first_narrow(d, headline, fnt, text_w - 60, text_w)
        if len(lines) <= 2:
            head_font, head_lines = fnt, lines
            break
    else:
        head_font = font(SERIF_B, 24)
        head_lines = head_lines[:2]
    hy = 56
    for line in head_lines:
        d.text((pad, hy), line, font=head_font, fill=INK + (255,))
        hy += 34

    # Body: 20pt, dropping to 19pt if it would need a fifth line.
    body_lines = wrap(d, body, FONTS["body"], text_w)
    body_font = FONTS["body"]
    if len(body_lines) > 4:
        body_font = font(SANS, 19)
        body_lines = wrap(d, body, body_font, text_w)[:4]
    else:
        body_lines = body_lines[:4]
    by = hy + 6
    for line in body_lines:
        d.text((pad, by), line, font=body_font, fill=BODY + (255,))
        by += 25

    d.text((pad, h - 28), sources, font=FONTS["source"],
           fill=GREY + (255,))
    base.paste(layer, (x, y), layer)


def draw_masthead(draw):
    draw.rectangle([0, 0, W - 1, 117], fill=NAVY)
    draw.rectangle([0, 118, W - 1, 121], fill=GOLD)
    draw.text((26, 14), "THE WORLD IN ONE PICTURE",
              font=FONTS["masthead"], fill=WHITE)
    draw.text((26, 64), "THURSDAY, 19 NOVEMBER 2026",
              font=FONTS["date"], fill=GOLD)
    draw.text((692, 16), "6 STORIES THAT", font=FONTS["side"], fill=WHITE)
    draw.text((692, 44), "DEFINED THE DAY", font=FONTS["side"], fill=WHITE)
    draw.text((692, 76), "ONE DAY \u2022 ONE IMAGE",
              font=FONTS["side_gold"], fill=GOLD)
    # wireframe globe, top right
    gx, gy, gr = 954, 56, 27
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=GOLD,
                 width=3)
    draw.ellipse([gx - 12, gy - gr, gx + 12, gy + gr], outline=GOLD,
                 width=2)
    draw.line([gx - gr, gy, gx + gr, gy], fill=GOLD, width=2)
    draw.line([gx - 26, gy - 15, gx + 26, gy - 15], fill=GOLD, width=2)
    draw.line([gx - 26, gy + 15, gx + 26, gy + 15], fill=GOLD, width=2)


def draw_footer(draw):
    draw.rectangle([0, 950, W - 1, H - 1], fill=NAVY)
    line = "ALSO TODAY  \u2014  " + "  \u2022  ".join(FOOTER_ITEMS)
    fnt = shrink_to_fit(draw, line, FONTS["foot"], W - 52)
    draw.text((26, 960), line, font=fnt, fill=WHITE)
    draw.text((26, 990), "Sources: Reuters, Bloomberg, CNN, NASA, "
              "White House, TradingView",
              font=FONTS["foot_src"], fill=SOFT)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    margin, gap = 16, 14
    card_w = (W - 2 * margin - gap) // 2
    card_h = 260
    for i, story in enumerate(STORIES):
        x = margin + (i % 2) * (card_w + gap)
        y = 132 + (i // 2) * (card_h + gap)
        draw_card(img, x, y, card_w, card_h, story)
    draw_footer(ImageDraw.Draw(img))
    out = HERE / "entry.png"
    img.save(out)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
