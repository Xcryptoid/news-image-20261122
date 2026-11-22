"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Deterministic: same inputs always produce byte-identical output.
Run: python3 draw.py  -> writes entry.png in this directory.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
INK = (26, 26, 26)
PAPER = (246, 241, 229)
RED = (163, 18, 18)
GREY = (90, 86, 76)
SKY = (38, 52, 84)
ORANGE = (232, 122, 32)
GOLD = (212, 160, 44)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", 62)
SERIF = ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", 21)
SANS_B = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 30)
SANS_B_SM = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 25)
SANS = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 20)
SANS_SM = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 16)
KICKER = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 15)
DATE_F = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 17)


def wrap(draw, text, font, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, font, max_w)
    lh = leading or int(font.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=INK, width=2)


def kicker_line(draw, x, y, text):
    draw.text((x, y), text, font=KICKER, fill=RED)
    return y + 22


def draw_bahrain(d, x, y, w, h):
    """Night sky, skyline, missile trails and a jagged explosion burst."""
    import math
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # stars
    for sx, sy in [(18, 14), (60, 30), (120, 10), (180, 26), (240, 12),
                   (300, 34), (40, 55), (210, 48), (330, 16), (150, 58)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(240, 238, 220))
    # skyline silhouette
    base = y + h
    for bx, bw, bh in [(0, 42, 70), (48, 30, 95), (84, 46, 60), (136, 34, 105),
                       (176, 44, 78), (226, 30, 92), (262, 40, 64), (308, 36, 88)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(16, 20, 36))
        for wy in range(base - bh + 10, base - 8, 16):
            d.rectangle([x + bx + 6, wy, x + bx + 12, wy + 7], fill=(232, 190, 90))
    # missile trails: parabolic arcs kept inside the box
    for (x0, y0, x1, y1, lift) in [(30, 150, 250, 40, 90), (80, 170, 300, 70, 110)]:
        pts = []
        for i in range(21):
            t = i / 20
            px = x + x0 + (x1 - x0) * t
            py = y + y0 + (y1 - y0) * t - lift * 4 * t * (1 - t)
            pts.append((px, py))
        d.line(pts, fill=(245, 245, 240), width=3)
    # jagged explosion burst (not a sun: irregular spikes, no round disc)
    cx, cy = x + w - 78, y + 62
    spikes = []
    for i in range(24):
        ang = math.radians(i * 15)
        r = (58, 34, 26)[i % 3]
        spikes.append((cx + int(r * math.cos(ang)), cy + int(r * math.sin(ang))))
    d.polygon(spikes, fill=ORANGE)
    # small hot core only — the earlier 26px disc made it read as a sun
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(252, 226, 140))


def draw_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 226))
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 14
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 178, 205), outline=INK, width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=INK, width=1)
    d.line([cx - r, cy, cx + r, cy], fill=INK, width=1)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], start=0, end=360, fill=INK, width=1)
    # irregular land blobs (polygons, kept inside the globe)
    d.polygon([(cx - r + 14, cy - r + 22), (cx - r + 34, cy - r + 10),
               (cx - 12, cy - r + 18), (cx - 8, cy - 4), (cx - r + 10, cy - 2)],
              fill=(96, 160, 96))
    d.polygon([(cx + 4, cy + 8), (cx + 22, cy + 2), (cx + r - 16, cy + 14),
               (cx + r - 20, cy + r - 20), (cx + 10, cy + r - 16), (cx - 2, cy + 24)],
              fill=(96, 160, 96))
    # sun / heat
    d.ellipse([x + w - 46, y + 12, x + w - 18, y + 40], fill=GOLD, outline=INK, width=1)


def draw_badge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 224, 216))
    cx, cy = x + w // 2, y + h // 2
    # shield
    d.polygon([(cx - 52, cy - 44), (cx + 52, cy - 44), (cx + 52, cy + 6),
               (cx, cy + 52), (cx - 52, cy + 6)], fill=(52, 84, 140), outline=INK, width=2)
    d.text((cx - 8, cy - 26), "*", font=ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 52), fill=(240, 238, 220))


