# Introduction

Welcome to the CamachoLab Photonics Bootcamp, created with support from Google.

We present a new open-source, online and freely available set of course
material and resources for teaching integrated photonic design and simulation
to electrical engineers and students with an interest in photonic engineering.
In collaboration with Google, we’ve designed a curriculum complete with
background motivation material, code examples, component and system design
problems, and full circuit examples that teach learners a series of open-source
Python tools and guide them step-by-step through design, simulation, and
modeling, giving them the resources and information on how to submit their
devices for manufacturing should they wish to test their devices’ performance.
Open-source tools include Meep {cite:p}`oskooi2010meep` for FDTD simulation,
Simphony {cite:p}`ploeg2020simphony` for creating compact models and simulating
larger circuits, and GDS Factory {cite:p}`gdsfactory` for layout of GDS files
for submission to fabrication facilities. Introductions to open-source software
for testing PICs post-fabrication and instructional material on analyzing the
results are also included in the course. 

The course is hosted on GitHub, allowing for contributions from subject-matter
experts and future expansion of covered material. It can also be forked by
parties interested in creating a more customized set of materials for their own
trainings or courses. The website is written in the format of Jupyter Notebooks
allowing code to be embedded inline with the explanatory material. It also
allows entire webpages and their code examples to be launched directly into a
Google Colab environment or downloaded directly and run locally, allowing
learners to have an immediate connection between the teaching material and
putting the principles into practice. 

As with many things in open-source, there's always multiple ways to do the same
thing. In this course, workflows will be presented with one approach, single
tools will be introduced as if they're the only option, and we usually won't
bother mentioning all the different possible system configurations. All the
software we will be using is cross-platform, however. And, if you'd like to
use a different tool, or a different code editor, if you have the know-how, go
ahead! To keep things simple and standardized for us, however, we'll give
instructions just for one single method.

**References**

```{bibliography}
:filter: docname in docnames
:style: unsrt
```
