# Episode 00 — Python Environment Setup (No Global Pollution)

What I mean by **"No Global Pollution"** is avoiding installing Python packages system-wide (globally).

Installing packages globally can cause several problems:

- **Version conflicts**: different projects may require different versions of the same package.
- **Dependency nightmare**: one project's requirements can break another.
- **Permission issues**: you may need administrator rights (`sudo` on Linux).
- **System stability risks**: system tools that depend on Python could break.

To avoid this "pollution," the solution is to use a **virtual environment**.

A virtual environment is basically an isolated workspace where Python packages are installed only for a specific project.

> **Goal:** Build a professional Machine Learning environment using Conda, without breaking the global system.

---

## Why am I starting with this—and documenting it?

In Python, you *can* install libraries globally, directly onto your computer.

At first, it works... until one day (maybe on a Monday) it doesn't.

Suddenly:

- one project breaks another project
- version conflicts appear
- you waste hours (or even days) fixing your system

That's why the clean and professional approach is to **never work globally**.  
Instead, isolate each project in its own environment.

To visualize this, think of it like cooking:

- **Global Python** = one kitchen for all restaurants in your city
- **Conda environment** = one private kitchen for each restaurant

Result: no pollution, no conflicts, no chaos, no fights.

---

## Step 1 — Check if Conda Exists

I personally prefer working inside the **VS Code terminal**, but you can also use **PowerShell** or **Windows Terminal**.

Run:
```powershell
conda --version
```

Expected output:
```txt
conda 25.11.1
```

If Conda is not installed, the terminal will return something like:
```txt
conda : The term 'conda' is not recognized...
```

### What we just did:
We made sure Conda is installed on our machine. Think of this as checking if we have the tools before we start building. Without Conda, we can't create isolated environments, so this check saves us from wasting time on the next steps.

**Next up:** We're going to create the recipe file that tells Conda exactly what our environment needs.

---

## Step 2 — Create 'environment.yml' File

`environment.yml` is like the recipe for our project. It's one of the most important files in any professional ML project. We can consider it as the **official recipe** for our Conda environment.

### But why do we need `environment.yml`?

Right now, we could install packages manually like this:
```powershell
conda install numpy pandas scikit-learn
```

And guess what... yes, it works. But the problems are:

- **Only you know what's installed** : You're the only one who knows the exact setup on your machine
- **Your laptop/machine/PC is the only place where the project works** : It's not reproducible elsewhere
- **Others will struggle** : If you send your project to someone else, they won't be able to set it up easily
- **Everything is vulnerable** : If issues affect your operating system, everything could be lost
- **No GitHub reproducibility** : If you push it to GitHub, nobody can reproduce your exact setup

So instead of installing packages randomly, we create a recipe file that we call `environment.yml`.

As above, we'll use the same restaurant analogy by thinking of our ML project as a restaurant. Simple analogy but powerful:

- **Your machine/computer** = City
- **Global Python** = One shared kitchen for all restaurants in the city (seems crazy, but imagine it!)
- **Conda environment** = Your private kitchen for your restaurant
- **`environment.yml`** = The recipe book for your restaurant

Without the recipe book, nobody can recreate your dishes. With the recipe book, anyone can rebuild the same kitchen anywhere in the world.

The `environment.yml` file must be created inside the root folder. In my case, I already have an empty `environment.yml` file created, as shown below:
```
lending-club-credit-risk/
├── **environment.yml**
├── README.md
├── src/
├── notebooks/
├── data/
└── docs/
```

### Another Thing: Why Exactly YAML?

YAML is a configuration format that's human readable, and most importantly, it supports comments, unlike JSON. We use it to describe the environment in a readable and structured way. For example:

```yml
name: myenv
dependencies:
  - python=3.11
  - numpy
```

It looks like plain text rather than code, which makes it both useful and usable.

### Now we are going to write the environment file:
```yml
name: lending-club-ml
channels:
  - conda-forge
  - defaults

dependencies:
  - python=3.11
  - pip
  - numpy
  - pandas
  - matplotlib
  - seaborn
  - scikit-learn
  - jupyterlab
```

### Explanation of each part inside `environment.yml`:

