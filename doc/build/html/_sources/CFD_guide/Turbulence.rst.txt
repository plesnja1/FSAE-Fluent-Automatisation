.. _turbulence:

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
