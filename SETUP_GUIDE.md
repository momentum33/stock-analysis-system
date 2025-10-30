# 🚀 COMPLETE SYSTEM SETUP GUIDE

## Welcome to Your Enhanced Stock Analysis System!

This system now includes:
✅ Technical Analysis (momentum, volume, RSI, moving averages)
✅ Fundamental Analysis (financial ratios, growth metrics)
✅ Short Interest Analysis (squeeze detection)
✅ **Options Analysis** (via Polygon.io) 🆕
✅ AI Analysis (Claude Opus 4)

---

## 📦 What's Included

### Core System Files:
1. **config.py** - Configuration (API keys go here)
2. **main.py** - Standard analysis mode
3. **main_with_claude.py** - AI-enhanced analysis mode
4. **analyzer.py** - Scoring engine (all 10 scores)
5. **fmp_client.py** - Financial Modeling Prep API client
6. **polygon_client.py** - Polygon.io API client (options & short interest)
7. **report_generator.py** - HTML/CSV report generation
8. **claude_analyzer.py** - Basic Claude integration
9. **claude_analyzer_optimized.py** - Optimized Claude prompts
10. **claude_report_generator.py** - AI-enhanced reports

### Documentation (16 files):
- Setup guides
- Configuration help
- Troubleshooting
- Feature explanations
- Best practices

---

## ⚡ QUICK START (5 Minutes)

### Step 1: Install Dependencies (30 seconds)

```bash
cd stock-analysis-system
pip install -r requirements.txt
```

**Requirements:**
- Python 3.8+
- anthropic
- requests
- numpy
- (all listed in requirements.txt)

---

### Step 2: Add Your API Keys (2 minutes)

Open `config.py` and add your keys:

#### A) FMP API Key (Required)
```python
# Line 6:
FMP_API_KEY = "your_fmp_key_here"
```
**Get it:** https://financialmodelingprep.com/developer/docs
- Free tier: 250 calls/day (sufficient for small portfolios)
- Starter: $14.99/month, 750 calls/day
- Professional: $29.99/month, 5,000 calls/day

#### B) Polygon API Key (Required for Options)
```python
# Line 14:
POLYGON_API_KEY = "your_polygon_starter_key_here"
```
**Get it:** https://polygon.io/dashboard/api-keys
- **Your Starter Plan: $29/month** ✓
- 100 requests/minute
- Perfect for this system!

**IMPORTANT:** Also verify this setting:
```python
# Line 20:
POLYGON_RATE_LIMIT = 100  # ✓ Already set for Starter plan
```

#### C) Claude API Key (Optional - for AI analysis)
```python
# Line 24:
CLAUDE_API_KEY = "your_anthropic_key_here"
```
**Get it:** https://console.anthropic.com/
- Pay as you go
- ~$6 per deep analysis run (20 stocks)
- Optional: System works without it

---

### Step 3: Prepare Your Stock List (1 minute)

Create or edit `input_tickers.txt`:

```
AAPL
MSFT
GOOGL
TSLA
NVDA
```

**Format:**
- One ticker per line
- Uppercase letters
- No commas or extra text
- Comments with # are ignored

---

### Step 4: Run Your First Analysis (1 minute)

```bash
# Standard mode (fast, free after API setup)
python main.py input_tickers.txt
```

**What it does:**
- Analyzes all 10 scoring components:
  1. Momentum (18%)
  2. Volume (11%)
  3. Technical (17%)
  4. Volatility (7%)
  5. Relative Strength (11%)
  6. Catalyst/News (7%)
  7. Liquidity (4%)
  8. **Fundamental Quality (10%)** 🆕
  9. **Short Interest (4%)** 🆕
  10. **Growth (4%)** 🆕
  11. **Options Sentiment (7%)** 🆕 via Polygon
  
- Generates HTML report in `output/` folder
- Creates CSV with all scores
- Ranks stocks by total score

**Output location:**
```
output/
  ├── stock_analysis_report_2025-10-27.html
  ├── stock_analysis_data_2025-10-27.csv
  └── charts/ (if enabled)
```

---

### Step 5: (Optional) AI-Enhanced Analysis

```bash
# Deep analysis with Claude Opus 4
python main_with_claude.py input_tickers.txt --deep-analysis
```

**What it adds:**
- Detailed sentiment analysis
- Catalyst identification with dates
- Risk assessment with red flags
- Bull/bear thesis
- Trading recommendations
- Position sizing suggestions
- Entry/exit strategies

**Cost:** ~$6 per run (analyzes top 20 stocks)

---

## 📊 Understanding Your Results

### Standard Mode Output:

