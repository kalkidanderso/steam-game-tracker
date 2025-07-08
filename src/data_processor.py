"""
Data Processor Module
====================

Professional data processing and alignment for Steam and social media data.
Handles data cleaning, transformation, and export functionality.
"""

import logging
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from .config import Config
from .utils import ensure_directory, calculate_correlation


class DataProcessor:
    """Professional data processor for Steam and social media analytics."""
    
    def __init__(self, config: Config):
        """
        Initialize data processor with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = logging.getLogger('SteamGameTracker.DataProcessor')
    
    def process_data(self, steam_data: List[Dict], reddit_data: List[Dict]) -> pd.DataFrame:
        """
        Process and align Steam follower data with Reddit mentions.
        
        Args:
            steam_data: Steam follower history data
            reddit_data: Reddit mentions data
            
        Returns:
            Processed and aligned DataFrame
        """
        self.logger.info("Processing and aligning data from multiple sources")
        
        try:
            # Convert to DataFrames for easier manipulation
            steam_df = pd.DataFrame(steam_data) if steam_data else pd.DataFrame(columns=['date', 'followers'])
            reddit_df = pd.DataFrame(reddit_data) if reddit_data else pd.DataFrame(columns=['date', 'mentions'])
            
            # Ensure date columns are datetime
            if not steam_df.empty:
                steam_df['date'] = pd.to_datetime(steam_df['date'])
            if not reddit_df.empty:
                reddit_df['date'] = pd.to_datetime(reddit_df['date'])
            
            # Merge data on date
            if not steam_df.empty and not reddit_df.empty:
                merged_df = pd.merge(steam_df, reddit_df, on='date', how='outer')
            elif not steam_df.empty:
                merged_df = steam_df.copy()
                merged_df['mentions'] = 0
            elif not reddit_df.empty:
                merged_df = reddit_df.copy()
                merged_df['followers'] = 0
            else:
                # Create empty DataFrame with required columns
                merged_df = pd.DataFrame(columns=['date', 'followers', 'mentions'])
            
            # Fill missing values
            merged_df['followers'] = merged_df['followers'].fillna(method='ffill').fillna(0)
            merged_df['mentions'] = merged_df['mentions'].fillna(0)
            
            # Sort by date
            merged_df = merged_df.sort_values('date')
            
            # Add additional metrics
            merged_df = self._add_calculated_metrics(merged_df)
            
            self.logger.info(f"Successfully processed {len(merged_df)} data points")
            return merged_df
            
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            return pd.DataFrame(columns=['date', 'followers', 'mentions'])
    
    def _add_calculated_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add calculated metrics to the DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional metrics
        """
        try:
            if len(df) < 2:
                return df
            
            # Calculate daily changes
            df['followers_change'] = df['followers'].diff()
            df['mentions_change'] = df['mentions'].diff()
            
            # Calculate rolling averages (7-day window)
            if len(df) >= 7:
                df['followers_avg_7d'] = df['followers'].rolling(window=7, min_periods=1).mean()
                df['mentions_avg_7d'] = df['mentions'].rolling(window=7, min_periods=1).mean()
            
            # Calculate correlation if we have enough data
            if len(df) >= 10:
                correlation = calculate_correlation(
                    df['followers'].tolist(),
                    df['mentions'].tolist()
                )
                df['correlation'] = correlation
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error adding calculated metrics: {e}")
            return df
    
    def save_to_csv(self, df: pd.DataFrame, output_path: Path) -> None:
        """
        Save processed data to CSV file.
        
        Args:
            df: DataFrame to save
            output_path: Output file path
        """
        try:
            # Ensure output directory exists
            ensure_directory(output_path.parent)
            
            # Format the data for output
            output_df = df.copy()
            if 'date' in output_df.columns:
                output_df['date'] = output_df['date'].dt.strftime('%Y-%m-%d')
            
            # Round numeric columns
            numeric_columns = output_df.select_dtypes(include=['float64', 'int64']).columns
            output_df[numeric_columns] = output_df[numeric_columns].round(2)
            
            # Save to CSV
            output_df.to_csv(output_path, index=False)
            
            self.logger.info(f"Data saved to {output_path}")
            
            # Print summary to console
            self._print_summary(output_df)
            
        except Exception as e:
            self.logger.error(f"Error saving data to CSV: {e}")
    
    def _print_summary(self, df: pd.DataFrame) -> None:
        """
        Print a summary of the processed data.
        
        Args:
            df: DataFrame to summarize
        """
        print("\n" + "="*60)
        print("STEAM GAME TRACKER - DATA SUMMARY")
        print("="*60)
        
        if df.empty:
            print("No data to display.")
            return
        
        print(f"Game: {self.config.game_name}")
        print(f"Steam App ID: {self.config.steam_app_id}")
        print(f"Tracking Period: {self.config.tracking_days} days")
        print(f"Data Points: {len(df)}")
        
        if 'date' in df.columns and not df.empty:
            print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
        
        if 'followers' in df.columns:
            followers_stats = df['followers'].describe()
            print(f"\nSteam Followers:")
            print(f"  Average: {followers_stats['mean']:.0f}")
            print(f"  Min: {followers_stats['min']:.0f}")
            print(f"  Max: {followers_stats['max']:.0f}")
        
        if 'mentions' in df.columns:
            mentions_stats = df['mentions'].describe()
            print(f"\nReddit Mentions:")
            print(f"  Total: {df['mentions'].sum():.0f}")
            print(f"  Daily Average: {mentions_stats['mean']:.1f}")
            print(f"  Max Daily: {mentions_stats['max']:.0f}")
        
        if 'correlation' in df.columns and not df['correlation'].isna().all():
            correlation = df['correlation'].iloc[-1]
            print(f"\nCorrelation (Followers vs Mentions): {correlation:.3f}")
        
        print("\nFirst 5 rows:")
        print(df.head().to_string(index=False))
        
        if len(df) > 5:
            print("\nLast 5 rows:")
            print(df.tail().to_string(index=False))
        
        print("="*60 + "\n")
    
    def export_summary_report(self, df: pd.DataFrame, output_path: Path) -> None:
        """
        Export a detailed summary report.
        
        Args:
            df: DataFrame to analyze
            output_path: Output file path for the report
        """
        try:
            report_lines = []
            report_lines.append("Steam Game Tracker - Analysis Report")
            report_lines.append("=" * 50)
            report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append(f"Game: {self.config.game_name}")
            report_lines.append(f"Steam App ID: {self.config.steam_app_id}")
            report_lines.append(f"Tracking Period: {self.config.tracking_days} days")
            report_lines.append("")
            
            if not df.empty:
                # Statistical analysis
                if 'followers' in df.columns:
                    followers_stats = df['followers'].describe()
                    report_lines.append("Steam Followers Analysis:")
                    report_lines.append(f"  Count: {followers_stats['count']:.0f}")
                    report_lines.append(f"  Mean: {followers_stats['mean']:.2f}")
                    report_lines.append(f"  Std: {followers_stats['std']:.2f}")
                    report_lines.append(f"  Min: {followers_stats['min']:.0f}")
                    report_lines.append(f"  Max: {followers_stats['max']:.0f}")
                    report_lines.append("")
                
                if 'mentions' in df.columns:
                    mentions_stats = df['mentions'].describe()
                    report_lines.append("Reddit Mentions Analysis:")
                    report_lines.append(f"  Total Mentions: {df['mentions'].sum():.0f}")
                    report_lines.append(f"  Daily Average: {mentions_stats['mean']:.2f}")
                    report_lines.append(f"  Std: {mentions_stats['std']:.2f}")
                    report_lines.append(f"  Max Daily: {mentions_stats['max']:.0f}")
                    report_lines.append("")
                
                if 'correlation' in df.columns and not df['correlation'].isna().all():
                    correlation = df['correlation'].iloc[-1]
                    report_lines.append(f"Correlation Analysis:")
                    report_lines.append(f"  Followers vs Mentions: {correlation:.4f}")
                    
                    if abs(correlation) > 0.7:
                        strength = "Strong"
                    elif abs(correlation) > 0.4:
                        strength = "Moderate"
                    else:
                        strength = "Weak"
                    
                    direction = "positive" if correlation > 0 else "negative"
                    report_lines.append(f"  Interpretation: {strength} {direction} correlation")
                    report_lines.append("")
            
            # Save report
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            self.logger.info(f"Summary report saved to {output_path}")
            
        except Exception as e:
            self.logger.error(f"Error generating summary report: {e}")