**`name: lending-club-ml`**  
This is the name of the Conda environment that will be created. Later, we'll activate it using the standard command:
```powershell
conda activate lending-club-ml
```

We use `lending-club-ml` because it clearly describes the project's purpose. Using descriptive, meaningful names is highly recommended for professional projects to prevent confusion with other environments.

### Channels

Channels are like package stores. They tell Conda where to download packages from:

- **`conda-forge`**: A community-maintained store that's often the best first choice because packages are newer and updated frequently.
- **`defaults`**: The official Conda store maintained by Anaconda.

By listing `conda-forge` first, we tell Conda to prioritize this store. If it doesn't find what we need there, it will check the official `defaults` store.

### Dependencies

This lists all the packages we want in our environment. Think of it as the ingredient list for our project's kitchen—everything we need to cook up our machine learning solution.

The packages in our dependencies are:

- **`python=3.11`**: This fixes our project to Python 3.11, ensuring our code always runs the same way without version conflicts. As discussed earlier, this avoids random bugs and keeps everything stable and reproducible.

- **`pip`**: We need pip inside our environment as a backup installer. You'll definitely encounter situations where a library isn't available through Conda, and pip serves as our fallback solution.

- **`numpy`**: This is literally the mathematical backbone that almost all ML code relies on under the hood.

- **`pandas`**: We use this to work with tabular data (like loan records), clean it, transform it, and—most importantly for any data scientist—understand it.

- **`matplotlib`**: This package lets us plot and inspect patterns in the data.

- **`seaborn`**: Seaborn sits on top of **matplotlib** to make those plots more readable and visually clear.

- **`scikit-learn`**: This is the core machine learning library we'll use for preprocessing and baseline models. It's stable, widely used (an industry standard), and well-tested.

- **`jupyterlab`**: This is our interactive workspace where we explore data, test ideas, and document our reasoning step by step.

### What we just did:
We wrote the complete recipe for our environment. This file now contains everything: the environment name, where to get packages from, and which packages to install. It's reproducible, shareable, and professional. Anyone can take this file and recreate the exact same setup on their machine.

**Next up:** We're going to use this recipe to actually build the environment and activate it.

---

## Step 3 — Build and Activate the Environment

Now that our recipe is ready, we can build the environment automatically. But before doing that, always, **always** check and make sure you're located in the project root.

### Navigate to Project Root
```bash
cd C:\Users\[YourUsername]\Desktop\projects\lending-club-credit-risk
```

### Create the Environment
Run:
```bash
conda env create -f environment.yml
```

The command above means:
  - `conda env create` create new environment
  - `-f environment.yml` to create that environment please use the environment.yml file as the recipe
  
By specifying the `environment.yml` file we created earlier, we're telling Conda to download and install all the dependencies we listed in that file respecting everything from versions to channels.

So after running `conda env create -f environment.yml` you will see output similar to this:
```txt
channels:
  - conda-forge
  - defaults
Collecting package metadata: done
Solving environment: done
Downloading and Extracting Packages: done
Executing transaction: done

# To activate this environment, use
#
#     $ conda activate lending-club-ml
```

This process can take 5 to 10 minutes to download all the packages.

### Verify Environment Creation
Check if the environment was created successfully by running:
```bash
conda env list
```

Expected output should include something like: `lending-club-ml          C:\Users\[YourUsername]\Desktop\projects\lending-club-ml`

**Congratulations!** Now your project officially has its own **private kitchen**. You've successfully created a new environment by running the YAML file that contains all the required tools for your project.

### Activate the New Environment

To enter the world of our project, we must activate the environment we recently created—the `lending-club-ml` environment.

#### Deactivate Current Environment (If Needed)
First, we need to deactivate any currently active environment. In my case, it's `(ml)`. In your case, it might be `(base)` or something else.

```bash
conda deactivate
```

You should see your current environment name disappear from the terminal prompt.

#### Activate the New Environment
Next step is to activate the `lending-club-ml` environment, by running:
```bash
conda activate lending-club-ml
```

To confirm you're officially in the `lending-club-ml` environment, look for these signs:

1. **Terminal prompt**: You should see `(lending-club-ml)` at the start of your terminal line
2. **Environment list**: Run `conda env list` to see all existing environments—the active one will have an asterisk (`*`) next to it