```
AAPL - Total Score: 8.2/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Technical Scores:
  Momentum:          8.5/10  ★★★★☆
  Volume:            7.8/10  ★★★★☆
  Technical:         8.0/10  ★★★★☆
  Volatility:        7.2/10  ★★★★☆
  Relative Strength: 8.1/10  ★★★★☆
  
Fundamental Scores:
  Quality:           8.7/10  ★★★★★
  Short Interest:    6.5/10  ★★★☆☆
  Growth:            8.9/10  ★★★★★
  
Options Analysis:
  Options Score:     9.2/10  ★★★★★
  Put/Call Ratio:    0.68 (Very Bullish)
  Liquidity:         Excellent (150 contracts)
  
Overall: Strong Buy Setup ✓
```

### Score Interpretation:

**8.0-10.0:** Strong opportunity
- High confidence setup
- Multiple confirming signals
- Consider larger position size

**6.5-7.9:** Moderate opportunity
- Decent setup
- Some conflicting signals
- Normal position size

**5.0-6.4:** Weak opportunity
- Mixed signals
- High risk/low conviction
- Small position or skip

**0-4.9:** Avoid
- Red flags present
- More risks than rewards
- Do not trade

---

## 🎯 Key Features Explained

### 1. Options Analysis (Polygon.io)

**What it does:**
- Fetches options contracts for each stock
- Calculates Put/Call ratio
- Assesses options liquidity
- Detects bullish/bearish sentiment

**Scoring:**
- PCR < 0.7 = Very bullish (+3 pts)
- PCR 0.7-1.0 = Bullish (+2 pts)
- PCR 1.0-1.3 = Neutral (+1 pt)
- PCR > 1.3 = Bearish (-1 pt)
- High liquidity = +2 pts

**Example:**
```
AAPL Options:
  ✓ 150 active contracts (excellent liquidity)
  ✓ P/C Ratio: 0.68 (very bullish)
  ✓ Score: 9.2/10
  
Interpretation: Strong bullish sentiment in options market
```

### 2. Fundamental Quality

**What it evaluates:**
- ROE (Return on Equity)
- Profit Margins
- Debt Levels
- Liquidity Ratios
- Valuation (P/E range)

**Use case:** Avoid value traps!
- High technical + Low fundamental = Risky
- High technical + High fundamental = High conviction

### 3. Short Interest

**What it detects:**
- Short squeeze potential
- Bearish pressure
- Trend direction (shorts covering/building)

**Scoring:**
- 5-15% short + low days to cover = Squeeze setup
- >20% short + high days to cover = Major squeeze potential
- <5% short = Less bearish pressure

### 4. Growth Metrics

**What it tracks:**
- Revenue growth (QoQ and YoY)
- EPS growth
- Growth acceleration/deceleration

**Use case:** Validate momentum
- High momentum + High growth = Strong setup
- High momentum + Low growth = Possible exhaustion

---

## ⚙️ Configuration Options

### Adjust Scoring Weights

In `config.py`, modify the weights (lines 40-53):

```python
'weights': {
    'momentum_score': 0.18,              # Adjust to taste
    'volume_score': 0.11,
    'technical_score': 0.17,
    'volatility_score': 0.07,
    'relative_strength_score': 0.11,
    'catalyst_score': 0.07,
    'liquidity_score': 0.04,
    'fundamental_quality_score': 0.10,
    'short_interest_score': 0.04,
    'growth_score': 0.04,
    'options_score': 0.07,
}
# Must sum to 1.0
```

**Examples:**

**More Options-Focused:**
```python
'options_score': 0.12,           # Increase from 0.07
'momentum_score': 0.15,          # Decrease from 0.18
'technical_score': 0.14,         # Decrease from 0.17
```

**More Fundamental-Focused:**
```python
'fundamental_quality_score': 0.15,  # Increase from 0.10
'growth_score': 0.06,                # Increase from 0.04
'momentum_score': 0.15,              # Decrease from 0.18
```

### Risk Filters

```python
'min_avg_volume': 100000,    # Minimum daily volume
'min_price': 2.0,            # Minimum stock price
'max_price': 10000,          # Maximum stock price
```

**Adjust for your style:**
- Day trading: Higher min_volume (500K+)
- Swing trading: Current settings OK
- Penny stocks: Lower min_price (but risky!)

---

## 🧪 Testing Your Setup

### Test 1: API Connections

```bash
python -c "import config; print('FMP:', config.FMP_API_KEY[:10]); print('Polygon:', config.POLYGON_API_KEY[:10])"
```

**Expected:** Should print first 10 chars of your keys

### Test 2: Quick Analysis

```bash
# Create test file
echo -e "AAPL\nMSFT\nGOOGL" > test_tickers.txt

# Run analysis
python main.py test_tickers.txt
```

**Expected:** 
- Analysis completes in 2-3 minutes
- Generates report in `output/` folder
- Options data included for each stock

### Test 3: Polygon Connection

```bash
python -c "from polygon_client import PolygonClient; import config; c = PolygonClient(config.POLYGON_API_KEY); print(c.get_options_summary('AAPL'))"
```

**Expected:** Returns options data for AAPL

---

## 🐛 Troubleshooting

