.. _getting_started:



.. raw:: html

   <style> .red {color:#e3182d; font-weight:bold; font-size:16px} </style>

.. role:: red

.. raw:: html

   <style> .blue {color:#0078d7; font-weight:bold; font-size:16px} </style>

.. role:: blue

.. raw:: html

   <style> .yellow {color:#fbae17; font-weight:bold; font-size:16px} </style>

.. role:: yellow

.. raw:: html

   <style> .green {color:#00b44b; font-weight:bold; font-size:16px} </style>

.. role:: green

.. raw:: html

   <style> .purple {color:#914bb8; font-weight:bold; font-size:16px} </style>

.. role:: purple



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

.. image:: ../_static/Main_menu.png
  :width: 500


Navigating Graphical User Interface
-----------------------------------

GUI is divided into 5 distincted areas. Top select menu (:blue:`Blue`) switches between different options menus. 
Middle large window (:yellow:`Yellow`) is where options menus are shown.
Bottom static menu (:red:`Red`) is for general settings as working directory, solver stage, settings presets and starting simulation.
Right side bar (:purple:`Purple`) is a visualisation of a solution queue.
On bottom (:green:`Green`) is a transcript from a console. 

.. image:: ../_static/Main_menu_boxed.png
  :width: 500


.. toctree::
   :maxdepth: 2
   :hidden:

   
   first_project