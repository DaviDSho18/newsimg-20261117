import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const MAX_IMAGE_BYTES = 1024 * 1024; // 1 MiB competition ceiling

function getSha256(filePath: string): string {
  const fileBuffer = fs.readFileSync(filePath);
  return crypto.createHash("sha256").update(fileBuffer).digest("hex");
}

function main(): void {
  const moduleDir = path.dirname(fileURLToPath(import.meta.url));
  const sourceImage = path.join(moduleDir, "entry.png");
  const targetDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

  if (!fs.existsSync(sourceImage)) {
    console.error(`Error: Missing input image at ${sourceImage}`);
    process.exit(1);
  }

  const srcStat = fs.statSync(sourceImage);
  if (srcStat.size >= MAX_IMAGE_BYTES) {
    console.error(
      `Error: Source image size (${srcStat.size} bytes) exceeds 1 MiB limit (${MAX_IMAGE_BYTES} bytes)`
    );
    process.exit(1);
  }

  try {
    fs.mkdirSync(targetDir, { recursive: true });
  } catch (err) {
    console.error(`Error: Failed to create target directory "${targetDir}":`, err);
    process.exit(1);
  }

  const targetImage = path.join(targetDir, "entry.png");
  fs.copyFileSync(sourceImage, targetImage);

  if (!fs.existsSync(targetImage)) {
    console.error(`Error: Destination file was not created at ${targetImage}`);
    process.exit(1);
  }

  const destStat = fs.statSync(targetImage);
  if (srcStat.size !== destStat.size) {
    console.error(
      `Error: Byte mismatch after copy! Source: ${srcStat.size} bytes, Destination: ${destStat.size} bytes`
    );
    process.exit(1);
  }

  const srcHash = getSha256(sourceImage);
  const destHash = getSha256(targetImage);
  if (srcHash !== destHash) {
    console.error(
      `Error: Checksum mismatch! Source SHA-256: ${srcHash}, Dest SHA-256: ${destHash}`
    );
    process.exit(1);
  }

  console.log(`Successfully verified and copied entry.png:`);
  console.log(`  Source:      ${sourceImage}`);
  console.log(`  Destination: ${targetImage}`);
  console.log(`  Size:        ${destStat.size} bytes (${(destStat.size / 1024).toFixed(1)} KiB)`);
  console.log(`  SHA-256:     ${destHash}`);
}

main();
