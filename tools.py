import random
import time
from typing import Dict, Any

def fetch_mock_marketdata(symbol: str) -> Dict[str, Any]:
    """
    Mock function to fetch market data for a given symbol.
    Returns mock price data that would typically come from an API.
    """
    # Simulate API delay
    time.sleep(0.5)
    
    # Mock price
    base_prices = {
        "SOL": 100.0,
        "BTC": 45000.0,
        "ETH": 2500.0,
        "ADA": 0.5,
        "DOT": 8.0
    }
    
    base_price = base_prices.get(symbol.upper(), 50.0)
    
    # Generate mock OHLCV data
    mock_data = {
        "symbol": symbol.upper(),
        "price": round(base_price * (1 + random.uniform(-0.1, 0.1)), 2),
        "open": round(base_price * (1 + random.uniform(-0.05, 0.05)), 2),
        "high": round(base_price * (1 + random.uniform(0.0, 0.15)), 2),
        "low": round(base_price * (1 + random.uniform(-0.15, 0.0)), 2),
        "volume": random.randint(1000000, 10000000),
        "market_cap": random.randint(1000000000, 100000000000),
        "timestamp": int(time.time()),
        "24h_change": round(random.uniform(-15.0, 15.0), 2)
    }
    
    return mock_data

def secret_indicator(market_data: Dict[str, Any]) -> float:
    """
    Mock secret indicator calculation.
    This is a proprietary trading indicator that takes market data and returns a score.
    Higher scores indicate better buying opportunities.
    """
    if not market_data:
        raise ValueError("Market data is required for secret indicator calculation")
    
    price = market_data.get("price", 0)
    volume = market_data.get("volume", 0)
    market_cap = market_data.get("market_cap", 0)
    change_24h = market_data.get("24h_change", 0)
    
    # Mock secret formula (obviously not a real indicator 💀)
    volume_factor = (volume / 1000000) * 0.1
    price_momentum = abs(change_24h) * 0.05
    market_cap_factor = (market_cap / 1000000000) * 0.02
    
    secret_multiplier = random.uniform(0.8, 1.2)
    
    indicator_score = (volume_factor + price_momentum + market_cap_factor) * secret_multiplier
    
    # Normalize to 0-100 scale
    normalized_score = min(100, max(0, indicator_score * 10))
    
    return round(normalized_score, 2) 