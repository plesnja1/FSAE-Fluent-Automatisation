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
    "jupyter_sphinx",
    "numpydoc",
    "autodocsumm",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_toggleprompt",
]


numpydoc_use_plots = True
numpydoc_show_class_members = False
numpydoc_xref_param_type = True
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    "SS03",  # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}
numpydoc_validation_exclude = {
    "ansys.fluent.core.generated.solver.settings_231.",
    "ansys.fluent.core.generated.solver.settings_232.",
    "ansys.fluent.core.generated.solver.settings_241.",
    "ansys.fluent.core.generated.solver.settings_242.",
    "ansys.fluent.core.generated.solver.settings_251.",
    "ansys.fluent.core.generated.solver.settings_252.",
    "ansys.fluent.core.generated.solver.settings_261.",
    "ansys.fluent.core.services.batch_ops.BatchOps.__init__",
}

# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source file names.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

copybutton_prompt_text = r">>> ?|\.\.\. "
copybutton_prompt_is_regexp = True


toggleprompt_offset_right = 35

intersphinx_mapping = {
    "python": ("https://docs.python.org/", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
}

templates_path = ['_templates']
exclude_patterns = []

master_doc = "index"

pygments_style = "sphinx"
pygments_dark_style = "monokai"

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
