# codeml_automator
##automates codeml runs on subset trees

###Instructions
  1. Compile the codeml binary for your machine and put it in the project root
  2. Place .tree files in the tree folder (default is trees, but it can be remapped in the python command).
    * The master tree file should be named treen.trees (Or it can be respecified in the positive_selection_runner command.)
  3. Place .nuc file in the nuc directory (can also be respecified in the python command).
  4. Run positive_selection_runner.py
  ```
  usage: positive_selection_runner.py [-h] [-gene_dir GENE_DIR]
                                      [-tree_dir TREE_DIR]
                                      [-tree_file TREE_FILE]
                                      [-paml_output PAML_OUTPUT] [-c C]
                                      [-new_controls_dir NEW_CONTROLS_DIR]

  Process some codeml files.

  optional arguments:
    -h, --help            show this help message and exit
    -gene_dir GENE_DIR    Location of the genes that you want to run. (default
                          "nuc")
    -tree_dir TREE_DIR    location of your tree files. (default "tree")
    -tree_file TREE_FILE  location of the master tree file. (default
                          "<tree_dir>/treen.trees")
    -paml_output PAML_OUTPUT
                          where to output the paml files. (default
                          "paml_output")
    -c C                  Number of cores (default 1)
    -new_controls_dir NEW_CONTROLS_DIR
                          where more files are output. And codeml is run
                          (default "new_controls")
  ```
