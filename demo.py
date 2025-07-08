#!/usr/bin/env python3
"""
Steam Game Tracker - Simple Demo
================================

A simplified demo script that demonstrates the core functionality
without complex dependencies for testing purposes.
"""

import sys
import json
from datetime import datetime, timedelta
import asyncio

def create_sample_data():
    """Create sample data for demonstration."""
print("Creating sample Steam and Reddit data...")
    
    # Sample Steam follower data
    steam_data = []
    reddit_data = []
    
    base_date = datetime.now() - timedelta(days=14)
    base_followers = 45000
    
    for i in range(15):
        current_date = base_date + timedelta(days=i)
        
        # Generate realistic follower growth
        daily_change = (-50 + i * 20) + (i % 3 * 10)  # Some variation
        base_followers += daily_change
        
        steam_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'followers': base_followers,
            'source': 'steamdb'
        })
        
        # Generate sample Reddit mentions
        mentions = max(0, 15 - abs(i - 7) + (i % 4))  # Peak in the middle
        reddit_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'mentions': mentions,
            'source': 'reddit'
        })
    
    return steam_data, reddit_data

def process_data(steam_data, reddit_data):
    """Process and combine the data."""
print("Processing and aligning data...")
    
    # Combine data by date
    combined_data = []
    
    # Create a lookup for Reddit data
    reddit_lookup = {item['date']: item['mentions'] for item in reddit_data}
    
    for steam_item in steam_data:
        date = steam_item['date']
        combined_data.append({
            'date': date,
            'followers': steam_item['followers'],
            'mentions': reddit_lookup.get(date, 0)
        })
    
    return combined_data

def save_to_csv(data, filename):
    """Save data to CSV format."""
print(f"Saving data to {filename}...")
    
    with open(filename, 'w') as f:
        # Write header
        f.write("date,followers,mentions\n")
        
        # Write data
        for item in data:
            f.write(f"{item['date']},{item['followers']},{item['mentions']}\n")
    
print(f"Data saved successfully!")

def print_summary(data):
    """Print a summary of the data."""
    print("\n" + "="*60)
    print("STEAM GAME TRACKER - DEMO SUMMARY")
    print("="*60)
    
    if not data:
        print("No data to display.")
        return
    
    print(f"Game: Cyberpunk 2077 (Demo)")
    print(f"Steam App ID: 1091500")
    print(f"Data Points: {len(data)}")
    print(f"Date Range: {data[0]['date']} to {data[-1]['date']}")
    
    # Calculate statistics
    followers = [item['followers'] for item in data]
    mentions = [item['mentions'] for item in data]
    
    print(f"\nSteam Followers:")
    print(f"  Average: {sum(followers) / len(followers):.0f}")
    print(f"  Min: {min(followers)}")
    print(f"  Max: {max(followers)}")
    
    print(f"\nReddit Mentions:")
    print(f"  Total: {sum(mentions)}")
    print(f"  Daily Average: {sum(mentions) / len(mentions):.1f}")
    print(f"  Max Daily: {max(mentions)}")
    
    print("\nFirst 5 rows:")
    for i, item in enumerate(data[:5]):
        print(f"  {item['date']}: {item['followers']} followers, {item['mentions']} mentions")
    
    if len(data) > 5:
        print("\nLast 5 rows:")
        for item in data[-5:]:
            print(f"  {item['date']}: {item['followers']} followers, {item['mentions']} mentions")
    
    print("="*60)

def main():
    """Main demo function."""
print("Steam Game Tracker - Professional Demo")
    print("="*50)
    
    try:
        # Create sample data
        steam_data, reddit_data = create_sample_data()
        
        # Process data
        processed_data = process_data(steam_data, reddit_data)
        
        # Save to CSV
        save_to_csv(processed_data, 'data/demo_results.csv')
        
        # Print summary
        print_summary(processed_data)
        
print("\nDemo completed successfully!")
        print("\nThis demonstrates the core functionality of the Steam Game Tracker:")
        print("- Data collection simulation")
        print("- Data processing and alignment")
        print("- CSV export capabilities")
        print("- Professional summary reporting")
        print("\nFor the full application with web scraping and visualization,")
        print("run: python main.py --game 'Cyberpunk 2077' --app-id 1091500 --days 14")
        
    except Exception as e:
print(f"Error during demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

