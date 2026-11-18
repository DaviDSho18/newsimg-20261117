# 17 November 2026 World News Front Page — make.fun Competition Entry

A competition entry for **"Sum up 17 November's world news in one image"**.

This project renders a high-contrast broadsheet newspaper front page titled **"THE WORLD"** dated **Tuesday 17 November 2026** into a clean 1024x1024 PNG image (`entry.png`) that remains crisp and legible down to 300 pixels across.

## Editorial Coverage (17 November 2026)

The entry comprehensively reflects the day's verified global news stories:

- **Lead Story (Europe / War):**
  - **Headline:** *Ukraine strikes the Crimean Bridge*
  - **Details:** The Kerch Strait crossing partly collapses following a coordinated Ukrainian strike; President Volodymyr Zelensky hails an "unprecedented" attack against a key symbol of Vladimir Putin's rule.
  - **Vector Illustration:** A high-resolution tactical vector schematic depicting the Kerch Strait crossing, the iconic white shipping arch, the sheared and collapsed highway span dropped into the water, rising impact smoke, fire, and geographic reconnaissance coordinates.
- **Right Column (Regional Briefings):**
  - **Middle East:** The US strikes Iran's Qeshm Island after Tehran attacks an American radar site in Bahrain; President Trump states the US takes any Iranian plot "very seriously".
  - **Health:** The United States officially loses its 26-year measles elimination status amid record case numbers and declining vaccine coverage.
  - **Russia:** A Russian military transport aircraft crashes during operations, killing all 19 personnel on board.
  - **Security:** An American soldier is detained by British police in the UK on suspicion of espionage and transferred to US military custody.
  - **West Bank:** A 72-year-old Palestinian woman is shot dead by Israeli settlers, according to the Palestinian health ministry.
- **Bottom Strip (Global Briefings & Departments):**
  - **Tech / Trade:** Nvidia partner Megaspeed is investigated by the US government over chip exports as new export restrictions on Southeast Asia impact supply into China.
  - **Space Exploration:** A Japanese space probe alters its mission trajectory toward a secondary asteroid target due to propulsion engine trouble.
  - **Culture:** Prince William and Catherine, Princess of Wales, celebrate the Earthshot Prize winners in Mumbai.

## Visual Design & Architecture

1. **2x Supersampled Rendering (`make_image.py`):**
   - Composed natively at 2048x2048 using Python's Pillow (`PIL`) library and DejaVu TrueType fonts (`/usr/share/fonts/truetype/dejavu/`).
   - Downscaled to 1024x1024 using Pillow's `LANCZOS` resampler, ensuring antialiased lines and sharp text readability even when inspected at 300px width.
   - Outputs an optimized PNG file of ~461 KiB, well under the 1 MiB competition ceiling.

2. **Runner & Verification (`main.ts`):**
   - Written in Node 22 TypeScript using Node's standard library (`node:fs`, `node:path`, `node:crypto`, `node:url`).
   - Copies `entry.png` from beside the module to `$MAKEFUN_OUTPUT_DIR` (or `/output` by default), creating destination directories recursively.
   - Performs post-copy validation: verifies source size is under 1 MiB, confirms destination file exists, ensures exact byte size parity, and computes SHA-256 hashes to guarantee bit-for-bit fidelity.

## Local Execution

### 1. Regenerate the Image
```bash
python3 make_image.py
```
This produces `entry.png` (1024x1024 PNG, < 1 MiB) at the repository root.

### 2. Run the Entry Program
```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
The program validates `entry.png`, creates `out/`, copies the image to `out/entry.png`, and verifies size and SHA-256 integrity.
