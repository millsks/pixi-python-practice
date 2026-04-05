# pixi-build-practice

A basic Hello World Python project using [FastAPI](https://fastapi.tiangolo.com/) to serve a Hello World message in the browser. [Pixi](https://pixi.sh) manages all dependencies, environments, and tasks using the `pixi-build-python` build backend.

## Requirements

- [Pixi](https://pixi.sh/latest/#installation) (v0.65.0 or later required)

## Getting Started

### Install dependencies

```bash
pixi install
```

### Start the server

```bash
pixi run start
```

Then open your browser at [http://localhost:8000](http://localhost:8000) to see the Hello World message.

## Project Structure

```
hello_world/
    __init__.py
    main.py         # FastAPI application
pixi.toml           # Pixi workspace, package, and task configuration
pyproject.toml      # Python package metadata and build system (hatchling)
```

## Pixi Tasks

| Task    | Description                        |
|---------|------------------------------------|
| `start` | Start the FastAPI development server |

## Build Backend

This project uses `pixi-build-python` as the build backend, which builds the Python package as a conda package using standard PEP 517/518 tooling (hatchling).