### "Invalid API Key"

**FMP:**
- Check spelling in config.py
- Verify at financialmodelingprep.com
- Check rate limits (free tier = 250/day)

**Polygon:**
- Check spelling in config.py
- Verify at polygon.io/dashboard/api-keys
- Ensure Starter plan is active

### "Rate Limit Exceeded"

**Solution 1:** Wait 60 seconds (counters reset)

**Solution 2:** Reduce rate limits:
```python
API_RATE_LIMIT = 250  # FMP (lower if on free tier)
POLYGON_RATE_LIMIT = 90  # Polygon (lower from 100 to be safe)
```

### "No Options Data"

**Possible causes:**
1. Stock doesn't have options (normal for small caps)
2. Polygon API key not set
3. Rate limit hit

**Solution:** System handles gracefully (uses neutral score 5/10)

### "Module Not Found"

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### "Windows Encoding Error"

See `WINDOWS_ENCODING_FIX.md` in documentation

---

## 💰 Cost Breakdown

### Monthly Costs:

**Required:**
- FMP API: $0-99/month
  - Free: 250 calls/day (works for small portfolios)
  - Starter: $14.99/month (recommended)
  - Professional: $29.99/month (for large portfolios)
  
- Polygon API: $29/month (your Starter plan) ✓
  - 100 requests/minute
  - Options + real-time data
  - Perfect for this system

**Optional:**
- Claude API: Pay-as-you-go
  - ~$6 per deep analysis session
  - Only if you use `main_with_claude.py`
  - Can skip and use standard mode only

**Total minimum:** $43.99/month (FMP Starter + Polygon Starter)
**With Claude:** ~$43.99 + $6/day you use it

### API Usage Per Analysis:

**50 stocks analyzed:**
- FMP calls: ~200 (quotes, historical, fundamentals)
- Polygon calls: ~100 (options data)
- Time: ~3-5 minutes
- Cost: Included in monthly plans

---

## 📚 Documentation

Check these guides for more info:

- **QUICKSTART.md** - 5-minute setup
- **README.md** - System overview
- **CONFIGURATION_GUIDE.md** - Detailed config options
- **CLAUDE_INTEGRATION_GUIDE.md** - AI analysis setup
- **FINANCIAL_FEATURES_GUIDE.md** - Fundamental analysis explained
- **POLYGON_INSTALLATION.md** - Options setup details
- **CLAUDE_TROUBLESHOOTING.md** - Fix AI issues
- **WINDOWS_ENCODING_FIX.md** - Windows-specific help

---

## 🎯 Usage Workflows

### Daily Trader Workflow:

```bash
# Morning: Run quick scan
python main.py watchlist.txt

# Review HTML report
# Identify top 3-5 opportunities

# Afternoon: Deep dive on top picks
python main_with_claude.py top_picks.txt --deep-analysis
```

### Swing Trader Workflow:

```bash
# Weekend: Scan universe
python main.py universe.txt  # 50-100 stocks

# Filter to top 10
# Create focused list

# Monday: Deep analysis
python main_with_claude.py top_10.txt --deep-analysis

# Track positions throughout week
```

### Portfolio Manager Workflow:

```bash
# Weekly: Full analysis
python main.py portfolio.txt

# Check fundamentals
# Review options sentiment
# Assess risks

# Monthly: Strategy review
python main_with_claude.py portfolio.txt --deep-analysis

# Generate reports for clients
```

---

## ✅ Pre-Flight Checklist

Before your first analysis:

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] FMP API key in config.py
- [ ] Polygon API key in config.py
- [ ] POLYGON_RATE_LIMIT = 100 (for Starter plan)
- [ ] Created input_tickers.txt with your stocks
- [ ] Ran test analysis (3 stocks)
- [ ] Reviewed output in `output/` folder
- [ ] Everything working? You're ready! 🚀

---

## 🆘 Need More Help?

### Quick Answers:
1. **"Where do I put Polygon key?"** → config.py line 14
2. **"How do I run it?"** → `python main.py input_tickers.txt`
3. **"Where's the output?"** → `output/` folder
4. **"Options not working?"** → Check Polygon key and rate limit
5. **"Too slow?"** → Normal for Starter plan (100 req/min limit)

### Documentation:
- Start with QUICKSTART.md
- Read POLYGON_INSTALLATION.md for options details
- Check TROUBLESHOOTING guides if issues

### Remember:
- System works fine without options (uses neutral score)
- System works fine without Claude (standard mode only)
- Start simple, add features as needed

---

## 🎉 You're All Set!

Your complete stock analysis system includes:

✅ 10 different scoring components
✅ Technical + Fundamental + Options analysis
✅ AI-enhanced insights (optional)
✅ Professional HTML reports
✅ CSV data exports
✅ Comprehensive documentation

**Ready to analyze?**

```bash
python main.py input_tickers.txt
```

Good luck with your trading! 📈
