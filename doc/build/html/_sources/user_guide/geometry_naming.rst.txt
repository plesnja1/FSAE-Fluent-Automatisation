.. _geometry_naming:

CAD model preparation
=====================
It is crutial to maintain a good naming system of your CAD geometry and to adhere to certain rules when naming your parts and assemblies.
The pyfluent script takes yopur imported CAD and renames each part and assembly so that it contains also name of its entire CAD tree hierarchy.
This enables us to find the correct parts even if part with same name exists in different assembly and allow us to assign mesh sizings to entire
assemblies without needing to specify them for each part. 

The tree structure
^^^^^^^^^^^^^^^^^^
The base of the cad tree should be divided into two assemblies. The **Vehicle** assembly, that contains the car geometry and the **BOIs** assembly,
which contains then bodies of influence. It is important to have them in separate assemblies as both are treated very differently.


.. image:: ../_static/user_guide/CAD_tree.png
  :width: 500

Above is an example of a functional CAD tree with a **Vehicle** and **BOIs** assemblies on top of CAD tree hierarchy.

Part naming
^^^^^^^^^^^
In terms of naming of parts, do not use signs such as **(\ *,-.: \ )** since these would interfere with either AutoFluent part search engine or 
Fluents internal part naming. If you want to seperate your part name use either underscore **(\  _ \ )** or start each new word with uppercase letter.

By default after CAD import fuent names the imported part in format:

**part_name:tree_path-part_name-solid_name**.

If we take a single solid in the front wing example bellow:

.. image:: ../_static/user_guide/part_naming.png
  :width: 500

We can see that the part name is **wing**, the solid name is **Solid** and tree path is **vehicle-a-fs-fwing**. The resulting part will then be named:

.. code-block:: console

   wing:vehicle-a-fs-fwing-wing-solid

Which makes later working with Fluent parts much easier.

Inheritance
^^^^^^^^^^^
During a CAD creation a concept of inheritance should be kept in mind. Here the concept of inheritance applies mainly on surface 
mesh sizing, meaning that a part inherits all of the surface mesh sizing options from all of its parents in CAD tree. The final 
resulting mesh sizing is then derived from the smallest mesh size setting applied.

As example if we apply *medium* surface mesh sizing for the aerodynamics assembly named **"a"** and this *medium* setting will be applied
to all its subassemblies (in this case **"sw", "rw", "fw"**) and their individual subassemblies and parts. I could then decide to apply
a *finer* sizing to a front wing endpalte part called **"endplate"**. This part also inherits the *medium* setting from the **"a"** assembly
which is its parent, but since the smallest settings applies, fluent will ignore the *medium* setting. 

It then makes sense to structure the CAD tree from the largest details to the finest.




