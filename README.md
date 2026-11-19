# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/DanuMahiru/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/DanuMahiru/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world's news on Wednesday, 18 November 2026, as a
newspaper front page: the Trump–Xi–Putin summit in Shenzhen leads, with the
Gulf escalation, the Alaska Senate result, the Anthropic IPO and Nvidia's
earnings, and unrest in Bangladesh below it, plus an in-brief ticker. Every
headline traces to real reporting from that day (Reuters, AP, BBC, The New
York Times, The Hindu). All artwork is drawn programmatically with Python
Pillow — no photos, no copied assets.

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
