# JupyterLite / JupyterBook notebook processing

These are utilities to take text-format notebooks in a Jupyter Book directory,
and write out a JupyterLite installation, containing `.ipynb` (JSON) notebooks with suitable processing.

The module provides the executable `jljb-write-dir`.  See the help for that command for more details.

That command will:

* Look for suitable `_config.yml` configuration in the current directory, or
  at a location you specify.
* It then looks in the configuration for a `jupyterlite` section, and within
  that section looks for these values (default if not specified):

  | Name             | Default |
  | ---------------- | ------- |
  | in_nb_ext        | .md     |
  | out_nb_ext       | .ipynb  |
  | in_nb_fmt        | myst    |
  | remove_remove    | True    |
  | proc_admonitions | True    |

* With that information, the script finds text format notebooks with the
  `in_nb_ext` extension, and applies the following processing to write into an
  output folder:

  * Replaces local kernel with Pyodide kernel in metadata.
  * Filters:
      * Note and admonition markers (if `proc_admonitions` is True)
      * Exercise markers (see
        [sphinx_exercise](https://ebp-sphinx-exercise.readthedocs.io)).
      * Solution blocks for exercises.
      * Cells marked with [`remove-cell`
        tag](https://jupyterbook.org/v1/interactive/hiding.html#removing-code-cell-content).
  * Writes notebooks to output directory.
  * Writes JSON JupyterLite file.

The typical way to use this module / command is to write your settings into
the `_config.yml` file as above, and have a `Makefile` target of form:

```Makefile
jl:
    # Jupyter-lite files for book build.
    # Install specified requirements for built JupyterLite site.
    $(PIP_INSTALL_CMD) -r requirements.txt
    jljb-write-dir $(BUILD_DIR)/interact data images
```

`$(BUILD_DIR)/interact` is the directory to which the JupyterLite site
will be written; `data` and `images` are directories that should be
copied into the JupyterLite notebook directories from the source
directory.

You will likely want to point your JupyterBook build at the JupyterLite
output directory.  See the [example configuration
file](./tests/example__config.yml) for an example, that further depends
on a modified version of `sphinx-book-theme`.  At time of writing, you should specify that version in your book build requirements files as:

```text
sphinx-book-theme@git+https://github.com/executablebooks/sphinx-book-theme@56874cb
```

See the [Scientific Python Lectures
requirements](https://github.com/scipy-lectures/scientific-python-lectures/blob/88549968903bfd697aaf5d25d88babb09281fa82/build_requirements.txt)
for an example.

For debugging notebook processing by `jljb-write-dir`, you might consider
writing out the processed intermediate notebooks into a directory that
you can inspect.  As an example, you could replace the last `Makefile`
line above with:`

```Makefile
    jljb-write-dir $(BUILD_DIR)/interact data images --jl-tmp $(JL_DIR)
```

where `$(JL_DIR)` is a directory into which the processed notebooks will
be written, prior to copying into the JupyterLite site.
