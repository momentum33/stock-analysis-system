"""
Enhanced Pre-Screening System
Filters stocks before expensive Claude analysis to save API costs
Only passes high-quality candidates that meet all criteria
"""

from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import config


class PreScreener:
    """Enhanced filtering before Claude analysis"""
    
    def __init__(self, fmp_client, polygon_client=None):
        """Initialize pre-screener with API clients"""
        self.fmp_client = fmp_client
        self.polygon_client = polygon_client
        
        # Default thresholds (can be customized)
        self.min_score = getattr(config, 'PRESCREEN_MIN_SCORE', 5.0)
        self.min_volume_ratio = getattr(config, 'PRESCREEN_MIN_VOLUME_RATIO', 0.8)
        self.min_options_volume = getattr(config, 'PRESCREEN_MIN_OPTIONS_VOLUME', 100)
        self.require_recent_news = getattr(config, 'PRESCREEN_REQUIRE_NEWS', True)
        self.news_days_back = getattr(config, 'PRESCREEN_NEWS_DAYS', 7)
        self.avoid_earnings_within_days = getattr(config, 'PRESCREEN_AVOID_EARNINGS', None)
        self.target_earnings_window = getattr(config, 'PRESCREEN_TARGET_EARNINGS', None)  # (min_days, max_days)
        
        print(f"📋 Pre-Screening Thresholds:")
        print(f"   Min Score: {self.min_score}")
        print(f"   Min Volume Ratio: {self.min_volume_ratio}x")
        print(f"   Min Options Volume: {self.min_options_volume:,}")
        print(f"   Require Recent News: {self.require_recent_news}")
        if self.avoid_earnings_within_days:
            print(f"   Avoid Earnings Within: {self.avoid_earnings_within_days} days")
        if self.target_earnings_window:
            print(f"   Target Earnings Window: {self.target_earnings_window[0]}-{self.target_earnings_window[1]} days")
    
    def apply_filters(self, stocks: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        Apply all pre-screening filters
        
        Returns:
            (filtered_stocks, filter_stats)
        """
        print(f"\n{'='*80}")
        print(f"PRE-SCREENING: Filtering {len(stocks)} stocks")
        print(f"{'='*80}\n")
        
        stats = {
            'total': len(stocks),
            'passed': 0,
            'failed_score': 0,
            'failed_volume': 0,
            'failed_options': 0,
            'failed_news': 0,
            'failed_earnings': 0,
            'reasons': {}
        }
        
        passed_stocks = []
        
        for stock in stocks:
            reasons = []
            
            # Filter 1: Minimum quantitative score
            if stock['total_score'] < self.min_score:
                reasons.append(f"Low score ({stock['total_score']:.2f} < {self.min_score})")
                stats['failed_score'] += 1
            
            # Filter 2: Volume requirement
            volume_ratio = stock.get('metrics', {}).get('volume_ratio', 0)
            if volume_ratio < self.min_volume_ratio:
                reasons.append(f"Low volume ({volume_ratio:.2f}x < {self.min_volume_ratio}x)")
                stats['failed_volume'] += 1
            
            # Filter 3: Options liquidity (if options enabled and data available)
            if config.ENABLE_OPTIONS_ANALYSIS and stock.get('options_analysis'):
                options = stock['options_analysis']
                total_vol = options.get('total_call_volume', 0) + options.get('total_put_volume', 0)
                
                if total_vol < self.min_options_volume:
                    reasons.append(f"Low options volume ({total_vol} < {self.min_options_volume})")
                    stats['failed_options'] += 1
            
            # Filter 4: Recent news requirement
            if self.require_recent_news:
                has_recent_news = self._check_recent_news(stock['symbol'])
                if not has_recent_news:
                    reasons.append(f"No news in {self.news_days_back} days")
                    stats['failed_news'] += 1
            
            # Filter 5: Earnings timing filter
            if self.avoid_earnings_within_days or self.target_earnings_window:
                earnings_status = self._check_earnings_timing(stock['symbol'])
                if earnings_status:
                    reasons.append(earnings_status)
                    stats['failed_earnings'] += 1
            
            # If no reasons, stock passes
            if not reasons:
                passed_stocks.append(stock)
                stats['passed'] += 1
                print(f"✅ {stock['symbol']:6} - PASSED (Score: {stock['total_score']:.2f})")
            else:
                print(f"❌ {stock['symbol']:6} - FILTERED: {', '.join(reasons)}")
                
                # Track reasons
                for reason in reasons:
                    stats['reasons'][reason] = stats['reasons'].get(reason, 0) + 1
        
        # Print summary
        print(f"\n{'='*80}")
        print(f"PRE-SCREENING RESULTS")
        print(f"{'='*80}")
        print(f"Total Stocks: {stats['total']}")
        print(f"✅ Passed: {stats['passed']} ({stats['passed']/stats['total']*100:.1f}%)")
        print(f"❌ Filtered: {stats['total'] - stats['passed']} ({(stats['total']-stats['passed'])/stats['total']*100:.1f}%)")
        print(f"\nFilter Breakdown:")
        print(f"  • Low Score: {stats['failed_score']}")
        print(f"  • Low Volume: {stats['failed_volume']}")
        print(f"  • Low Options Volume: {stats['failed_options']}")
        print(f"  • No Recent News: {stats['failed_news']}")
        print(f"  • Earnings Timing: {stats['failed_earnings']}")
        
        # Cost savings estimate
        filtered_count = stats['total'] - stats['passed']
        estimated_savings = filtered_count * 0.35  # ~$0.35 per stock with Claude
        print(f"\n💰 Estimated Savings: ${estimated_savings:.2f} (filtered {filtered_count} stocks)")
        print(f"{'='*80}\n")
        
        return passed_stocks, stats
    
    def _check_recent_news(self, ticker: str) -> bool:
        """Check if stock has recent news articles"""
        try:
            news = self.fmp_client.get_stock_news(ticker, limit=20)
            if not news:
                return False
            
            # Check for news within specified days
            cutoff_date = datetime.now() - timedelta(days=self.news_days_back)
            
            for article in news:
                pub_date_str = article.get('publishedDate', '')
                if pub_date_str:
                    try:
                        pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                        if pub_date >= cutoff_date:
                            return True
                    except:
                        continue
            
            return False
        except:
            # On error, don't filter out (benefit of doubt)
            return True
    
    def _check_earnings_timing(self, ticker: str) -> str:
        """
        Check earnings date and return filter reason if should be filtered
        
        Returns:
            None if passes, or string reason if should be filtered
        """
        try:
            # Get earnings calendar
            earnings = self.fmp_client.get_earnings_calendar(ticker)
            if not earnings or len(earnings) == 0:
                return None  # No earnings data, don't filter
            
            # Get next earnings date
            next_earnings_str = earnings[0].get('date', '')
            if not next_earnings_str:
                return None
            
            next_earnings = datetime.strptime(next_earnings_str, '%Y-%m-%d')
            days_until = (next_earnings - datetime.now()).days
            
            # Filter if earnings too soon (avoid)
            if self.avoid_earnings_within_days and 0 <= days_until <= self.avoid_earnings_within_days:
                return f"Earnings in {days_until} days (too soon)"
            
            # Filter if earnings outside target window
            if self.target_earnings_window:
                min_days, max_days = self.target_earnings_window
                if not (min_days <= days_until <= max_days):
                    if days_until < min_days:
                        return f"Earnings in {days_until} days (too soon, want {min_days}-{max_days})"
                    else:
                        return f"Earnings in {days_until} days (too far, want {min_days}-{max_days})"
            
            return None  # Passes all earnings checks
            
        except Exception as e:
            # On error, don't filter (benefit of doubt)
            return None
    
    def get_quality_score(self, stock: Dict) -> float:
        """
        Calculate a 'quality score' for ranking stocks
        Higher is better for Claude analysis
        
        Factors:
        - Quantitative score (50%)
        - Volume quality (20%)
        - Options liquidity (15%)
        - News recency (10%)
        - Technical momentum (5%)
        """
        score = 0.0
        
        # Quant score (0-10) -> 0-50 points
        score += stock['total_score'] * 5
        
        # Volume ratio (0.5-2.0) -> 0-20 points
        volume_ratio = stock.get('metrics', {}).get('volume_ratio', 1.0)
        volume_points = min((volume_ratio - 0.5) / 1.5 * 20, 20)
        score += max(volume_points, 0)
        
        # Options volume (0-10000) -> 0-15 points
        if stock.get('options_analysis'):
            options_vol = (stock['options_analysis'].get('total_call_volume', 0) + 
                          stock['options_analysis'].get('total_put_volume', 0))
            options_points = min(options_vol / 10000 * 15, 15)
            score += options_points
        
        # News recency -> 0-10 points
        if self._check_recent_news(stock['symbol']):
            score += 10
        
        # Momentum (RSI proximity to sweet spot) -> 0-5 points
        rsi = stock.get('metrics', {}).get('rsi_14', 50)
        # Ideal RSI: 50-60 (bullish but not overbought)
        if 50 <= rsi <= 60:
            score += 5
        elif 45 <= rsi < 50 or 60 < rsi <= 65:
            score += 3
        elif 40 <= rsi < 45 or 65 < rsi <= 70:
            score += 1
        
        return score
    
    def rank_by_quality(self, stocks: List[Dict]) -> List[Dict]:
        """Rank stocks by quality score for optimal Claude usage"""
        print("\n📊 Ranking stocks by analysis quality...")
        
        for stock in stocks:
            stock['quality_score'] = self.get_quality_score(stock)
        
        ranked = sorted(stocks, key=lambda x: x['quality_score'], reverse=True)
        
        print("\nTop candidates for deep analysis:")
        for i, stock in enumerate(ranked[:10], 1):
            print(f"  {i}. {stock['symbol']:6} - Quality: {stock['quality_score']:.1f} "
                  f"(Quant: {stock['total_score']:.2f}, Vol: {stock.get('metrics', {}).get('volume_ratio', 0):.2f}x)")
        
        return ranked


def create_default_config_additions():
    """
    Returns config additions for pre-screening
    Add these to your config.py
    """
    return """
# Pre-Screening Configuration
# These filters run BEFORE Claude analysis to save API costs

# Minimum quantitative score to qualify for deep analysis
PRESCREEN_MIN_SCORE = 5.0  # Only analyze stocks scoring 5.0 or higher

# Minimum volume ratio (current volume / average volume)
PRESCREEN_MIN_VOLUME_RATIO = 0.8  # Must have at least 80% of normal volume

# Minimum options volume (if using options strategies)
PRESCREEN_MIN_OPTIONS_VOLUME = 100  # Total call + put volume

# Require recent news?
PRESCREEN_REQUIRE_NEWS = True  # Only analyze stocks with recent catalysts
PRESCREEN_NEWS_DAYS = 7  # News must be within last 7 days

# Earnings timing filters (set to None to disable)
PRESCREEN_AVOID_EARNINGS = None  # e.g., 2 = avoid if earnings within 2 days
PRESCREEN_TARGET_EARNINGS = (14, 35)  # e.g., (14, 35) = only if earnings in 2-5 weeks

# Examples:
# Conservative (fewer stocks, higher quality):
#   PRESCREEN_MIN_SCORE = 6.5
#   PRESCREEN_MIN_VOLUME_RATIO = 1.2
#   PRESCREEN_REQUIRE_NEWS = True
#
# Aggressive (more stocks, lower bar):
#   PRESCREEN_MIN_SCORE = 4.0
#   PRESCREEN_MIN_VOLUME_RATIO = 0.5
#   PRESCREEN_REQUIRE_NEWS = False
"""


if __name__ == "__main__":
    # Print default config
    print("Add these settings to your config.py:\n")
    print(create_default_config_additions())
