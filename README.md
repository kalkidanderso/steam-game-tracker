# Steam Game Tracker

**Professional Analytics Tool for Steam Game Follower Dynamics and Social Media Mentions**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated, production-ready tool for tracking Steam game follower dynamics and correlating them with social media mentions. Built with professional software development practices, comprehensive error handling, and scalable architecture.

## Features

- **Steam Follower Tracking**: Monitor follower count changes over time using SteamDB data
- **Reddit Mentions Analytics**: Track game mentions across Reddit with configurable search parameters
- **Data Correlation Analysis**: Calculate statistical relationships between follower growth and social media buzz
- **Professional Visualizations**: Generate publication-quality graphs and charts
- **Flexible Configuration**: JSON-based configuration with command-line overrides
- **Robust Error Handling**: Comprehensive retry logic and graceful failure management
- **Async Performance**: High-performance async operations for concurrent data collection
- **Export Capabilities**: CSV output with detailed summary reports

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kalkidanderso/steam-game-tracker.git
   cd steam-game-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run with default settings (Cyberpunk 2077)**
   ```bash
   python main.py --days 14 --visualize
   ```

## Usage Guide

### Command Line Interface

```bash
python main.py [OPTIONS]
```

#### Essential Options

| Option | Description | Example |
|--------|-------------|---------|
| `--game` | Game name for tracking | `--game "The Witcher 3"` |
| `--app-id` | Steam App ID | `--app-id 292030` |
| `--days` | Days to track (default: 30) | `--days 14` |
| `--visualize` | Generate graphs | `--visualize` |
| `--output` | Output CSV path | `--output results.csv` |

#### Usage Examples

**Track Cyberpunk 2077 for 30 days with visualization:**
```bash
python main.py --game "Cyberpunk 2077" --app-id 1091500 --days 30 --visualize
```

**Track The Witcher 3 for 14 days:**
```bash
python main.py --game "The Witcher 3" --app-id 292030 --days 14
```

**Use custom configuration file:**
```bash
python main.py --config my_config.json
```

### Configuration File

Create a `config.json` file for persistent settings:

```json
{
  "game_name": "Cyberpunk 2077",
  "steam_app_id": 1091500,
  "tracking_days": 30,
  "output_dir": "data",
  "rate_limit_delay": 1.0,
  "enable_caching": true
}
```

### Finding Steam App IDs

You can find Steam App IDs by:
1. Visiting the game's Steam store page
2. Looking at the URL: `https://store.steampowered.com/app/[APP_ID]/`
3. Or using SteamDB: `https://steamdb.info/`

**Popular Game IDs:**
- Cyberpunk 2077: `1091500`
- The Witcher 3: `292030`
- Counter-Strike 2: `730`
- Dota 2: `570`

## Output

The tool generates several types of output:

### 1. CSV Data File (`data/results.csv`)
```csv
date,followers,mentions,followers_change,mentions_change,correlation
2024-01-01,45230,12,0,0,0.0
2024-01-02,45340,8,110,-4,0.23
```

### 2. Console Summary
```
============================================================
STEAM GAME TRACKER - DATA SUMMARY
============================================================
Game: Cyberpunk 2077
Steam App ID: 1091500
Tracking Period: 30 days
Data Points: 30

Steam Followers:
  Average: 45,230
  Min: 44,890
  Max: 45,670

Reddit Mentions:
  Total: 287
  Daily Average: 9.6
  Max Daily: 23
```

### 3. Visualizations (when `--visualize` is used)
- **Main Graph**: Steam followers over time with Reddit mentions overlay
- **Correlation Analysis**: Statistical relationship visualization
- **Trend Analysis**: Daily changes and distribution plots

## Architecture

### Project Structure
```
steam-game-tracker/
├── main.py                 # Application entry point
├── src/                    # Core modules
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── steam_tracker.py   # Steam data collection
│   ├── reddit_tracker.py  # Reddit API integration
│   ├── data_processor.py  # Data processing and alignment
│   ├── visualizer.py      # Graph generation
│   └── utils.py           # Utility functions
├── data/                  # Output directory
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
└── README.md             # This file
```