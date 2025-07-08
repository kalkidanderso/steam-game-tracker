"""
Visualizer Module
================

Professional visualization for Steam follower and social media mention data.
Creates publication-quality graphs with proper styling and annotations.
"""

import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
from pathlib import Path
import seaborn as sns

from .config import Config
from .utils import ensure_directory, format_number


class Visualizer:
    """Professional data visualizer for Steam game analytics."""
    
    def __init__(self, config: Config):
        """
        Initialize visualizer with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = logging.getLogger('SteamGameTracker.Visualizer')
        
        # Set professional styling
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Configure matplotlib for high-quality output
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 11
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
    
    def create_graph(self, df: pd.DataFrame, output_path: str = 'data/graph.png') -> None:
        """
        Create a comprehensive visualization of the data.
        
        Args:
            df: DataFrame containing the processed data
            output_path: Output path for the graph
        """
        try:
            self.logger.info("Creating comprehensive data visualization")
            
            if df.empty:
                self.logger.warning("No data to visualize")
                return
            
            # Ensure output directory exists
            output_path = Path(output_path)
            ensure_directory(output_path.parent)
            
            # Convert date column to datetime if it's not already
            if 'date' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['date']):
                    df['date'] = pd.to_datetime(df['date'])
            
            # Create figure with subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
            fig.suptitle(f'Steam Game Analytics: {self.config.game_name}', 
                        fontsize=16, fontweight='bold', y=0.95)
            
            # Plot 1: Steam Followers
            if 'followers' in df.columns:
                ax1.plot(df['date'], df['followers'], 
                        color='#1f77b4', linewidth=2.5, marker='o', markersize=4,
                        label='Steam Followers', alpha=0.8)
                
                # Add trend line if we have enough data
                if len(df) >= 7 and 'followers_avg_7d' in df.columns:
                    ax1.plot(df['date'], df['followers_avg_7d'], 
                            color='#ff7f0e', linewidth=2, linestyle='--',
                            label='7-day Average', alpha=0.7)
                
                ax1.set_ylabel('Steam Followers', fontweight='bold')
                ax1.set_title('Steam Follower Count Over Time', fontweight='bold', pad=20)
                ax1.grid(True, alpha=0.3)
                ax1.legend(loc='upper left')
                
                # Format y-axis with readable numbers
                ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format_number(int(x))))
            
            # Plot 2: Reddit Mentions with Steam Followers as background
            if 'mentions' in df.columns:
                # Create secondary y-axis for followers
                ax3 = ax2.twinx()
                
                # Plot followers as background (light)
                if 'followers' in df.columns:
                    ax3.fill_between(df['date'], df['followers'], 
                                   alpha=0.2, color='#1f77b4', label='Steam Followers')
                    ax3.set_ylabel('Steam Followers', color='#1f77b4', fontweight='bold')
                    ax3.tick_params(axis='y', labelcolor='#1f77b4')
                    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format_number(int(x))))
                
                # Plot mentions as scatter points
                ax2.scatter(df['date'], df['mentions'], 
                          color='#d62728', s=50, alpha=0.8, 
                          label='Reddit Mentions', zorder=5)
                
                # Add trend line for mentions if available
                if len(df) >= 7 and 'mentions_avg_7d' in df.columns:
                    ax2.plot(df['date'], df['mentions_avg_7d'], 
                           color='#ff7f0e', linewidth=2, linestyle='-',
                           label='7-day Average', alpha=0.8)
                
                ax2.set_ylabel('Reddit Mentions', color='#d62728', fontweight='bold')
                ax2.set_title('Reddit Mentions vs Steam Followers', fontweight='bold', pad=20)
                ax2.tick_params(axis='y', labelcolor='#d62728')
                ax2.grid(True, alpha=0.3)
                
                # Combine legends
                lines1, labels1 = ax2.get_legend_handles_labels()
                lines2, labels2 = ax3.get_legend_handles_labels()
                ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
            
            # Format x-axis
            ax2.set_xlabel('Date', fontweight='bold')
            
            # Format dates on x-axis
            if len(df) <= 31:
                date_format = mdates.DateFormatter('%m-%d')
                ax2.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(df)//10)))
            else:
                date_format = mdates.DateFormatter('%m-%d')
                ax2.xaxis.set_major_locator(mdates.WeekdayLocator())
            
            ax2.xaxis.set_major_formatter(date_format)
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Add correlation info if available
            if 'correlation' in df.columns and not df['correlation'].isna().all():
                correlation = df['correlation'].iloc[-1]
                fig.text(0.02, 0.02, f'Correlation: {correlation:.3f}', 
                        fontsize=10, style='italic')
            
            # Add data source and timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            fig.text(0.98, 0.02, f'Generated: {timestamp}', 
                    fontsize=8, ha='right', style='italic')
            
            # Adjust layout and save
            plt.tight_layout()
            plt.subplots_adjust(top=0.9, bottom=0.15)
            
            # Save with high DPI for professional quality
            plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            
            self.logger.info(f"Graph saved to {output_path}")
            
            # Close the figure to free memory
            plt.close(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating visualization: {e}")
            if 'fig' in locals():
                plt.close(fig)
    
    def create_correlation_heatmap(self, df: pd.DataFrame, output_path: str = 'data/correlation_heatmap.png') -> None:
        """
        Create a correlation heatmap for numeric columns.
        
        Args:
            df: DataFrame containing the data
            output_path: Output path for the heatmap
        """
        try:
            self.logger.info("Creating correlation heatmap")
            
            if df.empty:
                self.logger.warning("No data to create heatmap")
                return
            
            # Select numeric columns only
            numeric_df = df.select_dtypes(include=['float64', 'int64'])
            
            if numeric_df.shape[1] < 2:
                self.logger.warning("Not enough numeric columns for correlation heatmap")
                return
            
            # Calculate correlation matrix
            correlation_matrix = numeric_df.corr()
            
            # Create heatmap
            plt.figure(figsize=(10, 8))
            mask = correlation_matrix.isnull()
            
            sns.heatmap(correlation_matrix, 
                       annot=True, 
                       cmap='RdBu_r', 
                       center=0,
                       square=True,
                       mask=mask,
                       cbar_kws={"shrink": .8})
            
            plt.title(f'Correlation Matrix: {self.config.game_name}', 
                     fontsize=14, fontweight='bold', pad=20)
            
            # Ensure output directory exists
            output_path = Path(output_path)
            ensure_directory(output_path.parent)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            
            self.logger.info(f"Correlation heatmap saved to {output_path}")
            plt.close()
            
        except Exception as e:
            self.logger.error(f"Error creating correlation heatmap: {e}")
            plt.close()
    
    def create_trend_analysis(self, df: pd.DataFrame, output_path: str = 'data/trend_analysis.png') -> None:
        """
        Create a detailed trend analysis visualization.
        
        Args:
            df: DataFrame containing the data
            output_path: Output path for the analysis
        """
        try:
            self.logger.info("Creating trend analysis visualization")
            
            if df.empty or len(df) < 7:
                self.logger.warning("Insufficient data for trend analysis")
                return
            
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(f'Trend Analysis: {self.config.game_name}', 
                        fontsize=16, fontweight='bold')
            
            # Daily changes
            if 'followers_change' in df.columns:
                axes[0, 0].bar(df['date'], df['followers_change'], 
                              color='#1f77b4', alpha=0.7)
                axes[0, 0].set_title('Daily Follower Changes')
                axes[0, 0].set_ylabel('Change in Followers')
                axes[0, 0].tick_params(axis='x', rotation=45)
            
            if 'mentions_change' in df.columns:
                axes[0, 1].bar(df['date'], df['mentions_change'], 
                              color='#d62728', alpha=0.7)
                axes[0, 1].set_title('Daily Mention Changes')
                axes[0, 1].set_ylabel('Change in Mentions')
                axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Distribution plots
            if 'followers' in df.columns:
                axes[1, 0].hist(df['followers'], bins=20, 
                               color='#1f77b4', alpha=0.7, edgecolor='black')
                axes[1, 0].set_title('Follower Count Distribution')
                axes[1, 0].set_xlabel('Followers')
                axes[1, 0].set_ylabel('Frequency')
            
            if 'mentions' in df.columns:
                axes[1, 1].hist(df['mentions'], bins=20, 
                               color='#d62728', alpha=0.7, edgecolor='black')
                axes[1, 1].set_title('Mention Count Distribution')
                axes[1, 1].set_xlabel('Mentions')
                axes[1, 1].set_ylabel('Frequency')
            
            # Ensure output directory exists
            output_path = Path(output_path)
            ensure_directory(output_path.parent)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            
            self.logger.info(f"Trend analysis saved to {output_path}")
            plt.close(fig)
            
        except Exception as e:
            self.logger.error(f"Error creating trend analysis: {e}")
            if 'fig' in locals():
                plt.close(fig)

