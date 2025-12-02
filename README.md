# Advent of Code 2025

Python solutions for [Advent of Code 2025](https://adventofcode.com/2025) challenges.

## Overview

This repository contains solutions for the Advent of Code 2025 programming puzzles.

**Attribution**: This framework is built upon excellent work by [Landcruiser87](https://github.com/Landcruiser87) and [anze3db](https://github.com/anze3db/adventofcode). Thank you for the inspiration and foundation!

## Features

- **Automated Puzzle Fetching**: Automatically downloads puzzle descriptions and input data
- **Intelligent Caching**: Uses `percache` to cache API responses and avoid unnecessary requests
- **Test Case Validation**: Validates solutions against sample data before running on full input
- **Rich Terminal Output**: Console logging with the `rich` library
- **Template System**: Consistent structure for each day's solution

## Setup

### Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nehat312/AoC2025.git
   cd AoC2025
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Configure your session cookie**
   
   Create a `secret` directory and add your Advent of Code session cookie:
   ```bash
   mkdir -p secret
   # Copy your session cookie from browser dev tools (Application > Cookies)
   echo "your_session_cookie_here" > secret/cookie.txt
   ```

   > **Note**: The `secret/` directory is excluded from Git via `.gitignore` to protect your credentials.

## Usage

### Running Solutions

To run a specific day's solution:

```bash
# Activate the Poetry virtual environment
poetry shell

# Run a specific day
cd scripts
python day1/day1.py
```

Or run directly without activating the shell:

```bash
poetry run python scripts/day1/day1.py
```

### Creating New Day Solutions

Use the provided template to create solutions for new days:

```bash
# Copy the template
cp scripts/utils/day_template.py scripts/day5/day5.py

# Update the DAY constant in the new file
# Then implement your solution in the problemsolver() function
```

## Project Structure

```
AoC2025/
├── scripts/
│   ├── day1/           # Day 1 solution
│   ├── day2/           # Day 2 solution
│   ├── day3/           # Day 3 template (ready for implementation)
│   ├── day4/           # Day 4 template (ready for implementation)
│   └── utils/
│       ├── support.py      # Core utilities (API calls, caching, logging)
│       └── day_template.py # Template for new days
├── secret/
│   └── cookie.txt      # Your AOC session cookie (not tracked by Git)
├── pyproject.toml      # Poetry dependencies
└── README.md
```

## Dependencies

- **numpy**: Array operations and numerical computing
- **matplotlib**: Data visualization
- **rich**: Beautiful terminal output and logging
- **requests**: HTTP requests for puzzle fetching
- **beautifulsoup4**: HTML parsing for puzzle descriptions
- **lxml**: XML/HTML processing
- **percache**: Persistent caching of API responses

## Development

### Virtual Environment

Poetry automatically manages the virtual environment:

```bash
# Activate the virtual environment
poetry shell

# Check environment info
poetry env info

# View installed packages
poetry show
```

### Adding Dependencies

```bash
poetry add package-name
```

## Progress

| Day | Stars | Solution | Name | Time A | Time B |
|-----|-------|----------|------|--------|--------|
| 01  | ⭐⭐ | [day1.py](scripts/day1/day1.py) | TBD | - | - |
| 02  | ⭐⭐ | [day2.py](scripts/day2/day2.py) | TBD | - | - |
| 03  | - | [day3.py](scripts/day3/day3.py) | TBD | - | - |
| 04  | - | [day4.py](scripts/day4/day4.py) | TBD | - | - |

## License

MIT

## Acknowledgments

- [Eric Wastl](http://was.tl/) for creating Advent of Code
- [Landcruiser87](https://github.com/Landcruiser87) for the framework foundation
- [anze3db](https://github.com/anze3db/adventofcode) for the original Python framework inspiration