#### Example Verification:
```powershell
# Activate the new environment
conda activate lending-club-ml

# Verify it's active and see all environments
conda env list
```

Example output:

```powershell
(ml) PS C:\path\to\lending-club-credit-risk> conda activate lending-club-ml
(lending-club-ml) PS C:\path\to\lending-club-credit-risk> conda env list

# conda environments:
#
# * -> active
# + -> frozen
base                     C:\Users\User\miniconda3
lending-club-ml      *   C:\Users\User\miniconda3\envs\lending-club-ml
ml                       C:\Users\User\miniconda3\envs\ml

(lending-club-ml) PS C:\path\to\lending-club-credit-risk>
```

As you can see:
- The prompt changes from `(ml)` to `(lending-club-ml)`
- The `*` symbol next to `lending-club-ml` indicates it's currently the active environment

In this example output, there are three environments:
- `base` (the default Conda environment)
- `ml` (a previously created environment)
- `lending-club-ml` (currently active, as shown by the `*`)

### Final Verification

To ensure everything is under control and we're working with the exact tools specified:

Check Python Version by running:
```bash
python --version
```

Expected output (must match what we specified in the YAML file): 
```txt
Python 3.11.x
```

Verify Packages Exist by running:
```bash
python -c "import numpy, pandas, sklearn; print('ok')"
```

By getting `ok` as output, you're officially ready to move on to the next step!

### What we just did:
We built the environment from our recipe file, activated it, and verified everything works. Our terminal now operates inside this isolated environment. When we install packages or run Python code, it all happens inside this bubble—completely separate from the global system. The environment exists, it's active, and it's ready.

**Next up:** We need to make sure VS Code uses this same environment. Otherwise, VS Code might be running a different Python in the background, and we'd be back to debugging mystery errors.

---

## Step 4 — Connect VS Code to Your Environment

We need to connect VS Code to the environment we created in the previous steps. This is crucial because VS Code might use a different Python version in the background without our knowledge. By forcing it to use the `lending-club-ml` environment, we ensure everything runs in the right order and avoid wasting time debugging issues caused by environment mismatches.

### Ensure Your Environment is Activated
Make sure you're in the `lending-club-ml` environment (you should see `(lending-club-ml)` in your terminal prompt).

### Launch VS Code from the Activated Environment
Run this command from your project directory:

```bash
code .
```

### VS Code Python Interpreter Check

Now we gotta make sure VS Code is actually using our `lending-club-ml` environment. Sometimes VS Code picks the wrong Python without telling you, then you get weird errors.

**How to check:**

1. Press `Ctrl + Shift + P` (that opens the command palette)
2. Type "Python: Select Interpreter" and hit Enter

You'll see a list of all Python installations VS Code found:

**Available Interpreters:**
- Python 3.14.0 (`~\AppData\Local\Programs\Python\Python314\python.exe`)
- Python 3.13.11 (base) (`~\miniconda3\python.exe`)
- **✓ Python 3.11.14 (lending-club-ml)** (`~\miniconda3\envs\lending-club-ml\python.exe`)
- Python 3.11.14 (ml) (`~\miniconda3\envs\ml\python.exe`)
    
**Pick the one that says `(lending-club-ml)` with Python 3.11.14**

Look for:
- `lending-club-ml` in parentheses
- Python 3.11.14 (not 3.14 or 3.13)
- The path that ends with `\envs\lending-club-ml\python.exe`

Once you click it, check the bottom right corner of VS Code, it should say something like:
`Python 3.11.14 ('lending-club-ml'): conda`. If you don't see it immediately, try opening a Python file (.py) and it should show up at the bottom right of that `(.py)` file. 

Once you see it, you are golden. That means VS Code is now using exact same environment as your terminal and that's how you know you're good to go.

To make things officially okay and crystal clear on VS Code terminal run:
```bash
python --version
```

The expected output:
```txt
Python 3.11.14
```

### Optional: `.vscode/settings.json` for Automatic Interpreter

This step is optional, but highly recommended. It ensures that anyone opening the project in VS Code will automatically use the correct Python environment.

To do this:

