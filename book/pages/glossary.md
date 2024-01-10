# Glossary

A listing of common terms and definitions used throughout the course.

```{glossary}

compact model
    A compact model is a mathematical description of the behavior of a device and is (usually) the result of a simulation, typically FDTD. It is used to simulate the behavior of a device without having to re-simulate the entire device each time. Compact models are generally used to simulate the behavior of a device within a larger circuit.

cutback
    A technique for measuring per-component attenuation by performing transmission measurements between the input and output ports across a number of devices. For example, multiple circuits each with different lengths of delay line waveguide, a number of circuits each with different counts of some element, etc.

design rule checking
    Design rule checking (DRC) is the process of verifying the {term}`design rules` of a photonic circuit. It is used to ensure that the circuit will be manufacturable, and that the design will not have any errors that would cause the circuit to fail. This may include electrical shorts or features with dimensions too small to be resolved, which would drastically change the performance of the device.

design rules
    Design rules are the set of rules that a photonic circuit must follow in order to be manufacturable. They are generally set by the foundry that will be manufacturing the circuit. These can include minimum feature sizes, minimum spacing between features, etc.

DRC
    See {term}`design rule checking`.

FDTD
    See {term}`finite-difference time-domain`.

finite-difference time-domain
    Finite-difference time-domain (FDTD) is a numerical analysis technique used for modeling computational electrodynamics (finding approximate solutions to the associated system of differential equations). Since it is a time-domain method, FDTD solutions can cover a wide frequency range with a single simulation run. FDTD is one of the primary computational electrodynamics modeling techniques available.

gdsfactory
    [gdsfactory](https://gdsfactory.github.io/gdsfactory/index.html) is a open source platform that allows you to create photonic chips in python or YAML. It uses a end-to-end design flow that helps you design, verify, and validate your photonic chip.

GDS file
    Graphic Data System file. Programs like meep output gds files that we must convert so we can use their geometry in gdsfactory.

grating coupler
    A photonic device that couples light from a waveguide to free space. It is used to couple light from a fiber to a photonic chip.

hierarchical component
    A component that is made up of other components. For example, a ring resonator is made up of a ring and two waveguides. The ring resonator is a hierarchical component.

interferometer
    An [interferometer](https://www.ligo.caltech.edu/page/what-is-interferometer) is an instrument that utilizes the interference between two beams of light to make precise measurements.

MMI
    A [multi-mode interferometer](https://en.wikipedia.org/wiki/Multi_mode_interferometer) is used to split or combine light waves. There are different shapes of MMIs. A 1x2 MMI for example takes one wave as an input and splits it into two outputs. Ideally the power between the outputs would be a 50-50 split but this is nearly impossible.

polygon
    An element of a component, polygons are the lowest building block of components, and if you print out a component’s information, it will tell you how many polygons are contained within it.

port
    An element of a component, ports are placed at the inputs and outputs of components, although in a component with many pieces, you can place it at the interconnect between two components. You must specify the direction the port is facing (generally either into or out of the component). You can also specify the width of the port, although it is generally just the width of the input or output of the component it is attached to.

PDK
    See {term}`process design kit`.

process design kit
    A process design kit (PDK) is a system of software, models, and tools for modeling a fabrication process for use in designing integrated circuits (electronic or photonic). A PDK typically includes process flow information, a layer stack, process design rules, geometric device models, circuit models, and digital models for simulation.

reference
    An element of a component that references other components. Follows the [DRY principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) and saves memory in larger designs, as it points to an existing geometry instead of creating a new one. Also ensures that a geometry modification in one place will be replicated in all references.

silicon-on-insulator
    Silicon-on-insulator (SOI) technology refers to the use of a layered silicon-insulator-silicon substrate in place of conventional silicon substrates in semiconductor manufacturing. This is necessary for photonic devices in order to construct waveguides, which could not be fashioned from silicon-only wafers.

SOI
    See {term}`silicon-on-insulator`.

vscode
    Visual Studio Code, also commonly referred to as VS Code, is a source-code editor developed by Microsoft for Windows, Linux and macOS. Features include support for debugging, syntax highlighting, intelligent code completion, snippets, code refactoring, and embedded Git ([Wikipedia](https://en.wikipedia.org/wiki/Visual_Studio_Code)).

WSL
    Windows Subsystem for Linux. WSL lets developers install and run a Linux distribution on Windows and use Linux applications, utilities, and Bash command-line tools directly on Windows, unmodified, without the overhead of a traditional virtual machine or dual-boot setup.

```
