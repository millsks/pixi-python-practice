# Pixi Python Practice

A collection of Python projects focused on learning and understanding [Pixi](https://pixi.sh) — a fast, modern package manager and workflow tool — and how it can be used to manage Python projects.

## Purpose

This repository serves as a hands-on playground for exploring Pixi's capabilities for Python development, including:

- Dependency management via conda-forge and PyPI
- Environment configuration and reproducibility
- Task running and build backends (e.g. `pixi-build-python`)
- Multi-platform support
- Project structure and best practices

## Projects

| Project | Description |
|---------|-------------|
| [hello-world](hello-world/) | A basic FastAPI Hello World app managed entirely by Pixi |

## Documentation

- [Pixi Guide](docs/pixi_guide.md) — A comprehensive guide covering Pixi from novice to pro

## Requirements

- [Pixi](https://pixi.sh/latest/#installation) (v0.65.0 or later)

## Getting Started

Each project lives in its own directory with its own `pixi.toml`. Navigate into a project folder and run:

```bash
pixi install
pixi run start
```

Refer to the individual project README for details.
