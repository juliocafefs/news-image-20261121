// news-image-20261121 entry program.
//
// The entry is a single still image, entry.png, kept beside this file in the
// repository. The grader runs this program twice with no network and expects
// both runs to leave exactly the same bytes in the output folder, so the job
// here is deliberately boring: validate the picture, then copy it verbatim.
//
// Before copying, the PNG header is inspected so a truncated or swapped file
// fails loudly instead of being judged as a broken entry:
//   * the 8-byte PNG signature must be present,
//   * the IHDR width and height must not exceed 1024 px on either side,
//   * the whole file must fit inside the competition's 1 MiB ceiling.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SIZE_LIMIT = 1_048_576; // 1 MiB, the largest entry.png the gate accepts
const SIDE_LIMIT = 1024; // pixels per side, ditto
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function refuse(reason) {
  console.error(`entry refused: ${reason}`);
  process.exit(1);
}

// The picture lives next to this script, wherever the repo was mounted.
const repoDir = dirname(fileURLToPath(import.meta.url));
const picture = readFileSync(join(repoDir, "entry.png"));

// --- header checks ---------------------------------------------------------
const hasSignature = PNG_SIGNATURE.every((byte, i) => picture[i] === byte);
if (!hasSignature) refuse("entry.png does not start with a PNG signature");
if (picture.length > SIZE_LIMIT) {
  refuse(`entry.png is ${picture.length} bytes, over the ${SIZE_LIMIT} byte cap`);
}
// IHDR is the first chunk: width and height are big-endian uint32s at 16/20.
const width = picture.readUInt32BE(16);
const height = picture.readUInt32BE(20);
if (width > SIDE_LIMIT || height > SIDE_LIMIT) {
  refuse(`entry.png is ${width}x${height}, over the ${SIDE_LIMIT}px side cap`);
}

// --- copy ------------------------------------------------------------------
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
writeFileSync(target, picture);

console.log(
  `wrote ${target}: ${width}x${height} PNG, ${picture.length} bytes, unchanged copy`,
);
