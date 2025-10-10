.. raw:: html

   <style> .red {color:#e3182d; font-weight:bold; font-size:16px} </style>

.. role:: red

.. raw:: html

   <style> .blue {color:#0078d7; font-weight:bold; font-size:16px} </style>

.. role:: blue

.. raw:: html

   <style> .yellow {color:#fbae17; font-weight:bold; font-size:16px} </style>

.. role:: yellow

.. raw:: html

   <style> .green {color:#00b44b; font-weight:bold; font-size:16px} </style>

.. role:: green

.. _mesh_settings:

Creatings mesh
==============
In Fluent creating a mesh consists of manz subtasks ranging from part import management, tunnel creation, edge extractions, surface mesh settings, volume mesh settings, 
mesh improvements, volume definisions, boundary definitions, scope sizings and prism sizings. Thankfully we need to concern ourselves only with the latter two, as most of the
other tasks are managed by the script. 


Scoped Sizing
^^^^^^^^^^^^^
Size Functions and Scoped Sizing provide control over how the mesh size is distributed on a surface or within the volume. 
They provide accurate sizing information for the mesh distribution and precise refinement control.

Scoped sizing differs from size functions in how the sizing can be associated with objects or zones, respectively. 
Scoped sizing may be applied to model features such as faces, edges, face zone labels or unreferenced face or edge zones

Assigning Scoped Sizing
"""""""""""""""""""""""
For specifying mesh size the **Scoped Sizing** menu is aviable. This menu consists of the :yellow:`tree window ` on the left side,  scoped sizing :green:`file loading` on top of the menu, 
:blue:`individual sizings` individual sizings controlls in the middle and :red:`tree manipulation` buttons on the bottom.

.. image:: ../_static/user_guide/ScopedMenu.png
  :width: 500