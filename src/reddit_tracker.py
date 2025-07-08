"""
Reddit Tracker Module
=====================

Professional implementation for tracking mentions of a game on Reddit.
Utilizes the Reddit API with async support and retries.
"""

import logging
from datetime import timedelta
from typing import List, Dict, Any
import aiohttp

from .config import Config
from .utils import retry_with_backoff, get_date_range


class RedditTracker:
    """Professional implementation for tracking Reddit mentions of a game."""
    
    def __init__(self, config: Config):
        """
        Initialize Reddit tracker with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.logger = logging.getLogger('SteamGameTracker.Reddit')
        self.session = None
        
        self.api_url = "https://www.reddit.com/search.json"
        self.headers = {
            "User-Agent": self.config.reddit_user_agent,
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    @retry_with_backoff(max_retries=3, base_delay=1.0)
    async def _fetch_reddit_posts(self, query: str, after: str) -> List[Dict[str, Any]]:
        """
        Fetch Reddit posts with specified query and time period.
        
        Args:
            query: Search query for posts
            after: Time period parameter
        
        Returns:
            List of posts found
        """
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
        
        params = {
            "q": query,
            "sort": "new",
            "restrict_sr": "on",
            "limit": 100,
            "after": after
        }

        try:
            async with self.session.get(self.api_url, params=params, timeout=30) as response:
                response.raise_for_status()
                data = await response.json()
                if data and 'data' in data:
                    return data.get('data', {}).get('children', [])
                else:
                    self.logger.warning("No data found in Reddit response")
                    return []
        except Exception as e:
            self.logger.error(f"Error fetching Reddit posts: {e}")
            # Return empty list instead of raising to allow graceful fallback
            return []

    async def get_mentions(self) -> List[Dict[str, Any]]:
        """
        Get mentions of the game on Reddit within the tracking period.
        
        Returns:
            List of dictionaries containing date and mention count
        """
        self.logger.info(f"Fetching mentions for '{self.config.game_name}' from Reddit")

        mentions = []
        start_date, end_date = get_date_range(self.config.tracking_days)
        after = int(start_date.timestamp())
        
        while start_date <= end_date:
            query = f'title:"{self.config.game_name}"'
            posts = await self._fetch_reddit_posts(query, str(after))
            count = len(posts)

            mentions.append({
                'date': start_date.strftime('%Y-%m-%d'),
                'mentions': count,
                'source': 'reddit'
            })

            self.logger.info(f"{count} mentions found on {start_date.strftime('%Y-%m-%d')}")

            start_date += timedelta(days=1)
            after = int(start_date.timestamp())

        return mentions

