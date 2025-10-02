.. _CFD_guide:

.. toctree::
   :maxdepth: 1

   Main
   CFD_guide/Mesh_sensitivity_study
   CFD_guide/Turbulence


CFD guide
=========
An automatisation can help with a lack of experience with specific software (in this case FLuent) or can help to share the simulation settings among the less experienced users. 
But at the end of the day, the resulting simulation is only as good as its settings and iterpretation. This section should give new CFD engineers a fundamentals of creating
robust and useful simulations, that can confidently the vehicle performance.


Mesh sensitivity
^^^^^^^^^^^^^^^^
A perfectly precise simulation is possible only with infinite amount of cells. Everything else is a compromise between a precision and computaiton time. 
Before any CFD development can be started, it is important to tune the fidelity of your mesh to fit this compromise and to quantify the simulation error 
due to the finite mesh. This proccess is what we call a :ref:`Mesh sensitivity sudy <mesh_sensitivity>`.

Turbulence modeling
^^^^^^^^^^^^^^^^^^^
Fluid flow, unless at small scales or velocities, is a chaotic phenomenon. This chaos is represented by swirls and vortecies at all scales. Some of these larger scales 
are important to describe the general flow, but most of the smaller scales only affect the general flow and are too small to simulate directly. To describe their effect 
we then need to use  :ref:`turbulence modeling <turbulence>`.


Useful guides
^^^^^^^^^^^^^

- `How to Detect Transient Behavior in Steady-State Simulations? <https://www.simscale.com/knowledge-base/transient-behavior-in-steady-state/>`_
- `How to set the Time Step Delta T in Transient CFD Simulations? <https://www.simscale.com/knowledge-base/time-step-transient-cfd-simulation/>`_
- `External Aero Automotive (ABP) - Ansys Learning Hub <https://learninghub.ansys.com/learn/courses/414/external-aero-automotive-abp>`_
- `Fault Tolerant Meshing for Vehicle External Aerodynamics (ABP) - Ansys Learning Hub <https://learninghub.ansys.com/learn/courses/372/ftm-for-vehicle-external-aerodynamics-abp>`_
- `External Aerodynamics using Ansys Fluent - Ansys Learning Hub <https://learninghub.ansys.com/learn/courses/539/external-aerodynamics-using-ansys-fluent>`_
- `Steady-State and Transient Wake Capturing through Mesh Adaption (ABP) - Ansys Learning Hub <https://learninghub.ansys.com/learn/courses/341/steady-state-and-transient-wake-capturing-through-mesh-adaption-abp>`_