.. FSAE CFD Automatisation documentation master file, created by
   sphinx-quickstart on Thu Aug 14 09:05:24 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FSAE CFD Automatisation documentation
=====================================

.. toctree::
   :hidden:
   :maxdepth: 2
   
   getting_started/getting_started


This prooject aims to incorporate pyFluent (a python Fluent wrapper) into a user friendly and easy to use graphical interface. 
As a result aerodynamicists with little experience in making CFD calculations can create quality external car simulations. 
At first the project aimed to create complete automatic workflow from importing a CAD file to getting complete results with
drag/lift data and pictures but over time it incorporated feeatures as automatic simulations queue, radiators and fans and turn simulations.

Why Use AutoFluent?
-------------------

- **Automation**: Fully atomated workflow from CAD to results.
- **Ease of use**: User friendly and simplified interface over Fluent.
- **Simulation speed**: Fully use both CPU and GPU resources at all time thanks to sim queue.
- **Flexibility**: Many options for solver settings, postprocessing, mesh sizings and presets saving.

How it works?
-------------
Through GUI user can load CAD files, create or load mesh sizings and choose solver and postprocessing option. 
GUI then sends selected settings into a simulation queue, which automatically sends these settings into a 
pyFluent script. The sctipt requires that the imported CAD tree is named in accordance with a .json scoped sizing file 
created through GUI.

Compatibility
-------------
AutoFluent supports **Ansys Fluent 2024 R2 and later**.

Resources
---------

- `PyFluent documentation <https://fluent.docs.pyansys.com/version/stable/index.html>`_
- `Fluent documentation <https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/prod_page.html?pn=Fluent>`_
- `Ansys customer portal <https://support.ansys.com>`_

Need Help?
----------

Visit the community or support resources:

- `PyAnsys community forum <https://forum.pyansys.com>`_
- `Submit a bug report <https://github.com/plesnja1/FSAE-Fluent-Automatisation/issues>`_
- `Contact Ansys support <https://support.ansys.com>`_