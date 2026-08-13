from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class DrcError:
    category: str
    description: str
    center_x: float
    center_y: float
    raw_value: str
    all_x: list[float]
    all_y: list[float]


def parse_lyrdb_errors(lyrdb_path: Path) -> list[dict]:
    """
    Parse a KLayout `.lyrdb` file and extract error locations with coordinates.

    Returns a list of dicts to match existing notebook usage.
    """
    errors: list[dict] = []
    tree = ET.parse(lyrdb_path)
    root = tree.getroot()

    categories: dict[str, str] = {}
    for cat in root.findall(".//categories/category"):
        name = cat.find("name")
        desc = cat.find("description")
        if name is not None and name.text is not None:
            categories[name.text] = desc.text if desc is not None and desc.text is not None else ""

    coord_pattern = r"[-+]?\d*\.?\d+"

    for item in root.findall(".//item"):
        category = item.find("category")
        if category is None or category.text is None:
            continue

        cat_name = category.text.strip("'")
        cat_desc = categories.get(cat_name, categories.get(f"'{cat_name}'", ""))

        value_elem = item.find(".//value")
        if value_elem is None or value_elem.text is None:
            continue

        value_text = value_elem.text
        coords = re.findall(coord_pattern, value_text)
        if len(coords) < 2:
            continue

        nums = [float(c) for c in coords]
        x_coords = nums[0::2]
        y_coords = nums[1::2]
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)

        errors.append(
            {
                "category": cat_name,
                "description": cat_desc,
                "center_x": center_x,
                "center_y": center_y,
                "raw_value": value_text,
                "all_x": x_coords,
                "all_y": y_coords,
            }
        )

    return errors


def list_example_pairs(examples_root: Path) -> list[tuple[Path, Path]]:
    """List (gds, lyrdb) example pairs under a folder."""
    pairs: list[tuple[Path, Path]] = []
    if not examples_root.exists():
        return pairs

    for gds_path in sorted(examples_root.glob("example_*.gds")):
        lyrdb_path = gds_path.with_suffix(".lyrdb")
        if lyrdb_path.exists():
            pairs.append((gds_path, lyrdb_path))

    return pairs
