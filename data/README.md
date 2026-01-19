# Pickup Soccer Data Directory

This directory contains all data files for the Pickup Soccer application.

## Structure

- `players/` - Player data in Parquet format
- `games/` - Game records in Parquet format
- `sample/` - Sample datasets generated for testing and demos

## Usage

Data is automatically generated when you run:
```bash
python scripts/generate_data.py
```

The application reads from these directories by default.
