from PIL import Image, ImageDraw, ImageFont
import os

# Constants
WHITE = (255, 255, 255, 255)
WHITE_30 = (255, 255, 255, 76)
BLACK = (0, 0, 0, 255)
BLACK_30 = (0, 0, 0, 51)
GRAY = (50, 50, 50, 255)
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
        main_font = ImageFont.truetype("arial.ttf", 20)
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
    return LIGHT_GREEN if ratio > 0.45 else LIGHT_YELLOW if ratio > 0.2 else LIGHT_RED

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

def generate_hud(name, level, current_hp, max_hp, status=None, stat_changes=None):
    name_font, main_font, stat_font = load_fonts()
    ratio = current_hp / max_hp if max_hp else 0

    img = Image.new("RGBA", (500, 150), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background
    draw_rounded_rectangle(draw, (0, 0, 450, 100), 16, fill=BLACK_30)
    draw_rounded_rectangle(draw, (25, 10, 425, 90), 16, fill=WHITE_30)

    # Name and Level
    draw.text((40, 15), name.title(), font=name_font, fill=BLACK)
    draw.text((300, 15), f"Lvl: {level}", font=name_font, fill=BLACK)
    
    # HP Bar
    draw_hp_bar(draw, 40, 55, 280, 22, ratio)
    draw.text((325, 53), f"[{current_hp} / {max_hp}]", font=main_font, fill=WHITE)

    # Status and Stat Changes
    if status:
        color = get_status_color(status)
        padding = 10
        status_txt = status.upper()
        sw = main_font.getlength(status_txt)
        box_w, box_h = sw + padding * 2, 32
        draw_rounded_rectangle(draw, (55, 95, 60 + box_w, 85 + box_h), 10, fill=color)
        draw.text((60 + padding, 95), status_txt, font=main_font, fill=WHITE)

    if stat_changes:
        start_x = 60 + box_w + 10 if status else 60
        draw_stat_boxes(draw, stat_changes, start_x, 93, stat_font)

    return img

# Example usage with all stats
# REPLACE THESE VALUES WITH THE ACTUAL POKE DETAILS
img = generate_hud(
    name="Pikachu",
    level=35,
    current_hp=75,
    max_hp=100,
    status="FRZ",
    stat_changes={
        "HP": 1.0,
        "ATK": 1.5, 
        "DEF": 0.5,
        "SPA": 2.0,
        "SPD": 0.25,
        "SPE": 3.0
    }
)

# Returns the image
return img
