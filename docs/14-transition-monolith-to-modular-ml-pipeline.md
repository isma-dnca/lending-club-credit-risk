at this point I changed `src/main.py` file from old version, where the whole project is one file, that contains :
    - load data
    - clean
    - feature engineering
    - handle missing values
    - split
    - encode
    - train
    - evaluate
    - print
from old version to new version, new `main.py` that is acting now as ONLY as entry point :
    - call preprocessing pipeline
    - call training module
    - call evaluation module
    - call saving module
  
So we moved from a `main.py` file hat is doing everything to `main.py` file that coordinates specialized modules.