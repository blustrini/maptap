# MapTap

A project for exploring new MapTap difficulty metrics.

This project is managed using [`uv`](https://github.com/astral-sh/uv). 

## Setup

Install dependencies:
```bash
uv sync
```

## Downloading geojsons

To download the required geojsons files for each country, run:
```bash
uv run python scripts/download_geometries.py
```
