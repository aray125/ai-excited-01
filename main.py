#!/usr/bin/env python3
"""ai-excited-01 entry: "WOW, JUDGE!"

A small robot in a fluttering magenta scarf rides a rocket surfboard on
a giant wave that bursts OUT of a tilted golden picture frame toward
the viewer, shouting "WOW, JUDGE!" in a big speech bubble. Flat poster
style, thick outlines, one focal point, dark ink-blue background,
magenta / yellow / cyan light bursts, speed lines, confetti and sparkles.
The frame's little painted seascape has its own sun; the wave crest
carries a white highlight over its navy edge and a second breaking lip.

Pure Python 3 standard library (zlib + struct for the PNG encoder).
Deterministic: fixed seed, no time, no network, no randomness from the
environment. Writes exactly one file: <MAKEFUN_OUTPUT_DIR>/entry.png
(default /output/entry.png), 1024x1024, under 1 MiB.
"""

import math
import os
import random
import struct
import zlib

W = H = 1024

# ---- palette ---------------------------------------------------------
INK = (8, 14, 38)          # darkest background
NAVY = (6, 26, 61)         # outline navy
DEEP_BLUE = (14, 42, 92)
TEAL_DARK = (10, 92, 122)
TEAL = (22, 168, 196)
TEAL_LIGHT = (120, 220, 240)
FOAM = (255, 255, 255)
FOAM_BLUE = (191, 243, 255)
GOLD = (245, 184, 29)
GOLD_DARK = (201, 138, 18)
GOLD_LIGHT = (255, 214, 90)  # frame highlight and rivets
MAGENTA = (255, 46, 136)
YELLOW = (255, 212, 0)
CYAN = (0, 229, 255)
ORANGE = (255, 107, 26)
SILVER = (232, 241, 248)
ROBOT_PINK = (255, 46, 136)

buf = bytearray(W * H * 3)
_rng = random.Random(20261116)


def _idx(x, y):
    return (y * W + x) * 3


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = _idx(x, y)
        buf[i], buf[i + 1], buf[i + 2] = color


def fill_rect(x0, y0, x1, y1, color):
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(W, x1)
    y1 = min(H, y1)
    if x1 <= x0 or y1 <= y0:
        return
    r, g, b = color
    row = bytes((r, g, b)) * (x1 - x0)
    for y in range(y0, y1):
        i = _idx(x0, y)
        buf[i:i + len(row)] = row


def circle(cx, cy, rad, color):
    r, g, b = color
    rad = int(rad)
    for y in range(max(0, cy - rad), min(H, cy + rad + 1)):
        dy = y - cy
        dx = int(math.sqrt(max(0, rad * rad - dy * dy)))
        x0 = max(0, cx - dx)
        x1 = min(W, cx + dx + 1)
        i = _idx(x0, y)
        buf[i:i + (x1 - x0) * 3] = bytes((r, g, b)) * (x1 - x0)


def star4(cx, cy, r, color):
    """Four-point sparkle: a plus sign of two crossed bars."""
    fill_rect(cx - 2, cy - r, cx + 3, cy + r + 1, color)
    fill_rect(cx - r, cy - 2, cx + r + 1, cy + 3, color)


def poly_fill(points, color):
    """Scanline fill of a simple polygon (list of (x, y))."""
    if len(points) < 3:
        return
    r, g, b = color
    ys = [p[1] for p in points]
    y0 = max(0, int(min(ys)))
    y1 = min(H - 1, int(max(ys)) + 1)
    n = len(points)
    for y in range(y0, y1 + 1):
        xs = []
        for i in range(n):
            x1, y1p = points[i]
            x2, y2p = points[(i + 1) % n]
            if (y1p <= y < y2p) or (y2p <= y < y1p):
                t = (y - y1p) / (y2p - y1p)
                xs.append(x1 + t * (x2 - x1))
        if len(xs) < 2:
            continue
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            xa = max(0, int(xs[k]))
            xb = min(W, int(xs[k + 1]) + 1)
            if xb > xa:
                i = _idx(xa, y)
                buf[i:i + (xb - xa) * 3] = bytes((r, g, b)) * (xb - xa)


