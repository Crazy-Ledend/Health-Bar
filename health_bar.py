from PIL import Image, ImageDraw, ImageFont
import os

# Constants
WHITE = (255, 255, 255, 255)
WHITE_30 = (255, 255, 255, 76)
BLACK = (0, 0, 0, 255)
BLACK_30 = (0, 0, 0, 51)
GRAY = (50, 50, 50, 255)
LIGHT_GRAY = (70, 70, 70, 255)
GREEN = (0, 200, 0, 255)
LIGHT_GREEN = (150, 255, 150, 255)
PALE_GREEN = (229, 255, 224, 255)
YELLOW = (255, 200, 0, 255)
LIGHT_YELLOW = (255, 255, 150, 255)
RED = (200, 50, 50, 255)
LIGHT_RED = (255, 150, 150, 255)
PALE_RED = (255, 229, 224, 255)

# Fonts
def load_fonts():
    try:
        name_font = ImageFont.truetype("arialbd.ttf", 26)
        main_font = ImageFont.truetype("arialbd.ttf", 18)
        stat_font = ImageFont.truetype("arial.ttf", 17)
    except:
        name_font = ImageFont.load_default()
        main_font = ImageFont.load_default()
        stat_font = ImageFont.load_default()
    return name_font, main_font, stat_font

# Helpers
def get_status_color(status):
    return {
        "PAR": (184, 184, 24, 255),
        "BRN": (224, 112, 80, 255),
        "PSN": (192, 96, 192, 255),
        "TOX": (192, 96, 192, 255),
        "SLP": (160, 160, 136, 255),
        "FRZ": (136, 176, 224, 255),
    }.get(status.upper(), GRAY)

def get_hp_color(ratio):
    return GREEN if ratio > 0.66 else YELLOW if ratio > 0.33 else RED

def get_light_color(ratio):
    return LIGHT_GREEN if ratio > 0.66 else LIGHT_YELLOW if ratio > 0.33 else LIGHT_RED

