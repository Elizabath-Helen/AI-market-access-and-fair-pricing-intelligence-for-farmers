"""
Caching logic for market data.
"""

import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


class MarketDataCache:
    """
    Handles caching of market data with appropriate TTLs.
    """
    
    @staticmethod
    def get_realtime_prices(cache_key):
        """Get cached real-time prices."""
        return cache.get(cache_key)
    
    @staticmethod
    def set_realtime_prices(cache_key, data):
        """Cache real-time prices with 1-hour TTL."""
        cache.set(cache_key, data, settings.CACHE_TTL_REALTIME)
    
    @staticmethod
    def get_historical_prices(cache_key):
        """Get cached historical prices."""
        return cache.get(cache_key)
    
    @staticmethod
    def set_historical_prices(cache_key, data):
        """Cache historical prices with 24-hour TTL."""
        cache.set(cache_key, data, settings.CACHE_TTL_HISTORICAL)
    
    @staticmethod
    def get_transport_cost(cache_key):
        """Get cached transport cost."""
        return cache.get(cache_key)
    
    @staticmethod
    def set_transport_cost(cache_key, data):
        """Cache transport cost with 7-day TTL."""
        cache.set(cache_key, data, settings.CACHE_TTL_TRANSPORT)
