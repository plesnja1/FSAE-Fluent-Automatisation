
.. toctree::
   :maxdepth: 1
   :hidden:

Getting Started with AutoFluent
===============================

.. vale Google.Spacing = NO



.. vale Google.Spacing = YES

Downloading AutoFluent
----------------------
User can either download entire branch from `gitHub web <https://github.com/plesnja1/FSAE-Fluent-Automatisation>`_ or pull the branch from git.

.. code-block:: console

   git clone https://github.com/plesnja1/FSAE-Fluent-Automatisation.git

Dependend libraries
-------------------

AutoFluent is dependend on these external libraries that need  to be installed prior:

- **customtkinter**
- **PIL**
- **ansys.fluent.core**
- **ansys.geometry.core**
- **pint**
- **openpyxl**
- **numpy**
- **pandas**

which you can all instal through:

.. code-block:: console

   pip install <library name>


Starting AutoFluent
----------------------
To use AutoFluent a Python 3.8 or higher needs to be installed. Inside a downloaded folder a Main.py script is located. 
If started throug Python a graphical user interface will appear.

.. image:: ../Main_menu.png
  :width: 400
  :alt: AutoFluent menu