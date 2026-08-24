from __future__ import annotations

from marimo_course.lib.mzi_modelling_core import compute_mzi_transfer
import csv
from pathlib import Path


def main() -> None:
    center_wl_um = 1.55
    span_um = 0.04
    neff = 2.4
    delta_length_um = 10.0
    loss_dB_per_cm = 2.0

    wl_um, T = compute_mzi_transfer(
        center_wl_um=center_wl_um,
        span_um=span_um,
        neff=neff,
        delta_length_um=delta_length_um,
        loss_dB_per_cm=loss_dB_per_cm,
    )

    print("wavelength range (um):", wl_um.min(), "→", wl_um.max())
    print("T range:", T.min(), "→", T.max())

    # Print basic ranges
    print("wavelength range (um):", wl_um.min(), "→", wl_um.max())
    print("T range:", T.min(), "→", T.max())

    # Save sampled data so we can inspect or plot it elsewhere
    out_path = Path(__file__).with_name("debug_mzi_data.csv")
    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["wavelength_nm", "T"])
        for wl, t in zip(wl_um * 1e3, T):
            writer.writerow([wl, t])
    print("Saved sampled data to:", out_path)


if __name__ == "__main__":
    main()
