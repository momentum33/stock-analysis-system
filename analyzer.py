"""
Stock Analyzer v4.0 - Advanced Scoring System
Implements sophisticated technical analysis with percentile-based scoring
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import config

class StockAnalyzer:
    """Advanced stock analysis with multi-dimensional scoring"""
    
    def __init__(self):
        self.config = config.ANALYSIS_CONFIG
        self.weights = self.config['weights']
        
    # ========================================================================
    # MAIN ANALYSIS FUNCTION
    # ========================================================================
    
    def analyze_stock(self, data: Dict) -> Dict:
        """
        Perform complete analysis on a stock
        
        Args:
            data: Dictionary containing:
                - historical: List of OHLCV dictionaries
                - profile: Company profile
                - news: List of news articles
                - spy_data: SPY historical data for RS calculation
                - sector_data: Sector ETF data for RS calculation
                - financials: Financial ratios and metrics (for fundamental scores)
        
        Returns:
            Dictionary with all scores and metrics
        """
        if not self._validate_data(data):
            return None
        
        # Calculate all scores
        scores = {}
        
        # Technical scores (70%)
        scores['momentum_score'] = self.calculate_momentum_score(data)
        scores['volume_score'] = self.calculate_volume_score(data)
        scores['technical_score'] = self.calculate_technical_score(data)
        scores['volatility_score'] = self.calculate_volatility_score(data)
        scores['relative_strength_score'] = self.calculate_relative_strength_score(data)
        scores['catalyst_score'] = self.calculate_catalyst_score(data)
        
        # Fundamental scores (20%)
        scores['fundamental_quality_score'] = self.calculate_fundamental_quality_score(data)
        scores['short_interest_score'] = self.calculate_short_interest_score(data)
        scores['growth_score'] = self.calculate_growth_score(data)
        scores['options_score'] = self.calculate_options_score(data)
        
        # Calculate composite score
        composite = sum(scores[k] * self.weights[k] for k in scores.keys())
        scores['composite_score'] = composite
        
        # Add supporting metrics for reporting
        scores['metrics'] = self._extract_metrics(data)
        
        return scores
    
    # ========================================================================
    # 1. MOMENTUM SCORE (26.3%)
    # ========================================================================
    
    def calculate_momentum_score(self, data: Dict) -> float:
        """
        Momentum = 0.30*ROC(5) + 0.30*ROC(20) + 0.20*EMA_slope + 0.10*VWAP_sign + 0.10*Trend_align
        All converted to 0-100 scale using percentiles
        """
        hist = data['historical']
        closes = np.array([d['close'] for d in hist])
        volumes = np.array([d['volume'] for d in hist])
        highs = np.array([d['high'] for d in hist])
        lows = np.array([d['low'] for d in hist])
        
        cfg = self.config['momentum']
        
        # 1. ROC(5) - 5-day rate of change
        roc5 = (closes[-1] / closes[-6] - 1) * 100 if len(closes) > 5 else 0
        roc5_pct = self._to_percentile(roc5, [-10, -5, -2, 0, 2, 5, 10, 20])
        
        # 2. ROC(20) - 20-day rate of change
        roc20 = (closes[-1] / closes[-21] - 1) * 100 if len(closes) > 20 else 0
        roc20_pct = self._to_percentile(roc20, [-20, -10, -5, 0, 5, 10, 20, 40])
        
        # 3. EMA(20) slope - trend acceleration
        ema20 = self._calculate_ema(closes, 20)
        if len(ema20) > cfg['slope_lookback']:
            ema_slope = ((ema20[-1] - ema20[-cfg['slope_lookback']-1]) / closes[-1]) * 100
            ema_slope_pct = self._to_percentile(ema_slope, [-2, -1, -0.5, 0, 0.5, 1, 2, 4])
        else:
            ema_slope_pct = 50
        
        # 4. VWAP deviation sign - price position vs VWAP
        vwap = self._calculate_vwap(highs, lows, closes, volumes)
        vwap_sign = 100 if closes[-1] > vwap else 0
        
        # 5. Trend alignment - EMA hierarchy
        ema20_val = ema20[-1]
        ema50 = self._calculate_ema(closes, 50)
        ema50_val = ema50[-1] if len(ema50) > 0 else ema20_val
        
        trend_align = 100 if (closes[-1] > ema20_val > ema50_val) else 0
        
        # Combine with weights
        w = cfg['weights']
        momentum_score = (
            w['roc_5'] * roc5_pct +
            w['roc_20'] * roc20_pct +
            w['ema_slope'] * ema_slope_pct +
            w['vwap_sign'] * vwap_sign +
            w['trend_align'] * trend_align
        )
        
        return np.clip(momentum_score / 10, 0, 10)  # Scale to 0-10
    
    # ========================================================================
    # 2. VOLUME SCORE (15.8%)
    # ========================================================================
    
    def calculate_volume_score(self, data: Dict) -> float:
        """
        Volume = 0.50*RelVol + 0.30*VolSpike_pct + 0.20*HV_cluster
        """
        hist = data['historical']
        volumes = np.array([d['volume'] for d in hist])
        
        cfg = self.config['volume']
        
        # 1. Relative Volume (current vs 20-day average)
        if len(volumes) > cfg['rel_vol_period']:
            sma_vol = np.mean(volumes[-cfg['rel_vol_period']-1:-1])
            rel_vol = volumes[-1] / sma_vol if sma_vol > 0 else 1.0
            rel_vol_pct = self._to_percentile(rel_vol, [0.5, 0.7, 0.9, 1.0, 1.2, 1.5, 2.0, 3.0])
        else:
            rel_vol_pct = 50
        
        # 2. Volume Spike Percentile (200-bar history)
        lookback = min(cfg['spike_lookback'], len(volumes))
        if lookback > 20:
            recent_volumes = volumes[-lookback:]
            vol_percentile = (np.sum(recent_volumes < volumes[-1]) / len(recent_volumes)) * 100
        else:
            vol_percentile = 50
        
        # 3. High-Volume Cluster (last 10 bars with RelVol > 1.5)
        if len(volumes) > cfg['cluster_period'] + cfg['rel_vol_period']:
            cluster_count = 0
            for i in range(cfg['cluster_period']):
                idx = -(i+1)
                period_start = idx - cfg['rel_vol_period']
                period_vol = volumes[period_start:idx] if period_start > -len(volumes) else volumes[:idx]
                if len(period_vol) > 0:
                    avg_vol = np.mean(period_vol)
                    if volumes[idx] / avg_vol > cfg['cluster_threshold']:
                        cluster_count += 1
            
            hv_cluster = (cluster_count / cfg['cluster_period']) * 100
            hv_cluster_pct = self._to_percentile(hv_cluster, [0, 10, 20, 30, 40, 50, 60, 80])
        else:
            hv_cluster_pct = 50
        
        # Combine with weights
        w = cfg['weights']
        volume_score = (
            w['rel_vol'] * rel_vol_pct +
            w['spike_percentile'] * vol_percentile +
            w['hv_cluster'] * hv_cluster_pct
        )
        
        return np.clip(volume_score / 10, 0, 10)
    
    # ========================================================================
    # 3. TECHNICAL SCORE (21.1%)
    # ========================================================================
    
    def calculate_technical_score(self, data: Dict) -> float:
        """
        Technical = 0.25*RSI_div + 0.25*ATR_exp + 0.25*MA_stack + 0.25*Breakout_prox
        """
        hist = data['historical']
        closes = np.array([d['close'] for d in hist])
        highs = np.array([d['high'] for d in hist])
        lows = np.array([d['low'] for d in hist])
        
        cfg = self.config['technical']
        
        # 1. RSI Divergence
        rsi = self._calculate_rsi(closes, cfg['rsi_period'])
        rsi_div_score = self._detect_rsi_divergence(closes, rsi)
        
        # 2. ATR Expansion
        atr = self._calculate_atr(highs, lows, closes, cfg['atr_period'])
        if len(atr) > cfg['atr_lookback']:
            atr_expansion = atr[-1] / atr[-cfg['atr_lookback']-1] if atr[-cfg['atr_lookback']-1] > 0 else 1.0
            atr_exp_pct = self._to_percentile(atr_expansion, [0.8, 0.9, 0.95, 1.0, 1.05, 1.1, 1.2, 1.5])
        else:
            atr_exp_pct = 50
        
        # 3. MA Stack
        ema20 = self._calculate_ema(closes, 20)
        ema50 = self._calculate_ema(closes, 50)
        ema200 = self._calculate_ema(closes, 200)
        
        ma_stack = self._calculate_ma_stack(closes[-1], 
                                           ema20[-1] if len(ema20) > 0 else closes[-1],
                                           ema50[-1] if len(ema50) > 0 else closes[-1],
                                           ema200[-1] if len(ema200) > 0 else closes[-1])
        
        # 4. Breakout Proximity
        breakout_prox = self._calculate_breakout_proximity(closes, highs, lows, cfg['breakout_period'])
        breakout_prox_pct = self._to_percentile(breakout_prox, [-20, -10, -5, 0, 5, 10, 20, 40])
        
        # Combine with weights
        w = cfg['weights']
        technical_score = (
            w['rsi_divergence'] * rsi_div_score +
            w['atr_expansion'] * atr_exp_pct +
            w['ma_stack'] * ma_stack +
            w['breakout_prox'] * breakout_prox_pct
        )
        
        return np.clip(technical_score / 10, 0, 10)
    
    # ========================================================================
    # 4. VOLATILITY SCORE (10.5%)
    # ========================================================================
    
    def calculate_volatility_score(self, data: Dict) -> float:
        """
        Volatility = 0.60*ATR% + 0.40*BB_signal
        Favors expansion after compression (squeeze setups)
        """
        hist = data['historical']
        closes = np.array([d['close'] for d in hist])
        highs = np.array([d['high'] for d in hist])
        lows = np.array([d['low'] for d in hist])
        
        cfg = self.config['volatility']
        
        # 1. ATR as percentage of price
        atr = self._calculate_atr(highs, lows, closes, cfg['atr_period'])
        if len(atr) > 0 and closes[-1] > 0:
            atr_percent = (atr[-1] / closes[-1]) * 100
            atr_pct = self._to_percentile(atr_percent, [1, 2, 3, 4, 5, 6, 8, 12])
        else:
            atr_pct = 50
        
        # 2. Bollinger Band squeeze-to-expansion signal
        bb_width = self._calculate_bb_width(closes, cfg['bb_period'], cfg['bb_std'])
        
        if len(bb_width) > cfg['bb_lookback']:
            # Current BB width percentile
            bb_pct_today = (np.sum(bb_width[:-1] < bb_width[-1]) / len(bb_width[:-1])) * 100
            
            # Historical BB width percentile 10 bars ago
            bb_pct_prior = (np.sum(bb_width[:-cfg['bb_lookback']-1] < bb_width[-cfg['bb_lookback']-1]) / 
                           len(bb_width[:-cfg['bb_lookback']-1])) * 100 if len(bb_width) > cfg['bb_lookback']+1 else 50
            
            # Squeeze-to-expansion signal (rising from low)
            bb_signal = np.clip((bb_pct_today - bb_pct_prior) * 0.5 + 50, 0, 100)
        else:
            bb_signal = 50
        
        # Combine with weights
        w = cfg['weights']
        volatility_score = (
            w['atr_percent'] * atr_pct +
            w['bb_signal'] * bb_signal
        )
        
        return np.clip(volatility_score / 10, 0, 10)
    
    # ========================================================================
    # 5. RELATIVE STRENGTH SCORE (15.8%)
    # ========================================================================
    
    def calculate_relative_strength_score(self, data: Dict) -> float:
        """
        RelStr = Adj*(0.6*vs_SPY + 0.4*vs_Sector) + (1-Adj)*0.5*(vs_SPY + vs_Sector)
        With breadth adjustment for choppy markets
        """
        hist = data['historical']
        spy_hist = data.get('spy_data', [])
        sector_hist = data.get('sector_data', [])
        
        cfg = self.config['relative_strength']
        period = cfg['comparison_period']
        
        if len(hist) < period or len(spy_hist) < period:
            return 5.0  # Neutral score if insufficient data
        
        # Calculate stock ROC
        stock_closes = np.array([d['close'] for d in hist])
        stock_roc = (stock_closes[-1] / stock_closes[-period-1] - 1) * 100
        
        # Calculate SPY ROC
        spy_closes = np.array([d['close'] for d in spy_hist])
        spy_roc = (spy_closes[-1] / spy_closes[-period-1] - 1) * 100
        
        # Calculate vs SPY
        vs_spy = stock_roc - spy_roc
        vs_spy_pct = self._to_percentile(vs_spy, [-10, -5, -2, 0, 2, 5, 10, 20])
        
        # Calculate vs Sector (if available)
        if len(sector_hist) >= period:
            sector_closes = np.array([d['close'] for d in sector_hist])
            sector_roc = (sector_closes[-1] / sector_closes[-period-1] - 1) * 100
            vs_sector = stock_roc - sector_roc
            vs_sector_pct = self._to_percentile(vs_sector, [-10, -5, -2, 0, 2, 5, 10, 20])
        else:
            vs_sector_pct = vs_spy_pct  # Fallback to vs SPY
        
        # Detect choppy market (adjust weighting)
        spy_roc_20d = (spy_closes[-1] / spy_closes[-21] - 1) * 100 if len(spy_closes) > 20 else 0
        spy_highs = np.array([d['high'] for d in spy_hist])
        spy_lows = np.array([d['low'] for d in spy_hist])
        spy_atr = self._calculate_atr(spy_highs, spy_lows, spy_closes, cfg['chop_atr_period'])
        
        # Check if market is choppy (low ROC + rising ATR)
        is_choppy = (abs(spy_roc_20d) < cfg['chop_threshold'] * 100 and 
                    len(spy_atr) > 10 and spy_atr[-1] > spy_atr[-11])
        
        adj = cfg['breadth_adjustment']['choppy'] if is_choppy else cfg['breadth_adjustment']['normal']
        
        # Calculate relative strength with adjustment
        w = cfg['weights']
        rs_score = (
            adj * (w['vs_spy'] * vs_spy_pct + w['vs_sector'] * vs_sector_pct) +
            (1 - adj) * 0.5 * (vs_spy_pct + vs_sector_pct)
        )
        
        return np.clip(rs_score / 10, 0, 10)
    
    # ========================================================================
    # 6. CATALYST SCORE (10.5%)
    # ========================================================================
    
    def calculate_catalyst_score(self, data: Dict) -> float:
        """
        Catalyst = News sentiment with earnings window, PR bonuses, and negative flags
        """
        news = data.get('news', [])
        profile = data.get('profile', {})
        
        cfg = self.config['catalyst']
        
        # 1. Base news sentiment
        sentiment_score = self._calculate_news_sentiment(news, cfg)
        
        # 2. Earnings window boost
        earnings_date = profile.get('next_earnings_date')
        if earnings_date:
            days_to_earnings = self._days_until(earnings_date)
            if abs(days_to_earnings) <= cfg['earnings_window_days']:
                sentiment_score = max(sentiment_score, cfg['earnings_boost'])
        
        # 3. Major PR bonus
        has_major_pr = self._check_major_news(news, cfg['sentiment_keywords']['major_positive'])
        if has_major_pr:
            sentiment_score = min(sentiment_score + cfg['pr_bonus'], 100)
        
        # 4. Negative flags (cap score)
        has_negative = self._check_major_news(news, cfg['sentiment_keywords']['major_negative'])
        if has_negative:
            sentiment_score = min(sentiment_score, cfg['negative_cap'])
        
        return np.clip(sentiment_score / 10, 0, 10)
    
    # ========================================================================
    # 7. FUNDAMENTAL QUALITY SCORE (10%)
    # ========================================================================
    
    def calculate_fundamental_quality_score(self, data: Dict) -> float:
        """
        FundQuality = 0.35*ROIC + 0.35*FCF_Yield + 0.15*(100-Debt/Eq) + 0.15*(100-EPS_stdev)
        """
        financials = data.get('financials', {})
        
        if not financials:
            return 5.0  # Neutral if no data
        
        cfg = self.config['fundamental_quality']
        weights = cfg['metrics']
        
        # 1. ROIC (Return on Invested Capital) - higher is better
        roic = financials.get('roic', 0)
        roic_pct = self._to_percentile(roic, cfg['roic_percentile_refs'])
        
        # 2. FCF Yield (Free Cash Flow / Market Cap) - higher is better
        fcf_yield = financials.get('fcf_yield', 0)
        fcf_pct = self._to_percentile(fcf_yield, cfg['fcf_yield_percentile_refs'])
        
        # 3. Debt-to-Equity - lower is better (inverse percentile)
        debt_to_equity = financials.get('debt_to_equity', 1.0)
        debt_pct = self._to_percentile(debt_to_equity, cfg['debt_to_equity_percentile_refs'])
        debt_score = 100 - debt_pct  # Inverse (lower debt = higher score)
        
        # 4. EPS Stability (stdev of TTM EPS growth) - lower volatility is better
        eps_stdev = financials.get('eps_stability', 50)
        eps_stdev_pct = self._to_percentile(eps_stdev, cfg['eps_stdev_percentile_refs'])
        eps_stability_score = 100 - eps_stdev_pct  # Inverse (lower stdev = higher score)
        
        # Combine with weights
        fund_quality = (
            weights['roic'] * roic_pct +
            weights['fcf_yield'] * fcf_pct +
            weights['debt_to_equity'] * debt_score +
            weights['eps_stability'] * eps_stability_score
        )
        
        return np.clip(fund_quality / 10, 0, 10)
    
    # ========================================================================
    # 8. SHORT INTEREST SCORE (5%)
    # ========================================================================
    
    def calculate_short_interest_score(self, data: Dict) -> float:
        """
        ShortInt = 0.4*(100-DaysToCover) + 0.4*(100-ShortFloat) + 0.2*(100-Î”Short)
        Higher score = lower short pressure / potential squeeze
        """
        short_data = data.get('short_interest', {})
        
        if not short_data:
            return 5.0  # Neutral if no data
        
        cfg = self.config['short_interest']
        weights = cfg['metrics']
        
        # 1. Days to Cover (Short Interest / Avg Daily Volume) - lower is better
        days_to_cover = short_data.get('days_to_cover', 3)
        dtc_pct = self._to_percentile(days_to_cover, cfg['days_to_cover_percentile_refs'])
        dtc_score = 100 - dtc_pct  # Inverse (lower = less pressure = higher score)
        
        # 2. Short Float % - lower is better (less bearish pressure)
        short_float = short_data.get('short_float_percent', 10)
        sf_pct = self._to_percentile(short_float, cfg['short_float_percentile_refs'])
        sf_score = 100 - sf_pct  # Inverse
        
        # 3. Change in Short Interest (1 month) - decreasing shorts = bullish
        short_change = short_data.get('short_change_1m', 0)
        sc_pct = self._to_percentile(short_change, cfg['short_change_percentile_refs'])
        sc_score = 100 - sc_pct  # Inverse (decreasing shorts = higher score)
        
        # Combine with weights
        short_score = (
            weights['days_to_cover'] * dtc_score +
            weights['short_float'] * sf_score +
            weights['short_change'] * sc_score
        )
        
        return np.clip(short_score / 10, 0, 10)
    
    # ========================================================================
    # 9. GROWTH SCORE (5%)
    # ========================================================================
    
    def calculate_growth_score(self, data: Dict) -> float:
        """
        Growth = 0.4*RevGrowth + 0.4*EPSGrowth + 0.2*CAGR
        """
        growth_data = data.get('growth_metrics', {})
        
        if not growth_data:
            return 5.0  # Neutral if no data
        
        cfg = self.config['growth']
        weights = cfg['metrics']
        
        # 1. Revenue Growth (1 year) - higher is better
        rev_growth = growth_data.get('revenue_growth_1y', 0)
        rev_pct = self._to_percentile(rev_growth, cfg['revenue_growth_percentile_refs'])
        
        # 2. EPS Growth (1 year) - higher is better
        eps_growth = growth_data.get('eps_growth_1y', 0)
        eps_pct = self._to_percentile(eps_growth, cfg['eps_growth_percentile_refs'])
        
        # 3. 5-Year CAGR (if available) - higher is better
        cagr = growth_data.get('cagr_5y', 0)
        cagr_pct = self._to_percentile(cagr, cfg['cagr_percentile_refs'])
        
        # Combine with weights
        growth_score = (
            weights['revenue_growth'] * rev_pct +
            weights['eps_growth'] * eps_pct +
            weights['cagr_5y'] * cagr_pct
        )
        
        return np.clip(growth_score / 10, 0, 10)
    
    # ========================================================================
    # TECHNICAL INDICATOR CALCULATIONS
    # ========================================================================
    
    def _calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        if len(data) < period:
            return np.array([])
        
        ema = np.zeros(len(data))
        multiplier = 2 / (period + 1)
        
        # Start with SMA
        ema[period-1] = np.mean(data[:period])
        
        # Calculate EMA
        for i in range(period, len(data)):
            ema[i] = (data[i] - ema[i-1]) * multiplier + ema[i-1]
        
        return ema[period-1:]
    
    def _calculate_rsi(self, closes: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Relative Strength Index"""
        if len(closes) < period + 1:
            return np.array([50])
        
        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        rsi = np.zeros(len(closes))
        rsi[:period] = 50  # Default value
        
        for i in range(period, len(deltas)):
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
            
            if avg_loss == 0:
                rsi[i+1] = 100
            else:
                rs = avg_gain / avg_loss
                rsi[i+1] = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _calculate_atr(self, highs: np.ndarray, lows: np.ndarray, 
                       closes: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Average True Range"""
        if len(closes) < period + 1:
            return np.array([])
        
        tr = np.maximum(highs[1:] - lows[1:],
                       np.maximum(abs(highs[1:] - closes[:-1]),
                                 abs(lows[1:] - closes[:-1])))
        
        atr = np.zeros(len(tr))
        atr[period-1] = np.mean(tr[:period])
        
        for i in range(period, len(tr)):
            atr[i] = (atr[i-1] * (period - 1) + tr[i]) / period
        
        return atr[period-1:]
    
    def _calculate_vwap(self, highs: np.ndarray, lows: np.ndarray, 
                       closes: np.ndarray, volumes: np.ndarray) -> float:
        """Calculate Volume Weighted Average Price (last 20 days)"""
        period = min(20, len(closes))
        typical_price = (highs[-period:] + lows[-period:] + closes[-period:]) / 3
        vwap = np.sum(typical_price * volumes[-period:]) / np.sum(volumes[-period:])
        return vwap
    
    def _calculate_bb_width(self, closes: np.ndarray, period: int = 20, 
                           num_std: float = 2.0) -> np.ndarray:
        """Calculate Bollinger Band Width"""
        if len(closes) < period:
            return np.array([])
        
        bb_width = np.zeros(len(closes) - period + 1)
        
        for i in range(period - 1, len(closes)):
            window = closes[i-period+1:i+1]
            sma = np.mean(window)
            std = np.std(window)
            upper = sma + (std * num_std)
            lower = sma - (std * num_std)
            bb_width[i-period+1] = ((upper - lower) / sma) * 100 if sma > 0 else 0
        
        return bb_width
    
    # ========================================================================
    # PATTERN DETECTION
    # ========================================================================
    
    def _detect_rsi_divergence(self, closes: np.ndarray, rsi: np.ndarray) -> float:
        """
        Detect RSI divergence (simplified swing detection)
        Returns: 100 (bullish), 50 (none), 0 (bearish)
        """
        if len(closes) < 20 or len(rsi) < 20:
            return 50
        
        # Find recent swing high/low (last 10 bars)
        recent_closes = closes[-10:]
        recent_rsi = rsi[-10:]
        
        # Simple logic: if price making new highs but RSI isn't = bearish divergence
        # If price making new lows but RSI isn't = bullish divergence
        
        price_high_idx = np.argmax(recent_closes)
        rsi_high_idx = np.argmax(recent_rsi)
        price_low_idx = np.argmin(recent_closes)
        rsi_low_idx = np.argmin(recent_rsi)
        
        # Check for bullish divergence (lower low in price, higher low in RSI)
        if price_low_idx > 5 and recent_closes[-1] > recent_closes[price_low_idx]:
            if recent_rsi[-1] > recent_rsi[rsi_low_idx]:
                return 100  # Bullish divergence
        
        # Check for bearish divergence (higher high in price, lower high in RSI)
        if price_high_idx > 5 and recent_closes[-1] < recent_closes[price_high_idx]:
            if recent_rsi[-1] < recent_rsi[rsi_high_idx]:
                return 0  # Bearish divergence
        
        return 50  # No clear divergence
    
    def _calculate_ma_stack(self, price: float, ema20: float, 
                           ema50: float, ema200: float) -> float:
        """
        Calculate MA stack score
        100: Bullish stack (price > EMA20 > EMA50 > EMA200)
        0: Bearish stack (reverse)
        50: Mixed
        """
        if price > ema20 > ema50 > ema200:
            return 100
        elif price < ema20 < ema50 < ema200:
            return 0
        else:
            return 50
    
    def _calculate_breakout_proximity(self, closes: np.ndarray, 
                                     highs: np.ndarray, lows: np.ndarray, 
                                     period: int = 20) -> float:
        """
        Calculate proximity to breakout
        Positive: Close to upper breakout
        Negative: Close to lower breakdown
        """
        if len(closes) < period:
            return 0
        
        recent_high = np.max(highs[-period:])
        recent_low = np.min(lows[-period:])
        current_price = closes[-1]
        
        # Calculate distance to high/low as percentage
        range_size = recent_high - recent_low
        if range_size == 0:
            return 0
        
        distance_to_high = ((recent_high - current_price) / range_size) * 100
        distance_to_low = ((current_price - recent_low) / range_size) * 100
        
        # Positive score if closer to high, negative if closer to low
        if distance_to_high < distance_to_low:
            return (100 - distance_to_high)  # Close to breakout
        else:
            return -(100 - distance_to_low)  # Close to breakdown
    
    # ========================================================================
    # NEWS AND SENTIMENT
    # ========================================================================
    
    def _calculate_news_sentiment(self, news: List[Dict], cfg: Dict) -> float:
        """Calculate news sentiment score (0-100)"""
        if not news:
            return 50  # Neutral
        
        keywords = cfg['sentiment_keywords']
        positive_words = keywords['positive']
        negative_words = keywords['negative']
        
        sentiment_scores = []
        
        for article in news:
            text = (article.get('title', '') + ' ' + article.get('text', '')).lower()
            
            pos_count = sum(1 for word in positive_words if word in text)
            neg_count = sum(1 for word in negative_words if word in text)
            
            if pos_count + neg_count == 0:
                sentiment = 50
            else:
                sentiment = (pos_count / (pos_count + neg_count)) * 100
            
            sentiment_scores.append(sentiment)
        
        return np.mean(sentiment_scores) if sentiment_scores else 50
    
    def _check_major_news(self, news: List[Dict], keywords: List[str]) -> bool:
        """Check for major news based on keywords"""
        if not news:
            return False
        
        for article in news:
            text = (article.get('title', '') + ' ' + article.get('text', '')).lower()
            for keyword in keywords:
                if keyword.lower() in text:
                    return True
        
        return False
    

    def calculate_options_score(self, data: Dict) -> float:
        """Calculate options sentiment score (0-10)"""
        options_data = data.get('options_analysis')
        if not options_data:
            return 0.0
        
        score = 0.0
        
        # Put/Call Ratio (4 points)
        put_call = options_data.get('put_call_ratio')
        if put_call is not None:
            if put_call < 0.7: score += 4.0
            elif put_call < 0.85: score += 3.0
            elif put_call < 1.0: score += 2.0
            elif put_call < 1.2: score += 1.5
            elif put_call < 1.5: score += 1.0
        
        # IV (3 points)
        atm_iv = options_data.get('atm_implied_volatility')
        if atm_iv is not None:
            iv_pct = atm_iv * 100 if atm_iv < 1 else atm_iv
            if 20 <= iv_pct <= 40: score += 3.0
            elif 40 < iv_pct <= 50: score += 2.0
            elif 15 <= iv_pct < 20 or 50 < iv_pct <= 60: score += 1.0
            else: score += 0.5
        
        # Volume (2 points)
        total_vol = options_data.get('total_call_volume', 0) + options_data.get('total_put_volume', 0)
        if total_vol > 10000: score += 2.0
        elif total_vol > 5000: score += 1.5
        elif total_vol > 1000: score += 1.0
        elif total_vol > 100: score += 0.5
        
        # Net Delta (1 point)
        net_delta = options_data.get('net_delta', 0)
        if net_delta > 100: score += 1.0
        elif net_delta > 0: score += 0.7
        elif net_delta > -100: score += 0.3
        
        return min(score, 10.0)    # ========================================================================
    # UTILITY FUNCTIONS
    # ========================================================================
    
    def _to_percentile(self, value: float, reference_points: List[float]) -> float:
        """
        Convert a value to percentile score (0-100) using reference points
        Reference points should be sorted from low to high
        """
        reference_points = sorted(reference_points)
        
        if value <= reference_points[0]:
            return 0
        elif value >= reference_points[-1]:
            return 100
        else:
            # Linear interpolation between reference points
            for i in range(len(reference_points) - 1):
                if reference_points[i] <= value <= reference_points[i+1]:
                    lower = reference_points[i]
                    upper = reference_points[i+1]
                    pct_lower = (i / (len(reference_points) - 1)) * 100
                    pct_upper = ((i + 1) / (len(reference_points) - 1)) * 100
                    
                    # Interpolate
                    ratio = (value - lower) / (upper - lower)
                    return pct_lower + (pct_upper - pct_lower) * ratio
        
        return 50  # Default
    
    def _validate_data(self, data: Dict) -> bool:
        """Validate that required data is present"""
        if not data or 'historical' not in data:
            return False
        
        if len(data['historical']) < self.config['filters']['min_data_points']:
            return False
        
        return True
    
    def _extract_metrics(self, data: Dict) -> Dict:
        """Extract key metrics for reporting"""
        hist = data['historical']
        closes = np.array([d['close'] for d in hist])
        volumes = np.array([d['volume'] for d in hist])
        
        return {
            'current_price': closes[-1],
            'daily_change': (closes[-1] / closes[-2] - 1) * 100 if len(closes) > 1 else 0,
            'volume': volumes[-1],
            'avg_volume': np.mean(volumes[-20:]) if len(volumes) >= 20 else np.mean(volumes),
            'roc_5d': (closes[-1] / closes[-6] - 1) * 100 if len(closes) > 5 else 0,
            'roc_20d': (closes[-1] / closes[-21] - 1) * 100 if len(closes) > 20 else 0,
        }
    
    def _days_until(self, date_str: str) -> int:
        """Calculate days until a date (simplified)"""
        from datetime import datetime
        try:
            target = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.now()
            return (target - today).days
        except:
            return 999  # Far future if can't parse
    
    # ========================================================================
    # BATCH ANALYSIS
    # ========================================================================
    
    def analyze_batch(self, stocks_data: List[Dict]) -> List[Dict]:
        """Analyze multiple stocks and return sorted results"""
        results = []
        
        for stock_data in stocks_data:
            try:
                scores = self.analyze_stock(stock_data)
                if scores:
                    scores['symbol'] = stock_data.get('symbol', 'N/A')
                    scores['company'] = stock_data.get('profile', {}).get('companyName', 'N/A')
                    results.append(scores)
            except Exception as e:
                print(f"Error analyzing {stock_data.get('symbol', 'unknown')}: {e}")
                continue
        
        # Sort by composite score
        results.sort(key=lambda x: x['composite_score'], reverse=True)
        
        return results

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("Stock Analyzer v4.0 - Hybrid Technical + Fundamental System")
    print("=" * 70)
    print("\nâœ… Analyzer module loaded successfully")
    print(f"âœ… Configured with {len(config.ANALYSIS_CONFIG['weights'])} scoring dimensions:")
    print("   - Technical: 6 dimensions (70%)")
    print("   - Fundamental: 3 dimensions (20%)")
    print("   - Buffer: 10%")
    
    # Validate configuration
    try:
        config.validate_config()
    except Exception as e:
        print(f"âŒ Configuration error: {e}")


