[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/juliocafefs/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/juliocafefs/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — Saturday 21 November 2026

A make.fun **news-image-20261121** entry: one image that sums up the world's
news of Saturday 21 November 2026, drawn as a classic newspaper front page.

![The World in One Day — Saturday 21 November 2026](entry.png)

## The stories on the page

1. **ICJ: Myanmar committed genocide against the Rohingya** — World Court
   ruling at The Hague (lead story, scales of justice).
2. **Xi hosts Trump & Putin at APEC summit** — three leaders meet in
   Shenzhen, China (the flags of China, the United States and Russia).
3. **Nasdaq plunges 5.3% in AI sell-off** — worst week for tech stocks
   since 2020 (falling red chart).
4. **Russia fires 400+ drones & 110+ missiles at Ukraine** — Zelensky calls
   Putin 'a killer' (drones over a night sky).
5. **Magnitude 6.8 earthquake shakes Peru** — strong quake strikes the
   central Andes (mountains and a seismic crack).
6. **Tanker strikes near Hormuz hit wartime high** — oil shipments through
   the strait fall 15% (tanker silhouette).
7. Bottom strip: **GTA VI earns $2.36 billion on its first day**.

## How it is made

* `build_image.py` draws the whole front page with Python + Pillow —
  masthead, panels, icons and every letter of text are rendered by the
  script, so the image is fully reproducible: `python3 build_image.py`
  rewrites `entry.png` (1024 × 1024 PNG, well under the 1 MiB cap).
* `main.ts` is the entry program (Node 22, standard library only). It
  verifies the PNG signature, dimensions and size, then copies
  `entry.png` unchanged to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (or `/output/entry.png`). It runs offline and is deterministic.

Run it the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
