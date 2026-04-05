# 🌱 Spec-Kit: The Complete Guide
### From Novice to Professional — with Pixi & Python Examples

> **spec-kit** is GitHub's open-source toolkit for **Spec-Driven Development (SDD)** — a methodology where specifications, not code, are the primary artifact. AI agents generate, test, and validate code from your specs. The result: less guesswork, fewer surprises, higher-quality software.
>
> 📦 [GitHub Repo](https://github.com/github/spec-kit) · 📖 [Official Docs](https://speckit.org/) · 📝 [SDD Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)

---

## Table of Contents

1. [What is Spec-Driven Development?](#1-what-is-spec-driven-development)
2. [Installation & Setup](#2-installation--setup)
3. [The Core Workflow (4 Phases)](#3-the-core-workflow-4-phases)
4. [Level 1 — Novice: Your First Spec](#4-level-1--novice-your-first-spec)
5. [Level 2 — Intermediate: Planning & Tasks](#5-level-2--intermediate-planning--tasks)
6. [Level 3 — Advanced: Constitution & Extensions](#6-level-3--advanced-constitution--extensions)
7. [Level 4 — Professional: Multi-Agent Orchestration](#7-level-4--professional-multi-agent-orchestration)
8. [Pixi + Python Project Examples](#8-pixi--python-project-examples)
9. [Cheatsheet](#9-cheatsheet)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. What is Spec-Driven Development?

Traditional development treats code as the source of truth. Specs are written, then discarded. SDD **inverts this**:

```
Traditional:  Idea → Spec (discarded) → Code (source of truth)
SDD:          Idea → Spec (source of truth) → Code (generated output)
```

### Why it matters for AI-assisted development

When you "vibe code" with an AI agent — describe a goal and get code back — the result often looks right but doesn't quite work. The problem isn't the AI's ability; it's the lack of structure. Spec-kit provides that structure:

- **Specs** define *what* and *why*
- **Plans** define *how* (tech stack, architecture)
- **Tasks** define *what to build next* (small, testable chunks)
- **AI agents** implement each task, validated against the spec

### The SDD Mindset

| Old Mindset | SDD Mindset |
|---|---|
| Write code, document later | Write spec, generate code |
| AI as a search engine | AI as a literal-minded pair programmer |
| Specs are scaffolding | Specs are living artifacts |
| Debug the code | Debug the specification |
| Refactor code | Refactor the spec |

---

## 2. Installation & Setup

### Prerequisites

- Python 3.8+
- Git 2.20+
- `uv` package manager (recommended)
- An AI agent: Claude Code, GitHub Copilot, Cursor, Gemini CLI, Windsurf, etc.

### Install `uv` (if not already installed)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install the `specify` CLI

```bash
# Recommended: persistent installation (pinned to latest stable release)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Verify installation
specify --version
specify check
```

### One-time usage (no install)

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init my-project --ai claude
```

### Upgrading

```bash
uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

### Initialize a project

```bash
# New project
specify init my-pixi-project --ai claude

# Existing project (run from inside the project directory)
specify init . --ai claude
# or
specify init --here --ai copilot

# Skip git init (if already a git repo)
specify init . --ai claude --no-git
```

### Supported AI Agents

| Agent | Support Level |
|---|---|
| Claude Code | ✅ Full |
| GitHub Copilot | ✅ Full |
| Cursor | ✅ Full |
| Gemini CLI | ✅ Full |
| Windsurf | ✅ Full |
| Codex CLI | ⚠️ Limited (no custom slash command args) |
| Qwen Code, Roo Code, Kilo Code, Auggie CLI, opencode | ✅ Full |

---

## 3. The Core Workflow (4 Phases)

```
┌─────────────────────────────────────────────────────────────────┐
│                     SPEC-KIT WORKFLOW                           │
│                                                                 │
│  [Constitution]  →  [Specify]  →  [Plan]  →  [Tasks]  →  [Implement] │
│       ↑                ↑            ↑           ↑          ↑    │
│  Project rules    What & Why    How & Stack  Breakdown   Build  │
└─────────────────────────────────────────────────────────────────┘
```

### Phase Overview

| Phase | Command | Purpose | Your Role |
|---|---|---|---|
| **Constitution** | `/speckit.constitution` | Establish immutable project principles | Define standards, constraints, quality bars |
| **Specify** | `/speckit.specify` | Describe what to build (user journeys, outcomes) | Focus on *what* and *why*, not tech |
| **Clarify** | `/speckit.clarify` | Resolve ambiguities before planning | Answer AI's targeted questions |
| **Plan** | `/speckit.plan` | Generate technical implementation plan | Provide stack, architecture, constraints |
| **Tasks** | `/speckit.tasks` | Break plan into small, testable tasks | Review and approve task list |
| **Analyze** | `/speckit.analyze` | Cross-artifact consistency check | Validate before implementing |
| **Implement** | `/speckit.implement` | Execute tasks, generate working code | Review focused changes |

> **Key rule:** Do not move to the next phase until the current one is fully validated. Your role is to **steer and verify**, not just accept.

---

## 4. Level 1 — Novice: Your First Spec

### Goal: Understand the basic loop

At this level, you'll learn to initialize a project and run your first `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement` cycle.

### Step 1: Set up a Pixi Python project

```bash
# Install pixi
curl -fsSL https://pixi.sh/install.sh | bash

# Create a new pixi project
pixi init my-data-tool
cd my-data-tool

# Add Python and basic dependencies
pixi add python pytest

# Initialize spec-kit inside the pixi project
specify init . --ai claude
```

### Step 2: Create your first specification

Open your AI agent (e.g., Claude Code) in the project directory and run:

```
/speckit.specify Build a CSV file analyzer that reads a CSV file from the command line,
prints summary statistics (row count, column names, data types, null counts),
and outputs a simple text report. Users are data analysts who need quick insights
without opening a spreadsheet.
```

The AI will generate a `specs/001-csv-analyzer/spec.md` file with:
- User stories
- Acceptance criteria
- Edge cases
- Success metrics

**Your job:** Read it. Does it capture what you actually want? Edit it if not.

### Step 3: Create the technical plan

```
/speckit.plan Use Python with pandas and rich for terminal output.
No external API calls. All processing is local. Output should be
colorized and readable in a standard terminal.
```

This generates `specs/001-csv-analyzer/plan.md` with architecture decisions, data flow, and library choices.

### Step 4: Generate tasks

```
/speckit.tasks
```

This creates `specs/001-csv-analyzer/tasks.md` — a list of small, independently testable tasks like:
- `[T001]` Set up CLI argument parsing with argparse
- `[T002]` Implement CSV loading with error handling
- `[T003]` Compute summary statistics per column
- `[T004]` Render output with rich tables
- `[T005]` Write pytest tests for each function

### Step 5: Implement

```
/speckit.implement
```

The AI works through each task, generating code and tests. You review focused, small changes — not a 500-line dump.

### What you'll have after Level 1

```
my-data-tool/
├── pixi.toml
├── specs/
│   └── 001-csv-analyzer/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── src/
│   └── csv_analyzer.py
└── tests/
    └── test_csv_analyzer.py
```

---

## 5. Level 2 — Intermediate: Planning & Tasks

### Goal: Write better specs and control the planning phase

At this level, you'll learn to write richer specifications, use `/speckit.clarify`, and understand how to guide the planning phase with real constraints.

### Writing a Better Specification

A weak spec:
```
/speckit.specify Build a web scraper
```

A strong spec:
```
/speckit.specify Build a price monitoring tool that scrapes product prices
from e-commerce pages on a schedule. Users are small business owners who
want to track competitor pricing without manual checking. The tool should:
- Accept a list of URLs and CSS selectors via a config file
- Run on a configurable schedule (hourly, daily)
- Store historical price data
- Alert the user via terminal output when a price drops by more than X%
- Never require a browser or GUI to operate
```

**Rule of thumb:** The more specific your first prompt, the better the spec the AI generates.

### Using `/speckit.clarify`

After `/speckit.specify`, always run:

```
/speckit.clarify
```

The AI will ask targeted questions like:
- "Should the tool handle JavaScript-rendered pages?"
- "What format should the config file use (YAML, TOML, JSON)?"
- "Should alerts be stored or only shown in real-time?"

Answer these before moving to `/speckit.plan`. This prevents costly rework later.

### Pixi-Specific Planning Example

```
/speckit.plan
- Package manager: pixi (pixi.toml, not requirements.txt or pyproject.toml)
- Python version: 3.11 via pixi
- Dependencies: httpx for HTTP, beautifulsoup4 for parsing,
  apscheduler for scheduling, sqlite3 (stdlib) for storage
- Testing: pytest with pytest-asyncio
- No Docker. Runs as a local pixi task.
- Add pixi tasks for: run, test, lint
```

### Adding Pixi Tasks to the Plan

Instruct the AI to include pixi task definitions in the plan:

```
/speckit.plan
...also generate pixi task definitions for:
- `pixi run test` → runs pytest
- `pixi run lint` → runs ruff
- `pixi run start` → runs the main script
```

The resulting `pixi.toml` will include:

```toml
[project]
name = "price-monitor"
version = "0.1.0"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "win-64"]

[dependencies]
python = ">=3.11"
httpx = "*"
beautifulsoup4 = "*"
apscheduler = "*"
pytest = "*"
pytest-asyncio = "*"
ruff = "*"

[tasks]
test = "pytest tests/"
lint = "ruff check src/"
start = "python src/main.py"
```

### Understanding the Task File

After `/speckit.tasks`, review `tasks.md` carefully. Look for:

- **`[P]` markers** — tasks that can run in parallel
- **Dependencies** — tasks that must complete before others
- **Test tasks** — every implementation task should have a corresponding test task

Example task structure:
```markdown
## Tasks

### Group 1 (Foundation)
- [T001] Create pixi.toml with all dependencies
- [T002] Implement config file loader (TOML format) [P]
- [T003] Implement URL fetcher with httpx [P]

### Group 2 (Core Logic — depends on Group 1)
- [T004] Implement price extractor with BeautifulSoup
- [T005] Implement SQLite storage layer
- [T006] Write tests for T002, T003, T004, T005 [P]

### Group 3 (Scheduling & Alerts — depends on Group 2)
- [T007] Implement APScheduler integration
- [T008] Implement price drop alert logic
- [T009] Write integration tests
```

---

## 6. Level 3 — Advanced: Constitution & Extensions

### Goal: Establish project-wide principles and use community extensions

### The Constitution: Your Project's Immutable Rules

The constitution is spec-kit's "memory bank" — a powerful rules file that governs every spec, plan, and task in your project. Run it **once**, at the very beginning.

```
/speckit.constitution
Create principles for a Python data science project managed with pixi:
- All code must be typed (use type hints everywhere)
- All functions must have docstrings
- Test coverage must be >= 80%
- Use ruff for linting, black for formatting
- Dependencies managed exclusively via pixi.toml (no pip install)
- No global state; prefer pure functions and dependency injection
- All I/O operations must be async where possible
- Errors must be handled explicitly; no bare except clauses
- Logging over print statements
- All pixi tasks must be documented in README.md
```

This creates a `constitution.md` (or `.github/copilot-instructions.md` depending on your agent) that the AI references for every subsequent command.

### Constitution Template for Pixi + Python Projects

```markdown
# Project Constitution

## Package Management
- Use pixi exclusively. Never suggest pip, conda, or poetry.
- All dependencies go in pixi.toml under [dependencies]
- Dev dependencies go under [feature.dev.dependencies]
- All runnable scripts are defined as [tasks] in pixi.toml

## Code Quality
- Python 3.11+ type hints required on all functions
- Docstrings required (Google style)
- ruff for linting (line length: 100)
- black for formatting
- pytest for all tests; minimum 80% coverage

## Architecture
- src/ layout: all source code in src/<package_name>/
- tests/ layout: mirrors src/ structure
- No circular imports
- Prefer composition over inheritance

## AI Agent Behavior
- Never suggest requirements.txt or setup.py
- Always generate pixi.toml task definitions alongside code
- Always generate tests alongside implementation
- Flag any dependency that is not available on conda-forge
```

### Using Community Extensions

Extensions add new slash commands to your workflow. Install them via the spec-kit extension catalog.

#### Useful extensions for Python/Pixi projects:

| Extension | Command | What it does |
|---|---|---|
| **Cleanup** | `/speckit.cleanup` | Post-implementation quality gate; fixes small issues, creates tasks for larger ones |
| **FixIt** | `/speckit.fixit` | Spec-aware bug fixing — maps bugs back to spec artifacts |
| **Checkpoint** | `/speckit.checkpoint` | Commits changes mid-implementation (avoids one giant commit) |
| **Iterate** | `/speckit.iterate` | Refine specs mid-implementation and resume building |
| **Conduct** | `/speckit.conduct` | Orchestrates all phases via sub-agents to reduce context pollution |
| **Learning** | `/speckit.learn` | Generates educational guides from your implementation |

#### Installing an extension

Extensions are defined in `catalog.community.json`. To add one, follow the spec-kit extension installation guide in the [GitHub repo](https://github.com/github/spec-kit).

### Advanced Spec Patterns

#### Brownfield (existing codebase) specs

When adding a feature to an existing pixi project:

```
/speckit.specify
Add a caching layer to the existing price monitor. The cache should:
- Store HTTP responses in SQLite to avoid redundant requests
- Respect cache TTL configured per-URL in config.toml
- Be transparent to the existing fetcher interface (no breaking changes)
- Include cache invalidation via CLI flag --clear-cache

EXISTING CONSTRAINTS:
- The project uses httpx and sqlite3 (already in pixi.toml)
- The fetcher interface is defined in src/fetcher.py
- Do not change the public API of PriceFetcher class
```

#### Spec for a pixi task pipeline

```
/speckit.specify
Build a data processing pipeline as a series of pixi tasks.
The pipeline should:
- Stage 1 (pixi run fetch): Download raw data from a public API to data/raw/
- Stage 2 (pixi run transform): Clean and normalize data to data/processed/
- Stage 3 (pixi run report): Generate a markdown report in reports/
Each stage should be independently runnable and idempotent.
```

---

## 7. Level 4 — Professional: Multi-Agent Orchestration

### Goal: Run parallel agents, manage complex features, and maintain living specs

### The Conduct Extension: Sub-Agent Delegation

For large features, context pollution is a real problem — the AI loses track of earlier decisions as the conversation grows. The **Conduct extension** solves this by delegating each phase to a fresh sub-agent:

```
/speckit.conduct
Build a full ML training pipeline with experiment tracking.
```

Conduct will:
1. Spawn a **Specify agent** → generates spec, returns result
2. Spawn a **Plan agent** → reads spec, generates plan, returns result
3. Spawn a **Tasks agent** → reads plan, generates tasks, returns result
4. Spawn **Implementation agents** (potentially parallel) → implement tasks

Each agent starts with a clean context, reducing hallucination and drift.

### Parallel Implementation with MAQA

The **MAQA (Multi-Agent & Quality Assurance)** extension enables parallel worktree-based implementation:

```
/speckit.maqa
```

This creates separate git worktrees for independent task groups and runs implementation agents in parallel, then merges results.

### Managing Living Specs

A professional SDD workflow treats specs as living documents:

#### When to update the spec

- A requirement changes → update `spec.md`, re-run `/speckit.plan`
- A bug is found → use `/speckit.fixit` to trace it back to the spec
- A new edge case is discovered → add it to acceptance criteria
- Performance issues arise → add non-functional requirements to the spec

#### Spec versioning strategy

```bash
# Each feature lives on its own branch (spec-kit creates this automatically)
git branch
# 001-csv-analyzer
# 002-price-monitor
# 003-caching-layer   ← current feature

# Merge spec + implementation together
git checkout main
git merge 003-caching-layer
```

#### The Archive Extension

After merging, archive the feature spec into project memory:

```
/speckit.archive
```

This distills the spec into a summary that future agents can reference, keeping the constitution up to date.

### Professional Pixi + SDD Project Structure

```
my-professional-project/
├── pixi.toml                    # Package manager config
├── constitution.md              # Project immutable principles
├── README.md                    # Auto-updated by spec-kit tasks
├── specs/
│   ├── 001-csv-analyzer/
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── data-model.md
│   │   ├── research.md
│   │   └── contracts/
│   │       └── cli-interface.md
│   └── 002-price-monitor/
│       └── ...
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── csv_analyzer.py
│       └── price_monitor.py
└── tests/
    ├── test_csv_analyzer.py
    └── test_price_monitor.py
```

### Controlling AI Agent Behavior

Use the constitution and spec to constrain agent behavior precisely:

```
/speckit.specify
...
AGENT CONSTRAINTS:
- Do not install any package not already in pixi.toml without asking
- Do not modify files outside of src/ and tests/
- Run `pixi run test` after each task and report results before proceeding
- If a task fails tests, stop and report — do not auto-fix silently
- Prefer stdlib solutions over new dependencies
```

---

## 8. Pixi + Python Project Examples

### Example A: Data Science Notebook Pipeline

**Spec prompt:**
```
/speckit.specify
Build a reproducible data science pipeline for analyzing sales data.
The pipeline reads CSV files from data/raw/, performs EDA, trains a
simple forecasting model, and outputs charts to reports/.
Target users: data analysts who are not software engineers.
The entire pipeline must be runnable with a single command.
```

**Plan prompt:**
```
/speckit.plan
- pixi for environment management
- pandas + matplotlib + scikit-learn (all available on conda-forge)
- Jupyter notebooks for EDA (pixi run notebook)
- Python scripts for the automated pipeline (pixi run pipeline)
- pytest for testing utility functions
- No cloud dependencies; fully local
```

**Resulting pixi.toml tasks:**
```toml
[tasks]
notebook = "jupyter lab notebooks/"
pipeline = "python src/pipeline.py"
test = "pytest tests/ -v"
clean = "rm -rf reports/*.png data/processed/*"
```

---

### Example B: CLI Tool with Typer

**Spec prompt:**
```
/speckit.specify
Build a CLI tool called `pixicheck` that audits a pixi.toml file and
reports: unused dependencies, dependencies not available on conda-forge,
missing pixi tasks for common operations (test, lint, format), and
outdated package versions. Output should be colorized and actionable.
```

**Plan prompt:**
```
/speckit.plan
- typer for CLI framework
- rich for terminal output
- httpx for conda-forge API checks
- tomllib (stdlib, Python 3.11+) for parsing pixi.toml
- pytest + typer's testing utilities for tests
- Distributed as a pixi tool (specify in pixi.toml)
```

---

### Example C: FastAPI Microservice

**Spec prompt:**
```
/speckit.specify
Build a REST API microservice that exposes a machine learning model
for text classification. Data scientists will POST text to /classify
and receive a label and confidence score. The service must handle
concurrent requests and return results in under 200ms for inputs
under 512 tokens.
```

**Plan prompt:**
```
/speckit.plan
- FastAPI + uvicorn
- scikit-learn for the model (loaded at startup)
- pydantic for request/response validation
- pytest + httpx for API tests
- pixi tasks: serve (uvicorn), test, train (model training script)
- No database; model loaded from a .pkl file in models/
```

**Resulting pixi.toml:**
```toml
[dependencies]
python = ">=3.11"
fastapi = "*"
uvicorn = "*"
scikit-learn = "*"
pydantic = "*"
pytest = "*"
httpx = "*"

[tasks]
serve = "uvicorn src.api:app --reload"
test = "pytest tests/ -v --tb=short"
train = "python src/train.py"
```

---

## 9. Cheatsheet

### 🚀 Quick Reference

```
specify init <name> --ai <agent>    Initialize new project
specify init . --ai claude          Initialize in current directory
specify init --here --ai copilot    Same as above
specify check                       Check system requirements
specify --version                   Show CLI version
```

### 📋 Slash Commands

| Command | When to use | Key tip |
|---|---|---|
| `/speckit.constitution` | **Once**, at project start | Be specific about standards; this governs everything |
| `/speckit.specify <description>` | Start of every new feature | Focus on *what* and *why*, not tech stack |
| `/speckit.clarify` | After specify, before plan | Always run this; prevents rework |
| `/speckit.plan <stack>` | After clarify | Specify pixi.toml, Python version, all constraints |
| `/speckit.tasks` | After plan | Review for `[P]` parallel markers |
| `/speckit.analyze` | After tasks, before implement | Catches inconsistencies early |
| `/speckit.implement` | After analyze | Review each task's output before approving next |

### 🔄 The SDD Loop

```
New Feature?
    ↓
/speckit.specify → Review spec.md → Edit if needed
    ↓
/speckit.clarify → Answer AI questions
    ↓
/speckit.plan → Review plan.md → Edit if needed
    ↓
/speckit.tasks → Review tasks.md → Reorder if needed
    ↓
/speckit.analyze → Fix any inconsistencies
    ↓
/speckit.implement → Review each task → Approve/reject
    ↓
pixi run test → All green? → Merge branch
```

### 📁 File Structure Reference

| File | Created by | Purpose |
|---|---|---|
| `constitution.md` | `/speckit.constitution` | Immutable project principles |
| `specs/NNN-name/spec.md` | `/speckit.specify` | Feature requirements & user stories |
| `specs/NNN-name/plan.md` | `/speckit.plan` | Technical architecture & decisions |
| `specs/NNN-name/tasks.md` | `/speckit.tasks` | Executable task list |
| `specs/NNN-name/data-model.md` | `/speckit.plan` | Data schemas & models |
| `specs/NNN-name/research.md` | `/speckit.plan` | Library comparisons & findings |
| `specs/NNN-name/contracts/` | `/speckit.plan` | API contracts & interfaces |

### ⚡ Pixi-Specific Tips

```bash
# Always initialize spec-kit inside your pixi project
cd my-pixi-project
specify init . --ai claude

# Tell the AI to use pixi in your plan
/speckit.plan Use pixi for all dependency management. Never suggest pip.

# Run tests after implementation
pixi run test

# Common pixi.toml task pattern
[tasks]
test    = "pytest tests/ -v"
lint    = "ruff check src/"
format  = "black src/ tests/"
typecheck = "mypy src/"
ci      = { depends-on = ["lint", "typecheck", "test"] }
```

### 🧩 Extension Quick Reference

| Extension | Command | Best for |
|---|---|---|
| Cleanup | `/speckit.cleanup` | Post-implementation quality gate |
| FixIt | `/speckit.fixit` | Bug fixing traced to spec |
| Checkpoint | `/speckit.checkpoint` | Granular commits during implementation |
| Iterate | `/speckit.iterate` | Mid-implementation spec refinement |
| Conduct | `/speckit.conduct` | Large features, reduce context pollution |
| Archive | `/speckit.archive` | Post-merge spec archiving |
| MAQA | `/speckit.maqa` | Parallel multi-agent implementation |

### 🚦 Phase Gates (Don't Skip These)

```
✅ Before /speckit.plan:    spec.md reviewed and approved by you
✅ Before /speckit.tasks:   plan.md reviewed and approved by you
✅ Before /speckit.implement: tasks.md reviewed, /speckit.analyze run
✅ Before merging:          pixi run test passes, /speckit.cleanup run
```

### 🔧 Environment Variables

```bash
# Override feature detection
export SPECIFY_FEATURE=001-my-feature

# GitHub token for corporate environments
export GITHUB_TOKEN=ghp_your_token_here

# Debug mode
specify init . --ai claude --debug
```

### 💡 Spec Writing Tips

| Do | Don't |
|---|---|
| Describe user journeys and outcomes | Describe implementation details |
| Specify who the users are | Assume the AI knows your users |
| Include edge cases and failure modes | Leave error handling unspecified |
| State explicit constraints (no cloud, local only, etc.) | Leave constraints implicit |
| Reference existing interfaces when brownfield | Ignore existing code |
| Be specific about performance requirements | Use vague terms like "fast" |

---

## 10. Troubleshooting

### `specify` command not found

```bash
# Ensure uv tools are in PATH
export PATH="$HOME/.local/bin:$PATH"
# Or re-install
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### Git authentication issues (Linux)

```bash
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
git config --global credential.helper manager
```

### AI agent not picking up slash commands

- Ensure you ran `specify init` in the project root
- Restart your AI agent/editor after initialization
- Check that `.github/` or agent-specific config files were created

### Spec is too vague / AI asks too many questions

- Add more detail to your `/speckit.specify` prompt
- Run `/speckit.clarify` and answer all questions before `/speckit.plan`
- Reference the constitution to set baseline expectations

### pixi dependency not on conda-forge

```
/speckit.plan
Note: <package> is not available on conda-forge. Use the PyPI channel:
[dependencies]
<package> = { version = "*", channel = "pypi" }
```

### Tasks are too large / implementation drifts

- Break the spec into smaller features (one spec per PR)
- Use `/speckit.conduct` to reduce context pollution
- Use `/speckit.checkpoint` to commit after each task

---

*Guide based on [github/spec-kit](https://github.com/github/spec-kit) (MIT License) · [speckit.org](https://speckit.org/) · [SDD Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)*
