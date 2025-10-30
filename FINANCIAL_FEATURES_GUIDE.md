# Financial Ratios, Metrics & Short Interest Features

## 🎉 NEW Features Added to Your Stock Analysis System

Your system has been enhanced with comprehensive fundamental analysis capabilities!

## 📊 What's New

### 1. **Financial Ratios** (via FMP API)
Now tracks 30+ financial ratios including:

#### Valuation Ratios:
- P/E Ratio (Price-to-Earnings)
- P/B Ratio (Price-to-Book)
- P/S Ratio (Price-to-Sales)
- EV/EBITDA (Enterprise Value to EBITDA)

#### Profitability Ratios:
- ROE (Return on Equity)
- ROA (Return on Assets)
- Gross Profit Margin
- Operating Margin
- Net Profit Margin

#### Liquidity Ratios:
- Current Ratio
- Quick Ratio
- Cash Ratio

#### Leverage Ratios:
- Debt-to-Equity
- Debt-to-Assets
- Interest Coverage

### 2. **Key Metrics** (via FMP API)
- Market Capitalization
- Enterprise Value
- Revenue per Share
- Earnings per Share
- Book Value per Share
- Free Cash Flow per Share
- Dividend Yield
- Payout Ratio

### 3. **Short Interest Data** (via FMP API)
- Short Interest (number of shares)
- Short % of Float
- Days to Cover
- Historical short interest trends
- Fail-to-Deliver (FTD) data

### 4. **Growth Metrics** (via FMP API)
- Revenue Growth (YoY and QoQ)
- Earnings Growth
- EPS Growth
- Free Cash Flow Growth
- Asset Growth

### 5. **Options Data Framework** (Ready to Integrate)
- Placeholder methods for options chain
- Implied volatility structure
- Greeks (delta, gamma, theta, vega)
- Options flow detection
- See `OPTIONS_INTEGRATION_GUIDE.md` for implementation

## 🔧 Technical Implementation

### New Methods in `fmp_client.py`:
```python
# Enhanced financial data methods
get_financial_ratios_ttm(symbol)        # TTM ratios
get_financial_ratios_history(symbol)    # Historical ratios
get_key_metrics_ttm(symbol)             # TTM key metrics
get_key_metrics_history(symbol)         # Historical metrics
get_short_interest(symbol)              # Short interest data
get_financial_growth(symbol)            # Growth metrics
get_enterprise_value(symbol)            # Enterprise value
get_fail_to_deliver(symbol)             # FTD data

# Options placeholders (ready for your provider)
get_options_chain(symbol)               # Options chain
get_implied_volatility(symbol)          # IV data
```

### New Scoring in `analyzer.py`:

#### 1. **Fundamental Quality Score** (0-10 points)
Evaluates business quality based on:
- **Profitability** (3 pts): ROE, net margins
- **Financial Health** (3 pts): Current ratio, debt levels
- **Valuation Sanity** (2 pts): Reasonable P/E range

```python
fundamental_quality_score = self._calculate_fundamental_quality_score(ratios_ttm, key_metrics_ttm)
```

**Scoring Logic**:
- ROE > 15% = Up to 3 points
- Net Margin > 10% = Up to 2 points
- Current Ratio > 1.5 = 1.5 points
- Debt/Equity < 0.5 = 1.5 points
- P/E between 5-30 = 2 points

#### 2. **Short Interest Score** (0-10 points)
Evaluates short squeeze potential and bearish pressure:

```python
short_interest_score = self._calculate_short_interest_score(short_interest)
```

**Scoring Logic**:
- Moderate short (5-15%) + quick cover (<3 days) = +3 points (squeeze setup)
- High short (>20%) + days to cover >5 = +4 points (strong squeeze potential)
- Low short (<5%) = +2 points (less bearish pressure)
- Short interest decreasing = +2 points (shorts covering)
- Short interest increasing >20% = -1 point (more bearish)

#### 3. **Growth Score** (0-10 points)
Evaluates growth momentum:

```python
growth_score = self._calculate_growth_score(growth_metrics)
```

**Scoring Logic**:
- Revenue growth >20% = +3 points
- Revenue growth >10% = +2 points
- EPS growth >20% = +2 points
- Accelerating growth (vs previous quarter) = +1 point
- Declining revenue (<-10%) = -2 points

### Updated Weights in `config.py`:
```python
'weights': {
    'momentum_score': 0.20,              # Technical momentum
    'volume_score': 0.12,                # Volume analysis
    'technical_score': 0.18,             # RSI, MAs, breakouts
    'volatility_score': 0.08,            # Volatility sweet spot
    'relative_strength_score': 0.12,     # vs SPY
    'catalyst_score': 0.08,              # News sentiment
    'liquidity_score': 0.04,             # Trading liquidity
    'fundamental_quality_score': 0.10,   # 🆕 Business quality
    'short_interest_score': 0.04,        # 🆕 Short squeeze
    'growth_score': 0.04,                # 🆕 Growth momentum
}
# Total: 1.00 (100%)
```

### Enhanced Claude Analysis

Claude now receives and analyzes:
- Financial ratios in context
- Short interest data and squeeze potential
- Growth trends and momentum
- Fundamental quality indicators

The enhanced context includes:
```
Fundamentals: P/E 25.3, ROE 0.18, Debt/Equity 0.45, Current Ratio 2.1, Net Margin 0.15
Short Interest: 12.5% of float, 2.8 days to cover
Growth: Revenue 0.23, EPS 0.31
```

