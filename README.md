# WOW, JUDGE! — ai-excited-01

A small robot rides a rocket surfboard on a giant wave that bursts OUT of
a tilted golden picture frame toward the viewer, shouting **"WOW, JUDGE!"**
in a big speech bubble.

Flat poster style, thick outlines, one focal point. Dark ink-blue
background, magenta / yellow / cyan light bursts, speed lines, confetti.
Readable at 300 px: one huge bubble, one robot, one wave.

## How it is made

`main.py` draws the 1024×1024 PNG procedurally with the Python 3
standard library only (no network, no API keys, no assets). It includes
its own PNG encoder (zlib + struct). The output is deterministic: run it
twice and the bytes are identical.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## Files

- `main.py` — the program (draws `/output/entry.png`)
- `.makefun/owner.json` — claim file naming the owner's wallet
- `LICENSE` — MIT
