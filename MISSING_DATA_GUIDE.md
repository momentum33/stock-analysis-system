# 🔍 MISSING DATA HANDLING GUIDE

## Overview

This document explains what happens when FMP API data is missing or incomplete, and how the system handles it.

---

## 📊 Data Points Used by the System

### Critical Data (Required)
These must be available or the stock is skipped:

| Data Point | FMP Endpoint | Used For |
|------------|--------------|----------|
| **Current Quote** | `/quote/{ticker}` | Price, volume, day change |
| **Historical Prices** | `/historical-price-full/{ticker}` | All technical analysis, trends |
| **50+ Days History** | Same as above | Moving averages, RSI, volatility |

**If missing:** Stock is **SKIPPED** with message: `"Insufficient data for {symbol}"`

### Important Data (Has Fallbacks)
These improve analysis but have defaults if missing:

| Data Point | FMP Endpoint | Used For | Fallback |
|------------|--------------|----------|----------|
| **Company Profile** | `/profile/{ticker}` | Company name, sector, market cap | "N/A" values |
| **News Articles** | `/stock_news` | Catalyst score | Score = 5/10 (neutral) |
| **Bid/Ask Spread** | `/quote/{ticker}` | Liquidity score | Assume average spread |
| **SPY Data** | `/historical-price-full/SPY` | Relative strength | Score = 5/10 (neutral) |

**If missing:** Stock is **ANALYZED** with reduced accuracy

### Optional Data (Not Currently Used)
These could enhance the system but aren't implemented yet:

- Earnings calendar dates
- Financial ratios (P/E, P/B, etc.)
- Key metrics (ROE, debt ratios)
- Options data
- Short interest

---

## 🔄 How Missing Data is Handled

### 1. Stock-Level Handling

```python
# In analyzer.py - analyze_stock() method

try:
    # Fetch all data
    quote = self.client.get_quote(symbol)
    historical = self.client.get_historical_prices(symbol, days=90)
    profile = self.client.get_company_profile(symbol)
    news = self.client.get_stock_news(symbol, limit=5)
    
    # CRITICAL CHECK #1: Quote exists?
    if not quote:
        print(f"  ✗ No quote data for {symbol}")
        return None  # SKIP THIS STOCK
    
    # CRITICAL CHECK #2: Enough history?
    if not historical or len(historical) < 50:
        print(f"  ✗ Insufficient data for {symbol}")
        return None  # SKIP THIS STOCK
    
    # FALLBACK #1: No profile?
    if not profile:
        profile = {
            'companyName': 'N/A',
            'sector': 'N/A',
            'mktCap': 0
        }
    
    # FALLBACK #2: No news?
    if not news:
        news = []  # Empty list, catalyst score will be neutral
    
except Exception as e:
    print(f"  ✗ Error analyzing {symbol}: {e}")
    return None  # SKIP THIS STOCK
```

### 2. Score-Level Handling

Each scoring method has built-in safety checks:

#### A. Momentum Score
```python
def _calculate_momentum_score(self, historical):
    if len(historical) < 50:
        return 0  # Can't calculate, return minimum
    
    prices = [day['close'] for day in historical[:50]]
    
    # Safety checks
    if prices[9] <= 0:
        short_return = 0
    else:
        short_return = (prices[0] - prices[9]) / prices[9]
```

**Missing data impact:**
- < 10 days history: Minimum score (0)
- < 20 days history: Reduced accuracy
- < 50 days history: Stock skipped entirely

#### B. Volume Score
```python
def _calculate_volume_score(self, historical, quote):
    if len(historical) < 20:
        return 0  # Can't calculate trends
    
    volumes = [day['volume'] for day in historical[:20]]
    avg_volume = np.mean(volumes)
    current_volume = quote['volume']
    
    # Safety check
    if avg_volume <= 0:
        return 5  # Neutral score if no volume data
```

**Missing data impact:**
- No volume data: Neutral score (5/10)
- < 20 days volume: Minimum score (0)

#### C. Technical Score
```python
def _calculate_technical_score(self, historical, quote):
    if len(historical) < 50:
        return 0
    
    # RSI calculation with safety
    rsi = self._calculate_rsi(prices[:14])
    # Returns 50 (neutral) if insufficient data
```

**Missing data impact:**
- < 14 days: RSI defaults to 50 (neutral)
- < 50 days: Stock skipped
- No moving average possible: Score reduced

#### D. Volatility Score
```python
def _calculate_volatility_score(self, historical):
    if len(historical) < 20:
        return 0
    
    prices = [day['close'] for day in historical[:20]]
    returns = [(prices[i] - prices[i+1]) / prices[i+1] 
               for i in range(len(prices)-1)]
    
    volatility = np.std(returns)
```

