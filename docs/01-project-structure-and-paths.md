
# Project Structure & Root Paths

## Purpose Of This Doc

Documenting everything related to structuring the project properly, like :
    -   How to organize the code base (`src/`, `data`, `docs`, etc)
    -   How to handle the **paths** cleanly and properly
    -   How to import modules without errors
    -   How to make the project **stable, reproducible, and scalable**
The main goal is to eliminate the classic excuse of every cooder:
    **`"It works on my machine"`**
So the project must be work the same way in every machine, at any time, as long as the environment is correctly installed.

---------------

## Step 1 : Define The Project Root

**Question:** So what is the Project Root?

**Answer:** It is the Top-Level folder that contains the entire repository.
In this project, the Project Root is :

    ```txt
    PROJECT_ROOT/  (lending-club-credit-risk)
    ```
On my local machine the projects live exactly here :
    `C:\Users\Utilisateur\Desktop\...\\lending-club-credit-risk>`

But when documenting it is recommended to refer to it as `PROJECT_ROOT/` to stay clean and professional,
because that previous path ("`C:\Users\Utilisateur\Desktop\...\\lending-club-credit-risk>`") it only
lives in my machine.

## Step 2 : Organizing projects folders : High-Level Layout

So at the root, the project contains :
```txt
    -   data/               : All our datasets lives here.
    -   docs/               : Any documentation, clarification or guides about the ongoing.
    -   notebooks/          : Jupyter notebooks for exploration and experiment like a visualization draft
    -   src/                : The reality of your projects like functions modules and pipelines
                                this is what we would actually import and build, code code code
    -   .gitignore          : Telling Git what to ignore when pushing like sensitive stuff : secrets, pycache
    -   environment.yml     : The setup for the whole environment so anyone can recreate it by simply
                                running `conda env create -f environment.yml` like all dependencies in one place
    -   .vscode             : Editor setting for *VS Code*, checked into git so everyone on the team shares 
                                the exact same coding environment. What I mean here by Checked into git is instead of each temmate setting up their own *VS Code* from scratch, we commit those config files (in .vscode) once and everyone who clones the repo, he gets automatically the same *VS Code setup*. 


                                and this is what we would typically put there :
                                    
                                    ```txt
                                    **settings.json **: The main config file. Typical settings:
                                                        - "python.defaultInterpreterPath" pointing to our conda  env
                                                        - Auto-format on save (black or autopep8)
                                                        - Tab size, rulers, file associations
                            
                                    **extensions.json** : Recommended extensions for the project.
                                                        When a teammate opens the project, VS Code will
                                                        suggest installing these automatically. Useful ones:
                                                        - ms-python.python        (Python support)
                                                        - ms-toolsai.jupyter      (Jupyter notebooks)
                                                        - charliermarsh.ruff      (fast Python linter (a linter is a tool to      
                                                                                     automatically analyse code and flag style or potential error issues, all this in order to improve the quality of our code))
                                                        - eamodio.gitlens         (better Git visibility)
                            
                                    **launch.json**     : Debug configurations. e.g. "Run main.py with
                                                        these args" or "Debug this specific pipeline step"
                                                        so we don't have to reconfigure the debugger every time.
                            


                                IF we want the OPPOSITE case, I mean to let the configurations of the editore stays on our machine only we add (`.vscode`) to (`.gitignore`) and here we go all happy.
                                
                                **!! What NOT To Put In *VS Code* !!**
                                    -   Any secrets or API Keys (Those must stay in our machine)
                                    -   Absolute paths like `C:/Users/Username...`
                                ONE RULE: If a setting makes theproject consistent ---> COMMIT
                                          If it is just a personal preference ---> Leavt it out for yourself, don't share or commit it
    -   README.md           :   Litteraly the front door of the project. it is the first thing anyone reads. It explain what the 
                                    the project does, how to set it up and how to use it.
    
    -   .ipynb_checkpoints/ :   This folder is auto-enerated by Jupyter. It saves backup versions of our notebooks automatically.
                                We must listed in `.gitignore` so it never gets pushed to the repo
```
----------

## Quick Cheat Sheet — What Goes Where?

| Type of file                           | Where it belongs   |
|---------------------------------       |--------------------|
| Raw or processed datasets              | `data/`            |
| Reusable functions, modules, pipelines | `src/`             |
| Exploration notebooks, drafts          | `notebooks/`       |
| Guides, write-ups, documentation       | `docs/`            |
| Editor config (shared)                 | `.vscode/`         |
| Environment dependencies               | `environment.yml`  |
| Files Git should ignore                | `.gitignore`       |
| Project overview and setup guide       | `README.md`        |

--------

## Full project tree
By running this command :

    ```powershell
    tree /f
    ```
the following structure is the result of the full project layout:

    ```txt
    C:.
|   .gitignore
|   environment.yml
|   README.md
|
+---.ipynb_checkpoints
+---.vscode
|       settings.json
|
+---data
|   +---processed
|   \---raw
|           LC_loans_granting_model_dataset.csv
|
+---docs
|       00-environment-setup.md
|       01project-execustion-model(root-paths-imports).md
|
+---notebooks
|   |   01-data-loading-and-exploration.ipynb
|   |
|   \---.ipynb_checkpoints
|           01-data-loading-and-exploration-checkpoint.ipynb
|
\---src
    |   __init__.py
    |
    \---data
            load.py
            __init__.py
```
----------------

## Why This Structure Matters

We can imagine and think of this Layout as giving every file a **"home"** and making sure it is actually living there

This structure enforces a clean separation between 4 pillars **code**, **data**, **experimets** and **documentation**.

| Pillar          | Folder        |
|-----------------|---------------|
| Code            | `src/`        |
| Data            | `data/`       |
| Experiments     | `notebooks/`  |
| Documentation   | `docs/`       |


So code goes to (`src/`), data goes to (`data/`), experiments goes to (`notebooks`), and documentation goes to (`docs`). By keeping things cleanly separated from the start, the project becomes easier to navigate, so we alwauys know where to look. Easier to debug, when something breaks we know exactly where to check. Easier to share, teammates can clone and run without playing detective and a private investigator, and reproducible on any machine, as long as the environment is installed correctly.

All of this to prevent a messy project, avoid headaches, and most importantly; to eliminate the classic excuse: "`It works on my machine`".


--------------------
-----------------------

## Step 3: The Golden Rule Of Paths (Absolute VS Relative)

### The Problem :
