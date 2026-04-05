# Pixi Package Manager: Novice to Pro Guide
> **Covers Pixi v0.65.0 and newer** | [Official Docs](https://pixi.sh) | [GitHub](https://github.com/prefix-dev/pixi)

---

## Table of Contents

1. [What is Pixi?](#1-what-is-pixi)
2. [Installation](#2-installation)
3. [Core Concepts](#3-core-concepts)
4. [Your First Python Project](#4-your-first-python-project)
5. [The Manifest File: pixi.toml vs pyproject.toml](#5-the-manifest-file-pixitoml-vs-pyprojecttoml)
6. [Managing Dependencies](#6-managing-dependencies)
7. [Environments](#7-environments) *(includes default-environment)*
8. [Tasks](#8-tasks)
9. [The Lock File](#9-the-lock-file)
10. [Multi-Platform Support](#10-multi-platform-support)
11. [Multi-Environment Workflows](#11-multi-environment-workflows) *(includes default-environment patterns)*
12. [Global Tools](#12-global-tools)
13. [Build Backends (pixi build)](#13-build-backends-pixi-build)
14. [The Python Build Backend (pixi-build-python)](#14-the-python-build-backend-pixi-build-python)
15. [Other Build Backends](#15-other-build-backends)
16. [Distributing Your Project](#16-distributing-your-project)
17. [CI/CD Integration](#17-cicd-integration)
18. [Advanced Features](#18-advanced-features) *(includes exclude-newer, constraints, and more)*
19. [Configuration Reference](#19-configuration-reference)
20. [CLI Reference](#20-cli-reference)
21. [Tips, Tricks & Best Practices](#21-tips-tricks--best-practices)

---

## 1. What is Pixi?

Pixi is a **fast, modern, cross-platform package manager and developer workflow tool** built in Rust by [prefix.dev](https://prefix.dev). It sits on top of the conda ecosystem (specifically conda-forge) and integrates seamlessly with PyPI via `uv`.

Think of it as the best of all worlds:
- The **reproducibility** of Poetry/cargo (lockfiles built-in)
- The **multi-language** power of conda (Python, C++, R, Rust, CUDA, etc.)
- The **speed** of mamba/uv (up to 10× faster than conda)
- A **built-in task runner** (like `make` or `npm run`)
- **No base environment required** — single self-contained binary

### How Pixi Compares

| Feature                  | Pixi | conda | pip | Poetry | uv |
|--------------------------|:----:|:-----:|:---:|:------:|:--:|
| Installs Python          | ✅   | ✅    | ❌  | ❌     | ✅ |
| Multi-language support   | ✅   | ✅    | ❌  | ❌     | ❌ |
| Built-in lockfiles       | ✅   | ❌    | ❌  | ✅     | ✅ |
| Task runner              | ✅   | ❌    | ❌  | ❌     | ❌ |
| Workspace management     | ✅   | ❌    | ❌  | ✅     | ✅ |
| PyPI + conda in one tool | ✅   | ❌    | ❌  | ❌     | ❌ |

### Key Terminology

| Term | Meaning |
|------|---------|
| **Workspace** | A project directory managed by Pixi (contains `pixi.toml` or `pyproject.toml`) |
| **Environment** | An isolated set of installed packages (like a conda env or venv) |
| **Feature** | A named group of dependencies/tasks that can be composed into environments |
| **Channel** | A package repository (e.g., `conda-forge`, `pytorch`) |
| **Lock file** | `pixi.lock` — exact pinned versions of all resolved packages |
| **Task** | A named shell command defined in the manifest |
| **default-environment** | The environment Pixi uses when no `-e`/`--environment` flag is given |

---

## 2. Installation

### Linux & macOS

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

### macOS (Homebrew)

```bash
brew install pixi
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

### Windows (winget)

```powershell
winget install prefix-dev.pixi
```

After installation, **restart your terminal** or source your shell config.

### Verify Installation

```bash
pixi --version
# Pixi 0.65.0
```

### Update Pixi

```bash
pixi self-update
```

> ⚠️ If you installed via Homebrew or a system package manager, use that tool to update instead (e.g., `brew upgrade pixi`).

### Shell Autocompletion

Add the appropriate line to your shell config file and restart your terminal:

**Bash** (`~/.bashrc`):
```bash
eval "$(pixi completion --shell bash)"
```

**Zsh** (`~/.zshrc`):
```bash
eval "$(pixi completion --shell zsh)"
```

**Fish** (`~/.config/fish/config.fish`):
```fish
pixi completion --shell fish | source
```

**PowerShell** (`$PROFILE`):
```powershell
(& pixi completion --shell powershell) | Out-String | Invoke-Expression
```

---

## 3. Core Concepts

### How Pixi Resolves Packages

Pixi uses a **SAT (Boolean Satisfiability) solver** written in Rust to resolve dependencies. This is the same approach used by cargo (Rust) and is significantly faster than conda's solver. When you run `pixi install` or `pixi add`, Pixi:

1. Reads your manifest (`pixi.toml` or `pyproject.toml`)
2. Fetches package metadata from configured channels
3. Solves the dependency graph using the SAT solver
4. Writes exact pinned versions to `pixi.lock`
5. Downloads and installs packages (using hard links / reflinks for disk efficiency)

### Conda + PyPI Integration

Pixi can install packages from two sources simultaneously:

- **Conda packages** (from channels like `conda-forge`) — defined in `[dependencies]`
- **PyPI packages** (from PyPI, via `uv`) — defined in `[pypi-dependencies]`

When both are available, **conda packages take precedence** over PyPI packages for the same library. This is important because conda packages often include compiled binaries and system-level dependencies that pip wheels may not.

### Disk Efficiency

Pixi uses **hard links** (or reflinks on supported filesystems) to share package files across environments. This means if you have 10 projects all using `numpy`, the actual files are stored only once on disk.

---

## 4. Your First Python Project

### Initialize a New Project

```bash
# Create a new project directory with pixi.toml
pixi init my-python-app
cd my-python-app

# OR: Create using pyproject.toml format (recommended for Python packages)
pixi init my-python-app --format pyproject
cd my-python-app
```

### Add Python and Dependencies

```bash
# Add a specific Python version
pixi add python==3.12.*

# Add packages from conda-forge
pixi add numpy pandas matplotlib scikit-learn

# Add packages from PyPI
pixi add --pypi requests httpx rich
```

### Run Code

```bash
# Run a one-off command in the pixi environment
pixi run python -c "import numpy; print(numpy.__version__)"

# Run a Python script
pixi run python my_script.py

# Open an interactive shell inside the environment
pixi shell
python  # now you're in the pixi environment
exit    # leave the pixi shell
```

### A Complete Hello World

```bash
pixi init hello-world
cd hello-world
pixi add python numpy
```

Create `hello.py`:
```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(f"Array: {arr}")
print(f"Mean: {arr.mean()}")
print(f"NumPy version: {np.__version__}")
```

```bash
pixi run python hello.py
```

---

## 5. The Manifest File: pixi.toml vs pyproject.toml

Pixi supports two manifest formats. You can use either one — Pixi prefers `pixi.toml` if both exist.

### pixi.toml

The native Pixi manifest. Best for multi-language projects or when you don't need to publish to PyPI.

```toml
[workspace]
name = "my-project"
version = "0.1.0"
description = "My awesome Python project"
authors = ["Alice <alice@example.com>"]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "osx-64", "win-64"]

[dependencies]
python = ">=3.11,<3.13"
numpy = ">=1.26"
pandas = ">=2.0"

[pypi-dependencies]
requests = ">=2.31"

[tasks]
start = "python src/main.py"
test  = "pytest tests/"
lint  = "ruff check src/"

[feature.dev.dependencies]
pytest = ">=8.0"
ruff   = ">=0.4"

[environments]
dev = { features = ["dev"], solve-group = "default" }
```

### pyproject.toml

The standard Python packaging format. All Pixi config goes under `[tool.pixi]`. Best for Python packages you want to publish to PyPI.

```toml
[project]
name = "my-python-package"
version = "0.1.0"
description = "My Python package"
requires-python = ">=3.11"
authors = [{ name = "Alice", email = "alice@example.com" }]
dependencies = [
    "numpy>=1.26",
    "pandas>=2.0",
    "requests>=2.31",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# ── Pixi configuration ──────────────────────────────────────────────────────
[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "osx-64", "win-64"]

# Install this package itself in editable mode
[tool.pixi.pypi-dependencies]
my-python-package = { path = ".", editable = true }

[tool.pixi.tasks]
start = "python src/my_python_package/main.py"
test  = "pytest tests/"

[tool.pixi.feature.dev.dependencies]
pytest     = ">=8.0"
pytest-cov = "*"
ruff       = ">=0.4"
mypy       = "*"

[tool.pixi.feature.dev.tasks]
test     = "pytest tests/ -v"
coverage = "pytest --cov=src tests/"
lint     = "ruff check src/"
typecheck = "mypy src/"

[tool.pixi.environments]
dev = { features = ["dev"], solve-group = "default" }
```

> **Tip:** `pixi init --format pyproject` generates a `pyproject.toml` with `hatchling` as the default build backend. This is the recommended starting point for Python packages.

### When to Use Which

| Use `pixi.toml` when... | Use `pyproject.toml` when... |
|-------------------------|------------------------------|
| Multi-language project (C++, Rust, etc.) | Pure Python package |
| Building conda packages | Publishing to PyPI |
| Better editor support for Pixi features | Single manifest file preferred |
| Non-Python primary language | Using Python build tools (hatch, setuptools) |

---

## 6. Managing Dependencies

### Adding Dependencies

```bash
# Add a conda package (from conda-forge by default)
pixi add numpy

# Add with version constraint
pixi add "numpy>=1.26,<2.0"

# Add from a specific channel
pixi add pytorch --channel pytorch
pixi add "cuda>=12.0" --channel nvidia

# Add a PyPI package
pixi add --pypi requests
pixi add --pypi "fastapi>=0.100"

# Add as a development dependency (only in dev feature)
pixi add --feature dev pytest ruff mypy

# Add to a specific environment
pixi add --environment test pytest
```

### Removing Dependencies

```bash
pixi remove numpy
pixi remove --pypi requests
pixi remove --feature dev pytest
```

### Updating Dependencies

```bash
# Update a specific package
pixi update numpy

# Update all packages
pixi update

# Update and re-solve the lock file
pixi update --no-install
```

### Listing Installed Packages

```bash
# List all packages in the default environment
pixi list

# List packages in a specific environment
pixi list --environment dev

# Show only explicit (non-transitive) dependencies
pixi list --explicit

# Output as JSON
pixi list --json
```

### Searching for Packages

```bash
# Search conda-forge for a package
pixi search numpy

# Search with a version constraint (MatchSpec)
pixi search "numpy>=2.0"

# Search in a specific channel
pixi search pytorch --channel pytorch

# Output as JSON
pixi search numpy --json
```

### Version Specifiers

Pixi supports standard conda MatchSpec and PEP 440 version specifiers:

```toml
[dependencies]
# Exact version
python = "3.12.0"

# Compatible release (>=3.11, <4.0)
python = "~=3.11"

# Range
numpy = ">=1.26,<3.0"

# Wildcard (any 3.12.x)
python = "3.12.*"

# Any version
scipy = "*"

# Build string constraint (conda-specific)
cudatoolkit = "11.8.*"
```

### PyPI-Specific Dependency Options

```toml
[pypi-dependencies]
# Standard version constraint
requests = ">=2.31"

# Install from a local path (editable)
my-package = { path = ".", editable = true }

# Install from a local path (non-editable)
my-lib = { path = "../my-lib" }

# Install from a git repository
my-fork = { git = "https://github.com/user/repo.git", branch = "main" }
my-tag  = { git = "https://github.com/user/repo.git", tag = "v1.2.3" }
my-rev  = { git = "https://github.com/user/repo.git", rev = "abc1234" }

# Install with extras
fastapi = { version = ">=0.100", extras = ["standard"] }

# Install from a URL
my-wheel = { url = "https://example.com/my_package-1.0-py3-none-any.whl" }
```

### Conda Source Dependencies (Preview)

As of v0.65+, you can depend on conda packages built from source:

```toml
[dependencies]
my-c-lib = { git = "https://github.com/user/my-c-lib.git", branch = "main" }
```

### Dependency Overrides / Constraints

Use `[constraints]` to limit versions of packages that may be pulled in transitively, without explicitly requiring them:

```toml
[constraints]
openssl = ">=3"
libssl  = ">=3"
```

This is similar to `run_constraints` in conda recipes.

---

## 7. Environments

### Default Environment

Every Pixi project has a `default` environment that includes all packages from `[dependencies]` and `[pypi-dependencies]`. When you run `pixi run`, `pixi shell`, or any other environment-aware command **without** the `-e`/`--environment` flag, Pixi uses whichever environment is designated as the *default environment*.

#### Changing the Default Environment

By default the environment named `default` is used. You can override this with the `default-environment` key in `[workspace]` (or `[project]` for older manifests):

```toml
[workspace]
name             = "my-project"
channels         = ["conda-forge"]
platforms        = ["linux-64", "osx-arm64", "win-64"]
default-environment = "dev"   # ← pixi run / pixi shell now target "dev"
```

With this setting, every bare `pixi run <task>` or `pixi shell` automatically activates the `dev` environment — no `-e dev` needed.

#### Why This Matters

When a project has multiple environments (e.g. `default`, `dev`, `test`, `docs`) the most useful one for day-to-day work is rarely the bare `default`. Setting `default-environment = "dev"` means:

- `pixi run test` → runs in `dev` (which includes pytest, ruff, etc.)
- `pixi shell` → drops you into `dev`
- CI can still target specific environments explicitly with `-e test`

#### Shared Features and default-environment

A common pattern is to have several environments that all share a common feature (e.g. `base`) and then set the richest one as the default:

```toml
[workspace]
default-environment = "dev"

[feature.base.dependencies]
python = "3.12.*"
numpy  = ">=1.26"
pandas = ">=2.0"

[feature.test.dependencies]
pytest     = ">=8.0"
pytest-cov = "*"

[feature.lint.dependencies]
ruff = ">=0.4"
mypy = "*"

[environments]
# "dev" is the default — includes everything a developer needs
dev  = { features = ["base", "test", "lint"], solve-group = "default" }
# "test" is used in CI — lean, only what's needed to run tests
test = { features = ["base", "test"],         solve-group = "default" }
# "default" is kept minimal for end-users / production installs
default = { features = ["base"],              solve-group = "default" }
```

Now a developer can just type `pixi run test` or `pixi shell` and land in `dev` automatically, while CI explicitly passes `-e test`.

### Features

A **feature** is a named group of dependencies, tasks, and configuration that can be mixed into environments:

```toml
# pixi.toml

[feature.test.dependencies]
pytest     = ">=8.0"
pytest-cov = "*"
hypothesis = "*"

[feature.test.tasks]
test     = "pytest tests/ -v"
coverage = "pytest --cov=src --cov-report=html tests/"

[feature.lint.dependencies]
ruff = ">=0.4"
mypy = "*"

[feature.lint.tasks]
lint      = "ruff check src/"
format    = "ruff format src/"
typecheck = "mypy src/"

[feature.docs.dependencies]
mkdocs          = "*"
mkdocs-material = "*"

[feature.docs.tasks]
docs       = "mkdocs serve"
build-docs = "mkdocs build"
```

### Defining Environments

```toml
[environments]
# Default environment (just the base dependencies)
default = { features = [], solve-group = "default" }

# Dev environment: base + test + lint + docs
dev = { features = ["test", "lint", "docs"], solve-group = "default" }

# CI test environment: base + test only
test = { features = ["test"], solve-group = "default" }

# Docs-only environment
docs = { features = ["docs"] }

# Environment without the default feature
minimal = { features = ["test"], no-default-feature = true }
```

> **`solve-group`**: Environments in the same solve group are solved together, ensuring compatible package versions across all of them. This is important for monorepos.

### Using Environments

```bash
# Install all environments
pixi install

# Install a specific environment
pixi install --environment dev
pixi install -e dev          # shorthand

# Run a command in a specific environment
pixi run --environment test pytest
pixi run -e test pytest      # shorthand

# Open a shell in a specific environment
pixi shell --environment dev
pixi shell -e dev            # shorthand

# List available environments
pixi info
```

> **Tip — skip `-e` entirely:** Set `default-environment = "dev"` in `[workspace]` and bare `pixi run` / `pixi shell` commands will automatically target `dev`. You only need `-e` when you want a *non-default* environment.

---

## 8. Tasks

Tasks are named shell commands defined in your manifest. They are cross-platform (Pixi handles path separators, etc.) and support dependencies between tasks.

### Basic Tasks

```toml
[tasks]
# Simple command
start = "python src/main.py"

# Command with arguments
serve = "uvicorn src.app:app --reload --port 8000"

# Multi-line command (use array form)
setup = { cmd = "python -m pip install -e . && echo Done" }
```

### Task with Dependencies

```toml
[tasks]
# 'test' depends on 'lint' — lint runs first
lint = "ruff check src/"
test = { cmd = "pytest tests/", depends-on = ["lint"] }

# Chain multiple dependencies
build = { cmd = "python -m build", depends-on = ["lint", "test"] }
```

### Task with Working Directory

```toml
[tasks]
docs = { cmd = "mkdocs serve", cwd = "docs/" }
```

### Task with Environment Variables

```toml
[tasks]
dev-server = { cmd = "uvicorn app:app --reload", env = { DEBUG = "1", PORT = "8000" } }
```

### Task with Arguments (v0.65+)

Tasks can accept typed arguments with validation:

```toml
[tasks]
# Pass extra args after '--'
# Usage: pixi run greet -- --name Alice
greet = "python scripts/greet.py"

# Task with defined argument choices
deploy = { cmd = "python deploy.py", args = [{ name = "env", choices = ["staging", "production"] }] }
```

### Feature-Specific Tasks

```toml
[feature.test.tasks]
test     = "pytest tests/ -v"
coverage = "pytest --cov=src tests/"

[feature.lint.tasks]
lint   = "ruff check src/"
format = "ruff format src/ --fix"
```

### Running Tasks

```bash
# Run a task
pixi run start
pixi run test
pixi run lint

# Run a task in a specific environment
pixi run --environment dev test

# Run a raw command (not a defined task)
pixi run python --version
pixi run -- python -c "print('hello')"

# List all available tasks
pixi task list
```

### Adding/Removing Tasks via CLI

```bash
# Add a task
pixi task add start "python src/main.py"
pixi task add test "pytest tests/" --depends-on lint

# Remove a task
pixi task remove start

# Alias a task
pixi task alias t test
```

---

## 9. The Lock File

`pixi.lock` is automatically generated and should be **committed to version control**. It records the exact versions of every package (including transitive dependencies) for every platform and environment.

### What's in pixi.lock?

- Exact package versions and build strings
- Package hashes (SHA256) for security verification
- Platform-specific entries (linux-64, osx-arm64, win-64, etc.)
- Both conda and PyPI package entries
- Entries for every defined environment

### Lock File Commands

```bash
# Install from the lock file (no solving, fast)
pixi install --locked

# Update the lock file (re-solve all dependencies)
pixi update

# Update a specific package in the lock file
pixi update numpy

# Check if the lock file is up to date (useful in CI)
pixi install --locked --check
```

### Lock File in CI

Always use `--locked` in CI to ensure reproducibility:

```yaml
# GitHub Actions example
- name: Install dependencies
  run: pixi install --locked
```

---

## 10. Multi-Platform Support

Pixi is designed to work identically on Linux, macOS (Intel + Apple Silicon), and Windows.

### Declaring Platforms

```toml
[workspace]
channels   = ["conda-forge"]
platforms  = ["linux-64", "osx-arm64", "osx-64", "win-64"]
```

### Platform-Specific Dependencies

```toml
[dependencies]
python = ">=3.11"
numpy  = "*"

# Only on Linux
[target.linux-64.dependencies]
libc = ">=2.17"

# Only on macOS (Apple Silicon)
[target.osx-arm64.dependencies]
accelerate = "*"

# Only on Windows
[target.win-64.dependencies]
pywin32 = "*"
```

### Platform-Specific Tasks

```toml
[tasks]
build = "python -m build"

[target.win-64.tasks]
build = "python -m build --wheel"
```

### System Requirements

Declare minimum system-level requirements (e.g., glibc version, CUDA):

```toml
[system-requirements]
linux   = "4.18"    # Minimum Linux kernel version
libc    = { family = "glibc", version = "2.28" }
cuda    = "12.0"    # Minimum CUDA version
macos   = "13.0"    # Minimum macOS version
```

---

## 11. Multi-Environment Workflows

A common real-world Python project setup with multiple environments:

```toml
# pixi.toml — Full multi-environment Python project

[workspace]
name      = "my-data-science-project"
version   = "0.1.0"
channels  = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]

# ── Base dependencies (all environments) ────────────────────────────────────
[dependencies]
python  = "3.12.*"
numpy   = ">=1.26"
pandas  = ">=2.0"
scipy   = ">=1.12"

[pypi-dependencies]
my-data-science-project = { path = ".", editable = true }

# ── Feature: testing ────────────────────────────────────────────────────────
[feature.test.dependencies]
pytest       = ">=8.0"
pytest-cov   = "*"
pytest-xdist = "*"   # parallel test execution

[feature.test.tasks]
test     = "pytest tests/ -v"
test-par = "pytest tests/ -n auto"
coverage = "pytest --cov=src --cov-report=html tests/"

# ── Feature: linting / formatting ───────────────────────────────────────────
[feature.lint.dependencies]
ruff = ">=0.4"
mypy = "*"

[feature.lint.tasks]
lint      = "ruff check src/"
format    = "ruff format src/"
typecheck = "mypy src/"
check-all = { cmd = "echo All checks passed", depends-on = ["lint", "typecheck"] }

# ── Feature: Jupyter notebooks ──────────────────────────────────────────────
[feature.notebook.dependencies]
jupyterlab = ">=4.0"
ipywidgets = "*"
matplotlib = "*"
seaborn    = "*"

[feature.notebook.tasks]
notebook = "jupyter lab"

# ── Feature: GPU / deep learning ────────────────────────────────────────────
[feature.gpu.dependencies]
pytorch-gpu = { version = "*", channel = "pytorch" }
torchvision = { version = "*", channel = "pytorch" }

[feature.gpu.system-requirements]
cuda = "12.0"

# ── Environments ────────────────────────────────────────────────────────────
# Set "dev" as the default so bare `pixi run` / `pixi shell` targets it
[workspace]
default-environment = "dev"

[environments]
default  = { features = [],                              solve-group = "default" }
dev      = { features = ["test", "lint", "notebook"],    solve-group = "default" }
test     = { features = ["test"],                        solve-group = "default" }
notebook = { features = ["notebook"],                    solve-group = "default" }
gpu      = { features = ["gpu"],                         solve-group = "gpu" }
```

> **Note:** `[workspace]` must appear before `[environments]` in the file. The `default-environment` key tells Pixi which environment to activate when no `-e` flag is given.

### Using Multiple Environments

```bash
# Install all environments
pixi install

# ── With default-environment = "dev" set ────────────────────────────────────

# Run tests — no -e needed because "dev" includes the test feature
pixi run test

# Open a Jupyter notebook — also in "dev" (includes notebook feature)
pixi run notebook

# Run linting — also in "dev"
pixi run lint

# Drop into a shell — lands in "dev" automatically
pixi shell

# ── Explicitly target a non-default environment ──────────────────────────────

# Run tests in the lean CI environment (no notebook/lint overhead)
pixi run -e test test

# Open a Jupyter notebook in the isolated notebook environment
pixi run -e notebook notebook

# Open a shell in the GPU environment
pixi shell -e gpu
```

#### When to Use `-e` vs. Relying on `default-environment`

| Scenario | Recommendation |
|----------|---------------|
| Day-to-day development | Set `default-environment = "dev"`, use bare `pixi run` |
| CI pipeline (lean, fast) | Always pass `-e test` explicitly for reproducibility |
| Multiple devs with different needs | Each can override locally; CI always pins with `-e` |
| Shared feature used by many envs | Put it in a feature, include in `dev`, set as default |

---

## 12. Global Tools

Pixi can install tools globally (system-wide), replacing `brew`, `apt`, `winget`, etc. for developer tools.

### Installing Global Tools

```bash
# Install one or more tools globally
pixi global install ripgrep
pixi global install gh nvim ipython btop

# Install a specific version
pixi global install "python==3.12.*"

# Install from a specific channel
pixi global install pytorch --channel pytorch

# Install from a git repository (v0.65+)
pixi global install --git https://github.com/prefix-dev/rattler-build
```

### Managing Global Tools

```bash
# List installed global tools
pixi global list
pixi global list --json

# Update a global tool
pixi global update ripgrep

# Update all global tools
pixi global update

# Remove a global tool
pixi global remove ripgrep

# Sync global tools from the global manifest
pixi global sync
```

### The Global Manifest

Global tools are managed via `~/.pixi/manifests/pixi-global.toml`:

```toml
[envs.my-python-tools]
channels = ["conda-forge"]
dependencies = { python = "3.12.*", ipython = "*", black = "*" }
exposed = { ipython = "ipython", black = "black" }

[envs.rust-tools]
channels = ["conda-forge"]
dependencies = { rust = "*", cargo-edit = "*" }
exposed = { cargo = "cargo", rustc = "rustc" }
```

---

## 13. Build Backends (pixi build)

`pixi build` is a **preview feature** (opt-in) that lets you build your project into a conda package (`.conda` artifact). It uses a modular backend system inspired by Python's PEP 517/518.

> ⚠️ **Preview Feature**: You must opt in by adding `"pixi-build"` to `workspace.preview`.

### Enabling pixi build

```toml
[workspace]
channels = ["conda-forge"]
preview   = ["pixi-build"]   # ← required to enable pixi build
```

### The Build Command

```bash
# Build the current package
pixi build

# Build and output to a specific directory
pixi build --output-dir dist/

# Build for a specific platform
pixi build --target-platform linux-64
```

### Available Build Backends

| Backend | Use Case |
|---------|----------|
| `pixi-build-python` | Python packages (hatchling, setuptools, meson-python, etc.) |
| `pixi-build-cmake` | C/C++ projects using CMake |
| `pixi-build-rattler-build` | Direct `recipe.yaml` builds (full control) |
| `pixi-build-ros` | ROS (Robot Operating System) packages |
| `pixi-build-r` | R packages using `R CMD INSTALL` |
| `pixi-build-rust` | Cargo-based Rust applications |
| `pixi-build-mojo` | Mojo applications and packages |

All backends are available on `conda-forge`. For the latest versions, prepend `https://prefix.dev/pixi-build-backends` to your channels.

### How Build Backends Work

Build backends are executables that communicate with Pixi via **JSON-RPC**. When you run `pixi build`:

1. Pixi reads your `[package.build]` section
2. It installs the specified backend from conda channels
3. The backend generates a `rattler-build` recipe from your project model
4. `rattler-build` compiles/packages your project
5. A `.conda` artifact is produced

You can inspect the generated recipe at:
```
.pixi/build/work/<package-name>--<hash>/debug/recipe.yaml
```

### Overriding Build Backends (for development)

```bash
# Override a specific backend with a local binary
export PIXI_BUILD_BACKEND_OVERRIDE="pixi-build-python=/path/to/my/backend"

# Override all backends (use PATH)
export PIXI_BUILD_BACKEND_OVERRIDE_ALL=1
```

---

## 14. The Python Build Backend (pixi-build-python)

`pixi-build-python` is the most important backend for Python developers. It builds Python packages into conda packages using standard Python packaging tools.

### What It Supports

- **PEP 517 / PEP 518** compliant projects
- Any Python build backend: `hatchling`, `setuptools`, `flit`, `meson-python`, `maturin` (Rust+Python), `pdm-backend`, `uv-build`
- Automatic detection of the build backend from `[build-system]` in `pyproject.toml`
- Automatic Rust compiler setup when `maturin` is detected

### Basic Setup

```toml
# pixi.toml

[workspace]
name     = "my-python-lib"
channels = ["conda-forge"]
preview  = ["pixi-build"]

[package]
name    = "my-python-lib"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-python", version = "0.4.*" }
channels = [
    "https://prefix.dev/pixi-build-backends",
    "https://prefix.dev/conda-forge",
]
```

Or in `pyproject.toml`:

```toml
[project]
name            = "my-python-lib"
version         = "0.1.0"
requires-python = ">=3.11"
dependencies    = ["numpy>=1.26", "pandas>=2.0"]

[build-system]
requires      = ["hatchling"]
build-backend = "hatchling.build"

[tool.pixi.workspace]
channels = ["conda-forge"]
preview  = ["pixi-build"]

[tool.pixi.package.build]
backend  = { name = "pixi-build-python", version = "0.4.*" }
channels = [
    "https://prefix.dev/pixi-build-backends",
    "https://prefix.dev/conda-forge",
]
```

### Configuration Options

```toml
[package.build]
backend = { name = "pixi-build-python", version = "0.4.*" }

[package.build.config]
# Whether to map PyPI dependencies to conda packages
# Set to false to keep PyPI deps as PyPI deps in the conda package
ignore-pypi-mapping = false

# Extra glob patterns to watch for changes (triggers rebuild)
extra-input-globs = ["data/**/*", "templates/**/*.html"]

# Environment variables during build
env = { MY_BUILD_FLAG = "1" }
```

### Supported Python Build Backends

#### Hatchling (Recommended)

```toml
[build-system]
requires      = ["hatchling"]
build-backend = "hatchling.build"
```

Hatchling is the default when you run `pixi init --format pyproject`. It's modern, fast, and has excellent defaults.

```toml
# Optional hatchling configuration
[tool.hatch.version]
path = "src/my_package/__init__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

#### Setuptools

```toml
[build-system]
requires      = ["setuptools>=77.0", "wheel"]
build-backend = "setuptools.build_meta"
```

```toml
# setuptools configuration
[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
"*" = ["*.yaml", "*.json"]
```

#### Flit

```toml
[build-system]
requires      = ["flit_core>=3.12,<4"]
build-backend = "flit_core.buildapi"
```

Flit is minimal and great for pure-Python packages with no complex build steps.

#### Meson-Python (for C extensions)

```toml
[build-system]
requires      = ["meson-python", "ninja"]
build-backend = "mesonpy"
```

Meson-python is used by NumPy, SciPy, and other scientific packages with C/Fortran extensions.

#### Maturin (Rust + Python)

```toml
[build-system]
requires      = ["maturin>=1.0,<2.0"]
build-backend = "maturin"
```

When `pixi-build-python` detects `maturin`, it **automatically sets up a Rust compiler** from conda-forge. No manual compiler configuration needed.

```toml
# Cargo.toml (for the Rust extension)
[lib]
name = "my_rust_ext"
crate-type = ["cdylib"]

[dependencies]
pyo3 = { version = "0.21", features = ["extension-module"] }
```

#### PDM Backend

```toml
[build-system]
requires      = ["pdm-backend>=2.4"]
build-backend = "pdm.backend"
```

#### uv-build

```toml
[build-system]
requires      = ["uv_build>=0.10"]
build-backend = "uv_build"
```

### Building from Remote Source

You can build a Python package directly from a git repository:

```toml
[package.build.source]
git    = "https://github.com/astral-sh/ruff.git"
branch = "main"

[package.build]
backend = { name = "pixi-build-python", version = "0.4.*" }
```

Or from a URL:

```toml
[package.build.source]
url = "https://github.com/user/repo/archive/refs/tags/v1.0.0.tar.gz"
```

### Package Dependencies

```toml
# Runtime dependencies (installed with the package)
[package.dependencies]
python = ">=3.11"
numpy  = ">=1.26"

# Build-time dependencies (only needed during build)
[package.build-dependencies]
hatchling = "*"
cython    = ">=3.0"

# Host dependencies (available during build, linked into the package)
[package.host-dependencies]
python = ">=3.11"
pip    = "*"
```

### Full Python Package Example

Here is a complete, real-world `pyproject.toml` for a Python library that can be built as a conda package:

```toml
[project]
name            = "mylib"
version         = "0.2.0"
description     = "A high-performance data processing library"
readme          = "README.md"
license         = { text = "MIT" }
requires-python = ">=3.11"
authors         = [{ name = "Alice", email = "alice@example.com" }]
keywords        = ["data", "processing", "science"]
classifiers     = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "numpy>=1.26",
    "pandas>=2.0",
    "scipy>=1.12",
]

[project.optional-dependencies]
viz  = ["matplotlib>=3.8", "seaborn>=0.13"]
test = ["pytest>=8.0", "pytest-cov", "hypothesis"]

[project.scripts]
mylib-cli = "mylib.cli:main"

[project.urls]
Homepage   = "https://github.com/alice/mylib"
Repository = "https://github.com/alice/mylib"

[build-system]
requires      = ["hatchling>=1.26"]
build-backend = "hatchling.build"

[tool.hatch.version]
path = "src/mylib/__init__.py"

[tool.hatch.build.targets.wheel]
packages = ["src/mylib"]

# ── Pixi workspace configuration ────────────────────────────────────────────
[tool.pixi.workspace]
channels  = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "osx-64", "win-64"]
preview   = ["pixi-build"]

# ── Pixi package build configuration ────────────────────────────────────────
[tool.pixi.package.build]
backend  = { name = "pixi-build-python", version = "0.4.*" }
channels = [
    "https://prefix.dev/pixi-build-backends",
    "https://prefix.dev/conda-forge",
]

[tool.pixi.package.build.config]
ignore-pypi-mapping = false

# ── Development environment ──────────────────────────────────────────────────
[tool.pixi.pypi-dependencies]
mylib = { path = ".", editable = true }

[tool.pixi.dependencies]
python = "3.12.*"
numpy  = ">=1.26"
pandas = ">=2.0"
scipy  = ">=1.12"

[tool.pixi.feature.test.dependencies]
pytest       = ">=8.0"
pytest-cov   = "*"
pytest-xdist = "*"
hypothesis   = "*"

[tool.pixi.feature.test.tasks]
test     = "pytest tests/ -v"
coverage = "pytest --cov=src --cov-report=html tests/"

[tool.pixi.feature.lint.dependencies]
ruff = ">=0.4"
mypy = "*"

[tool.pixi.feature.lint.tasks]
lint      = "ruff check src/"
format    = "ruff format src/ --fix"
typecheck = "mypy src/"

[tool.pixi.feature.viz.dependencies]
matplotlib = ">=3.8"
seaborn    = ">=0.13"

[tool.pixi.tasks]
build = "pixi build"

[tool.pixi.environments]
default = { features = [], solve-group = "default" }
dev     = { features = ["test", "lint", "viz"], solve-group = "default" }
test    = { features = ["test"], solve-group = "default" }
```

---

## 15. Other Build Backends

### pixi-build-cmake (C/C++)

```toml
[workspace]
channels = ["conda-forge"]
preview  = ["pixi-build"]

[package]
name    = "my-cpp-lib"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-cmake", version = "*" }
channels = ["https://prefix.dev/conda-forge"]

[package.build.config]
# Extra CMake arguments
extra-args = ["-DCMAKE_BUILD_TYPE=Release", "-DENABLE_TESTS=ON"]

# Environment variables during build
env = { CMAKE_VERBOSE_MAKEFILE = "ON" }

# Compilers to use (default: ["cxx"])
compilers = ["c", "cxx"]

[package.host-dependencies]
sdl2   = ">=2.26"
opengl = "*"
```

The CMake backend automatically:
- Detects and configures platform-appropriate compilers (GCC on Linux, Clang on macOS, MSVC on Windows)
- Uses Ninja as the build system
- Handles cross-platform compiler flags

### pixi-build-rattler-build (Full Control)

For maximum control, use `pixi-build-rattler-build` with a `recipe.yaml`:

```toml
[package.build]
backend = { name = "pixi-build-rattler-build", version = "*" }
```

```yaml
# recipe.yaml
package:
  name: my-package
  version: 1.0.0

source:
  path: .

build:
  script:
    - python -m pip install . --no-deps -vv

requirements:
  host:
    - python >=3.11
    - pip
  run:
    - python >=3.11
    - numpy >=1.26
```

### pixi-build-rust

```toml
[workspace]
channels = ["conda-forge"]
preview  = ["pixi-build"]

[package]
name    = "my-rust-tool"
version = "0.1.0"

[package.build]
backend = { name = "pixi-build-rust", version = "*" }
channels = ["https://prefix.dev/conda-forge"]
```

The Rust backend automatically installs the Rust toolchain from conda-forge.

### pixi-build-r

```toml
[package.build]
backend = { name = "pixi-build-r", version = "*" }
channels = ["https://prefix.dev/conda-forge"]
```

Builds R packages using `R CMD INSTALL`.

### pixi-build-mojo

```toml
[package.build]
backend = { name = "pixi-build-mojo", version = "*" }
channels = [
    "https://conda.modular.com/max",
    "https://prefix.dev/conda-forge",
]
```

### pixi-build-ros

```toml
[workspace]
channels = [
    "https://prefix.dev/pixi-build-backends",
    "https://prefix.dev/robostack-jazzy",
    "https://prefix.dev/conda-forge",
]
preview = ["pixi-build"]

[package.build]
backend = { name = "pixi-build-ros", version = "*" }

[package.build.config]
distro = "jazzy"  # or "humble", "noetic", etc.
```

---

## 16. Distributing Your Project

### Publishing to a Conda Channel (prefix.dev)

```bash
# Build the conda package
pixi build

# Upload to your prefix.dev channel
rattler-build upload prefix --channel my-channel dist/*.conda
```

### Publishing to PyPI

Since `pyproject.toml` is standard Python packaging, you can publish to PyPI normally:

```bash
# Build wheel and sdist
pixi run python -m build

# Upload to PyPI
pixi run twine upload dist/*
```

Or add it as a task:

```toml
[tasks]
build-pypi = "python -m build"
publish    = { cmd = "twine upload dist/*", depends-on = ["build-pypi"] }
```

### Pixi Pack (Offline Distribution)

`pixi-pack` bundles your entire environment into a single archive for offline deployment:

```bash
# Install pixi-pack
pixi global install pixi-pack

# Pack the default environment
pixi-pack pack --manifest pixi.toml --environment default

# Unpack on the target machine (no internet required)
pixi-pack unpack environment.tar
```

### Container / Docker

```dockerfile
FROM ghcr.io/prefix-dev/pixi:0.65.0 AS build

WORKDIR /app
COPY pixi.toml pixi.lock ./
COPY src/ src/

RUN pixi install --locked

FROM ubuntu:22.04
COPY --from=build /app/.pixi/envs/default /app/.pixi/envs/default
COPY --from=build /app/src /app/src

ENV PATH="/app/.pixi/envs/default/bin:$PATH"
CMD ["python", "/app/src/main.py"]
```

---

## 17. CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Pixi
        uses: prefix-dev/setup-pixi@v0.8.0
        with:
          pixi-version: v0.65.0
          cache: true
          locked: true

      - name: Run tests
        run: pixi run --environment test test

      - name: Run linting
        run: pixi run --environment dev lint
```

### GitHub Actions — Multiple Environments

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [test, lint]
    steps:
      - uses: actions/checkout@v4
      - uses: prefix-dev/setup-pixi@v0.8.0
        with:
          environments: ${{ matrix.environment }}
      - run: pixi run --environment ${{ matrix.environment }} ${{ matrix.environment }}
```

### Caching in CI

The `setup-pixi` action automatically caches the Pixi environment based on the lock file hash. You can also manually cache:

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.pixi
      .pixi
    key: pixi-${{ runner.os }}-${{ hashFiles('pixi.lock') }}
```

---

## 18. Advanced Features


### Security Hardening: `exclude-newer`

Pixi (via its `uv` integration for PyPI) supports the `exclude-newer` field. This is a critical feature for **security hardening**, **reproducible builds**, and **package cooldown periods**.

#### What is `exclude-newer`?

It tells the resolver to ignore any PyPI packages published *after* a specific UTC timestamp. This is useful for:
- **Reproducibility:** Ensuring that a "fresh" install today results in the same versions as an install from a month ago, even without a lockfile.
- **Supply Chain Security:** Preventing "dependency confusion" or "malicious release" attacks where an attacker pushes a compromised version of a popular package.
- **Cooldown Periods:** Giving the community time to find bugs in new releases before your project automatically adopts them.

#### How to use it in `pixi.toml` / `pyproject.toml`:

```toml
[workspace]
name = "secure-project"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64"]

[pypi-options]
# Only consider PyPI packages published before 2024-05-01
exclude-newer = "2024-05-01T00:00:00Z"
```

#### Real-world Hardening Strategy

A robust security strategy involves keeping this date slightly behind current time (e.g., "now minus 7 days"). This ensures you are never the "first mover" on a new, unvetted package version.

---



### Workspace Registration (v0.66+)

Register your workspace so you can reference it by name from anywhere:

```bash
cd /path/to/my/project
pixi workspace register

# Now use it from anywhere
pixi run --workspace my-project test
pixi shell -w my-project
```

### Shebang Scripts

You can use Pixi environments in shebang scripts:

```python
#!/usr/bin/env -S pixi exec --spec "python>=3.11" --spec "requests>=2.31" python

import requests
response = requests.get("https://api.github.com")
print(response.status_code)
```

```bash
chmod +x my_script.py
./my_script.py
```

### Dependency Overrides

Force a specific version of a transitive dependency:

```toml
[dependency-overrides]
# Force all environments to use this exact version
openssl = "3.3.*"
```

### Channel Priority and Logic

Channels are searched in order. The first channel that has a matching package wins:

```toml
[workspace]
channels = [
    "pytorch",          # searched first
    "nvidia",           # searched second
    "conda-forge",      # searched last (fallback)
]
```

You can also use full URLs:

```toml
channels = [
    "https://prefix.dev/conda-forge",
    "https://prefix.dev/my-private-channel",
]
```

### Authentication for Private Channels

```bash
# Set credentials for a private channel
pixi auth login https://my-private-channel.example.com --username user --password pass

# Or use a token
pixi auth login https://prefix.dev --token my-api-token
```

### Direnv Integration

Create a `.envrc` file to automatically activate the Pixi environment when you `cd` into the project:

```bash
# .envrc
eval "$(pixi shell-hook)"
```

```bash
direnv allow
```

### Starship Prompt Integration

Add to your Starship config (`~/.config/starship.toml`):

```toml
[custom.pixi]
command = "pixi info --json | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d.get('project_info',{}).get('name',''))\""
when = "test -f pixi.toml || test -f pyproject.toml"
symbol = "🧩 "
```

### VSCode Integration

Install the [Pixi VSCode extension](https://marketplace.visualstudio.com/items?itemName=prefix-dev.pixi-vscode) for:
- Environment activation
- Task running from the UI
- Manifest file syntax highlighting

Add to `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.pixi/envs/default/bin/python",
    "python.terminal.activateEnvironment": false
}
```

### JetBrains Integration

In PyCharm/IntelliJ, set the Python interpreter to:
```
<project>/.pixi/envs/default/bin/python
```

---

## 19. Configuration Reference

### Global Pixi Configuration

Located at `~/.pixi/config.toml` (or `$PIXI_HOME/config.toml`):

```toml
# Default channels for all new projects
default-channels = ["conda-forge"]

# Default platforms
default-platforms = ["linux-64", "osx-arm64", "win-64"]

# Cache directory
cache-dir = "~/.pixi/cache"

# Concurrent downloads
concurrent-downloads = 50

# Concurrent solves
concurrent-solves = 8

# TLS verification
tls-no-verify = false

# Detached environments (store envs outside project)
detached-environments = false

# Shell hook on pixi shell
shell-hook = "bash"
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PIXI_HOME` | Override Pixi home directory (default: `~/.pixi`) |
| `PIXI_CACHE_DIR` | Override cache directory |
| `PIXI_NO_PATH_UPDATE` | Don't update PATH during install |
| `PIXI_COLOR` | Force color output (`always`, `never`, `auto`) |
| `PIXI_FROZEN` | Equivalent to `--frozen` flag |
| `PIXI_LOCKED` | Equivalent to `--locked` flag |
| `PIXI_BUILD_BACKEND_OVERRIDE` | Override build backend binary |
| `PIXI_BUILD_BACKEND_OVERRIDE_ALL` | Use all backends from PATH |
| `CONDA_OVERRIDE_CUDA` | Override detected CUDA version |

---

## 20. CLI Reference

### Project Commands

```bash
pixi init [path]                    # Initialize a new workspace
pixi init --format pyproject        # Initialize with pyproject.toml
pixi init -c conda-forge -c pytorch # Initialize with specific channels

pixi install                        # Install all environments
pixi install --locked               # Install from lock file (no solving)
pixi install --frozen               # Install without updating lock file
pixi install --environment dev      # Install specific environment

pixi add <package>                  # Add a conda dependency
pixi add --pypi <package>           # Add a PyPI dependency
pixi add --feature dev <package>    # Add to a feature
pixi add --environment test <pkg>   # Add to an environment

pixi remove <package>               # Remove a dependency
pixi update [package]               # Update dependencies

pixi run <task-or-command>          # Run a task or command
pixi run --environment dev test     # Run in specific environment
pixi run -- python script.py        # Run raw command

pixi shell                          # Open a shell in the environment
pixi shell --environment dev        # Open shell in specific environment
pixi shell-hook                     # Print shell activation script

pixi list                           # List installed packages
pixi list --environment dev         # List in specific environment
pixi list --json                    # JSON output

pixi search <package>               # Search for packages
pixi search --json <package>        # JSON output

pixi info                           # Show workspace info
pixi info --json                    # JSON output

pixi clean                          # Remove all environments
pixi clean --environment dev        # Remove specific environment
```

### Task Commands

```bash
pixi task add <name> <cmd>          # Add a task
pixi task remove <name>             # Remove a task
pixi task alias <alias> <task>      # Create a task alias
pixi task list                      # List all tasks
```

### Global Commands

```bash
pixi global install <package>       # Install a global tool
pixi global remove <package>        # Remove a global tool
pixi global update [package]        # Update global tools
pixi global list                    # List global tools
pixi global list --json             # JSON output
pixi global sync                    # Sync from global manifest
```

### Build Commands

```bash
pixi build                          # Build the package
pixi build --output-dir dist/       # Specify output directory
```

### Workspace Commands (v0.66+)

```bash
pixi workspace register             # Register current workspace
pixi workspace list                 # List registered workspaces
```

### Utility Commands

```bash
pixi self-update                    # Update Pixi itself
pixi completion --shell bash        # Generate shell completions
pixi auth login <url>               # Authenticate with a channel
pixi auth logout <url>              # Remove authentication
pixi upload <channel> <file>        # Upload a package to a channel
```

---

## 21. Tips, Tricks & Best Practices

### Always Commit pixi.lock

```bash
# .gitignore — do NOT ignore pixi.lock
# pixi.lock  ← don't add this!

# DO commit:
git add pixi.toml pixi.lock
```

### Use --locked in CI

```bash
pixi install --locked  # Ensures exact reproducibility
```

### Prefer Conda Packages Over PyPI When Available

Conda packages from conda-forge often include compiled binaries and system dependencies. For scientific computing, always prefer conda:

```toml
# Prefer this (conda):
[dependencies]
numpy  = "*"
scipy  = "*"
pandas = "*"

# Over this (PyPI) for scientific packages:
[pypi-dependencies]
# numpy = "*"  ← avoid for packages available on conda-forge
```

### Use solve-group for Consistent Environments

```toml
[environments]
# All in the same solve group = compatible versions guaranteed
default = { features = [],       solve-group = "default" }
dev     = { features = ["dev"],  solve-group = "default" }
test    = { features = ["test"], solve-group = "default" }
```

### Set default-environment for Frictionless Developer Experience

When your project has more than one environment, always set `default-environment` so developers never have to remember `-e`:

```toml
[workspace]
name                = "my-project"
channels            = ["conda-forge"]
platforms           = ["linux-64", "osx-arm64", "win-64"]
default-environment = "dev"   # ← the magic line

[environments]
default = { features = ["base"],                    solve-group = "default" }
dev     = { features = ["base", "test", "lint"],    solve-group = "default" }
test    = { features = ["base", "test"],             solve-group = "default" }
docs    = { features = ["base", "docs"] }
```

```bash
# Developer — no flags needed
pixi run test        # runs pytest in "dev"
pixi run lint        # runs ruff in "dev"
pixi shell           # opens "dev" shell

# CI — explicit for reproducibility
pixi run -e test test
pixi run -e docs build-docs
```

**Rule of thumb:** `default-environment` should be the environment that contains the *union* of all features a developer needs day-to-day. Lean, single-purpose environments (like `test` or `docs`) are for CI and automation — always target them explicitly with `-e`.

### Pin Python Version Precisely

```toml
[dependencies]
# Use wildcard for patch versions, pin major.minor
python = "3.12.*"
```

### Use Editable Installs for Development

```toml
[pypi-dependencies]
my-package = { path = ".", editable = true }
```

This lets you edit source code and see changes immediately without reinstalling.

### Organize Large Projects with Features

Instead of one giant environment, use features to compose targeted environments. Then set `default-environment` to the richest one so developers don't need `-e` for everyday work:

```toml
[workspace]
default-environment = "all"   # developers get everything by default

[feature.test.dependencies]
pytest = "*"

[feature.gpu.dependencies]
pytorch-gpu = "*"

[environments]
test    = { features = ["test"] }          # lean CI environment
gpu     = { features = ["gpu"] }           # GPU-only environment
all     = { features = ["test", "gpu"] }   # default for developers
```

```bash
# Developer workflow — no -e needed
pixi run pytest          # runs in "all" (has pytest)
pixi run train-model     # runs in "all" (has pytorch-gpu)

# CI workflow — explicit environment
pixi run -e test pytest  # lean, no GPU packages
```

### Use pixi run for All Commands

Even for simple commands, use `pixi run` to ensure you're always in the right environment:

```bash
# Instead of:
source .pixi/envs/default/bin/activate && python script.py

# Use:
pixi run python script.py
```

### Inspect the Environment

```bash
# See what's installed and where
pixi info

# See all packages with versions
pixi list

# See the resolved environment
pixi run -- python -c "import sys; print(sys.prefix)"
```

### Debug Build Issues

```bash
# Inspect the generated rattler-build recipe
cat .pixi/build/work/<package>--<hash>/debug/recipe.yaml

# Rebuild with rattler-build directly
rattler-build build --recipe .pixi/build/work/<package>--<hash>/debug/recipe/<hash>/
```

### Speed Up CI with Caching

```yaml
- uses: prefix-dev/setup-pixi@v0.8.0
  with:
    cache: true           # Cache based on pixi.lock hash
    locked: true          # Use lock file
    frozen: false
```

### Use pixi global for Developer Tools

Instead of installing tools in your project environment, install them globally:

```bash
pixi global install gh ripgrep fd bat delta lazygit
```

This keeps your project environments lean and focused.

---

## Quick Reference Card

```
# Initialize
pixi init my-project --format pyproject

# Add dependencies
pixi add numpy pandas                    # conda
pixi add --pypi requests fastapi         # PyPI
pixi add --feature dev pytest ruff       # dev feature

# Run
pixi run python script.py
pixi run test
pixi run --environment dev lint

# Shell
pixi shell
pixi shell --environment dev

# List / Search
pixi list
pixi search numpy

# Update
pixi update numpy
pixi update

# Build (preview)
pixi build

# Global tools
pixi global install ripgrep gh
```

---

*This guide covers Pixi v0.65.0+. For the latest documentation, visit [pixi.sh](https://pixi.sh) or the [GitHub repository](https://github.com/prefix-dev/pixi).*
