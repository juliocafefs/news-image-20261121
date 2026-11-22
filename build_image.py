#!/usr/bin/env python3
"""
build_image.py — draws entry.png for the make.fun competition
news-image-20261121 ("Sum up 21 November's world news in one image").

The picture is a classic newspaper front page, drawn entirely with Pillow
primitives (rectangles, lines, polygons, ellipses) plus Pillow-rendered text.
No external artwork is used, so the result is fully reproducible: run this
script and it rewrites entry.png next to itself, byte for byte.

Layout (1024 x 1024):
  * masthead  — "THE WORLD IN ONE DAY" over a black date band
  * lead      — ICJ rules Myanmar committed genocide against the Rohingya
  * grid 2x2  — APEC summit / Nasdaq sell-off / Ukraine barrage / Peru quake
  * wide      — tanker strikes near Hormuz
  * strip     — GTA VI first-day earnings
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette ---
PAPER = (247, 243, 233)      # warm off-white newsprint
PANEL = (253, 251, 245)      # slightly lighter panel fill
INK = (18, 18, 18)           # near-black ink
GRAY = (74, 74, 74)          # sub-caption grey
RED = (178, 30, 40)          # the one accent colour
NAVY = (24, 34, 58)          # night-sky panel for the drone story
WHITE = (255, 255, 255)
GOLD = (232, 184, 32)

W = H = 1024
MARGIN = 28
RIGHT = W - MARGIN

# ------------------------------------------------------------------ fonts ---
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- helpers ---
def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using real glyph widths."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def star(draw, cx, cy, r, fill):
    """Small five-pointed star polygon (flag detail)."""
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def panel_box(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=PANEL, outline=INK, width=2)


def story_text(draw, x, y, headline, sub, width, hsize=25, lh=31):
    """Headline (wrapped, bold caps) followed by a one/two-line sub-caption."""
    hfont = font(SANS_BOLD, hsize)
    for line in wrap(draw, headline, hfont, width):
        draw.text((x, y), line, font=hfont, fill=INK)
        y += lh
    y += 5
    sfont = font(SANS_BOLD, 17)
    for line in wrap(draw, sub, sfont, width):
        draw.text((x, y), line, font=sfont, fill=GRAY)
        y += 21
    return y


# ---------------------------------------------------------------- visuals ---
def draw_scales(draw, cx, top, bottom):
    """Scales of justice for the ICJ lead story."""
    beam_y = top + 34
    pan_y = beam_y + 52
    # finial + pole + base
    draw.ellipse([cx - 8, top + 6, cx + 8, top + 22], fill=INK)
    draw.line([cx, top + 20, cx, bottom - 16], fill=INK, width=7)
    draw.rectangle([cx - 34, bottom - 14, cx + 34, bottom - 4], fill=INK)
    # beam
    draw.line([cx - 78, beam_y, cx + 78, beam_y], fill=INK, width=7)
    for side in (-1, 1):
        px = cx + side * 78
        # hanger strings
        draw.line([px, beam_y, px - 26, pan_y], fill=INK, width=3)
        draw.line([px, beam_y, px + 26, pan_y], fill=INK, width=3)
        draw.line([px, beam_y, px, pan_y + 2], fill=INK, width=3)
        # bowl: bottom half of an ellipse
        draw.pieslice([px - 34, pan_y - 10, px + 34, pan_y + 22], 0, 180, fill=INK)
        draw.line([px - 34, pan_y + 6, px + 34, pan_y + 6], fill=RED, width=3)


def draw_flags(draw, x, y):
    """Three summit flags: China, United States, Russia (host first)."""
    fw, fh, gap = 34, 46, 8
    for i in range(3):
        fx = x + i * (fw + gap)
        draw.line([fx - 3, y - 4, fx - 3, y + fh + 16], fill=GRAY, width=3)
        if i == 0:      # China: red field, gold star
            draw.rectangle([fx, y, fx + fw, y + fh], fill=(222, 41, 16))
            star(draw, fx + 11, y + 12, 7, GOLD)
            draw.ellipse([fx + 22, y + 6, fx + 26, y + 10], fill=GOLD)
            draw.ellipse([fx + 24, y + 14, fx + 28, y + 18], fill=GOLD)
        elif i == 1:    # United States: stripes + blue canton
            for s in range(7):
                col = (178, 34, 52) if s % 2 == 0 else WHITE
                draw.rectangle([fx, y + s * fh // 7, fx + fw, y + (s + 1) * fh // 7], fill=col)
            draw.rectangle([fx, y, fx + 17, y + fh // 2], fill=(60, 59, 110))
            for r in range(3):
                for c in range(3):
                    draw.ellipse([fx + 3 + c * 5, y + 3 + r * 6,
                                  fx + 5 + c * 5, y + 5 + r * 6], fill=WHITE)
        else:           # Russia: white / blue / red thirds
            draw.rectangle([fx, y, fx + fw, y + fh // 3], fill=WHITE)
            draw.rectangle([fx, y + fh // 3, fx + fw, y + 2 * fh // 3], fill=(0, 57, 166))
            draw.rectangle([fx, y + 2 * fh // 3, fx + fw, y + fh], fill=(213, 43, 30))
        draw.rectangle([fx, y, fx + fw, y + fh], outline=INK, width=1)


def draw_chart(draw, x, y, w, h):
    """A plunging red stock chart for the Nasdaq sell-off."""
    draw.line([x, y + 6, x, y + h], fill=INK, width=3)          # y axis
    draw.line([x, y + h, x + w, y + h], fill=INK, width=3)      # x axis
    for i in range(1, 4):                                        # gridlines
        gy = y + h * i // 4
        draw.line([x + 2, gy, x + w, gy], fill=(205, 200, 188), width=1)
    pts = [(x + 6, y + 16), (x + 26, y + 12), (x + 44, y + 24), (x + 60, y + 20),
           (x + 76, y + 40), (x + 90, y + 36), (x + 104, y + 58), (x + 116, y + 70)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex + 2, ey - 8), (ex + 16, ey + 6), (ex + 2, ey + 8)], fill=RED)


def draw_drones(draw, x0, y0, x1, y1):
    """Night sky with quadcopter-drone silhouettes for the Ukraine barrage."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    for sx, sy in [(14, 16), (52, 8), (88, 22), (30, 40), (70, 44), (100, 6)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3], fill=WHITE)

    def drone(cx, cy, s, col):
        draw.ellipse([cx - 5 * s, cy - 3 * s, cx + 5 * s, cy + 3 * s], fill=col)
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            ex, ey = cx + dx * 13 * s, cy + dy * 9 * s
            draw.line([cx, cy, ex, ey], fill=col, width=max(2, s))
            draw.ellipse([ex - 5 * s, ey - 2 * s, ex + 5 * s, ey + 2 * s], outline=col, width=max(1, s))

    drone(x0 + 34, y0 + 34, 1, WHITE)
    drone(x0 + 82, y0 + 62, 1, (198, 208, 226))
    drone(x0 + 48, y0 + 96, 1, (160, 172, 196))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_mountains(draw, x, y, w):
    """Andes outline with snow caps and a red seismic crack."""
    base = y + 74
    peaks = [(x, base), (x + 34, y + 18), (x + 58, base)]
    peaks2 = [(x + 40, base), (x + 76, y + 4), (x + w, base)]
    draw.line(peaks + [peaks[0]], fill=INK, width=3, joint="curve")
    draw.line(peaks2 + [peaks2[0]], fill=INK, width=3, joint="curve")
    draw.polygon([(x + 76 - 9, y + 16), (x + 76, y + 4), (x + 76 + 9, y + 16),
                  (x + 76 + 4, y + 12), (x + 76, y + 17), (x + 76 - 4, y + 12)], fill=WHITE)
    draw.polygon([(x + 34 - 7, y + 28), (x + 34, y + 18), (x + 34 + 7, y + 28),
                  (x + 34, y + 24)], fill=WHITE)
    crack = [(x + 8, base + 8), (x + 30, base + 14), (x + 44, base + 9),
             (x + 62, base + 17), (x + 84, base + 11), (x + 104, base + 16)]
    draw.line(crack, fill=RED, width=4, joint="curve")
    draw.line([x, base + 22, x + w, base + 22], fill=INK, width=2)


