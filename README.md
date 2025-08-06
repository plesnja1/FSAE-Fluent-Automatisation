FSAE-Fluent-Automatisation
----------------------
An automatization for Fluent CFD external aerodynamics optimised for FSAE styled vehicles. Meshing, Solver, Postprocessing included.
This automatisation utilises an aoutomatic name selection based on CAD tree of imported model and automatic mesh sizing based on theese name selections and included scope sizing .json file. Main part of the script is a GUI, which takes care of starting individual scripts, mannaging important solver settings, loading files, rewriting and saving scope siying files and queue management. If set properly. the entire workflow can generate data, images and .AVZ files.

<h1 align="left">
<img src="/doc/source/Main_menu.png" width="500">
</h1><br>

Scoped sizing
----------------------

The import skript is able to save complete tree path for every part of an assembly. This enables to repeatedly apply scoped sizing to same parts and addition of new parts without the need for updated scoped sizing settings (unless desired). Even if part is not explicitly in scoped sizing settings file, it inherrits scoped sizing settings from its immidiate parrent assembly. The scoped sizing settings can be either overwritten in .json file directly or through graphical interface, which allows reading existing setting files, overwriting them and creation of new files.

<h1 align="left">
<img src="/doc/source/CAD_tree.png" width="350">


<img src="/doc/source/Scope_sizing.png" width="350">
</h1><br>
