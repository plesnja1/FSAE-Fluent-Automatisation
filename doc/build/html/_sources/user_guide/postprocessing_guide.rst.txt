.. _postprocessing_guide:

Posprocessing
=============
Posprocessing options menu gives users options to choose which and how detailed postprocessing features they want to perform for their simulation.

.. image:: ../_static/GUI_guide/postprocessing.png
  :width: 650

Excell file
^^^^^^^^^^^
For every part and subassembly defined in scoped sizing tree the script creates a lift and drag report deffinition, These created monitors can be writtten into a excell table
together with radiator mass flow and aerodynamic balance. User can also tweak a **Iteration averaging** value which averages all numerical results over specified ammount of
iterations to mitigate influece of cyclic behaviors.

.. image:: ../_static/user_guide/Excell.png
  :width: 170


AVZ files
^^^^^^^^^

AutoFluent can generate several .AVZ files which can be opened in Ansys Viewer. These files contain 3D data of saved scene, which means user can look at the wall conntours or
created isosurfaces from all angles. Currently the script generates .AVZ files of: isosurfaces of total pressure zero, isosurface of Q-criterion, wall contour of pressure
coefficient, wall shear stress in x direction and wall y+.

.. image:: ../_static/user_guide/AVZ.png
  :width: 650

Cut planes
^^^^^^^^^^

AutoFluent can generate several types fo cut planes. A number of cut planes and rangin in which the cut planes are generated need to be defined for each XYZ direction.
On created cut planes several contours can be generated. These include:

.. figure:: ../_static/user_guide/LIC.png
  :align: left
  :figwidth: 410
  :width: 400
  :alt: Line Integral Convolution of velocity

  Line Integral Convolution of velocity

.. figure:: ../_static/user_guide/TotP.png
  :align: right
  :figwidth: 410
  :width: 400
  :alt: Contours of total pressure

  Contours of total pressure

.. figure:: ../_static/user_guide/Vel.png
  :align: left
  :figwidth: 410
  :width: 400
  :alt: Contours of velocity magnitude

  Contours of velocity magnitude


.. figure:: ../_static/user_guide/Vort.png
  :align: right
  :figwidth: 410
  :width: 400
  :alt: Contours of vorticity

  Contours of vorticity