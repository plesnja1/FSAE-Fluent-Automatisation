.. _boundaryconditions:

Boundary Conditions Options Menu
================================
Boundary conditions options menu specifies inlet velocity, wheel diameter and wheel base, radiators and fan settings.

.. image:: ../_static/GUI_guide/boundary_conditions.png
  :width: 650

Inlet velocity [m/s]
^^^^^^^^^^^^^^^^^^^^
- **type**: text win. - float

Inlet air velocity. Same as car speed.

Wheel diameter [m]
^^^^^^^^^^^^^^^^^^
- **type**: text win. - float

Outer wheel diameter. Used for wheel rotational speed calcualtion.

Front wheel axis origin [m] (X, Y, Z)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: 3x text win. - float

Coordinates that define front axis together with [0,1,0] vector.

Rear wheel axis origin [m] (X, Y, Z)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: 3x text win. - float

Coordinates that define rear axis together with [0,1,0] vector.


Simulate radiators?
^^^^^^^^^^^^^^^^^^^
- **type**: check - bool

Wether cad model includes a radiator which would be simulated as porous zone with power law model.
For more info see `Porous Media Conditions <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_ug/flu_ug_bcs_sec_cell_zones.html%23flu_ug_sec_bc_porous_media>`_


Radiator C0
^^^^^^^^^^^
- **type**: text win. - float

C0 constant used in power law model.

Radiator C0
^^^^^^^^^^^
- **type**: text win. - float

C1 constant used in power law model.

Simulate fan?
^^^^^^^^^^^^^
- **type**: check - bool

Wether cad model includes a fan which would be simulated as 2d fan zone with piecewise linear pressure curve.
For more info see `Fan Boundary Conditions <https://ansyshelp.ansys.com/account/secured?returnurl=/Views/Secured/corp/v252/en/flu_ug/flu_ug_bcs_sec_bound_cond.html%23flu_ug_sec_bc_fan>`_

Fan curve .txt (max 50 points!)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: text win. - string

String path to a .txt file that specify fan pressure curve.