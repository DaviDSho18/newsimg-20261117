#!/usr/bin/env python3
"""
make_image.py - Generate the 17 November 2026 World News Front Page Entry.

Sum up 17 November's world news in one newspaper-style image at 1024x1024.
Rendered at 2x (2048x2048) with Pillow vector primitives and downscaled with
LANCZOS to produce a sharp, high-contrast, fully legible broadsheet.
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONTS_DIR = "/usr/share/fonts/truetype/dejavu"


def get_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a DejaVu TrueType font by base name and size."""
    font_path = os.path.join(FONTS_DIR, f"{name}.ttf")
    return ImageFont.truetype(font_path, size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int):
    """Greedy word wrapping based on PIL text bounding boxes."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def draw_bridge_illustration(draw: ImageDraw.ImageDraw, origin: tuple[int, int], size: tuple[int, int], fonts: dict):
    """
    Draw a vector diagram of the Crimean (Kerch) Bridge showing the collapsed span,
    the iconic shipping channel arch, smoke, fire, and tactical annotations.
    """
    ox, oy = origin
    bw, bh = size

    # 1. Sky twilight gradient
    horizon_y = oy + int(bh * 0.60)
    sky_h = horizon_y - oy
    for i in range(sky_h):
        ratio = i / float(sky_h)
        r = int(24 + ratio * 32)
        g = int(36 + ratio * 40)
        b = int(54 + ratio * 46)
        draw.line([(ox, oy + i), (ox + bw, oy + i)], fill=(r, g, b))

    # Distant headlands / coastal silhouettes
    draw.polygon([
        (ox, horizon_y),
        (ox, horizon_y - 45),
        (ox + 140, horizon_y - 65),
        (ox + 280, horizon_y - 25),
        (ox + 420, horizon_y)
    ], fill=(42, 58, 78))

    draw.polygon([
        (ox + bw - 380, horizon_y),
        (ox + bw - 260, horizon_y - 40),
        (ox + bw - 120, horizon_y - 55),
        (ox + bw, horizon_y - 30),
        (ox + bw, horizon_y)
    ], fill=(42, 58, 78))

    # 2. Sea gradient and stylized water ripples
    sea_h = (oy + bh) - horizon_y
    for i in range(sea_h):
        ratio = i / float(sea_h)
        r = int(14 - ratio * 6)
        g = int(28 - ratio * 10)
        b = int(48 - ratio * 14)
        draw.line([(ox, horizon_y + i), (ox + bw, horizon_y + i)], fill=(r, g, b))

    for wy in [horizon_y + 25, horizon_y + 60, horizon_y + 105, horizon_y + 160, horizon_y + 225]:
        draw.line([(ox, wy), (ox + bw, wy)], fill=(32, 68, 108), width=2)

    # 3. Structural Piers & Viaducts
    deck_y = oy + int(bh * 0.56)
    pier_x_offsets = [90, 210, 330, 460, 750, 920, 1030, 1120]

    for pxo in pier_x_offsets:
        px = ox + pxo
        draw.rectangle([px - 15, deck_y, px + 15, horizon_y + 90], fill="#475569")
        draw.rectangle([px - 24, horizon_y + 80, px + 24, horizon_y + 115], fill="#334155")
        draw.line([(px - 13, deck_y), (px - 13, horizon_y + 90)], fill="#64748B", width=2)

    # 4. Intact horizontal deck sections
    arch_start = ox + 460
    arch_end = ox + 750
    span_break_end = ox + 920

    # Left road & rail approaches
    draw.rectangle([ox, deck_y - 6, arch_end, deck_y + 6], fill="#334155")
    draw.line([(ox, deck_y - 12), (arch_end, deck_y - 12)], fill="#94A3B8", width=2)
    draw.rectangle([ox, deck_y + 6, arch_end, deck_y + 14], fill="#1E293B")

    # Right approach (intact beyond the damaged sector)
    draw.rectangle([span_break_end, deck_y - 6, ox + bw, deck_y + 6], fill="#334155")
    draw.line([(span_break_end, deck_y - 12), (ox + bw, deck_y - 12)], fill="#94A3B8", width=2)
    draw.rectangle([span_break_end, deck_y + 6, ox + bw, deck_y + 14], fill="#1E293B")

    # 5. Iconic Kerch Shipping Arch Span
    arch_mid = (arch_start + arch_end) // 2
    arch_half_w = (arch_end - arch_start) // 2
    arch_height = 190

    # Parabolic curve
    arch_points = []
    for x in range(arch_start, arch_end + 1, 3):
        norm = (x - arch_mid) / float(arch_half_w)
        ay = (deck_y - 6) - (1.0 - norm * norm) * arch_height
        arch_points.append((x, ay))

    for i in range(len(arch_points) - 1):
        draw.line([arch_points[i], arch_points[i + 1]], fill="#FFFFFF", width=8)

    # Suspension cables
    for cx in range(arch_start + 18, arch_end - 15, 16):
        norm = (cx - arch_mid) / float(arch_half_w)
        cay = (deck_y - 6) - (1.0 - norm * norm) * arch_height
        draw.line([(cx, cay), (cx, deck_y - 6)], fill="#E2E8F0", width=2)

    # Arch Portal cross ties
    draw.line([(arch_mid - 60, (deck_y - 6) - 160), (arch_mid + 60, (deck_y - 6) - 160)], fill="#CBD5E1", width=3)

    # 6. Severed and Collapsed Road Span (between arch_end and span_break_end)
    pier_a = arch_end
    pier_b = span_break_end

    # Sheared concrete edges and bent steel rebar
    draw.line([(pier_a, deck_y), (pier_a + 12, deck_y - 8)], fill="#F59E0B", width=3)
    draw.line([(pier_a, deck_y + 6), (pier_a + 16, deck_y + 14)], fill="#EF4444", width=3)

    # Left collapsed slab tilted down sharply into the water
    slab1 = [
        (pier_a, deck_y),
        (pier_a + 85, horizon_y + 40),
        (pier_a + 80, horizon_y + 55),
        (pier_a, deck_y + 14)
    ]
    draw.polygon(slab1, fill="#334155", outline="#1E293B")

    # Right fallen slab lying in water
    slab2 = [
        (pier_a + 80, horizon_y + 85),
        (pier_b - 10, horizon_y + 50),
        (pier_b, horizon_y + 65),
        (pier_a + 85, horizon_y + 100)
    ]
    draw.polygon(slab2, fill="#475569", outline="#1E293B")

    # Impact blast & fireball at the strike site
    impact_x = pier_a + 85
    impact_y = horizon_y - 10

    burst_outer = [
        (impact_x - 35, impact_y - 10),
        (impact_x - 15, impact_y - 35),
        (impact_x, impact_y - 15),
        (impact_x + 25, impact_y - 45),
        (impact_x + 20, impact_y - 5),
        (impact_x + 45, impact_y + 10),
        (impact_x + 10, impact_y + 25),
        (impact_x - 20, impact_y + 35),
        (impact_x - 15, impact_y + 10)
    ]
    draw.polygon(burst_outer, fill="#EA580C")

    burst_inner = [
        (impact_x - 20, impact_y - 5),
        (impact_x - 8, impact_y - 22),
        (impact_x + 5, impact_y - 10),
        (impact_x + 16, impact_y - 25),
        (impact_x + 12, impact_y),
        (impact_x + 25, impact_y + 10),
        (impact_x + 5, impact_y + 16),
        (impact_x - 10, impact_y + 20)
    ]
    draw.polygon(burst_inner, fill="#FDE047")

    # Water splash & churning foam
    draw.ellipse([impact_x - 30, horizon_y + 70, impact_x + 40, horizon_y + 115], fill="#BAE6FD")
    draw.ellipse([impact_x - 15, horizon_y + 78, impact_x + 25, horizon_y + 105], fill="#FFFFFF")

    # Heavy rising smoke plume
    smoke_clouds = [
        (impact_x, impact_y - 30, 26, "#1E293B"),
        (impact_x + 15, impact_y - 70, 38, "#0F172A"),
        (impact_x + 5, impact_y - 125, 48, "#1E293B"),
        (impact_x + 30, impact_y - 180, 60, "#334155"),
        (impact_x + 55, impact_y - 245, 74, "#475569"),
        (impact_x + 85, impact_y - 315, 88, "#64748B"),
        (impact_x + 120, impact_y - 380, 105, "#94A3B8"),
        (impact_x + 160, impact_y - 440, 120, "#CBD5E1"),
    ]
    for sx, sy, sr, sc in smoke_clouds:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=sc)

    # 7. Editorial Tactical Infographics Overlay
    tag_font = fonts["sans_bold"](19)
    note_font = fonts["sans_bold"](17)
    coord_font = fonts["sans"](16)

    # Title badge
    draw.rectangle([ox + 20, oy + 20, ox + 410, oy + 62], fill="#0F172A", outline="#38BDF8", width=2)
    draw.text((ox + 35, oy + 30), "KERCH STRAIT TACTICAL RECON", fill="#38BDF8", font=tag_font)

    # Coordinates badge
    draw.rectangle([ox + bw - 240, oy + 20, ox + bw - 20, oy + 62], fill="#0F172A", outline="#94A3B8", width=1)
    draw.text((ox + bw - 225, oy + 30), "LOC: 45°18'N 36°30'E", fill="#E2E8F0", font=coord_font)

    # Red callout tag pointing to collapsed span
    callout_x0, callout_y0 = ox + 710, oy + 120
    draw.rectangle([callout_x0, callout_y0, callout_x0 + 270, callout_y0 + 44], fill="#B91C1C", outline="#F87171", width=2)
    draw.text((callout_x0 + 15, callout_y0 + 11), "COLLAPSED ROAD SPAN", fill="#FFFFFF", font=note_font)
    draw.line([(callout_x0 + 135, callout_y0 + 44), (impact_x, impact_y - 15)], fill="#EF4444", width=3)
    draw.polygon([(impact_x, impact_y - 15), (impact_x - 7, impact_y - 30), (impact_x + 7, impact_y - 30)], fill="#EF4444")

    # Blue callout tag pointing to main arch
    arch_callout_x0, arch_callout_y0 = ox + 410, oy + 120
    draw.rectangle([arch_callout_x0, arch_callout_y0, arch_callout_x0 + 260, arch_callout_y0 + 44], fill="#1E3A8A", outline="#60A5FA", width=2)
    draw.text((arch_callout_x0 + 18, arch_callout_y0 + 11), "MAIN SHIPPING ARCH", fill="#FFFFFF", font=note_font)
    draw.line([(arch_callout_x0 + 130, arch_callout_y0 + 44), (arch_mid, (deck_y - 6) - 190)], fill="#3B82F6", width=3)

    # Directional markers
    draw.text((ox + 25, oy + bh - 40), "◄ TO CRIMEA (KERCH)", fill="#93C5FD", font=note_font)
    draw.text((ox + bw - 260, oy + bh - 40), "TO RUSSIA (TAMAN) ►", fill="#93C5FD", font=note_font)

    # 8. Clean enclosing border
    draw.rectangle([ox, oy, ox + bw, oy + bh], outline="#0F172A", width=3)


def build_world_news_page() -> Image.Image:
    """Compose the 2048x2048 front page and return the downscaled 1024x1024 image."""
    canvas_w, canvas_h = 2048, 2048
    img = Image.new("RGB", (canvas_w, canvas_h), "#FAF8F5")
    draw = ImageDraw.Draw(img)

    # Font definitions
    fonts = {
        "masthead": get_font("DejaVuSerif-Bold", 132),
        "subhead": get_font("DejaVuSerif", 24),
        "lead_head": get_font("DejaVuSerif-Bold", 66),
        "lead_deck": get_font("DejaVuSans", 28),
        "lead_body": get_font("DejaVuSerif", 22),
        "story_head": get_font("DejaVuSerif-Bold", 29),
        "story_body": get_font("DejaVuSans", 22),
        "tag_bold": get_font("DejaVuSans-Bold", 21),
        "meta_bold": get_font("DejaVuSans-Bold", 26),
        "meta_norm": get_font("DejaVuSans", 21),
        "sans_bold": lambda sz: get_font("DejaVuSans-Bold", sz),
        "sans": lambda sz: get_font("DejaVuSans", sz),
    }

    margin_x = 60
    content_w = canvas_w - (margin_x * 2)  # 1928px

    # ----------------------------------------------------
    # TOP HEADER & FOLIO
    # ----------------------------------------------------
    draw.line([(margin_x, 48), (margin_x + content_w, 48)], fill="#0F172A", width=2)
    draw.text((margin_x, 56), "THE INTERNATIONAL DAILY OF RECORD", fill="#334155", font=fonts["meta_norm"])
    draw.text((margin_x + 850, 56), "GLOBAL EDITION", fill="#0F172A", font=fonts["meta_bold"])
    draw.text((margin_x + content_w - 320, 56), "VOL. CXXXVIII · NO. 48,211", fill="#334155", font=fonts["meta_norm"])
    draw.line([(margin_x, 92), (margin_x + content_w, 92)], fill="#0F172A", width=2)

    # ----------------------------------------------------
    # MASTHEAD
    # ----------------------------------------------------
    masthead_text = "THE WORLD"
    tb_m = draw.textbbox((0, 0), masthead_text, font=fonts["masthead"])
    m_w = tb_m[2] - tb_m[0]
    draw.text(((canvas_w - m_w) // 2, 100), masthead_text, fill="#0F172A", font=fonts["masthead"])

    sub_text = "Independent Global Journalism · Comprehensive Analysis of 17 November 2026"
    tb_s = draw.textbbox((0, 0), sub_text, font=fonts["subhead"])
    draw.text(((canvas_w - (tb_s[2] - tb_s[0])) // 2, 240), sub_text, fill="#475569", font=fonts["subhead"])

    # Double rule enclosing date bar
    draw.line([(margin_x, 275), (margin_x + content_w, 275)], fill="#0F172A", width=4)

    # Date bar
    date_text = "★  TUESDAY 17 NOVEMBER 2026  ★"
    tb_d = draw.textbbox((0, 0), date_text, font=fonts["meta_bold"])
    draw.text(((canvas_w - (tb_d[2] - tb_d[0])) // 2, 283), date_text, fill="#0F172A", font=fonts["meta_bold"])
    draw.text((margin_x, 286), "SPECIAL WORLD DIGEST", fill="#64748B", font=fonts["tag_bold"])
    draw.text((margin_x + content_w - 230, 286), "PRICE: €3.50 · $4.00 · £3.00", fill="#64748B", font=fonts["tag_bold"])

    draw.line([(margin_x, 320), (margin_x + content_w, 320)], fill="#0F172A", width=2)

    # ----------------------------------------------------
    # TWO-COLUMN EDITORIAL GRID
    # Left column: Lead story + bridge illustration (width 1180px)
    # Right column: Five regional stories (width 700px)
    # ----------------------------------------------------
    col_split_x = margin_x + 1200
    right_col_x = col_split_x + 35
    right_col_w = (margin_x + content_w) - right_col_x

    # Vertical dividing column rule
    draw.line([(col_split_x, 335), (col_split_x, 1720)], fill="#CBD5E1", width=2)

    # ----------------------------------------------------
    # LEFT COLUMN: LEAD STORY (CRIMEAN BRIDGE)
    # ----------------------------------------------------
    # Category tag
    draw.rectangle([margin_x, 345, margin_x + 290, 380], fill="#B91C1C")
    draw.text((margin_x + 14, 350), "EUROPE / WAR · LEAD STORY", fill="#FFFFFF", font=fonts["tag_bold"])

    # Lead Headline
    lead_head_line1 = "Ukraine strikes the"
    lead_head_line2 = "Crimean Bridge"
    draw.text((margin_x, 395), lead_head_line1, fill="#0F172A", font=fonts["lead_head"])
    draw.text((margin_x, 470), lead_head_line2, fill="#0F172A", font=fonts["lead_head"])

    # Lead Deck / Sub-headline
    deck_text = (
        "Kerch Strait crossing partly collapses after heavy strike; "
        "Zelensky hails unprecedented attack on a key symbol of Putin's rule."
    )
    deck_lines = wrap_text(draw, deck_text, fonts["lead_deck"], 1180)
    curr_y = 555
    for dl in deck_lines:
        draw.text((margin_x, curr_y), dl, fill="#334155", font=fonts["lead_deck"])
        curr_y += 36

    # Bridge Vector Pictogram
    picto_y = 650
    picto_h = 690
    draw_bridge_illustration(draw, (margin_x, picto_y), (1180, picto_h), fonts)

    # Photo/Illustration Caption
    caption_y = picto_y + picto_h + 14
    cap_line1 = "STRATEGIC ARTERY FRACTURED: Ukrainian forces struck the Kerch Bridge early Tuesday, dropping a vital road span into the sea."
    cap_line2 = "President Volodymyr Zelensky declared the operation an unprecedented success against Moscow's wartime logistical network."
    draw.text((margin_x, caption_y), cap_line1, fill="#475569", font=fonts["sans_bold"](20))
    draw.text((margin_x, caption_y + 26), cap_line2, fill="#64748B", font=fonts["sans"](19))

    # Short lead story narrative block
    lead_body_y = caption_y + 60
    draw.line([(margin_x, lead_body_y - 8), (margin_x + 1180, lead_body_y - 8)], fill="#E2E8F0", width=1)

    lead_p1 = (
        "KYIV / MOSCOW — Ukrainian military and intelligence units executed a coordinated precision strike "
        "against the Crimean Bridge early Tuesday morning, causing the catastrophic partial collapse of a primary highway span. "
        "The assault cuts the premier transit artery linking mainland Russia with occupied Crimea, dealing a major blow to Kremlin "
        "military logistics and political prestige. Russian authorities immediately halted rail and vehicular traffic."
    )
    lead_lines = wrap_text(draw, lead_p1, fonts["lead_body"], 1180)
    b_y = lead_body_y + 4
    for bl in lead_lines:
        draw.text((margin_x, b_y), bl, fill="#1E293B", font=fonts["lead_body"])
        b_y += 30

    # ----------------------------------------------------
    # RIGHT COLUMN: FIVE REGIONAL STORIES
    # Middle East, Health, Russia, Security, West Bank
    # ----------------------------------------------------
    right_stories = [
        {
            "tag": "MIDDLE EAST",
            "head": "US Strikes Iran's Qeshm Island After Bahrain Radar Hit",
            "body": "The US launched strikes on Iran's Qeshm Island after Tehran attacked an American radar site in Bahrain; Trump warned the US takes any plot very seriously."
        },
        {
            "tag": "HEALTH",
            "head": "US Loses Measles Elimination Status After 26 Years",
            "body": "Federal health authorities confirmed the United States has lost its 26-year measles elimination status amid surging cases and falling vaccine coverage."
        },
        {
            "tag": "RUSSIA",
            "head": "Military Transport Plane Crashes, Killing All 19",
            "body": "A Russian military cargo aircraft crashed during flight operations on Tuesday; defense officials confirmed all 19 crew and passengers on board perished."
        },
        {
            "tag": "SECURITY",
            "head": "US Soldier Arrested in UK on Suspicion of Spying",
            "body": "British police detained an American soldier on suspicion of espionage before formally transferring the serviceman into US military custody."
        },
        {
            "tag": "WEST BANK",
            "head": "Palestinian Woman, 72, Shot Dead by Settlers",
            "body": "A 72-year-old Palestinian woman was shot dead by Israeli settlers in the West Bank, the Palestinian health ministry reported on Tuesday."
        }
    ]

    story_y = 345
    story_slot_h = 270

    for idx, story in enumerate(right_stories):
        # Category label badge
        draw.rectangle([right_col_x, story_y, right_col_x + 180, story_y + 32], fill="#0F172A")
        draw.text((right_col_x + 10, story_y + 5), story["tag"], fill="#FFFFFF", font=fonts["tag_bold"])

        # Headline
        head_lines = wrap_text(draw, story["head"], fonts["story_head"], right_col_w)
        hy = story_y + 42
        for hl in head_lines:
            draw.text((right_col_x, hy), hl, fill="#0F172A", font=fonts["story_head"])
            hy += 36

        # One short line summary
        body_lines = wrap_text(draw, story["body"], fonts["story_body"], right_col_w)
        by = hy + 8
        for bl in body_lines:
            draw.text((right_col_x, by), bl, fill="#334155", font=fonts["story_body"])
            by += 29

        # Dividing line between right-column stories
        if idx < len(right_stories) - 1:
            divider_y = story_y + story_slot_h
            draw.line([(right_col_x, divider_y), (margin_x + content_w, divider_y)], fill="#E2E8F0", width=1)
            story_y += story_slot_h + 8

    # ----------------------------------------------------
    # BOTTOM STRIP: TECH / TRADE, SPACE, CULTURE
    # ----------------------------------------------------
    bottom_y_start = 1730
    draw.line([(margin_x, bottom_y_start), (margin_x + content_w, bottom_y_start)], fill="#0F172A", width=4)
    draw.line([(margin_x, bottom_y_start + 6), (margin_x + content_w, bottom_y_start + 6)], fill="#0F172A", width=1)

    # Section title
    strip_header_y = bottom_y_start + 14
    draw.text((margin_x, strip_header_y), "GLOBAL BRIEFINGS & DEPARTMENTS", fill="#0F172A", font=fonts["tag_bold"])
    draw.text((margin_x + content_w - 380, strip_header_y), "TECH · SCIENCE · WORLD CULTURE", fill="#64748B", font=fonts["tag_bold"])

    strip_content_y = strip_header_y + 36
    draw.line([(margin_x, strip_content_y - 6), (margin_x + content_w, strip_content_y - 6)], fill="#CBD5E1", width=1)

    bottom_cols = [
        {
            "tag": "TECH / TRADE",
            "head": "Megaspeed Probed Over Nvidia Chip Exports",
            "body": "Nvidia partner Megaspeed is under US government investigation over chip exports, as new US restrictions on Southeast Asia tighten supply into China."
        },
        {
            "tag": "SPACE EXPLORATION",
            "head": "Japanese Probe Changes Target Over Engine Fault",
            "body": "A Japanese deep-space probe was forced to alter its primary mission trajectory to a secondary asteroid target after suffering severe propulsion anomalies."
        },
        {
            "tag": "CULTURE & MONARCHY",
            "head": "William & Kate Celebrate Earthshot in Mumbai",
            "body": "The Prince and Princess of Wales attended the Earthshot Prize awards in Mumbai, honoring pioneering innovators leading global environmental solutions."
        }
    ]

    col_w = (content_w - 60) // 3
    for c_idx, bcol in enumerate(bottom_cols):
        cx = margin_x + c_idx * (col_w + 30)

        # Tag
        draw.text((cx, strip_content_y), bcol["tag"], fill="#B91C1C", font=fonts["sans_bold"](19))

        # Headline
        bh_lines = wrap_text(draw, bcol["head"], fonts["story_head"], col_w)
        bhy = strip_content_y + 28
        for bhl in bh_lines:
            draw.text((cx, bhy), bhl, fill="#0F172A", font=fonts["story_head"])
            bhy += 34

        # Summary line
        bb_lines = wrap_text(draw, bcol["body"], fonts["story_body"], col_w)
        bby = bhy + 6
        for bbl in bb_lines:
            draw.text((cx, bby), bbl, fill="#334155", font=fonts["story_body"])
            bby += 27

        # Vertical separator between bottom columns
        if c_idx < 2:
            sep_x = cx + col_w + 15
            draw.line([(sep_x, strip_content_y), (sep_x, 2005)], fill="#E2E8F0", width=1)

    # ----------------------------------------------------
    # FOOTER BAR
    # ----------------------------------------------------
    draw.line([(margin_x, 2012), (margin_x + content_w, 2012)], fill="#0F172A", width=2)
    footer_text = "THE WORLD · SPECIAL EDITION FOR 17 NOVEMBER 2026 · MAKE.FUN COMPETITION ENTRY · ALL STORIES VERIFIED"
    tb_f = draw.textbbox((0, 0), footer_text, font=fonts["sans"](18))
    draw.text(((canvas_w - (tb_f[2] - tb_f[0])) // 2, 2022), footer_text, fill="#64748B", font=fonts["sans"](18))

    # Downscale 2x (2048x2048) -> 1x (1024x1024) with LANCZOS
    img_downscaled = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    return img_downscaled


def main():
    print("Generating front page image at 2x resolution (2048x2048)...")
    final_image = build_world_news_page()
    output_path = os.path.join(os.path.dirname(__file__), "entry.png")
    final_image.save(output_path, format="PNG", optimize=True)
    size_bytes = os.path.getsize(output_path)
    print(f"Saved {output_path} ({final_image.width}x{final_image.height}, {size_bytes} bytes, {size_bytes / 1024:.1f} KiB)")


if __name__ == "__main__":
    main()
