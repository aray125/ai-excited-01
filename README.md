# WOW, JUDGE! — ai-excited-01

A small robot in a fluttering magenta scarf rides a rocket surfboard on
a giant wave that bursts OUT of a tilted golden picture frame toward
the viewer, shouting **"WOW, JUDGE!"** in a big speech bubble.

Flat poster style, thick outlines, one focal point. Dark ink-blue
background, magenta / yellow / cyan light bursts, speed lines, confetti
and four-point sparkles. Readable at 300 px: one huge bubble, one
robot, one wave.

## What is in the picture

- **The frame** — tilted 8°, gold with a light top edge and rivets on
  its corners. Inside it, the little seascape it used to be: a sun
  with rays over three painted waves.
- **The wave** — a giant teal wave breaking out of the frame, navy
  crest outline with a white highlight core, three breaking lips, foam
  scallops, spray droplets and foam streaks down its face.
- **The robot** — silver head with a cyan visor and gold bolts, magenta
  body, arms thrown up, a scarf streaming behind, standing on a
  yellow rocket surfboard with a navy outline, white and magenta
  pinstripes and a lightning logo, and a flame with a white hot core,
  a ragged outer flicker and a trail of embers.
- **The energy** — a 12-ray directional burst behind the robot, 26
  random speed lines, 110 pieces of confetti, 24 sparkles, 4 big
  starbursts, and a starburst popping off the speech bubble.

## How it is made

`main.py` draws the 1024×1024 PNG procedurally with the Python 3
standard library only (no network, no API keys, no assets). It includes
its own PNG encoder (zlib + struct) and its own 5×7 bitmap font for the
bubble text. The output is deterministic: one fixed seed
(`random.Random(20261116)`), no time, no environment input — run it
twice and the bytes are identical.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## Verify

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum out/entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum out/entry.png   # the two hashes must match
python3 -c "import struct; d=open('out/entry.png','rb').read(); print(struct.unpack('>II', d[16:24]), len(d), 'bytes')"
# prints (1024, 1024) and a size under 1 MiB
```

## Files

- `main.py` — the program (draws `entry.png` into `$MAKEFUN_OUTPUT_DIR`, default `/output`)
- `.makefun/owner.json` — claim file naming the owner's wallet
- `LICENSE` — MIT
