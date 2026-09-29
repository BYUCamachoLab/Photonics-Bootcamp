import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Waveguides
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    (wiaw-target)=
    ## What is a Waveguide?

    Traditional circuits transmit electrical signals via traces, which are typically made of a conductive material like copper. Photonic circuits transmit light signals via waveguides. Waveguides are used to guide light signals to different parts of photonic circuits. Waveguides can also be used to transmit light signals over very long distances.

    A simple waveguide consists of two parts: a core with a high index of refraction, and a material with a low index of refraction that surrounds the core (known as a "cladding"). One of the most popular waveguides for photonic circuits is the Silicon on Insulator (SOI) waveguide.  A silicon core, with a refractive index of ~3.47, is clad with silicon dioxide, which has a refractive index of ~1.44. SOI waveguides are favored for their ease of manufacture - the silicon dioxide layer can be deposited onto a silicon wafer, and then traces of silicon can be etched onto the wafer substrate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <div align="center">
        <figure>
            <img src="https://github.com/BYUCamachoLab/Photonics-Bootcamp/blob/main/book/images/soi_wg_xsection.png?raw=true" alt="Image of an SOI Waveguide" width="300">
            <figcaption><em>Figure: A Silicon on Insulator Waveguide</em></figcaption>
        </figure>
    </div>
    """)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
