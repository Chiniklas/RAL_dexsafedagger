#!/usr/bin/env python3
"""Render compact verification sheets from VisDex point-cloud assets."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import pickle
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def load_points(asset_dir: Path) -> np.ndarray:
    with (asset_dir / "point_cloud_1000_pts.pkl").open("rb") as stream:
        points = np.asarray(pickle.load(stream), dtype=np.float32)
    points = points - points.mean(axis=0, keepdims=True)
    extent = np.ptp(points, axis=0)
    scale = float(max(extent.max(), 1.0e-6))
    return points / scale


def draw_asset(axis, points: np.ndarray, title: str, azimuth: float) -> None:
    axis.scatter(
        points[:, 0],
        points[:, 1],
        points[:, 2],
        c=points[:, 2],
        cmap="viridis",
        s=2.0,
        alpha=0.9,
        linewidths=0,
    )
    axis.view_init(elev=22, azim=azimuth)
    axis.set_xlim(-0.55, 0.55)
    axis.set_ylim(-0.55, 0.55)
    axis.set_zlim(-0.55, 0.55)
    axis.set_box_aspect((1, 1, 1))
    axis.set_axis_off()
    axis.set_title(title, fontsize=9, fontweight="bold", pad=-2)


def render_sheets(asset_root: Path, output_dir: Path, azimuth: float) -> None:
    asset_dirs = sorted(
        path
        for path in asset_root.iterdir()
        if path.is_dir() and (path / "point_cloud_1000_pts.pkl").is_file()
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    per_sheet = 24
    for page, start in enumerate(range(0, len(asset_dirs), per_sheet), start=1):
        page_assets = asset_dirs[start : start + per_sheet]
        figure = plt.figure(figsize=(18, 12), facecolor="white")
        for index, asset_dir in enumerate(page_assets, start=1):
            axis = figure.add_subplot(4, 6, index, projection="3d")
            draw_asset(axis, load_points(asset_dir), asset_dir.name, azimuth)
        figure.suptitle(
            f"VisDex asset inventory — view azimuth {azimuth:g}° — page {page}",
            fontsize=16,
            fontweight="bold",
        )
        figure.tight_layout(rect=(0, 0, 1, 0.97), pad=0.2)
        figure.savefig(output_dir / f"assets_{page:02d}.png", dpi=150)
        plt.close(figure)


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").lower()


def render_selected(asset_root: Path, manifest: Path, output_dir: Path) -> None:
    records = load_manifest(manifest)
    output_dir.mkdir(parents=True, exist_ok=True)
    azimuths = (-60.0, 30.0, 120.0)
    for record in records:
        points = load_points(asset_root / record["asset_id"])
        figure = plt.figure(figsize=(12, 4), facecolor="white")
        for panel, azimuth in enumerate(azimuths, start=1):
            axis = figure.add_subplot(1, 3, panel, projection="3d")
            draw_asset(axis, points, f"view {panel}", azimuth)
        figure.suptitle(
            f'{record["index"]}. {record["name"]} — asset {record["asset_id"]} '
            f'— {record["group"]} — confidence: {record["identification_confidence"]}',
            fontsize=14,
            fontweight="bold",
        )
        figure.tight_layout(rect=(0, 0, 1, 0.92), pad=0.1)
        output_path = output_dir / (
            f'{int(record["index"]):02d}_{safe_name(record["name"])}_{record["asset_id"]}.png'
        )
        figure.savefig(output_path, dpi=150)
        plt.close(figure)

    figure = plt.figure(figsize=(18, 16), facecolor="white")
    for panel, record in enumerate(records, start=1):
        axis = figure.add_subplot(5, 5, panel, projection="3d")
        draw_asset(
            axis,
            load_points(asset_root / record["asset_id"]),
            f'{record["index"]}. {record["name"]}\n{record["asset_id"]}',
            -60.0,
        )
        if record["group"].startswith("main-paper"):
            axis.set_facecolor("#fff2cc")
    figure.suptitle(
        "Provisional 22-object selection — yellow panels are the six main-paper objects",
        fontsize=17,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0, 1, 0.97), pad=0.25)
    figure.savefig(output_dir.parent / "selected_objects_contact_sheet.png", dpi=160)
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_root", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--azimuth", type=float, default=-60.0)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if args.manifest is None:
        render_sheets(args.asset_root, args.output_dir, args.azimuth)
    else:
        render_selected(args.asset_root, args.manifest, args.output_dir)


if __name__ == "__main__":
    main()