def draw_hp_bg(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    height_scale = 0.8

    # Reduce height by scaling around the center
    mid_y = (y1 + y2) / 2
    half_height = (y2 - y1) * height_scale / 2
    y1, y2 = mid_y - half_height, mid_y + half_height

    # Main rectangle body (pointed right, rounded left)
    draw.rectangle((x1 + (radius * 1.8), y1, x2 + radius + 6, y2),
                   fill=fill, outline=outline, width=width)

    # Rounded left side
    draw.pieslice((x1 + radius, y1, x1 + 2 * radius, y1 + 2 * radius),
                  180, 270, fill=fill, outline=outline)
    draw.pieslice((x1 + radius, y2 - 2 * radius, x1 + 2 * radius, y2),
                  90, 180, fill=fill, outline=outline)

    # Fill between the rounded corners
    draw.rectangle((x1 + radius, y1 + radius, x1 + 2 * radius, y2 - radius),
                   fill=fill, outline=outline, width=width)

def draw_rounded_rectangle(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rectangle((x1 + radius, y1, x2 - radius, y2), fill=fill, outline=outline, width=width)
    draw.rectangle((x1, y1 + radius, x2, y2 - radius), fill=fill, outline=outline, width=width)
    draw.pieslice((x1, y1, x1 + 2*radius, y1 + 2*radius), 180, 270, fill=fill, outline=outline)
    draw.pieslice((x2 - 2*radius, y1, x2, y1 + 2*radius), 270, 360, fill=fill, outline=outline)
    draw.pieslice((x1, y2 - 2*radius, x1 + 2*radius, y2), 90, 180, fill=fill, outline=outline)
    draw.pieslice((x2 - 2*radius, y2 - 2*radius, x2, y2), 0, 90, fill=fill, outline=outline)

def draw_hp_bar(draw, x, y, width, height, ratio):
    slant = 20
    fill_width = width * ratio
    fill_right = x + fill_width

    base = [
        (x + slant, y), (x + width, y),
        (x + width - slant, y + height), (x, y + height)
    ]
    fill = [
        (x + slant, y), (min(fill_right, x + width), y),
        (max(x, min(fill_right - slant, x + width - slant)), y + height), (x, y + height)
    ]
    highlight = [
        (x + (slant // 2) + 10, y + 2),
        (min(fill_right - 2, x + width - 20), y + 2),
        (max(x, min(fill_right - (slant // 2) - 20, x + width - (slant // 2) - 20)), y + height // 2),
        (x + 10, y + height // 2)
    ]

    draw.polygon(base, fill=GRAY)
    draw.polygon(fill, fill=get_hp_color(ratio))
    draw.polygon(highlight, fill=get_light_color(ratio))
    draw.polygon(base, outline=BLACK, width=4)

def draw_stat_boxes(draw, stat_changes, x, y, font):
    spacing_x = 70
    spacing_y = 28
    box_width = 65
    box_height = 24
    
    # Standard stat order
    stat_order = ['HP', 'ATK', 'DEF', 'SPA', 'SPD', 'SPE']
    
    # Convert input to uppercase and filter unchanged stats
    stat_changes = {k.upper(): v for k, v in stat_changes.items()}
    filtered_stats = [(stat, stat_changes[stat]) for stat in stat_order 
                     if stat in stat_changes and stat_changes[stat] != 1.0]
    
    for i, (stat, val) in enumerate(filtered_stats):
        col, row = i % 3, i // 3
        bx = x + col * (spacing_x + 15)
        by = y + row * spacing_y

        bg, border, txt = ((PALE_GREEN, GREEN, GREEN) if val > 1.0 
                          else (PALE_RED, RED, RED))
        
        # Draw stat box
        draw_rounded_rectangle(draw, (bx, by, bx + box_width + 14, by + box_height), 6, fill=border)
        draw_rounded_rectangle(draw, (bx + 1, by + 1, bx + box_width + 13, by + box_height - 1), 5, fill=bg)

        # Draw stat text
        label = f"{val:.1f}x{stat}"
        tw = font.getlength(label)
        draw.text((bx + (box_width + 14 - tw) / 2, by + 2), label, fill=txt, font=font)

# def draw_translucent_square(draw, x, y, size, radius=6):
#     rect = (x, y, x + size, y + size)
#     fill = (255, 255, 255, 76)  # white_30 → 30% opacity
#     draw.rounded_rectangle(rect, radius=radius, fill=fill)

def draw_hazard_icons(img, effects, x, y, size=42, spacing=5):
    """Draw up to 4 hazard icons (2x2 grid) to the given position."""
    from PIL import Image

    icon_paths = {
        "STEALTH_ROCK": "rock1.png",
        "SPIKES": "spike.png",
        "TOXIC_SPIKES": "t_spike.png",
        "STICKY_WEB": "web.png"
    }

    # Filter to only valid hazards
    active = [eff.upper() for eff in effects if eff.upper() in icon_paths]
    active = active[:4]  # Max 4 icons

    for i, effect in enumerate(active):
        try:
            icon = Image.open(icon_paths[effect]).convert("RGBA")
            icon = icon.resize((size, size), Image.Resampling.LANCZOS)
        except FileNotFoundError:
            continue  # Skip missing icons

        col, row = i % 2, i // 2
        pos_x = x + col * (size + spacing)
        pos_y = y + row * (size + spacing)
        img.paste(icon, (pos_x, pos_y), icon)

def draw_battle_effects(draw, effects, x, y, font):
    spacing_x = 70
    spacing_y = 28
    box_width = 65
    box_height = 24
    
    # Effect colors with light backgrounds and clear text contrast
    effect_colors = {
        # Format: (background, border, text)
        'LEECH_SEED': ((229, 255, 224), (100, 200, 100), (0, 100, 0)),       # Pale green / Leaf green text
        'STEALTH_ROCK': ((235, 222, 210), (139, 69, 19), (101, 67, 33)),      # Stone white / Brown text
        'SPIKES': ((255, 239, 213), (210, 180, 140), (160, 120, 60)),         # Light caramel / Dark caramel text
        'TOXIC_SPIKES': ((240, 224, 255), (192, 96, 192), (96, 32, 96)),     # Pale purple / Deep purple text
        'STICKY_WEB': ((240, 240, 240), (160, 160, 160), (40, 40, 40)),      # Off-white / Dark gray text + border
        'LIGHT_SCREEN': ((255, 255, 224), (255, 255, 0), (150, 150, 0)),     # Light yellow / Olive text
        'REFLECT': ((255, 253, 208), (255, 215, 0), (180, 140, 0)),          # Brighter yellow / Gold text
        'AURORA_VEIL': ((224, 255, 255), (135, 206, 250), (0, 100, 150))     # Ice blue / Deep blue text
    }
    
    # Effect display names
    effect_names = {
        'LEECH_SEED': "Seed",
        'STEALTH_ROCK': "Rocks",
        'SPIKES': "Spikes",
        'TOXIC_SPIKES': "T.Spikes",
        'STICKY_WEB': "Web",
        'LIGHT_SCREEN': "Screen",
        'REFLECT': "Reflect",
        'AURORA_VEIL': "Veil"
    }
    
    active_effects = [eff.upper() for eff in effects if eff.upper() in effect_colors]
    
    for i, effect in enumerate(active_effects):
        col, row = i % 3, i // 3
        bx = x + col * (spacing_x + 15)
        by = y + row * spacing_y

        bg, border, txt = effect_colors.get(effect, ((240, 240, 240), (200, 200, 200), (0, 0, 0)))
        
        # Draw effect box with consistent styling
        if effect == 'STICKY_WEB':
            draw_rounded_rectangle(draw, (bx, by, bx + box_width + 14, by + box_height), 6, fill=(0, 0, 0, 0))
        else:
            draw_rounded_rectangle(draw, (bx, by, bx + box_width + 14, by + box_height), 6, fill=(border))

        draw_rounded_rectangle(draw, (bx + 1, by + 1, bx + box_width + 13, by + box_height - 1), 5, fill=bg)

        # Special visibility treatment for Sticky Web
        # if effect == 'STICKY_WEB':
        #     draw.rectangle((bx, by, bx + box_width + 14, by + box_height), outline=(0, 0, 0), width=2)

        # Draw text with optimal contrast
        label = effect_names.get(effect, effect)
        tw = font.getlength(label)
        text_x = bx + (box_width + 14 - tw) / 2
        text_y = by + (box_height - 20) / 2  # Vertically centered
        
        # Text shadow for better readability
        draw.text((text_x + 1, text_y + 1), label, fill=(128, 128, 128, 50), font=font)
        draw.text((text_x, text_y), label, fill=txt, font=font)

def generate_hud(name, level, current_hp, max_hp, status=None, stat_changes=None, battle_effects=None):
    name_font, main_font, stat_font = load_fonts()
    ratio = current_hp / max_hp if max_hp else 0

    # Calculate required height based on content
    base_height = 150
    stat_rows = 0
    effect_rows = 0
    
    # Calculate rows needed for stat changes
    if stat_changes:
        filtered_stats = {k.upper(): v for k, v in stat_changes.items() 
                         if v != 1.0 and k.upper() in ['HP', 'ATK', 'DEF', 'SPA', 'SPD', 'SPE']}
        stat_rows = (len(filtered_stats) + 2) // 3  # 3 stats per row
    
    # Calculate rows needed for battle effects
    if battle_effects:
        active_effects = [eff.upper() for eff in battle_effects if eff.upper() in {
            'LEECH_SEED', 'STEALTH_ROCK', 'SPIKES', 'TOXIC_SPIKES', 
            'STICKY_WEB', 'LIGHT_SCREEN', 'REFLECT', 'AURORA_VEIL'}]
        effect_rows = (len(active_effects) + 2) // 3  # 3 effects per row
    
    # Adjust image height if needed
    extra_height = max(0, ((stat_rows + effect_rows) * 36) - 20)  # 32px per row, 20px original space
    total_height = base_height + extra_height
    
    img = Image.new("RGBA", (500, total_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background (extend if needed)
    bg_height = 100 + extra_height
    draw_rounded_rectangle(draw, (0, 0, 450, bg_height), 16, fill=BLACK_30)
    draw_rounded_rectangle(draw, (25, 10, 425, bg_height - 10), 16, fill=WHITE_30)

    # Name and Level
    draw.text((40, 15), name.title(), font=name_font, fill=BLACK)
    draw.text((300, 15), f"Lvl: {level}", font=name_font, fill=BLACK)
    
    # HP Bar
    draw_hp_bar(draw, 40, 55, 280, 22, ratio)
    
    hp_text = f"[{current_hp} / {max_hp}]"
    tw = main_font.getlength(hp_text)
    th = 22  # approximate text height
    tx, ty = 326, 56  # existing text position

    # Padding and background box
    padding_x, padding_y = 6, 2
    bg_x1, bg_y1 = tx - padding_x, ty - padding_y
    bg_x2, bg_y2 = tx + tw + padding_x, ty + th + padding_y

    draw_hp_bg(draw, (bg_x1 + 1, bg_y1 - 1, bg_x2 - 5, bg_y2 + 1), 6, fill=LIGHT_GRAY)
    draw.text((tx + 8, ty), f"[{current_hp} / {max_hp}]", font=main_font, fill=WHITE)


    # Status and Stat Changes/Battle Effects
    if status:
        color = get_status_color(status)
        padding = 10
        status_txt = status.upper()
        sw = main_font.getlength(status_txt)
        box_w, box_h = sw + padding * 2, 32
        draw_rounded_rectangle(draw, (55, 95, 55 + box_w, 95 + box_h), 10, fill=color)
        draw.text((55 + padding, 100), status_txt, font=main_font, fill=WHITE)

    # Starting positions
    start_x = 60 + (box_w + 10 if status else 0)
    start_y = 93
    
    # Draw stat changes first
    if stat_changes:
        draw_stat_boxes(draw, stat_changes, start_x, start_y, stat_font)
        start_y += stat_rows * 32  # Move down for battle effects
    
    # Draw battle effects immediately below
    if battle_effects:
        draw_battle_effects(draw, battle_effects, start_x, start_y, stat_font)

    return img

# REPLACE THIS PART WITH ACTUAL STATS OR USE FUNCTION CALLING
# Example usage with all stats
# img = generate_hud(
#     name="Pikachu",
#     level=35,
#     current_hp=111,
#     max_hp=338,
#     status="FRZ",
#     stat_changes={
#         "HP": 1.0,
#         "ATK": 1.5, 
#         "DEF": 0.5,
#         "SPA": 2.0,
#         "SPD": 0.25,
#         "SPE": 3.0
#     },
#     battle_effects=["STEALTH_ROCK", "STICKY_WEB", "LEECH_SEED", "TOXIC_SPIKES", "SPIKES"]
# )

# Save the result
# output_path = "pokemon_hud.png"
# img.save(output_path)
# print(f"Successfully generated Pokémon HUD at {output_path}")