def draw_tanker(draw, x, y):
    """Oil-tanker silhouette riding stylised waves."""
    draw.polygon([(x, y + 46), (x + 216, y + 46), (x + 198, y + 68), (x + 18, y + 68)], fill=INK)
    draw.line([x + 4, y + 52, x + 210, y + 52], fill=RED, width=4)
    for i, (cw, ch, col) in enumerate([(34, 16, (96, 96, 96)), (34, 22, RED),
                                       (34, 16, (96, 96, 96)), (30, 20, (60, 60, 60))]):
        cx = x + 22 + i * 38
        draw.rectangle([cx, y + 46 - ch, cx + cw, y + 46], fill=col)
    draw.rectangle([x + 178, y + 12, x + 200, y + 46], fill=INK)   # bridge tower
    draw.rectangle([x + 182, y + 18, x + 196, y + 26], fill=GOLD)  # bridge window
    for i in range(5):                                             # waves
        wx = x + 6 + i * 44
        draw.arc([wx, y + 72, wx + 34, y + 88], 180, 360, fill=INK, width=3)


# ------------------------------------------------------------------- page ---
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double frame
    d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=3)
    d.rectangle([18, 18, W - 18, H - 18], outline=INK, width=1)

    # ---- masthead ------------------------------------------------------
    centered(d, W // 2, 34, "THE WORLD IN ONE DAY", font(SERIF_BOLD, 64), INK)
    d.rectangle([MARGIN, 116, RIGHT, 172], fill=INK)
    centered(d, W // 2, 124, "SATURDAY 21 NOVEMBER 2026", font(SANS_BOLD, 44), WHITE)
    d.rectangle([MARGIN, 184, RIGHT, 189], fill=RED)

    # ---- lead story ----------------------------------------------------
    panel_box(d, MARGIN, 202, RIGHT, 420)
    d.rectangle([356, 216, 502, 242], fill=RED)
    d.text((368, 220), "TOP STORY", font=font(SANS_BOLD, 18), fill=WHITE)
    draw_scales(d, 187, 246, 414)
    story_text(d, 356, 250,
               "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST THE ROHINGYA",
               "World Court ruling at The Hague",
               RIGHT - 356 - 16, hsize=39, lh=47)

    # ---- 2 x 2 grid ------------------------------------------------------
    rows = [(434, 598), (610, 774)]
    cols = [(MARGIN, 500), (524, RIGHT)]
    stories = [
        ("flags", "XI HOSTS TRUMP & PUTIN AT APEC SUMMIT",
         "Three leaders meet in Shenzhen, China"),
        ("chart", "NASDAQ PLUNGES 5.3% IN AI SELL-OFF",
         "Worst week for tech stocks since 2020"),
        ("drones", "RUSSIA FIRES 400+ DRONES & 110+ MISSILES AT UKRAINE",
         "Zelensky calls Putin 'a killer'"),
        ("peaks", "MAGNITUDE 6.8 EARTHQUAKE SHAKES PERU",
         "Strong quake strikes the central Andes"),
    ]
    for (kind, head, sub), (gy0, gy1), (gx0, gx1) in zip(
            stories, [rows[0], rows[0], rows[1], rows[1]],
            [cols[0], cols[1], cols[0], cols[1]]):
        panel_box(d, gx0, gy0, gx1, gy1)
        vx, vy = gx0 + 16, gy0 + 14           # visual strip, 118 wide
        if kind == "flags":
            draw_flags(d, vx + 4, vy + 38)
        elif kind == "chart":
            draw_chart(d, vx, vy + 22, 112, 84)
        elif kind == "drones":
            draw_drones(d, vx, vy, vx + 116, gy1 - 14)
        elif kind == "peaks":
            draw_mountains(d, vx, vy + 16, 112)
        story_text(d, gx0 + 148, gy0 + 14, head, sub, gx1 - (gx0 + 148) - 14)

    # ---- wide panel: Hormuz ---------------------------------------------
    panel_box(d, MARGIN, 786, RIGHT, 906)
    draw_tanker(d, 48, 806)
    story_text(d, 300, 800,
               "TANKER STRIKES NEAR HORMUZ HIT WARTIME HIGH",
               "Oil shipments through the strait fall 15%",
               RIGHT - 300 - 16, hsize=30, lh=37)

    # ---- bottom strip -----------------------------------------------------
    d.rectangle([MARGIN, 918, RIGHT, 970], fill=INK)
    centered(d, W // 2, 932, "ALSO TODAY: GTA VI EARNS $2.36 BILLION ON ITS FIRST DAY",
             font(SANS_BOLD, 25), WHITE)
    centered(d, W // 2, 980, "Compiled from world news reports of Saturday 21 November 2026",
             font(SANS, 15), GRAY)

    img.save("entry.png", optimize=True)
    print("entry.png written:", img.size)


if __name__ == "__main__":
    build()
