import pygame
import sys

# Setup
pygame.init()
screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Pokémon HUD")

# Font
font = pygame.font.SysFont("Trebuchet MS", 24, bold=True)
name_font = pygame.font.SysFont("Verdana", 26, bold=True)

# Data
pokemon_name = "Spoink"
lvl = "Lvl: 53"
current_hp = 40
max_hp = 100
status = "FRZ"  # PAR, BRN, PSN, TOX, SLP, FRZ

# Stat changes
stat_changes = {
    "HP": 1.0,
    "ATK": 1.5,
    "DEF": 0.5,
    "SPA": 4.0,
    "SPD": 1.5,
    "SPE": 2.0
}

# Colors
WHITE = (255, 255, 255)
WHITE_30 = (255, 255, 255, 76)
BLACK = (0, 0, 0)
BLACK_30 = (0, 0, 0, 51)
GRAY = (50, 50, 50)
GREEN = (0, 200, 0)
LIGHT_GREEN = (150, 255, 150)
PALE_GREEN = (229,255,224,255)
YELLOW = (255, 200, 0)
LIGHT_YELLOW = (255, 255, 150)
RED = (200, 50, 50)
LIGHT_RED = (255, 150, 150)
PALE_RED = (255,229,224,255)

# Helpers
def get_status_color(status):
    status_colors = {
        "PAR": (184,184,24,255),
        "BRN": (224,112,80,255),
        "PSN": (192,96,192,255),
        "TOX": (192,96,192,255),
        "SLP": (160,160,136,255),
        "FRZ": (136,176,224,255),
    }
    return status_colors.get(status.upper(), GRAY)

def get_hp_color(ratio):
    if ratio > 0.66:
        return GREEN
    elif ratio > 0.33:
        return YELLOW
    else:
        return RED

def get_light_color(ratio):
    if ratio > 0.45:
        return LIGHT_GREEN
    elif ratio > 0.2:
        return LIGHT_YELLOW
    else:
        return LIGHT_RED

def draw_rounded_rect(surface, color, rect, radius=12):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_hp_bar(surface, x, y, width, height, ratio):
    slant = 20  # Slant offset
    fill_width = width * ratio

    outline_points = [
        (x + slant, y),
        (x + width, y),
        (x + width - slant, y + height),
        (x, y + height)
    ]

    # Base
    pygame.draw.polygon(surface, GRAY, outline_points)

    # Filled portion
    fill_right = x + fill_width
    fill_points = [
        (x + slant, y),
        (min(fill_right, x + width), y),
        (max(x, min(fill_right - slant, x + width - slant)), y + height),
        (x, y + height)
    ]
    pygame.draw.polygon(surface, get_hp_color(ratio), fill_points)

    # Highlight portion
    highlight_points = [
        (x + (slant // 2) + 10, y + 2),
        (min(fill_right - 2, x + width - 20), y + 2),
        (max(x, min(fill_right - (slant // 2) - 20, x + width - (slant // 2) - 20)), y + height // 2),
        (x + 10, y + height // 2)
    ]
    pygame.draw.polygon(surface, get_light_color(ratio), highlight_points)
    pygame.draw.polygon(surface, BLACK, outline_points, width=4)


def draw_stat_boxes(surface, start_x, start_y, spacing_x=70, spacing_y=28, box_width=65, box_height=24):
    font_small = pygame.font.SysFont("Verdana", 17, bold=True)

    # Filter out stats with no change
    filtered_stats = [(stat, change) for stat, change in stat_changes.items() if change != 1.0]

    for idx, (stat, change) in enumerate(filtered_stats):
        col = idx % 3  # 3 columns 
        row = idx // 3  # 2 rows 

        x = start_x + col * (spacing_x + 15)
        y = start_y + row * (spacing_y + 3)

        # Choose color based on stat change value
        if change > 1.0:
            bg_color = PALE_GREEN
            border_color = GREEN
            text_color = GREEN
        else: 
            bg_color = PALE_RED
            border_color = RED
            text_color = RED

        border = pygame.Rect(x, y, box_width+14, box_height)
        rect = pygame.Rect(x+1, y+1, box_width+12, box_height-2)
        draw_rounded_rect(surface, border_color, border, radius=6)
        draw_rounded_rect(surface, bg_color, rect, radius=5)

        # Render text 
        text_str = f"{change:.1f}x{stat}"
        text_surf = font_small.render(text_str, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)

        surface.blit(text_surf, text_rect)


def draw_status_box():
    bar_x, bar_y = 70, 120
    bar_width, bar_height = 300, 22
    ratio = current_hp / max_hp

    # Icon
    try:
        poke_icon = pygame.image.load("Gallade.png").convert_alpha()
        poke_icon = pygame.transform.scale(poke_icon, (30, 30))
        screen.blit(poke_icon, (bar_x - 20, bar_y - 48))
    except:
        pass

    # Name
    name_text = name_font.render(pokemon_name, True, BLACK)
    screen.blit(name_text, (bar_x, bar_y - 43))
    lvl_text = name_font.render(lvl, True, BLACK)
    screen.blit(lvl_text, (bar_x+320, bar_y - 43))

    # HUD Background
    bg_surface = pygame.Surface((400, 100), pygame.SRCALPHA)
    draw_rounded_rect(bg_surface, WHITE_30, bg_surface.get_rect(), radius=16)
    screen.blit(bg_surface, (50, 100))

    border_surface = pygame.Surface((450, 120), pygame.SRCALPHA)
    draw_rounded_rect(border_surface, BLACK_30, border_surface.get_rect(), radius=16)
    screen.blit(border_surface, (50, 100))

    # HP Bar
    draw_hp_bar(screen, bar_x, bar_y, bar_width, bar_height, ratio)

    # HP Text
    hp_text = font.render(f"[{current_hp} / {max_hp}]", True, BLACK)
    screen.blit(hp_text, (bar_x + bar_width + 15, bar_y))

    # Status box
    if status:
        status_color = get_status_color(status)
        status_text = font.render(status.upper(), True, WHITE)
        padding = 10
        text_w, text_h = status_text.get_size()
        box_w = text_w + padding * 2
        box_h = text_h + 8
        status_rect = pygame.Rect(bar_x, bar_y + 35, box_w, box_h)
        draw_rounded_rect(screen, status_color, status_rect, radius=10)
        screen.blit(status_text, (status_rect.x + padding, status_rect.y + 4))

        # Draw stat boxes to the right of status box
        stat_box_start_x = status_rect.right + 10
        stat_box_start_y = status_rect.y
        draw_stat_boxes(screen, stat_box_start_x, stat_box_start_y)
    else:
        # If no status
        bar_x, bar_y = 70, 120
        stat_box_start_x = bar_x
        stat_box_start_y = bar_y + 35
        draw_stat_boxes(screen, stat_box_start_x, stat_box_start_y)


# Game loop
clock = pygame.time.Clock()
while True:
    screen.fill((235, 235, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_status_box()
    pygame.display.flip()
    clock.tick(60)
