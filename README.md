# Plexos_Flow_Files
Scripts used to work on Brazilian Hydro Power Plant Flow Data

Flow data adjustments in order to compute incremental flow data by Hydro Power Plant in Brazil using https://github.com/tuberculo/incremental.

The output from https://github.com/tuberculo/incremental is also managed in this repo scripts to generate the flow input data for Plexos.

# Description
The basic files must be saved into Original folder. Three out of four files are avaible in this repo (further info about them can be found at https://github.com/DIUANA/Plexos_Flow_Files/blob/main/Original/README.md

It is necessary to download one extra file that is missing: **Vazões_Diárias_1931_2019.xlsx** from https://sintegre.ons.org.br

There are X scripts that will work upon the files stored in the Original folder

Scripts are divided based on actions they are realizing.

# How to run
Download the repository and create a project with Spyder IDE based on an existing folder (repo clone folder).

Scripts are designed to be run in the following order:
1. A
2. B
3. Run incremental script from https://github.com/tuberculo/incremental.
4. D
5. E

