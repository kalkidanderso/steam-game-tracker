#!/usr/bin/env python3
"""
Steam Game Tracker - Main Application
=====================================

A professional tool for tracking Steam game follower dynamics and social media mentions.
Demonstrates API integration, data processing, and analytics capabilities.

Author: Professional Developer
Date: 2025-07-07
"""

import asyncio
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

from src.config import Config
from src.steam_tracker import SteamTracker
from src.reddit_tracker import RedditTracker
from src.data_processor import DataProcessor
from src.visualizer import Visualizer
from src.utils import setup_logging, validate_config

# Configure professional logging
logger = setup_logging()


async def main():
    """Main application entry point with professional error handling."""
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(
            description='Steam Game Tracker - Professional Analytics Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python main.py --game "Cyberpunk 2077" --app-id 1091500 --days 30
  python main.py --game "The Witcher 3" --app-id 292030 --days 14 --visualize
  python main.py --config config.json
            """
        )
        
        parser.add_argument('--game', type=str, help='Game name for tracking')
        parser.add_argument('--app-id', type=int, help='Steam App ID')
        parser.add_argument('--days', type=int, default=30, help='Number of days to track (default: 30)')
        parser.add_argument('--config', type=str, help='Path to configuration file')
        parser.add_argument('--visualize', action='store_true', help='Generate visualization')
        parser.add_argument('--output', type=str, default='data/results.csv', help='Output file path')
        
        args = parser.parse_args()
        
        # Load configuration
        config = Config(args.config) if args.config else Config()
        
        # Override config with command line arguments
        if args.game:
            config.game_name = args.game
        if args.app_id:
            config.steam_app_id = args.app_id
        if args.days:
            config.tracking_days = args.days
        
        # Validate configuration
        if not validate_config(config):
            logger.error("Invalid configuration. Please check your settings.")
            sys.exit(1)
        
        logger.info(f"Starting Steam Game Tracker for '{config.game_name}' (AppID: {config.steam_app_id})")
        logger.info(f"Tracking period: {config.tracking_days} days")
        
        # Initialize tracking components
        steam_tracker = SteamTracker(config)
        reddit_tracker = RedditTracker(config)
        data_processor = DataProcessor(config)
        
        # Collect data concurrently for better performance
        logger.info("Collecting data from multiple sources...")
        
        steam_task = asyncio.create_task(steam_tracker.get_follower_history())
        reddit_task = asyncio.create_task(reddit_tracker.get_mentions())
        
        steam_data, reddit_data = await asyncio.gather(steam_task, reddit_task)
        
        # Process and align data
        logger.info("Processing and aligning data...")
        processed_data = data_processor.process_data(steam_data, reddit_data)
        
        # Save results
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        data_processor.save_to_csv(processed_data, output_path)
        logger.info(f"Results saved to {output_path}")
        
        # Generate visualization if requested
        if args.visualize:
            logger.info("Generating visualization...")
            visualizer = Visualizer(config)
            visualizer.create_graph(processed_data)
            logger.info("Visualization saved to data/graph.png")
        
        # Display summary
        logger.info("Analysis complete!")
        logger.info(f"Total data points: {len(processed_data)}")
        logger.info(f"Date range: {processed_data['date'].min()} to {processed_data['date'].max()}")
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

