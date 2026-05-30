
# GHIPM-Py (Modern Python/Pyomo Rebuild)

This is a modern, testable Python rebuild of the 1994 USDA APHIS/ARS rangeland grasshopper
economic optimization system (HOPPER + Ranch LP), tailored for **Wyoming cow-calf, North 40 site**.

## Quick start
1. Install **GLPK** (solver):
   - Conda: `conda install -c conda-forge glpk`
   - Ubuntu: `sudo apt-get install glpk-utils`
2. Install Python deps:
   ```bash
   pip install -e .
