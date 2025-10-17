.. _boundary_conditions_guide:

Boundary Conditions
===================

There are several boundarz conditions in every case. Some of them are predefined, like pressure outlet or symmetry on all sides except for road, but many can be 
defined by user.

.. image:: ../_static/GUI_guide/boundary_conditions.png
  :width: 650

Inlet
^^^^^
Inlet is here defined as a velocity inlet. For straight cases the inlet velocity is set directly at boundary and is the same value as defined in GUI. In case of turn case the
velocity is set as zero relative to neighboring cells and the velocity is instead defined by moving reference frame of the fluid cell zone. The MRF movement (rad/s) is calculated 
from specified inlet velocity and turn radius.

Road
^^^^
Road is defined as moving wall which moves at the same speed as inlet velocity. In case of turn simulation, the road has a rotational movement same as MRF.

Wheels 
^^^^^^
Wheels are defined as walls with a rotational movement. Their angular speed is calculated from inlet velocity value and specified wheel radius. User also needs to specify 
the origin of wheel axis in XYZ coordinates.

Radiators 
^^^^^^^^^

User can choose to simulate radiators on their car. The radiators need to be modelled as separate properkly named CAD body and is represented as porous medium.
The pressure loss characteristic of porous medium is defined through power law model, which characterises the specific pressure loss (presure loss through 1m of material) 
by linear constant (c0) and exponent constant (c1).

.. image:: ../_static/user_guide/Power_law.png
  :width: 500