# CONFIGURATION GUIDE - Trading Style Presets

This guide provides pre-configured settings for different trading styles. Simply copy the relevant section into your `config.py` file.

## 📋 Table of Contents

1. [Default Balanced Configuration](#default-balanced)
2. [Aggressive Momentum Trading](#aggressive-momentum)
3. [Conservative Technical Trading](#conservative-technical)
4. [News/Catalyst Driven Trading](#news-catalyst)
5. [Volume Breakout Trading](#volume-breakout)
6. [Volatility Scalping](#volatility-scalping)
7. [Custom Configuration Builder](#custom-builder)

---

## 1. Default Balanced Configuration
*Best for: General short-term trading, beginners*

```python
ANALYSIS_CONFIG = {
    'short_period': 10,
    'medium_period': 20,
    'long_period': 50,
    
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'rsi_neutral_low': 40,
    'rsi_neutral_high': 60,
    
    'volume_spike_multiplier': 1.5,
    'breakout_threshold': 0.02,
    
    'weights': {
        'momentum_score': 0.25,
        'volume_score': 0.15,
        'technical_score': 0.20,
        'volatility_score': 0.10,
        'relative_strength_score': 0.15,
        'catalyst_score': 0.10,
        'liquidity_score': 0.05,
    },
    
    'min_avg_volume': 100000,
    'min_price': 2.0,
    'max_price': 10000,
}
```

**Characteristics:**
- Balanced across all factors
- Good for learning the system
- Moderate risk/reward
- Works in most market conditions

---

## 2. Aggressive Momentum Trading
*Best for: Day traders, trending markets, risk-tolerant traders*

```python
ANALYSIS_CONFIG = {
    'short_period': 5,      # Shorter for faster signals
    'medium_period': 15,    
    'long_period': 30,      
    
    'rsi_oversold': 25,     # More aggressive thresholds
    'rsi_overbought': 75,
    'rsi_neutral_low': 35,
    'rsi_neutral_high': 65,
    
    'volume_spike_multiplier': 2.0,  # Look for bigger spikes
    'breakout_threshold': 0.03,       # 3% breakout
    
    'weights': {
        'momentum_score': 0.35,          # ⬆ Heavy momentum
        'volume_score': 0.25,            # ⬆ Heavy volume
        'technical_score': 0.15,
        'volatility_score': 0.05,        # ⬇ Less concern about volatility
        'relative_strength_score': 0.10,
        'catalyst_score': 0.10,
        'liquidity_score': 0.0,          # ⬇ Accept lower liquidity
    },
    
    'min_avg_volume': 200000,    # Higher for faster fills
    'min_price': 5.0,            # Avoid penny stocks
    'max_price': 500,            # Focus on moveable stocks
}
```

**Key Changes:**
- 35% weight on momentum (vs 25% default)
- 25% weight on volume (vs 15% default)
- Reduced volatility concern
- Higher volume requirements
- Faster lookback periods

**Best For:**
- Trending markets
- Strong directional moves
- Intraday to 1-week holds
- Active monitoring

---

## 3. Conservative Technical Trading
*Best for: Swing traders, risk-averse, technical analysts*

```python
ANALYSIS_CONFIG = {
    'short_period': 10,
    'medium_period': 20,
    'long_period': 50,
    
    'rsi_oversold': 35,     # More conservative
    'rsi_overbought': 65,
    'rsi_neutral_low': 45,
    'rsi_neutral_high': 55,
    
    'volume_spike_multiplier': 1.3,  # More sensitive
    'breakout_threshold': 0.015,      # 1.5% for confirmation
    
    'weights': {
        'momentum_score': 0.15,          # ⬇ Less aggressive
        'volume_score': 0.10,
        'technical_score': 0.35,         # ⬆ Heavy technical
        'volatility_score': 0.20,        # ⬆ Prefer stable movers
        'relative_strength_score': 0.10,
        'catalyst_score': 0.05,          # ⬇ Less news-driven
        'liquidity_score': 0.05,         # ⬆ Need good fills
    },
    
    'min_avg_volume': 500000,    # High liquidity
    'min_price': 10.0,           # Avoid cheap stocks
    'max_price': 1000,
}
```

**Key Changes:**
- 35% weight on technical analysis
- 20% weight on volatility (prefer stability)
- Higher volume & price requirements
- Less weight on momentum & catalysts

**Best For:**
- Swing trading (1-4 weeks)
- Pattern-based trading
- Lower risk tolerance
- Part-time traders

---

## 4. News/Catalyst Driven Trading
*Best for: Event traders, news-based strategies*

```python
ANALYSIS_CONFIG = {
    'short_period': 5,      # Short-term reaction
    'medium_period': 10,    
    'long_period': 20,      
    
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'rsi_neutral_low': 40,
    'rsi_neutral_high': 60,
    
    'volume_spike_multiplier': 2.5,  # Need strong confirmation
    'breakout_threshold': 0.04,       # Bigger moves
    
    'weights': {
        'momentum_score': 0.20,
        'volume_score': 0.20,            # ⬆ Volume confirms news
        'technical_score': 0.10,         # ⬇ Less important
        'volatility_score': 0.05,        # ⬇ Expecting volatility
        'relative_strength_score': 0.10,
        'catalyst_score': 0.30,          # ⬆ Heavy catalyst focus
        'liquidity_score': 0.05,
    },
    
    'min_avg_volume': 300000,
    'min_price': 3.0,
    'max_price': 5000,
}
```

**Key Changes:**
- 30% weight on catalysts (vs 10% default)
- 20% weight on volume confirmation
- Short lookback periods
- Higher volume spike threshold

**Best For:**
- Earnings plays
- FDA approvals
- M&A targets
- Breaking news trades

---

## 5. Volume Breakout Trading
*Best for: Breakout traders, institutional following*

```python
ANALYSIS_CONFIG = {
    'short_period': 10,
    'medium_period': 20,
    'long_period': 50,
    
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'rsi_neutral_low': 40,
    'rsi_neutral_high': 60,
    
    'volume_spike_multiplier': 2.0,   # Key factor
    'breakout_threshold': 0.025,       # 2.5% breakout
    
    'weights': {
        'momentum_score': 0.20,
        'volume_score': 0.35,            # ⬆ Heavy volume focus
        'technical_score': 0.20,         # Breakout patterns
        'volatility_score': 0.10,
        'relative_strength_score': 0.10,
        'catalyst_score': 0.05,
        'liquidity_score': 0.0,          # Willing to sacrifice
    },
    
    'min_avg_volume': 250000,
    'min_price': 5.0,
    'max_price': 500,
}
```

**Key Changes:**
- 35% weight on volume (vs 15% default)
- Focus on volume spikes
- Breakout detection
- Momentum + technical combination

**Best For:**
- Accumulation breakouts
- Institutional buying signals
- Range breakouts
- 1-3 week holds

---

## 6. Volatility Scalping
*Best for: Active traders, quick in/out, volatility exploitation*

```python
ANALYSIS_CONFIG = {
    'short_period': 3,      # Very short-term
    'medium_period': 7,     
    'long_period': 14,      
    
    'rsi_oversold': 20,     # Extreme readings
    'rsi_overbought': 80,
    'rsi_neutral_low': 30,
    'rsi_neutral_high': 70,
    
    'volume_spike_multiplier': 1.5,
    'breakout_threshold': 0.02,
    
    'weights': {
        'momentum_score': 0.25,
        'volume_score': 0.15,
        'technical_score': 0.15,
        'volatility_score': 0.30,        # ⬆ Heavy volatility focus
        'relative_strength_score': 0.05,
        'catalyst_score': 0.05,
        'liquidity_score': 0.05,         # ⬆ Need tight spreads
    },
    
    'min_avg_volume': 1000000,   # Very high liquidity
    'min_price': 10.0,           # Avoid penny stocks
    'max_price': 300,            # Prefer mid-cap
}
```

**Key Changes:**
- 30% weight on volatility
- Very short lookback periods
- Extreme RSI thresholds
- High liquidity requirements

**Best For:**
- Intraday trading
- Quick scalps
- Options trading
- Active monitoring required

---

## 🎯 Custom Configuration Builder

Use this template to build your own configuration:

```python
ANALYSIS_CONFIG = {
    # === LOOKBACK PERIODS ===
    # Shorter = more responsive, Longer = more stable
    'short_period': 10,     # Days for short-term (3-14)
    'medium_period': 20,    # Days for medium-term (10-30)
    'long_period': 50,      # Days for context (30-90)
    
    # === RSI THRESHOLDS ===
    # Lower oversold = more aggressive, Higher = conservative
    'rsi_oversold': 30,     # Entry signal (20-35)
    'rsi_overbought': 70,   # Exit signal (65-80)
    'rsi_neutral_low': 40,  # Neutral zone low (35-45)
    'rsi_neutral_high': 60, # Neutral zone high (55-65)
    
    # === VOLUME & BREAKOUT ===
    'volume_spike_multiplier': 1.5,  # Volume > avg × this (1.3-3.0)
    'breakout_threshold': 0.02,       # % above resistance (0.01-0.05)
    
    # === SCORING WEIGHTS (MUST SUM TO 1.0) ===
    'weights': {
        'momentum_score': 0.25,          # Price trends (0.10-0.40)
        'volume_score': 0.15,            # Trading activity (0.10-0.35)
        'technical_score': 0.20,         # Indicators (0.10-0.35)
        'volatility_score': 0.10,        # Movement range (0.05-0.30)
        'relative_strength_score': 0.15, # vs Market (0.05-0.20)
        'catalyst_score': 0.10,          # News/events (0.05-0.30)
        'liquidity_score': 0.05,         # Execution (0.00-0.15)
    },
    
    # === FILTERS ===
    'min_avg_volume': 100000,    # Minimum daily volume (50K-1M+)
    'min_price': 2.0,            # Minimum price ($1-$20)
    'max_price': 10000,          # Maximum price ($100-$10000)
}
```

### Weight Allocation Guide

**High Weight (0.25-0.40):** Your primary signal
- What you check first on charts
- Your edge in trading

**Medium Weight (0.10-0.25):** Supporting factors
- Confirmation signals
- Risk management

**Low Weight (0.05-0.10):** Nice-to-have
- Final tie-breakers
- Quality filters

---

## 🔧 Advanced Configurations

### Sector-Specific: Tech Stocks
```python
'weights': {
    'momentum_score': 0.30,      # Tech moves fast
    'catalyst_score': 0.20,      # News-driven
    'technical_score': 0.20,
    'relative_strength_score': 0.15,
    'volume_score': 0.10,
    'volatility_score': 0.05,
    'liquidity_score': 0.00,
}
```

### Sector-Specific: Blue Chips
```python
'weights': {
    'relative_strength_score': 0.25,  # Sector rotation
    'technical_score': 0.25,          # Clean patterns
    'volatility_score': 0.20,         # Predictable
    'liquidity_score': 0.15,          # Easy fills
    'momentum_score': 0.10,
    'volume_score': 0.05,
    'catalyst_score': 0.00,
}
```

### Market Condition: Bull Market
```python
'weights': {
    'momentum_score': 0.35,           # Ride the trend
    'relative_strength_score': 0.25,  # Find leaders
    'technical_score': 0.15,
    'volume_score': 0.15,
    'catalyst_score': 0.10,
    'volatility_score': 0.00,
    'liquidity_score': 0.00,
}
```

### Market Condition: Bear Market
```python
'weights': {
    'relative_strength_score': 0.30,  # Find outperformers
    'technical_score': 0.25,          # Respect support
    'volatility_score': 0.20,         # Stable stocks
    'liquidity_score': 0.15,          # Exit quickly
    'momentum_score': 0.10,
    'volume_score': 0.00,
    'catalyst_score': 0.00,
}
```

---

## 📊 Testing Your Configuration

After changing weights, test with:

```bash
# 1. Run on a known date
python main.py historical_tickers.txt

# 2. Compare top 10 with what actually performed well

# 3. Adjust weights based on results

# 4. Repeat until satisfied
```

### Metrics to Track
- Win rate of top 3 picks
- Average gain of top 10
- False positive rate
- Time to profit

---

## ⚠️ Configuration Rules

### Must Follow:
1. **Weights must sum to 1.0**
   ```python
   # Calculate: sum of all weights
   total = 0.25 + 0.15 + 0.20 + 0.10 + 0.15 + 0.10 + 0.05 = 1.0 ✓
   ```

2. **All values must be positive**
   ```python
   'momentum_score': -0.10  # ✗ Wrong!
   'momentum_score': 0.10   # ✓ Correct
   ```

3. **Price filters make sense**
   ```python
   'min_price': 100,
   'max_price': 10   # ✗ Wrong! Min > Max
   ```

4. **Period relationships**
   ```python
   'short_period': 20,
   'medium_period': 10  # ✗ Wrong! Short > Medium
   ```

---

## 💡 Pro Tips

1. **Start with defaults** and adjust incrementally
2. **Test changes** on past data before live trading
3. **Keep a log** of configurations and results
4. **Seasonal adjustments** (volatility changes throughout year)
5. **Review monthly** and optimize based on performance

---

## 🎓 Configuration Philosophy

### Conservative Traders
- Higher weight on technical & volatility
- Higher min_price and min_volume
- Longer lookback periods
- Tighter RSI thresholds

### Aggressive Traders
- Higher weight on momentum & catalysts
- Lower filters (more opportunities)
- Shorter lookback periods
- Wider RSI thresholds

### Balanced Traders
- Use default configuration
- Adjust only 1-2 factors based on style
- Test thoroughly before major changes

---

**Remember: The best configuration is one that matches YOUR trading style and risk tolerance!**