1. Create a folder named `.vscode` in the **root folder** of your project.
2. Inside that folder, create a file called `settings.json`.
3. Add the following content to the file (adjust the path according to where your environment is located):

```json
{
  "python.pythonPath": "C:\\Users\\Utilisateur\\miniconda3\\envs\\lending-club-ml\\python.exe"
}
```

To make sure you are using the correct Python path in `settings.json`, follow these practical steps:

1. Activate your environment in the terminal:

```powershell
conda activate lending-club-ml
```

2. Run the following command to locate all Python executables:

```powershell
where.exe python
```

3. You will see a list of paths. Select the one that contains your environment name `(lending-club-ml in this case)`.

`Windows users: Make sure to use double backslashes \\ in the path when adding it to settings.json.`

4. Save the `settings.json` file.

Now, every time you open VS Code in this project, it will automatically use the correct Python interpreter from your `lending-club-ml` environment.

### What we just did:
We connected VS Code to our environment. Now when you write Python code in VS Code, it runs using the exact same Python and packages as your terminal. No surprises, no hidden conflicts. Everything is aligned. If you also created the `settings.json` file, this configuration is now locked in—anyone who opens this project will automatically get the right Python.

**Next up:** One last piece—Jupyter notebooks. We need to register our environment as a kernel so Jupyter knows about it.

---

## Step 5 — Register Jupyter Kernel

We need to make sure our Jupyter notebooks use the right environment too.

Here's the thing: when you open a Jupyter notebook, you have to pick a "kernel" to run your code. That kernel is basically "which Python" your notebook is going to use.

But here's the problem: Jupyter doesn't automatically know about our fancy `lending-club-ml` environment. It might just show you the default Python or some random one.

So we gotta tell Jupyter: "Hey, register my `lending-club-ml` environment as an available kernel." That way, when we're in a notebook, we can select it and know for sure we're using the exact same tools we set up.

### The Kitchen Analogy (Extended):
- **Our environment** = Private kitchen with all our ingredients (packages)
- **Jupyter notebook** = Restaurant menu - it doesn't cook food, just sends orders (your code)
- **Jupyter kernel** = The chef in that kitchen - actually cooks (executes Python code)
- **Wrong kernel** = Wrong chef in the wrong kitchen = disaster

Otherwise, you might write code that works in your terminal but breaks in Jupyter because they're using different Pythons. Been there, not fun.

### The Magic Command:
```bash
python -m ipykernel install --user --name lending-club-ml --display-name "Python (lending-club-ml)"
```

### What This Command Actually Does:

**`ipykernel`** - This is the engine that connects Python to Jupyter. It's literally the bridge between the notebook interface (what you see in browser at `http://localhost:8888`) and the actual Python interpreter. Without `ipykernel`, Jupyter can't talk to that Python at all.

**`--user`** - This flag makes the installation local to your user account. It avoids needing admin rights, keeps things safe, and doesn't affect other users on the same machine.

**`--name lending-club-ml`** - This is the internal kernel name. It's what Jupyter uses behind the scenes as an ID. Think of it like a username for the kernel.

**`--display-name "Python (lending-club-ml)"`** - This is the human-friendly name that shows up in the Jupyter menu. It makes it understandable and matches directly with our environment name so we don't get confused.

### Quick Check After Running:
After you run the command, start Jupyter and look for `Python (lending-club-ml)` in the kernel selection menu. That's how you know it worked!

### What we just did:
We registered our environment as a Jupyter kernel. Now Jupyter knows about `lending-club-ml` and will show it as an option when you're picking which Python to use in a notebook. Terminal, VS Code, and Jupyter are all using the same environment. Everything is locked in and consistent.

---

## Final Wrap-Up

At this point, we've built a complete, professional Python environment that's:

- **Isolated** - No global pollution, no conflicts with other projects
- **Reproducible** - Anyone can recreate it from `environment.yml`
- **Consistent** - Terminal, VS Code, and Jupyter all use the same Python
- **Professional** - This is how real ML projects are set up

From now on, every time you work on this project:

1. Activate the environment: `conda activate lending-club-ml`
2. Open VS Code: `code .`
3. Start coding

And when you share the project? Just include `environment.yml` and others can build the exact same setup with one command.

That's it. Clean, simple, professional.