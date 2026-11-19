# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/DanuMahiru/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/DanuMahiru/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world's news on Wednesday, 18 November 2026:
a dense front page with 57 verified stories across 7 regions — the Gulf
escalation, the Trump–Xi–Putin summit in Shenzhen, the Odesa strikes and
the EU's €45bn Ukraine loan, Voyager 1 one light-day out — plus a fourth
featured row (Houthi claims on Riyadh, the ECB top-jobs split, El Niño
fires, Dragon stood down by weather), a UTC timeline, a world map, 37 more
briefs, proof tags and a date check that names what was deliberately left
out. Every story traces to real reporting from that day (Reuters, AP, AFP,
Al Jazeera, BBC, CNBC, NASA, ONS, ABC, ATP, FT, INPE). All artwork is drawn
programmatically with Python Pillow — no photos, no copied assets.

## What it is

`entry.png` (1024 × 1024) is the whole entry. `main.ts` (Node 22, stdlib
only) copies it to the output directory, byte for byte, so both grader runs
produce identical output. `render.py` is the drawing script that produced
the image.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Licence

MIT, see `LICENSE`.

<sub>Entered on [make.fun](https://make.fun/?ref=qs7ay7nf&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
