#!/usr/bin/env python3
"""Plot the Figure 3 training-time safety-autonomy tradeoff from JSON."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "fig3_safety_autonomy_tradeoff.json"
OUTPUT_PATH = (
    HERE.parent.parent
    / "response"
    / "figures"
    / "fig3_safety_autonomy_trajectory.png"
)

ORDER = ["c", "f", "e", "d"]
CHECKPOINT_MARKERS = {
    10000: "circle",
    40000: "square",
    70000: "triangle",
    100000: "diamond",
}
COLORS = {
    "c": "#2f9e44",
    "f": "#7b61a8",
    "e": "#2878b5",
    "d": "#d63333",
}

WIDTH, HEIGHT = 2048, 1280
LEFT, RIGHT, TOP, BOTTOM = 190, 70, 330, 170
PLOT_RIGHT = WIDTH - RIGHT
PLOT_BOTTOM = HEIGHT - BOTTOM
X_MIN, X_MAX = 79.0, 101.0
Y_MIN, Y_MAX = 0.0, 30.0


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)


def x_px(value: float) -> float:
    return LEFT + (value - X_MIN) / (X_MAX - X_MIN) * (PLOT_RIGHT - LEFT)


def y_px(value: float) -> float:
    return PLOT_BOTTOM - (value - Y_MIN) / (Y_MAX - Y_MIN) * (PLOT_BOTTOM - TOP)


def centered(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, text_font, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=text_font)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1]), text, font=text_font, fill=fill)


def draw_x(draw: ImageDraw.ImageDraw, x: float, y: float, color: str, size: int = 9) -> None:
    draw.line((x - size, y - size, x + size, y + size), fill=color, width=4)
    draw.line((x - size, y + size, x + size, y - size), fill=color, width=4)


def draw_marker(draw: ImageDraw.ImageDraw, x: float, y: float, shape: str, color: str, size: int = 12) -> None:
    style = {"fill": color, "outline": "white", "width": 2}
    if shape == "circle":
        draw.ellipse((x - size, y - size, x + size, y + size), **style)
    elif shape == "square":
        draw.rectangle((x - size, y - size, x + size, y + size), **style)
    elif shape == "triangle":
        draw.polygon(((x, y - size - 3), (x + size + 2, y + size), (x - size - 2, y + size)), **style)
    elif shape == "diamond":
        radius = size + 3
        draw.polygon(((x, y - radius), (x + radius, y), (x, y + radius), (x - radius, y)), **style)
    else:
        raise ValueError(f"Unknown checkpoint marker: {shape}")


def main() -> None:
    with DATA_PATH.open(encoding="utf-8") as handle:
        data = json.load(handle)

    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    title_font = font(48, bold=True)
    label_font = font(31, bold=True)
    tick_font = font(24)
    legend_font = font(26)
    legend_small_font = font(22)

    centered(
        draw,
        (WIDTH / 2, 35),
        "Training-time safety-autonomy tradeoff curve",
        title_font,
        "#222222",
    )

    legend_positions = {
        "c": (LEFT + 10, 128),
        "f": (LEFT + 770, 128),
        "e": (LEFT + 10, 186),
        "d": (LEFT + 770, 186),
    }
    completeness: dict[str, bool] = {}
    for key in ORDER:
        ablation = data["ablations"][key]
        complete = all(
            all(value is not None for value in point["xy"])
            for point in ablation["points"]
        )
        completeness[key] = complete
        lx, ly = legend_positions[key]
        if complete:
            draw.line((lx, ly + 17, lx + 72, ly + 17), fill=COLORS[key], width=7)
            label = f"({key}) {ablation['label']}"
        else:
            draw_x(draw, lx + 35, ly + 17, COLORS[key])
            label = f"({key}) {ablation['label']} — pending"
        draw.text((lx + 90, ly), label, font=legend_font, fill="#292929")

    draw.text(
        (LEFT + 10, 243),
        "Checkpoints:",
        font=legend_small_font,
        fill="#555555",
    )
    for index, (checkpoint, shape) in enumerate(CHECKPOINT_MARKERS.items()):
        lx = LEFT + 185 + index * 190
        draw_marker(draw, lx, 257, shape, "#444444")
        draw.text((lx + 25, 243), f"{checkpoint // 1000}k", font=legend_small_font, fill="#555555")
    draw.text(
        (LEFT + 10, 277),
        "Averaged over training data from all 40 training objects",
        font=legend_small_font,
        fill="#555555",
    )
    for x_tick in (80, 85, 90, 95, 100):
        px = x_px(x_tick)
        draw.line((px, TOP, px, PLOT_BOTTOM), fill="#d5dce4", width=2)
        centered(draw, (px, PLOT_BOTTOM + 24), str(x_tick), tick_font, "#333333")
    for y_tick in range(0, 31, 5):
        py = y_px(y_tick)
        draw.line((LEFT, py, PLOT_RIGHT, py), fill="#d5dce4", width=2)
        text = str(y_tick)
        box = draw.textbbox((0, 0), text, font=tick_font)
        draw.text((LEFT - 30 - (box[2] - box[0]), py - 14), text, font=tick_font, fill="#333333")

    draw.rectangle((LEFT, TOP, PLOT_RIGHT, PLOT_BOTTOM), outline="#3f3f3f", width=2)

    for key in ORDER:
        if not completeness[key]:
            continue
        points = data["ablations"][key]["points"]
        coords = [(x_px(point["xy"][0]), y_px(point["xy"][1])) for point in points]
        draw.line(coords, fill=COLORS[key], width=7, joint="curve")
        for point, (px, py) in zip(points, coords):
            draw_marker(draw, px, py, CHECKPOINT_MARKERS[point["training_episodes"]], COLORS[key])

    x_label = "Student autonomy = 100 - teacher-intervention rate (%)"
    centered(draw, (WIDTH / 2, HEIGHT - 90), x_label, label_font, "#222222")

    y_label = "Unsafe-episode rate during distillation (%)"
    y_box = label_font.getbbox(y_label)
    y_image = Image.new("RGBA", (y_box[2] - y_box[0] + 20, y_box[3] - y_box[1] + 20), (255, 255, 255, 0))
    y_draw = ImageDraw.Draw(y_image)
    y_draw.text((10, 5), y_label, font=label_font, fill="#222222")
    y_image = y_image.rotate(90, expand=True)
    image.paste(y_image, (32, int((HEIGHT - y_image.height) / 2 + 45)), y_image)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT_PATH, optimize=True)
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
