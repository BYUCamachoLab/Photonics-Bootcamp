# Open Source Software

```{warning} This does not constitute legal advice
The information provided on this website does not, and is not intended to, 
constitute legal advice; instead, all information, content, and materials 
available on this site are for general informational purposes only. Information 
on this website may not constitute the most up-to-date legal or other 
information. 

Especially if in a corporate environment, contact an attorney to be absolutely
sure about the legal implications of using open source software at your 
organization.
```

This course is built with software that is known as "open-source software." But
what does open source really mean, and what are you legally allowed to do with
it? This is a particularly important question if you work at a company that is
writing software to distribute to customers, because depending on the license,
any code that incorporates it may inherit the requirement to also be 
open-source.

Free and open source software (FOSS) is software where the source code is
freely availble to be read by end users or other developers. The open source
portion refers to the fact that anyone is allowed to inspect, modify, and/or
enhance the code--it refers more to the design methodology or methods of
collaboration in the creation of the software. It enables many people of
different skills or backgrounds to collaborate on a software, often outside of
the context of a company. While often monetarily free itself (perhaps under
certain conditions or use restrictions), the "free" part of FOSS refers to the
freedom to use the software in any way you wish as an end user; it means that
you have the freedom to run, copy, distribute, study, change, and improve the
software.

One advantage of open source software is that you can look under the hood to
see what's actually going on. You can extend it for your own specific needs,
there's a strong open source community focused on making more software more
accessible to more people. However, one potential downside is that it's often
thanklessly maintained by a few dedicated programmers spending their free time
on it. Some companies allow their engineers to spend a portion of their time
contributing to open source software. Some of the software in this course, for
example, is driven by engineers at Google, PsiQuantum, and other companies.
Because of its nature of being community driven, depending on the size of the
project, maintenance and bug fixes can be slower than a commercial software.
On the other hand, the community is free to submit fixes to the original 
software, meaning that depending on the size of the project and the number of
users it garners, it can actually become a very actively developed software.

Some of these software projects are more "friendly" to coporate environments
based on their licensing scheme; before incorporating any of these into your
code, you'll definitely want to confirm with your company's legal team the
ability to utilize existing open source software, especially if you're rolling
it into another software that you plan to release to customers. We'll introduce
a couple of the most commonly seen open source licenses below.

## Common Licenses

### MIT License

The MIT license is a very permissive license and is extremely short (only 162 
words). It carries with it two requirements; in your own copy of the code
(whether you modified it or not), you must include {cite:p}`mitlicense`:

1. The original copyright notice  
1. A copy of the license itself  

The MIT License does not require those who modify the original code to also
release it under the MIT or other open-source license. In other words, your
version remains proprietary, if you so wish. You can incorporate MIT licensed
code into commercial software, modify it, and use a different (perhaps
stricter) license for the derived work. As mentioned in the license text, 
however "the software is 'as is', without warranty".

Of the licenses mentioned here, this is the most commonly encountered  in the
open source software world.

### Apache 2.0 License

The Apache 2.0 License is also a permissive license, carrying few restrictions.
The requirements when incorporating modified or original code licensed under
this license are that you must include {cite:p}`apachelicense`:

1. The original copyright notice  
1. A copy of the license itself  
1. If applicable, a statement of any significant changes made to the original code  
1. A copy of the NOTICE file with attribution notes (if the original library has one)  

Similar to the MIT license, code licensed under the Apache 2.0 license can be
rereleased under a different license. Where it differs is in the explicit 
grant of patent rights to contributors or users of the code. That means you can
claim a patent on the portion of contributions you make to the original 
codebase.

Like the MIT license, you cannot hold contributors legally liable for any
reason. You're also not granted any rights to the trademarks of the licensor.
Of the open source licenses, this is potentially the most permissive.

### GPLv3+/AGPL License

These belong to a class of licenses known as "copyleft licenses", and they
mandate that distributed works based on any existing copyleft-licensed
components must use the same license as the original. In other words, a
derivative work of GPL v3-licensed software must also be licensed under the GPL
v3.

This is typically unpopular with companies, and many corporate environments
(especially software companies) will prohibit the use or inclusion of any 
software under this license to prevent any potential "contamination" of their
code witih this license, which would technically require them to open-source 
the offending software or open them to legal liability.

Users of GPLv3 code are required to {cite:p}`gpllicense`:

1. Include a copy of the full license text  
1. State all significant changes made to the original software  
1. Make available the original source code when you distribute any binaries
   based on the licensed work  
1. Include a copy of the original copyright notice  

The GPL license and others like it attempt to force a "pay-it-forward" attitude
when it comes to open source software. While not necessarily a downside---many
impressive projects use the GPL license (the GNU project, Notepad++, Wordpress,
and MySQL, to name a few)---because it would force a company to open source 
their code (and therefore be unable to control its sale), it's less popular.

## References

```{bibliography}
:filter: docname in docnames
:style: unsrt
```