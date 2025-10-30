"""
Configuration for Stock Analysis System v4.0
Updated with secure API key management via .env file
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# API CONFIGURATION - Loaded from .env file
# ============================================================================

# Financial Modeling Prep API Key
# Get your free key at: https://financialmodelingprep.com/developer/docs/
FMP_API_KEY = os.getenv('FMP_API_KEY', 'YOUR_FMP_API_KEY_HERE')

# Polygon.io API Key (for options data)
# Get your key at: https://polygon.io/dashboard/api-keys
POLYGON_API_KEY = os.getenv('POLYGON_API_KEY', 'YOUR_POLYGON_API_KEY_HERE')

# FinViz Elite API Token
# Get from: https://elite.finviz.com/export.ashx
FINVIZ_API_TOKEN = os.getenv('FINVIZ_API_TOKEN', 'YOUR_FINVIZ_TOKEN_HERE')

# Claude API Key (optional - for AI deep analysis)
# Get from: https://console.anthropic.com/
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY', 'YOUR_CLAUDE_API_KEY_HERE')

# API Rate Limiting
FMP_RATE_LIMIT = {
    'requests_per_minute': 300,  # Free tier: 300/min
    'requests_per_day': 250,     # Free tier: 250/day
    'delay_between_requests': 0.21  # Seconds between requests
}

POLYGON_RATE_LIMIT = {
    'requests_per_second': 100,   # Your tier: 100/sec
    'requests_per_minute': 6000,  # 100/sec * 60 = 6000/min
    'delay_between_requests': 0.01  # Seconds between requests (1/100)
}

# ============================================================================
# ANALYSIS CONFIGURATION v4.0
# ============================================================================

ANALYSIS_CONFIG = {
    # ------------------------------------------------------------------------
    # SCORING WEIGHTS (Must sum to 1.0 = 100%)
    # ------------------------------------------------------------------------
    'weights': {
        # Technical Scores (70%)
        'momentum_score': 0.20,            # 20% - Trend strength & direction
        'volume_score': 0.12,              # 12% - Trading activity & accumulation
        'technical_score': 0.18,           # 18% - Technical indicators & patterns
        'volatility_score': 0.08,          # 8% - Volatility expansion signals
        'relative_strength_score': 0.12,   # 12% - Market/sector outperformance
        'catalyst_score': 0.10,            # 10% - News & event catalysts
        
        # Fundamental Scores (20%)
        'fundamental_quality_score': 0.10, # 10% - Business quality (ROIC, FCF, debt)
        'short_interest_score': 0.05,      # 5% - Short pressure / squeeze potential
        'growth_score': 0.05,              # 5% - Revenue & earnings growth
    },
    
    # Verify weights sum to 1.0
    '_weight_check': lambda w: abs(sum(w.values()) - 1.0) < 0.001,
    
    # ------------------------------------------------------------------------
    # MOMENTUM SCORE CONFIGURATION (26.3%)
    # ------------------------------------------------------------------------
    'momentum': {
        'roc_periods': {
            'short': 5,      # 5-day rate of change
            'medium': 20,    # 20-day rate of change
        },
        'ema_periods': {
            'fast': 20,      # Fast EMA for slope calculation
            'slow': 50,      # Slow EMA for trend alignment
        },
        'slope_lookback': 5,  # Periods for EMA slope calculation
        'weights': {
            'roc_5': 0.30,         # 30% - Short-term momentum
            'roc_20': 0.30,        # 30% - Medium-term momentum
            'ema_slope': 0.20,     # 20% - Trend acceleration
            'vwap_sign': 0.10,     # 10% - Price vs VWAP
            'trend_align': 0.10,   # 10% - EMA alignment
        }
    },
    
    # ------------------------------------------------------------------------
    # VOLUME SCORE CONFIGURATION (15.8%)
    # ------------------------------------------------------------------------
    'volume': {
        'rel_vol_period': 20,        # Period for relative volume (SMA)
        'spike_lookback': 200,       # Historical period for volume percentile
        'cluster_period': 10,        # Bars to check for high-volume cluster
        'cluster_threshold': 1.5,    # RelVol threshold for cluster detection
        'weights': {
            'rel_vol': 0.50,         # 50% - Current vs average volume
            'spike_percentile': 0.30, # 30% - Historical volume ranking
            'hv_cluster': 0.20,      # 20% - Recent accumulation pattern
        }
    },
    
    # ------------------------------------------------------------------------
    # TECHNICAL SCORE CONFIGURATION (21.1%)
    # ------------------------------------------------------------------------
    'technical': {
        'rsi_period': 14,            # RSI calculation period
        'atr_period': 14,            # ATR calculation period
        'atr_lookback': 14,          # Lookback for ATR expansion
        'breakout_period': 20,       # Period for breakout detection
        'ema_periods': [20, 50, 200], # EMAs for stack detection
        'weights': {
            'rsi_divergence': 0.25,  # 25% - RSI divergence signals
            'atr_expansion': 0.25,   # 25% - Volatility expansion
            'ma_stack': 0.25,        # 25% - Moving average alignment
            'breakout_prox': 0.25,   # 25% - Proximity to breakout
        }
    },
    
    # ------------------------------------------------------------------------
    # VOLATILITY SCORE CONFIGURATION (10.5%)
    # ------------------------------------------------------------------------
    'volatility': {
        'atr_period': 14,            # ATR calculation period
        'bb_period': 20,             # Bollinger Band period
        'bb_std': 2.0,               # Bollinger Band standard deviations
        'bb_lookback': 10,           # Lookback for squeeze detection
        'weights': {
            'atr_percent': 0.60,     # 60% - ATR as % of price
            'bb_signal': 0.40,       # 40% - BB squeeze-to-expansion
        }
    },
    
    # ------------------------------------------------------------------------
    # RELATIVE STRENGTH CONFIGURATION (15.8%)
    # ------------------------------------------------------------------------
    'relative_strength': {
        'comparison_period': 5,      # Days for RS calculation
        'spy_symbol': 'SPY',         # Market benchmark
        'chop_threshold': 0.01,      # ±1% for choppy market detection
        'chop_atr_period': 20,       # ATR period for chop detection
        'weights': {
            'vs_spy': 0.60,          # 60% - Outperformance vs SPY
            'vs_sector': 0.40,       # 40% - Outperformance vs sector
        },
        'breadth_adjustment': {
            'normal': 0.5,           # Normal market weighting
            'choppy': 0.7,           # Choppy market weighting (favor RS)
        }
    },
    
    # ------------------------------------------------------------------------
    # CATALYST SCORE CONFIGURATION (10%)
    # ------------------------------------------------------------------------
    'catalyst': {
        'news_window_hours': [24, 72],  # News lookback window
        'earnings_window_days': 3,       # Days before/after earnings
        'earnings_boost': 70,            # Minimum score near earnings
        'pr_bonus': 15,                  # Bonus for major PR
        'negative_cap': 30,              # Cap for negative flags
        'sentiment_keywords': {
            'positive': [
                'beat', 'exceed', 'strong', 'growth', 'upgrade', 
                'breakthrough', 'record', 'surge', 'rally', 'momentum',
                'bullish', 'outperform', 'expansion', 'innovation',
                'partnership', 'acquisition', 'approved', 'launched'
            ],
            'negative': [
                'miss', 'weak', 'decline', 'downgrade', 'concern',
                'investigation', 'probe', 'lawsuit', 'recall', 'cut',
                'bearish', 'underperform', 'loss', 'delay', 'suspended',
                'warning', 'restructuring', 'bankruptcy'
            ],
            'major_positive': [
                'fda approval', 'major contract', 'breakthrough',
                'record earnings', 'strategic partnership'
            ],
            'major_negative': [
                'sec probe', 'guidance cut', 'class action',
                'bankruptcy', 'delisting'
            ]
        }
    },
    
    # ------------------------------------------------------------------------
    # FUNDAMENTAL QUALITY SCORE CONFIGURATION (10%)
    # ------------------------------------------------------------------------
    'fundamental_quality': {
        'metrics': {
            'roic': 0.35,              # Return on Invested Capital weight
            'fcf_yield': 0.35,         # Free Cash Flow Yield weight
            'debt_to_equity': 0.15,    # Debt-to-Equity weight (inverse)
            'eps_stability': 0.15,     # Earnings stability weight (inverse stdev)
        },
        'roic_percentile_refs': [0, 5, 10, 15, 20, 30, 40, 60],
        'fcf_yield_percentile_refs': [0, 2, 4, 6, 8, 10, 15, 25],
        'debt_to_equity_percentile_refs': [0, 0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0],
        'eps_stdev_percentile_refs': [0, 10, 20, 30, 50, 75, 100, 150],
    },
    
    # ------------------------------------------------------------------------
    # SHORT INTEREST SCORE CONFIGURATION (5%)
    # ------------------------------------------------------------------------
    'short_interest': {
        'metrics': {
            'days_to_cover': 0.40,     # Days-to-cover weight (inverse)
            'short_float': 0.40,       # Short % of float weight (inverse)
            'short_change': 0.20,      # 1-month change weight (inverse)
        },
        'days_to_cover_percentile_refs': [0, 1, 2, 3, 5, 7, 10, 15],
        'short_float_percentile_refs': [0, 5, 10, 15, 20, 30, 40, 60],
        'short_change_percentile_refs': [-50, -25, -10, 0, 10, 25, 50, 100],
    },
    
    # ------------------------------------------------------------------------
    # GROWTH SCORE CONFIGURATION (5%)
    # ------------------------------------------------------------------------
    'growth': {
        'metrics': {
            'revenue_growth': 0.40,    # Revenue growth weight
            'eps_growth': 0.40,        # EPS growth weight
            'cagr_5y': 0.20,          # 5-year CAGR weight
        },
        'revenue_growth_percentile_refs': [-10, 0, 5, 10, 15, 25, 40, 60],
        'eps_growth_percentile_refs': [-20, 0, 10, 20, 30, 50, 75, 100],
        'cagr_percentile_refs': [-5, 0, 5, 10, 15, 20, 30, 50],
    },
    
    # ------------------------------------------------------------------------
    # OPTIONS DATA CONFIGURATION (Optional - for enhanced analysis)
    # ------------------------------------------------------------------------
    'options': {
        'enabled': True,               # Enable options data fetching
        'days_to_expiry_min': 14,     # Minimum days to expiration
        'days_to_expiry_max': 60,     # Maximum days to expiration (2 months)
        'strike_range_pct': 10,       # % OTM/ITM to fetch (±10% from current price)
        'min_open_interest': 10,      # Minimum open interest to consider
        'min_volume': 5,              # Minimum daily volume to consider
        'quality_thresholds': {
            'pc_ratio_bullish': 0.7,  # P/C ratio below this = bullish
            'pc_ratio_bearish': 1.3,  # P/C ratio above this = bearish
            'iv_percentile_high': 70, # IV percentile above this = expensive
            'iv_percentile_low': 30,  # IV percentile below this = cheap
        }
    },
    
    # ------------------------------------------------------------------------
    # STOCK FILTERING CRITERIA
    # ------------------------------------------------------------------------
    'filters': {
        'min_price': 2.0,              # Minimum stock price
        'max_price': 10000,            # Maximum stock price
        'min_avg_volume': 100000,      # Minimum average volume
        'min_data_points': 200,        # Minimum historical bars needed
        'exclude_sectors': [],         # Sectors to exclude (if any)
    },
    
    # ------------------------------------------------------------------------
    # DATA REQUIREMENTS
    # ------------------------------------------------------------------------
    'data_requirements': {
        'historical_days': 250,        # Days of historical data to fetch
        'intraday_available': False,   # Whether to use intraday data
        'sector_etf_map': {            # Sector to ETF mapping for RS
            'Technology': 'XLK',
            'Financial Services': 'XLF',
            'Healthcare': 'XLV',
            'Consumer Cyclical': 'XLY',
            'Consumer Defensive': 'XLP',
            'Industrials': 'XLI',
            'Energy': 'XLE',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Basic Materials': 'XLB',
            'Communication Services': 'XLC',
        }
    },
    
    # ------------------------------------------------------------------------
    # OUTPUT CONFIGURATION
    # ------------------------------------------------------------------------
    'output': {
        'directory': 'output',
        'formats': ['csv', 'html', 'txt'],
        'top_n': 10,                   # Number of top picks to highlight
        'decimal_places': 2,           # Decimal precision for scores
    },
    
    # ------------------------------------------------------------------------
    # PERCENTILE CALCULATION
    # ------------------------------------------------------------------------
    'percentile': {
        'method': 'rank',              # Method: 'rank', 'normal', 'uniform'
        'clip_outliers': True,         # Clip extreme outliers
        'outlier_std': 3.0,            # Standard deviations for outlier clipping
    }
}

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validate configuration settings"""
    config = ANALYSIS_CONFIG
    
    # Check weights sum to 1.0
    weights = config['weights']
    total = sum(weights.values())
    assert abs(total - 1.0) < 0.001, f"Weights must sum to 1.0, got {total}"
    
    # Verify we have all 9 scores
    required_scores = [
        'momentum_score', 'volume_score', 'technical_score', 
        'volatility_score', 'relative_strength_score', 'catalyst_score',
        'fundamental_quality_score', 'short_interest_score', 'growth_score'
    ]
    for score in required_scores:
        assert score in weights, f"Missing required score: {score}"
    
    # Check sub-weights sum to 1.0
    for key in ['momentum', 'volume', 'technical', 'volatility']:
        if 'weights' in config[key]:
            sub_total = sum(config[key]['weights'].values())
            assert abs(sub_total - 1.0) < 0.001, f"{key} sub-weights must sum to 1.0, got {sub_total}"
    
    # Check fundamental sub-weights
    for key in ['fundamental_quality', 'short_interest', 'growth']:
        if 'metrics' in config[key]:
            sub_total = sum(config[key]['metrics'].values())
            assert abs(sub_total - 1.0) < 0.001, f"{key} metrics weights must sum to 1.0, got {sub_total}"
    
    # Check API key is set
    assert FMP_API_KEY != "YOUR_FMP_API_KEY_HERE", "Please set your FMP API key in .env file"
    
    # Check Polygon API key if options enabled
    if config['options']['enabled']:
        if POLYGON_API_KEY == "YOUR_POLYGON_API_KEY_HERE":
            print("⚠️  Warning: Options enabled but Polygon API key not set")
            print("   Set POLYGON_API_KEY in your .env file to enable options data")
    
    print("✅ Configuration validated successfully")
    print(f"✅ Total scoring dimensions: {len(weights)}")
    print(f"   - Technical scores: 6 (70%)")
    print(f"   - Fundamental scores: 3 (20%)")
    print(f"   - Options data: {'Enabled' if config['options']['enabled'] else 'Disabled'}")
    print(f"   - Buffer: 10%")
    return True

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_sector_etf(sector: str) -> str:
    """Get sector ETF symbol for relative strength calculation"""
    etf_map = ANALYSIS_CONFIG['data_requirements']['sector_etf_map']
    return etf_map.get(sector, 'SPY')  # Default to SPY if sector not found

def get_weight(score_type: str) -> float:
    """Get weight for a score type"""
    return ANALYSIS_CONFIG['weights'].get(score_type, 0.0)

def get_config(section: str, key: str = None):
    """Get configuration value"""
    config = ANALYSIS_CONFIG.get(section, {})
    if key:
        return config.get(key)
    return config

# Run validation when imported
if __name__ == "__main__":
    try:
        validate_config()
    except AssertionError as e:
        print(f"❌ Configuration error: {e}")
