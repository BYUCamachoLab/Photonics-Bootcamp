# Glossary
A glossary of common terms used throughout the course.
```{glossary}

WSL
    Short for Windows Subsystem for linux, WSL lets you run linux on windows, almost like a virtual machine.

GDS
    GDS Factory is a open source platform that allows you to create photonic chips in python or YAML. It uses a end-to-end design flow that helps you design, verify, and validate your photonic chip.

Polygons
    An element of a component, polygons are the lowest building block of components, and if you print out a component’s information, it will tell you how many polygons are contained within it.

References
    An element of a component, references to other components within a component, or circuit, are used to save memory as they point to an existing geometry instead of creating a new one.

Ports
    An element of a component, ports are placed at the inputs and outputs of components, although in a component with many pieces, you can place it at the interconnect between two components. You must specify the direction the port is facing (generally either into or out of the component). You can also specify the width of the port, although it is generally just the width of the input or output of the component it is attached to.

MMI
    A multi-mode interferometer is used to split or combine light waves. There are different shapes of MMIs. A 1x2 MMI for example takes one wave as an input and splits it into two outputs. Ideally the power between the outputs would be a 50-50 split but this is nearly impossible.

GDS File
    Graphic Data System file. Programs like meep output gds files that we must convert so we can use their geometry in gds factory.
```
<!-- Cutbacks
    I don't know

Grating Couplers
    They do something -->
