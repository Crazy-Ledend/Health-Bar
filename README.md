# Health-Bar
A health bar made especially for pokemon battles but can be modified for other battles too

-----------------------------------------------------------------------

# 🖼️ Pokémon HUD with Pygame

A dynamic, visually styled HUD (Heads-Up Display) built with Pygame, mimicking the classic Pokémon battle interface. It displays Pokémon name, level, current HP, status conditions, and stat changes in a compact status bar format.

---

## 📦 Features

* Custom Pokémon name and level display.
* Slanted **HP bar** with animated fill and highlight effect.
* Colored **status condition** box (e.g., FRZ, PAR, BRN).
* Optional stat change boxes (e.g., 2.0xATK, 0.5xDEF).
* Rounded box styling and shadow layers for a clean UI look.
* Modular layout for easy integration into battle systems.

---

## ✍️ Configurable Values

You can modify these **variables** at the top of the script to dynamically update the HUD:

```python
pokemon_name = "Spoink"  # Pokémon Name
lvl = "Lvl: 53"          # Pokémon Level Display
current_hp = 40          # Current HP
max_hp = 100             # Max HP
status = "FRZ"           # Status condition (e.g., PAR, BRN, PSN, FRZ, TOX, SLP)

stat_changes = {         # Stat stage multipliers (default 1.0 = no change)
    "HP": 1.0,
    "ATK": 1.5,
    "DEF": 0.5,
    "SPA": 4.0,
    "SPD": 1.5,
    "SPE": 2.0
}
```

---

## 🖼️ Pokémon Icon (Optional)

To display an icon beside the name:

* Save a Pokémon image as `"Gallade.png"` (or change filename inside the `draw_status_box()` function).
* Recommended size before scaling: \~96×96px.
* The icon is auto-scaled to 30×30px and positioned left of the name.

---

## 🎨 Color Indicators

* **HP bar** colors:

  * Green (>66%)
  * Yellow (33–66%)
  * Red (<33%)
* **Status box** colors:

  * Custom per condition (e.g., blue for FRZ, orange for BRN)
* **Stat change boxes**:

  * Green = buffed stat
  * Red = debuffed stat

---

## 🧩 Dependencies

* Python 3.x
* `pygame` library

Install pygame using:

```bash
pip install pygame
```

---

## ▶️ How to Run

Save the file as `hud.py`, then run:

```bash
python hud.py
```

A window will open showing the HUD. Close it to exit.

---

## 🧠 Logic Overview

* `draw_status_box()` handles rendering the entire HUD, including the HP bar, name, level, status, and stat boxes.
* `draw_hp_bar()` renders the slanted HP bar with shaded highlights.
* `draw_stat_boxes()` arranges buffs/debuffs into columns dynamically.
* Utility functions manage color mapping and rectangle drawing.

---

## 🧪 Tips for Integration

You can:

* Replace the static variables with dynamic values from your battle engine.
* Customize fonts, sizes, and colors to match your game’s aesthetic.
* Modularize each draw function for reuse in other scenes.