**Missing data impact:**
- < 20 days: Minimum score (0)
- Less data = less accurate volatility measure

#### E. Relative Strength Score
```python
def _calculate_relative_strength(self, historical):
    if not self.market_data or len(historical) < 20:
        return 5  # Neutral if no market comparison
    
    # Compare to SPY
```

**Missing data impact:**
- No SPY data: Neutral score (5/10) for ALL stocks
- < 20 days: Neutral score (5/10)

#### F. Catalyst Score
```python
def _calculate_catalyst_score(self, news, historical):
    score = 0
    
    # If no news available
    if not news:
        return 5  # Neutral score
    
    # Analyze news sentiment
    for article in news:
        text = (article.get('title', '') + ' ' + 
                article.get('text', '')).lower()
```

**Missing data impact:**
- No news: Neutral score (5/10)
- Fewer articles: Less accurate sentiment
- Missing article text: Only title analyzed

#### G. Liquidity Score
```python
def _calculate_liquidity_score(self, quote, avg_volume):
    score = 0
    
    # Volume-based (always available)
    if avg_volume > 1000000:
        score += 5
    
    # Spread-based (may be missing)
    if 'bid' in quote and 'ask' in quote and quote['bid'] > 0:
        spread_pct = (quote['ask'] - quote['bid']) / quote['bid']
        # Calculate spread score
    else:
        score += 2.5  # Assume average spread if missing
```

**Missing data impact:**
- No bid/ask: Assumes average spread
- Score accuracy reduced by ~50%

---

## 🚨 Common Missing Data Scenarios

### Scenario 1: New IPO
**What's Missing:**
- < 50 days of historical data
- May have limited news

**System Behavior:**
- Stock is **SKIPPED** entirely
- Message: "Insufficient data for {symbol}"

**Workaround:**
- Lower the history requirement in `config.py`:
```python
# In analyzer.py, modify line ~35:
if not historical or len(historical) < 20:  # Instead of 50
```

### Scenario 2: Penny Stock / Low Volume
**What's Missing:**
- May have spotty volume data
- Often missing bid/ask spreads
- Limited news coverage

**System Behavior:**
- If passes volume filter: Analyzed with reduced accuracy
- Catalyst score likely neutral
- Liquidity score uses fallback

**Output Warning Signs:**
- Catalyst score = 5.0 (exactly)
- Liquidity score = 2.5 or 5.0 (fallback values)
- No news in report

### Scenario 3: Foreign Stock / ADR
**What's Missing:**
- May have company profile issues
- News might be sparse
- Sector classification might be "N/A"

**System Behavior:**
- Stock analyzed if has quote + history
- Company name shows "N/A"
- Sector shows "N/A"
- May affect sorting/filtering

### Scenario 4: ETF or Fund
**What's Missing:**
- Traditional company data
- News might not apply
- Sector = "N/A"

**System Behavior:**
- Will be analyzed (might not be appropriate)
- Scores may be misleading
- Consider filtering out ETFs manually

### Scenario 5: API Rate Limit Hit
**What's Missing:**
- ALL data for stocks analyzed after limit

**System Behavior:**
- Stocks after limit show errors
- Script waits automatically
- May take longer or fail if on free tier

**Error Message:**
```
Error fetching quote/AAPL: 429 Too Many Requests
Rate limit approaching, sleeping 45.3s...
```

---

## 🔍 How to Identify Missing Data in Outputs

### In Console Output

```bash
[1/50] AAPL
  ✓ AAPL: Score = 8.2     # Good - all data available

[2/50] NEWIPO
  ✗ Insufficient data for NEWIPO    # Missing history

[3/50] PENNY
  ✗ PENNY filtered: Low volume (45000)    # Filtered out

[4/50] XYZ
  ✗ Error analyzing XYZ: 'NoneType' object...    # API error
```

### In CSV Output

Look for these indicators:

```csv
symbol,company_name,sector,news_count
AAPL,"Apple Inc","Technology",5     # Complete
NEWCO,"N/A","N/A",0                  # Missing profile & news
PENNY,"Penny Corp","N/A",0           # Missing sector & news
```

### In HTML Dashboard

Missing data indicators:
- Company name = "N/A"
- Sector = "N/A"
- No news section displayed
- Catalyst score exactly = 5.0
- Liquidity score = 2.5 or 5.0 exactly

### In Scores

Suspicious patterns indicating missing data:

| Score Value | Possible Meaning |
|-------------|------------------|
| 0.0 | Insufficient data for calculation |
| 5.0 (exact) | Neutral/fallback value |
| 2.5 (exact) | Fallback for liquidity spread component |

---

## 📋 Data Quality Checklist

Before relying on results, check:

✅ **Stock Count:** Did most stocks get analyzed?
```
Analysis complete: 45/50 stocks passed filters
```
Good: >80% pass rate
Bad: <50% pass rate

✅ **Console Warnings:** How many "Insufficient data" messages?

✅ **News Coverage:** Do top picks have news articles?

✅ **Company Info:** Are company names populated?

✅ **Score Distribution:** Are catalyst scores varied or all 5.0?

---

## 🛠️ Improving Data Coverage

### 1. Use Paid FMP Tier
**Benefits:**
- More requests/day (analyze more stocks)
- Better data coverage
- Faster response times
- Access to premium endpoints

### 2. Adjust History Requirements

In `analyzer.py`, line ~40:
```python
# Current (strict)
if not historical or len(historical) < 50:
    return None

# More lenient (for newer stocks)
if not historical or len(historical) < 30:
    return None
```

**Trade-off:** Less accurate technical scores

### 3. Add Data Validation

Add to `main.py` after analysis:
```python
# Count missing data
missing_news = sum(1 for s in results if len(s.get('news', [])) == 0)
missing_sector = sum(1 for s in results if s.get('sector') == 'N/A')

print(f"\nData Quality:")
print(f"  Stocks with news: {len(results) - missing_news}/{len(results)}")
print(f"  Stocks with sector: {len(results) - missing_sector}/{len(results)}")
```

### 4. Pre-Filter Input

Before running analysis, remove:
- Newly IPO'd stocks (< 3 months old)
- Penny stocks (< $2)
- Low volume stocks (< 100K daily)
- ETFs and funds

---

## 🎯 Recommended Approach

### For Daily Trading

**Accept some missing data:**
- Focus on stocks with >80% data completeness
- Review console output for warnings
- Manually verify top 3 picks before trading

### For Production System

**Enhance data handling:**
1. Add data quality scoring
2. Implement fallback data sources
3. Cache historical data locally
4. Add data freshness checks
5. Flag low-confidence scores

---

## 💡 Advanced: Adding Data Quality Metrics

Add this to `analyzer.py`:

```python
def _calculate_data_quality_score(self, profile, news, historical):
    """Calculate data quality score (0-100)"""
    score = 0
    
    # Has company profile? +30 points
    if profile and profile.get('companyName') != 'N/A':
        score += 30
    
    # Has news? +20 points
    if news and len(news) >= 3:
        score += 20
    elif news and len(news) > 0:
        score += 10
    
    # Has full history? +30 points
    if len(historical) >= 50:
        score += 30
    elif len(historical) >= 30:
        score += 20
    
    # Has sector data? +10 points
    if profile and profile.get('sector') != 'N/A':
        score += 10
    
    # Has volume data? +10 points
    if all(day.get('volume', 0) > 0 for day in historical[:20]):
        score += 10
    
    return score

# Then add to analysis output:
analysis['data_quality'] = self._calculate_data_quality_score(
    profile, news, historical
)
```

Then filter by quality:
```python
# Only keep high-quality data
top_stocks = [s for s in results if s['data_quality'] >= 70]
```

---

## 📊 Summary Table: What Happens When Data is Missing

| Data Point | If Missing | Score Impact | Stock Status |
|------------|-----------|--------------|--------------|
| Quote | → Skip | N/A | **SKIPPED** |
| < 50 days history | → Skip | N/A | **SKIPPED** |
| Company profile | → Use "N/A" | None | Analyzed |
| Sector | → Use "N/A" | None | Analyzed |
| News | → Empty list | Catalyst = 5.0 | Analyzed |
| Bid/Ask | → Assume avg | Liquidity -50% | Analyzed |
| SPY data | → Neutral | Rel.Str = 5.0 | All affected |
| Market cap | → Use 0 | None | Analyzed |

---

## 🎓 Key Takeaways

1. **Critical data missing** → Stock is skipped entirely
2. **Nice-to-have data missing** → Stock analyzed with fallbacks
3. **Missing data = neutral scores** (5.0) in most cases
4. **Watch console output** for warnings about missing data
5. **Free tier limitations** may cause incomplete analysis
6. **Data quality varies** by stock type and popularity

**Bottom Line:** The system is robust and handles missing data gracefully, but be aware of which stocks have complete data for best results.

---

**Want to see data quality in real-time?** Run `python main.py input_tickers.txt` and watch the console output carefully!