def draw_ruins(d, x, y, w, h):
    """Damaged skyline, drawn strictly inside the given box."""
    d.rectangle([x, y, x + w, y + h], fill=(228, 220, 204))
    base = y + h
    # damaged buildings, all within [x, x+w]
    d.polygon([(x + 8, base), (x + 8, base - 88), (x + 34, base - 104),
               (x + 52, base - 78), (x + 52, base)], fill=(120, 112, 98), outline=INK)
    d.rectangle([x + 62, base - 66, x + 104, base], fill=(140, 132, 116), outline=INK)
    d.polygon([(x + 112, base), (x + 112, base - 96), (x + 134, base - 80),
               (x + 148, base - 102), (x + 158, base - 72), (x + 158, base)],
              fill=(110, 102, 88), outline=INK)
    # smoke puffs above the broken roofs
    for sx, sy, sr in [(x + 30, y + 22, 11), (x + 48, y + 12, 13), (x + 132, y + 26, 10)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(160, 156, 146))
    # rubble at the base
    for rx, rw in [(x + 14, 20), (x + 70, 26), (x + 122, 18)]:
        d.polygon([(rx, base), (rx + rw // 2, base - 10), (rx + rw, base)], fill=(90, 84, 72))


def draw_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    # grid
    for gy in range(y + 18, y + h - 10, 26):
        d.line([x + 10, gy, x + w - 10, gy], fill=(220, 220, 214), width=1)
    # falling line (starts below the -3.7% label)
    pts = []
    n = 9
    for i in range(n):
        px = x + 16 + i * (w - 32) // (n - 1)
        py = y + 36 + int((h - 64) * (i / (n - 1)) ** 1.25)
        pts.append((px, py))
    d.line(pts, fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    # arrow head at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey + 12), (ex - 10, ey - 4), (ex + 10, ey - 4)], fill=RED)
    d.text((x + 14, y + 6), "-3.7%", font=ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 22), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=SERIF_B)
    d.text(((W - tw) / 2, 14), title, font=SERIF_B, fill=INK)
    d.line([MARGIN, 88, W - MARGIN, 88], fill=INK, width=2)
    date_line = "SUNDAY, 22 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE PAGE"
    dw = d.textlength(date_line, font=DATE_F)
    d.text(((W - dw) / 2, 96), date_line, font=DATE_F, fill=RED)
    d.line([MARGIN, 124, W - MARGIN, 124], fill=INK, width=1)

    # ---- lead: Iran strikes Bahrain ----
    lx, ly, lw, lh = MARGIN, 136, W - 2 * MARGIN, 268
    panel(d, lx, ly, lw, lh)
    ix, iy, iw, ih = lx + lw - 372, ly + 12, 360, 244
    draw_bahrain(d, ix, iy, iw, ih)
    tx = lx + 16
    y = kicker_line(d, tx, ly + 12, "GULF  •  CONFLICT  —  LEAD STORY")
    y = draw_wrapped(d, tx, y + 2, "IRAN STRIKES U.S. BASES IN BAHRAIN", SANS_B, 560, leading=38)
    y = draw_wrapped(d, tx, y + 8,
                     "Missiles and drones hit an industrial site; Bahrain says a civilian facility was damaged and two people were hurt. Tehran claims it destroyed two U.S. Patriot radars.",
                     SANS, 560, leading=26)
    d.text((tx, ly + lh - 30), "Reuters  •  AFP  •  Al Jazeera",
           font=SANS_SM, fill=GREY)

    # ---- row 2 ----
    ry, rh = 416, 232
    cw = (W - 2 * MARGIN - 12) // 2
    # COP31
    x = MARGIN
    panel(d, x, ry, cw, rh)
    ix, iy, iw, ih = x + cw - 176, ry + 10, 164, 150
    draw_globe(d, ix, iy, iw, ih)
    y = kicker_line(d, x + 14, ry + 12, "CLIMATE  •  ANTALYA")
    y = draw_wrapped(d, x + 14, y + 2, "COP31 IN OVERTIME IN FOSSIL-FUEL ROW", SANS_B_SM, cw - 200, leading=30)
    y = draw_wrapped(d, x + 14, y + 6,
                     "Climate talks run into a second day of overtime with no deal. The EU objects to a text with no mention of fossil fuels.",
                     SANS_SM, cw - 200, leading=21)
    # El Chapo Isidro
    x = MARGIN + cw + 12
    panel(d, x, ry, cw, rh)
    ix, iy, iw, ih = x + cw - 176, ry + 10, 164, 150
    draw_badge(d, ix, iy, iw, ih)
    y = kicker_line(d, x + 14, ry + 12, "MEXICO  •  JUSTICE")
    y = draw_wrapped(d, x + 14, y + 2, "'EL CHAPO ISIDRO' CAPTURED IN SINALOA", SANS_B_SM, cw - 200, leading=30)
    y = draw_wrapped(d, x + 14, y + 6,
                     "Special forces seize Fausto Isidro Meza Flores, on the FBI's ten most wanted list. Eleven die in the raid, four of them soldiers.",
                     SANS_SM, cw - 200, leading=21)

    # ---- row 3 ----
    ry, rh = 660, 232
    # Kryvyi Rih
    x = MARGIN
    panel(d, x, ry, cw, rh)
    ix, iy, iw, ih = x + cw - 176, ry + 10, 164, 150
    draw_ruins(d, ix, iy, iw, ih)
    y = kicker_line(d, x + 14, ry + 12, "UKRAINE  •  WAR")
    y = draw_wrapped(d, x + 14, y + 2, "MISSILE HITS KRYVYI RIH", SANS_B_SM, cw - 200, leading=30)
    y = draw_wrapped(d, x + 14, y + 6,
                     "Russian strike on Zelenskyy's hometown kills two, including a 7-year-old boy, and wounds 60. A cargo ship burns in the Baltic after a suspected drone attack.",
                     SANS_SM, cw - 200, leading=21)
    # Markets
    x = MARGIN + cw + 12
    panel(d, x, ry, cw, rh)
    ix, iy, iw, ih = x + cw - 176, ry + 10, 164, 150
    draw_chart(d, ix, iy, iw, ih)
    y = kicker_line(d, x + 14, ry + 12, "MARKETS  •  ECONOMY")
    y = draw_wrapped(d, x + 14, y + 2, "AI SELL-OFF DRAGS U.S. STOCKS INTO CORRECTION", SANS_B_SM, cw - 200, leading=30)
    y = draw_wrapped(d, x + 14, y + 6,
                     "The S&P 500 falls 3.7% and the Nasdaq 5.3% on Friday as the AI rout spreads to Japan and South Korea.",
                     SANS_SM, cw - 200, leading=21)

    # ---- in brief strip ----
    by = 904
    panel(d, MARGIN, by, W - 2 * MARGIN, 96)
    d.text((MARGIN + 14, by + 10), "IN BRIEF", font=KICKER, fill=RED)
    briefs = [
        "EU and Indonesia sign a landmark trade deal, cutting tariffs on up to 98.5% of goods.",
        "A magnitude 6.8 earthquake shakes Peru's central Andean region.",
        "Fire at a candy factory in Cikande, Indonesia, kills three; 36 workers are still missing.",
    ]
    col_w = (W - 2 * MARGIN - 28) // 3
    for i, b in enumerate(briefs):
        bx = MARGIN + 14 + i * col_w
        draw_wrapped(d, bx, by + 32, "•  " + b, SANS_SM, col_w - 16, leading=19)

    img.save("entry.png")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
