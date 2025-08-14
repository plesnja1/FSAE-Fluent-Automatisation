# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'FSAE CFD Automatisation'
copyright = '2025, plesnja1'
author = 'plesnja1'
release = '0.241'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
]

toggleprompt_offset_right = 35

templates_path = ['_templates']
exclude_patterns = []

sphinx_gallery_conf = {
    # convert rst to md for ipynb
    # "pypandoc": True,
    # path to your examples scripts
    "examples_dirs": ["../../examples/"],
    # path where to save gallery generated examples
    "gallery_dirs": ["examples"],
    # Pattern to search for example files
   
    "plot_gallery": False,
    # Remove the "Download all examples" button from the top level gallery
    "download_all_examples": False,
    # Sort gallery example by file name instead of number of lines (default)

    # directory where function granular galleries are stored
    "backreferences_dir": None,
    # Modules for which function level galleries are created.  In
    "doc_module": "ansys-fluent-core",
    "thumbnail_size": (350, 350),
    "reset_modules_order": "after",

    "capture_repr": (),
    "remove_config_comments": True,
    "abort_on_example_error": True,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