def thick_line(x0, y0, x1, y1, width, color):
    dx = x1 - x0
    dy = y1 - y0
    dist = math.hypot(dx, dy)
    steps = max(1, int(dist / max(1, width // 2)))
    rad = width // 2
    for s in range(steps + 1):
        t = s / steps
        circle(int(x0 + dx * t), int(y0 + dy * t), rad, color)


def poly_line(points, width, color):
    for a, b in zip(points, points[1:]):
        thick_line(a[0], a[1], b[0], b[1], width, color)


def round_rect(x0, y0, x1, y1, rad, color):
    fill_rect(x0 + rad, y0, x1 - rad, y1, color)
    fill_rect(x0, y0 + rad, x1, y1 - rad, color)
    circle(x0 + rad, y0 + rad, rad, color)
    circle(x1 - rad, y0 + rad, rad, color)
    circle(x0 + rad, y1 - rad, rad, color)
    circle(x1 - rad, y1 - rad, rad, color)


def rot(px, py, cx, cy, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    dx, dy = px - cx, py - cy
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


# ---- background: ink-blue gradient + stars ---------------------------
def draw_background():
    top = (11, 16, 48)
    mid = (18, 36, 92)
    bot = (8, 12, 30)
    for y in range(H):
        if y < 512:
            t = y / 512.0
            c = tuple(int(top[i] + (mid[i] - top[i]) * t) for i in range(3))
        else:
            t = (y - 512) / 512.0
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * t) for i in range(3))
        i = _idx(0, y)
        buf[i:i + W * 3] = bytes(c) * W
    # tiny stars / sparks, fixed seed
    for _ in range(70):
        x = _rng.randrange(0, W)
        y = _rng.randrange(0, 420)
        r = _rng.choice([1, 1, 2])
        col = _rng.choice([FOAM, CYAN, YELLOW])
        circle(x, y, r, col)
    # fainter stars lower down, where the wave will not cover them
    for _ in range(25):
        x = _rng.randrange(0, W)
        y = _rng.randrange(430, 700)
        circle(x, y, 1, FOAM_BLUE)
    # four-point sparkles in the open sky
    for _ in range(10):
        x = _rng.randrange(30, 990)
        y = _rng.randrange(30, 380)
        star4(x, y, _rng.randrange(6, 12),
              _rng.choice([FOAM, CYAN, YELLOW]))


# ---- light burst rays behind the frame --------------------------------
def draw_rays(cx, cy):
    cols = [MAGENTA, YELLOW, CYAN, MAGENTA, YELLOW, CYAN,
            MAGENTA, YELLOW, CYAN, MAGENTA, YELLOW, CYAN]
    for k in range(12):
        a0 = math.radians(k * 30 + 6)
        a1 = math.radians(k * 30 + 18)
        r = 720
        p1 = (cx + int(720 * math.cos(a0)), cy + int(720 * math.sin(a0)))
        p2 = (cx + int(720 * math.cos(a1)), cy + int(720 * math.sin(a1)))
        poly_fill([(cx, cy), p1, p2], cols[k])
    circle(cx, cy, 150, (24, 52, 130))


# ---- tilted golden picture frame --------------------------------------
def draw_frame():
    cx, cy = 470, 640
    tilt = -8
    hw, hh = 350, 240
    corners = [rot(cx - hw, cy - hh, cx, cy, tilt),
               rot(cx + hw, cy - hh, cx, cy, tilt),
               rot(cx + hw, cy + hh, cx, cy, tilt),
               rot(cx - hw, cy + hh, cx, cy, tilt)]
    corners = [(int(x), int(y)) for x, y in corners]
    poly_fill(corners, GOLD)
    inner = [(int(cx + (x - cx) * 0.90), int(cy + (y - cy) * 0.88))
             for x, y in corners]
    poly_fill(inner, GOLD_DARK)
    inner2 = [(int(cx + (x - cx) * 0.84), int(cy + (y - cy) * 0.80))
              for x, y in corners]
    poly_fill(inner2, (11, 46, 79))
    # little painted waves still inside the frame (the picture it was)
    for dy, col in ((30, TEAL), (70, TEAL_LIGHT), (110, FOAM)):
        pts = []
        for t in range(0, 21):
            fx = inner2[0][0] + int((inner2[1][0] - inner2[0][0]) * t / 20.0)
            fy = inner2[0][1] + dy + int(14 * math.sin(t * 0.9))
            pts.append((fx, fy))
        poly_line(pts, 10, col)
    # a small sun in the painted seascape, low enough to clear the frame
    sun_x, sun_y = 320, 540
    for k in range(8):
        a = math.radians(k * 45)
        x1 = int(sun_x + 30 * math.cos(a))
        y1 = int(sun_y + 30 * math.sin(a))
        x2 = int(sun_x + 42 * math.cos(a))
        y2 = int(sun_y + 42 * math.sin(a))
        thick_line(x1, y1, x2, y2, 5, GOLD_LIGHT)
    circle(sun_x, sun_y, 22, YELLOW)
    # gold rivets on the four frame corners
    for cxr, cyr in corners:
        circle(cxr, cyr, 12, GOLD_LIGHT)
        circle(cxr, cyr, 6, GOLD_DARK)
    # highlight along the frame's top outer edge
    thick_line(corners[0][0], corners[0][1], corners[1][0], corners[1][1],
               8, GOLD_LIGHT)


# ---- the giant wave bursting out of the frame -------------------------
WAVE_TOP = [(60, 1024), (50, 820), (120, 700), (240, 610), (380, 550),
            (520, 510), (640, 480), (750, 470), (830, 500), (870, 560),
            (840, 640), (760, 680), (700, 760), (740, 880), (780, 1024)]


def draw_wave():
    # dark teal under-layer, slightly offset down-left for depth
    shadow = [(x - 16, y + 22) for x, y in WAVE_TOP]
    poly_fill(shadow, TEAL_DARK)
    poly_fill(WAVE_TOP, TEAL)
    # navy outline along the crest (the visible top edge), with a white
    # highlight core so the crest reads against the dark sky
    poly_line(WAVE_TOP[3:11], 14, NAVY)
    poly_line(WAVE_TOP[3:11], 6, FOAM)
    # wave curl: a breaking lip, not a ring (offset blobs, never concentric)
    circle(815, 465, 80, FOAM)
    circle(760, 515, 34, TEAL_DARK)
    circle(800, 455, 20, FOAM)
    circle(790, 440, 18, FOAM_BLUE)
    # a second, smaller lip breaking just left of the main curl
    circle(700, 468, 42, FOAM)
    circle(672, 494, 18, TEAL_DARK)
    circle(694, 458, 12, FOAM_BLUE)
    # foam scallops along the crest
    for (fx, fy, fr) in [(250, 600, 28), (360, 556, 30), (480, 516, 32),
                         (590, 492, 32), (690, 478, 30), (840, 520, 30),
                         (860, 580, 26), (150, 690, 26), (100, 790, 24),
                         (560, 500, 26), (330, 580, 24), (60, 860, 22),
                         (900, 640, 24)]:
        circle(fx, fy, fr, FOAM)
    # spray droplets flying off the crest
    for _ in range(46):
        x = _rng.randrange(600, 990)
        y = _rng.randrange(300, 470)
        r = _rng.randrange(3, 13)
        circle(x, y, r, _rng.choice([FOAM, FOAM_BLUE, CYAN]))
    for _ in range(20):
        x = _rng.randrange(700, 1010)
        y = _rng.randrange(250, 420)
        r = _rng.randrange(2, 8)
        circle(x, y, r, _rng.choice([FOAM, FOAM_BLUE, CYAN]))
    # foam streaks on the wave face
    for (sx, sy, ex, ey) in [(300, 700, 520, 620), (420, 820, 640, 720),
                             (180, 880, 380, 800), (560, 920, 760, 840),
                             (240, 760, 460, 680), (640, 980, 820, 900)]:
        thick_line(sx, sy, ex, ey, 12, FOAM_BLUE)


# ---- speed lines -------------------------------------------------------
def draw_speed_lines():
    for _ in range(26):
        ang = _rng.uniform(0, 2 * math.pi)
        cx, cy = _rng.choice([(512, 512), (700, 400), (300, 700)])
        r0 = _rng.randrange(180, 420)
        r1 = r0 + _rng.randrange(50, 150)
        x0 = int(cx + r0 * math.cos(ang))
        y0 = int(cy + r0 * math.sin(ang))
        x1 = int(cx + r1 * math.cos(ang))
        y1 = int(cy + r1 * math.sin(ang))
        thick_line(x0, y0, x1, y1, _rng.choice([6, 8, 10]),
                   _rng.choice([FOAM, CYAN, YELLOW]))
    # a directional burst fanning out behind the robot, fixed angles so
    # it never depends on the random stream (the robot, drawn later,
    # covers the burst's centre)
    for k in range(12):
        a = math.radians(k * 30 + 15)
        r0 = 150
        r1 = 235 + (k % 3) * 40
        bx0 = int(700 + r0 * math.cos(a))
        by0 = int(420 + r0 * math.sin(a))
        bx1 = int(700 + r1 * math.cos(a))
        by1 = int(420 + r1 * math.sin(a))
        thick_line(bx0, by0, bx1, by1, 8, [CYAN, YELLOW, FOAM][k % 3])


# ---- robot on the rocket surfboard -------------------------------------
def draw_robot():
    # rocket flame + trail behind the board, with a hot white core
    poly_fill([(600, 450), (545, 420), (545, 480)], ORANGE)
    poly_fill([(600, 450), (565, 432), (565, 468)], YELLOW)
    poly_fill([(600, 450), (580, 440), (580, 460)], FOAM)
    circle(550, 450, 16, YELLOW)
    circle(550, 450, 8, FOAM)
    # fluttering magenta scarf streaming behind the robot's neck
    poly_fill([(700, 318), (640, 298), (598, 322), (646, 340)], ROBOT_PINK)
    poly_fill([(700, 322), (652, 312), (626, 330), (660, 342)], MAGENTA)
    circle(600, 322, 8, ROBOT_PINK)
    # board: navy outline under the yellow deck, feet planted on it
    thick_line(600, 450, 760, 385, 38, NAVY)
    thick_line(600, 450, 760, 385, 30, YELLOW)
    thick_line(615, 458, 750, 401, 8, ORANGE)
    # spray kicked up under the board
    circle(640, 452, 12, FOAM)
    circle(700, 432, 10, FOAM_BLUE)
    circle(745, 412, 9, FOAM)
    # legs
    thick_line(688, 420, 673, 385, 12, NAVY)
    thick_line(716, 418, 730, 382, 12, NAVY)
    # body (magenta, navy outline)
    round_rect(662, 310, 738, 388, 16, NAVY)
    round_rect(668, 316, 732, 382, 12, ROBOT_PINK)
    circle(700, 350, 12, YELLOW)        # chest light
    circle(700, 350, 6, FOAM)
    # arms thrown up in joy
    thick_line(666, 332, 626, 280, 14, ROBOT_PINK)
    thick_line(734, 332, 774, 278, 14, ROBOT_PINK)
    circle(624, 276, 10, ROBOT_PINK)
    circle(776, 274, 10, ROBOT_PINK)
    # head (silver, navy outline) + antenna
    thick_line(700, 310, 700, 276, 8, NAVY)
    circle(700, 270, 12, YELLOW)
    round_rect(662, 242, 738, 310, 18, NAVY)
    round_rect(668, 248, 732, 304, 14, SILVER)
    # cyan visor with two happy eyes
    round_rect(672, 262, 728, 294, 10, CYAN)
    circle(686, 278, 6, NAVY)
    circle(714, 278, 6, NAVY)
    # little smile under the visor
    thick_line(684, 302, 716, 302, 5, NAVY)
    # gold bolts on the head corners and a belly panel line
    circle(672, 254, 5, GOLD)
    circle(728, 254, 5, GOLD)
    thick_line(678, 368, 722, 368, 4, NAVY)
    # white cuffs where the arms meet the hands
    circle(630, 284, 6, FOAM)
    circle(770, 282, 6, FOAM)


# ---- confetti ----------------------------------------------------------
def draw_confetti():
    cols = [MAGENTA, YELLOW, CYAN, FOAM, ORANGE]
    for _ in range(110):
        x = _rng.randrange(20, 1004)
        y = _rng.randrange(20, 1004)
        col = _rng.choice(cols)
        if _rng.random() < 0.5:
            fill_rect(x, y, x + _rng.randrange(8, 18),
                      y + _rng.randrange(6, 12), col)
        else:
            circle(x, y, _rng.randrange(4, 9), col)
    # four-point star sparkles scattered over the poster
    for _ in range(24):
        x = _rng.randrange(30, 994)
        y = _rng.randrange(30, 994)
        star4(x, y, _rng.randrange(7, 14),
              _rng.choice([GOLD, CYAN, FOAM, YELLOW]))
    # a few big starbursts for focal pops
    for (sx, sy, sr) in [(120, 300, 18), (920, 260, 16), (880, 880, 18),
                         (140, 900, 16)]:
        star4(sx, sy, sr, YELLOW)
        star4(sx, sy, sr - 6, FOAM)


# ---- speech bubble "WOW, JUDGE!" --------------------------------------
# 5x7 bitmap font (rows top to bottom, '#' = on)
GLYPHS = {
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "D": ("###..", "#..#.", "#...#", "#...#", "#...#", "#..#.", "###.."),
    "G": (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    ",": (".....", ".....", ".....", ".....", "..#..", "..#..", ".#..."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}


def draw_text(text, x0, y0, scale, color):
    x = x0
    for ch in text:
        glyph = GLYPHS[ch]
        for row, bits in enumerate(glyph):
            for col, bit in enumerate(bits):
                if bit == "#":
                    fill_rect(x + col * scale, y0 + row * scale,
                              x + (col + 1) * scale, y0 + (row + 1) * scale,
                              color)
        x += 6 * scale


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_bubble():
    bx0, by0, bx1, by1 = 90, 40, 934, 180
    # tail (navy, then white inset) pointing down at the robot's antenna
    poly_fill([(610, by1 - 6), (690, by1 - 6), (655, 244)], NAVY)
    poly_fill([(622, by1 - 6), (678, by1 - 6), (653, 232)], FOAM)
    # bubble body: navy outline, white inside
    round_rect(bx0, by0, bx1, by1, 34, NAVY)
    round_rect(bx0 + 10, by0 + 10, bx1 - 10, by1 - 10, 26, FOAM)
    # text, centred
    word = "WOW, JUDGE!"
    scale = 10
    tw = text_width(word, scale)
    th = 7 * scale
    tx = bx0 + (bx1 - bx0 - tw) // 2
    ty = by0 + (by1 - by0 - th) // 2
    draw_text(word, tx, ty, scale, NAVY)
    # starburst accent popping off the bubble's top-right corner
    star4(908, 58, 22, NAVY)
    star4(908, 58, 18, YELLOW)
    star4(908, 58, 10, FOAM)
    # motion swooshes under the bubble's left side
    thick_line(120, 202, 182, 216, 8, CYAN)
    thick_line(142, 224, 202, 234, 8, YELLOW)


# ---- PNG encoding (stdlib only) ----------------------------------------
def _chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def write_png(path):
    raw = b"".join(
        b"\x00" + bytes(buf[y * W * 3:(y + 1) * W * 3]) for y in range(H))
    comp = zlib.compress(raw, 9)
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
           + _chunk(b"IDAT", comp) + _chunk(b"IEND", b""))
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    draw_background()
    draw_rays(512, 480)
    draw_frame()
    draw_wave()
    draw_speed_lines()
    draw_robot()
    draw_confetti()
    draw_bubble()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.png")
    size = write_png(path)
    print("wrote %s (%d bytes, %dx%d)" % (path, size, W, H))


if __name__ == "__main__":
    main()
