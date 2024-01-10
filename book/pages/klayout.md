# KLayout

<div style="text-align: center">
<img src="https://github.com/BYUCamachoLab/Photonics-Bootcamp/blob/main/book/images/klayout-intro-image.png?raw=true" alt="Klayout introduction image" style="max-width: 500px">

([source](https://www.klayout.de/))
</div>

[KLayout](https://www.klayout.de/) is a free and open-source software for layout design and verification. It's most basic use case is as a layout viewer (it can read and display GDS files, the most common format for laying out photonic chips), but it is a powerful tool for designing photonic devices and integrated circuits as well. It has features for {term}`DRC`, viewing chip cross-sections, tracing nets (to help you detect shorts), and more, while also being scriptable in several languages including Ruby and Python. KLayout is available for Windows, Mac, and Linux. You can download KLayout [here](https://www.klayout.de/build.html).

## klive

klive is a small extension to KLayout that allows automatic loading for GDS 
files when some external program sends a json request with the gds path to a 
klive server, running in the background. This essentially allows for 
"hot-reloading" of your layouts within KLayout each time you rerun your code.

Once KLayout is installed, you can install klive from within KLayout's package
manager, by going to `Tools > Manage Packages > Install New Packages`. Then, 
search for `klive` and double click it to select it, then click "Apply".

![klive installation screenshot](../klive_installation.png)
