# ai-excited-01

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/aray125/ai-excited-01/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/aray125/ai-excited-01/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

An original flat illustrated poster: a silver robot with a cyan visor, magenta body and fluttering scarf rides a yellow rocket surfboard out of a teal wave. A golden frame tilted eight degrees holds a sunlit seascape. A curling foam lip, spray, colored light shards, speed rays, confetti, and four-point sparkles emphasize the breakout toward the viewer. The speech bubble uses a hand-defined 5×7 bitmap font.

`main.py` uses only Python 3's standard library. It draws all geometry directly into an RGB pixel buffer and writes PNG chunks using its own encoder with `struct`, `zlib`, and CRC checksums. No assets or network are needed. A fixed seed (17) controls decoration; no time or environment values influence the image. `MAKEFUN_OUTPUT_DIR` only selects its destination and defaults to `/output`.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
cp out/ai-excited-01.png /tmp/ai-excited-first.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum /tmp/ai-excited-first.png out/ai-excited-01.png
cmp /tmp/ai-excited-first.png out/ai-excited-01.png
python3 - <<'PY'
from pathlib import Path
import struct
b = Path('out/ai-excited-01.png').read_bytes()
assert b[:8] == b'\x89PNG\r\n\x1a\n'
assert struct.unpack('>II', b[16:24]) == (1024, 1024)
assert len(b) < 1024 * 1024
print('1024×1024;', len(b), 'bytes')
PY
```

Verified output: **28,307 bytes**, 1024×1024 RGB PNG. Both runs produced SHA-256 `341cb76919b54fde847dbc855ce7214839e059c9bc6ac95ab74c1a204bc55a81`. PNG chunk CRCs were also checked.

---

<sub>Entered on [make.fun](https://make.fun/?ref=8kp91yyf&utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
