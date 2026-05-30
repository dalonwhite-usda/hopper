
#!/usr/bin/env bash
set -euo pipefail

# ---- settings ----
REPO_DIR="ghipm-py"
LEGACY_DIR="$REPO_DIR/data/legacy"

# ---- create tree ----
mkdir -p "$REPO_DIR"/{ghipm/{data_io,bio,econ_lp},tests,scripts,data/legacy}
cd "$REPO_DIR"

# ---- .gitignore ----
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.venv/
.env
data/legacy/*
EOF

# ---- README ----
cat > README.md << 'EOF'
# GHIPM-Py (Modern Python/Pyomo Rebuild)

Modern, testable Python rebuild of the 1994 USDA APHIS/ARS rangeland grasshopper economic optimization (HOPPER + Ranch LP), tuned for **Wyoming cow-calf, North 40 site**.

## Quick start
1. Install GLPK:
   - Conda: `conda install -c conda-forge glpk`
   - Ubuntu: `sudo apt-get install glpk-utils`
2. Install dependencies:
   ```bash
   pip install -e .