## 📈 How the New Scores Work Together

### Example Stock Analysis:

**ACME Corp (ACME) - $45.50**

**Original Scores** (Technical Only):
- Momentum: 8.2/10
- Volume: 7.5/10
- Technical: 7.8/10
- **Old Total: 7.4/10** ✅

**NEW Scores** (Technical + Fundamental):
- Momentum: 8.2/10
- Volume: 7.5/10
- Technical: 7.8/10
- **Fundamental Quality: 8.5/10** 🆕 (High ROE, low debt)
- **Short Interest: 7.2/10** 🆕 (15% short, 3 days cover - squeeze setup)
- **Growth: 8.0/10** 🆕 (25% revenue growth, accelerating)
- **New Total: 7.9/10** ✅✅ (Higher confidence!)

### Benefits:

1. **Avoid Value Traps**: High technical score + low fundamental score = avoid
2. **Identify Quality**: Technical + fundamental alignment = high conviction
3. **Spot Squeezes**: Short interest analysis adds catalyst awareness
4. **Growth Confirmation**: Growth score validates momentum trades

## 🎯 Usage Examples

### Standard Mode (No Changes Required):
```bash
python main.py input_tickers.txt
```

Your existing workflow works exactly the same! The new fundamental scores are automatically calculated and included in the total score.

### Claude Mode (Enhanced Context):
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```

Claude now receives the fundamental data and incorporates it into analysis:
- Mentions if fundamentals support the technical setup
- Flags fundamental red flags (high debt, declining growth)
- Identifies short squeeze opportunities
- Assesses business quality for risk management

## 🔍 Interpreting the New Scores

### Fundamental Quality Score:
- **8-10**: Excellent business (high margins, low debt, strong ROE)
- **6-8**: Good business (solid fundamentals)
- **4-6**: Average business (some concerns)
- **0-4**: Weak business (red flags, avoid)

### Short Interest Score:
- **8-10**: Strong squeeze setup (high short + catalysts)
- **6-8**: Potential squeeze or low bearish pressure
- **4-6**: Neutral short interest
- **0-4**: High bearish pressure or extreme short levels

### Growth Score:
- **8-10**: Strong accelerating growth
- **6-8**: Solid growth
- **4-6**: Modest or stable growth
- **0-4**: Declining or negative growth

## 📊 Data Availability Notes

### FMP API Coverage:
- ✅ **Financial Ratios**: Most US stocks, updated quarterly
- ✅ **Key Metrics**: Most US stocks, updated quarterly
- ✅ **Short Interest**: US stocks, updated bi-weekly
- ✅ **Growth Metrics**: Most US stocks, quarterly

### What to Expect:
- Small caps: May have limited fundamental data
- Recent IPOs: May not have historical ratios
- Non-US stocks: Coverage varies
- Missing data: System uses neutral scores (5/10)

## 🔄 Backward Compatibility

✅ **Fully backward compatible!**
- Existing scripts work without changes
- If fundamental data unavailable, uses neutral scores
- Old reports still generate correctly
- No breaking changes to your workflow

## 💡 Best Practices

### 1. **Use Fundamentals as a Filter**
- High technical score + low fundamental score = investigate carefully
- Low technical score + high fundamental score = watch for setup

### 2. **Short Interest Strategy**
- Score >7 with news catalyst = potential squeeze play
- Score <4 with high days-to-cover = avoid (bearish)

### 3. **Growth Validation**
- Momentum + Growth alignment = high conviction
- Momentum without growth = might be temporary

### 4. **Quality Check**
- Always check fundamental score for position sizing
- Higher fundamental score = can size larger
- Lower fundamental score = keep position smaller

## 🚀 Next Steps

### 1. **Test the New Features**
```bash
python main.py input_tickers.txt
```
Check the enhanced output with fundamental scores!

### 2. **Review Claude Analysis**
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```
See how Claude uses the new fundamental context.

### 3. **Add Options Data** (Optional)
Follow `OPTIONS_INTEGRATION_GUIDE.md` to add:
- Options chain analysis
- Implied volatility
- Options flow
- Greeks analysis

### 4. **Customize Weights** (Optional)
Edit `config.py` to adjust score weights for your strategy:
```python
# More fundamental-focused
'fundamental_quality_score': 0.15,  # Increase from 0.10
'growth_score': 0.05,               # Increase from 0.04

# More short-squeeze focused  
'short_interest_score': 0.08,       # Increase from 0.04
```

## 📝 Updated Files

The following files were enhanced:
1. ✅ `fmp_client.py` - Added 8 new API methods
2. ✅ `analyzer.py` - Added 3 new scoring methods
3. ✅ `config.py` - Updated scoring weights
4. ✅ `claude_analyzer_optimized.py` - Enhanced context with fundamentals

All changes are **additive only** - nothing was removed!

## 🎉 Summary

Your system now combines:
- ✅ **Technical Analysis** (original strength)
- ✅ **Fundamental Analysis** (new!)
- ✅ **Short Interest Analysis** (new!)
- ✅ **Growth Analysis** (new!)
- ✅ **AI Insights** (Claude Opus 4)

This gives you a **complete 360° view** of each stock for better short-term trading decisions!

---

**Questions?** Check these docs:
- `README.md` - System overview
- `CONFIGURATION_GUIDE.md` - Customize settings
- `OPTIONS_INTEGRATION_GUIDE.md` - Add options data
- `CLAUDE_TROUBLESHOOTING.md` - Fix issues
