.. _postprocessing:

Posprocessing Options Menu
==========================
Posprocessing options menu gives users options to choose which and how detailed postprocessing features they want to perform for their simulation.

.. image:: ../_static/GUI_guide/postprocessing.png
  :width: 650

Export forces to excell file?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: check - bool

Option to export drag, lift, and pressure distribution of all subassemblies into a .CSV file.


Iteration averaging
^^^^^^^^^^^^^^^^^^^
- **type**: text win. - integer

Number of latest iterations over which to average drag, lift, distributions data and RMS field values.


Create report file?
^^^^^^^^^^^^^^^^^^^
- **type**: check - bool

Option to create .pdf report file which include information about convergence, mesh quality and some results.

Create AVZ files?
^^^^^^^^^^^^^^^^^
- **type**: check - bool

Option to create .AVZ which contains 3D countured scenes which can be opend in Ansys Viewer. Fluent will create scenes of: 
*wall y+*, *x wall shear stress*, *static pressure*, *pressure coeficient* and *q-criterion* isosurface.

Starting coordinate [m]: (XY, XZ, YZ)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: 3x text win. - float

Starting coordinate from which postprocessing will start creating cutplanes.

End coordinate [m]: (XY, XZ, YZ)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: 3x text win. - float

End coordinate to which postprocessing will finish creating cutplanes.

Number of cuts: (XY, XZ, YZ)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: 3x text win. - integer

Number of contour cuts that will be created for each major plane.

Velocity magnitude cuts:
^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: check - bool

Whether to create cuts of velocity magnitude contours.

Velocity LIC cuts:
^^^^^^^^^^^^^^^^^^
- **type**: check - bool

Whether to create cuts of velocity Line Integral Convolutions.

Mean Static Pressure cuts:
^^^^^^^^^^^^^^^^^^^^^^^^^^
- **type**: check - bool

Whether to create cuts of Mean Static Pressure contours.


Total Pressure cuts:
^^^^^^^^^^^^^^^^^^^^
- **type**: check - bool

Whether to create cuts of Total Pressure contours.#


Vorticity cuts:
^^^^^^^^^^^^^^^
- **type**: check - bool

Whether to create cuts of Vorticity contours.