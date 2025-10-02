.. _user_guide_contents:

User Guide
==========

.. toctree::
   :maxdepth: 1
   :hidden:

   geometry_naming
   mesh_settings
   solver_setup
   boundary_conditions
   postprocessing_guide

This AutoFluent user guide should help you understand principles of working with AutoFluent as well as some basic principles of creating
CFD simulations of acceptable quality.

Setting up CAD geometry
^^^^^^^^^^^^^^^^^^^^^^^
AutoFluent uses tree hierarchy of imported CAD geometry to create named selections, mesh sizings and output variables.
As such, a rigorous :ref:`CAD naming conventions <geometry_naming>` during development needs to be ahered to.

Mesh creation
^^^^^^^^^^^^^
Even though AutoFluent automises entire Fluent Fault tolerant workflow, a propper mesh sizings needs to be defined. AutoFluent offers
an intuitive GUI tool to create mesh sizing settings .json files that offers repeatibility in :ref:`creating quality volumetric meshes <mesh_settings>`.

Solver setup
^^^^^^^^^^^^
AutoFluent offers an useful range of turbulence models, slovers, algorithms and temporal settings. This offers a variability in speed and 
complexity of simulations but :ref:`knowing how to set up the solver <solver_setup>` based on desired output, aviable hardvare and used mesh
is essential.

Boundary conditions
^^^^^^^^^^^^^^^^^^^
Apart from inlet velocity AutoFluent offers a posibility to set up your wheel base and incorporate a radiator or fans into your simulation.
A :ref:`propper setup of these boundaries <boundary_conditions_guide>` defines the simulation and provides an usefull input to other groups such as 
powertrain.

Postprocessing
^^^^^^^^^^^^^^
Most important part of any simulation is evaluating its results and making sure the results can be trusted. In postprocessing stage of
AutoFluent the user can :ref:`hoose which data and how detailed <postprocessing_guide>` he wants to be shown.
