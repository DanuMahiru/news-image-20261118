// news-image-20261118 — v4 entrypoint.
// The program is a single pre-rendered image: this script only places
// entry.png into the directory the harness asks for, unchanged.
import { copyFileSync as copy, mkdirSync as mkdir } from "node:fs";
import { dirname as dirOf, join as joinPath } from "node:path";
import { fileURLToPath as urlToPath } from "node:url";

const here = dirOf(urlToPath(import.meta.url));
const target = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdir(target, { recursive: true });
copy(joinPath(here, "entry.png"), joinPath(target, "entry.png"));
