# 🤖 CLAUDE AI DEEP ANALYSIS GUIDE

## Overview

This enhanced version uses Claude AI to perform qualitative, deep analysis on your top-ranked stocks. While the quantitative system identifies opportunities through technical and volume analysis, Claude provides the "human-like" insight that's hard to code: understanding news sentiment, identifying catalysts, assessing risks, and making nuanced trading recommendations.

---

## 🎯 What Claude Adds to the System

### Quantitative System (FMP API)
✅ Technical indicators (RSI, moving averages)  
✅ Volume analysis  
✅ Price momentum  
✅ Relative strength  
✅ Basic keyword sentiment  

### Qualitative Analysis (Claude AI)
✨ **Deep News Sentiment** - Understands context, sarcasm, and implications  
✨ **Catalyst Identification** - Recognizes earnings, FDA approvals, partnerships  
✨ **Risk Assessment** - Identifies regulatory, competitive, and operational risks  
✨ **Bull/Bear Thesis** - Creates reasoned cases for both sides  
✨ **Trading Recommendations** - Synthesizes everything into actionable advice  
✨ **Comparative Ranking** - Re-ranks stocks considering qualitative factors  

---

## 📊 Analysis Components

### 1. News Sentiment Analysis
**What it does:**
- Analyzes 5-10 recent news articles
- Scores sentiment 0-10 (0=very negative, 10=very positive)
- Identifies key themes in the news
- Provides nuanced understanding (not just keyword counting)

**Example Output:**
```
Sentiment: Very Positive (8.5/10)
Summary: "Recent earnings beat and new product launch 
         generating strong institutional interest. 
         Analyst upgrades following guidance raise."
Key Themes:
  • Earnings beat
  • Product innovation
  • Analyst upgrades
```

### 2. Catalyst Identification
**What it does:**
- Identifies upcoming events (earnings, FDA decisions, product launches)
- Assesses recent catalysts that already occurred
- Rates impact potential (High/Medium/Low)
- Estimates timeframes

**Example Output:**
```
Upcoming Catalysts:
  • Q4 Earnings (High impact, 2 weeks, positive expected)
  • New product launch (Medium impact, 1 month, positive)

Recent Catalysts:
  • FDA approval granted (High impact, 1 week ago)
  • Partnership announced (Medium impact, 3 days ago)

Catalyst Score: 8/10
```

### 3. Risk Assessment
**What it does:**
- Identifies specific risks (regulatory, competitive, market)
- Rates severity and likelihood
- Flags red flags that make it an "avoid"
- Provides risk score (0=very risky, 10=very safe)

**Example Output:**
```
Key Risks:
  • Patent expiration (High severity, Medium likelihood)
  • Regulatory scrutiny (Medium severity, Low likelihood)
  • Competition from ACME (Medium severity, High likelihood)

Overall Risk: Moderate (6/10)
Red Flags: None
```

### 4. Bull/Bear Thesis
**What it does:**
- Creates 3-5 reasons for price to go UP (bull case)
- Creates 3-5 reasons for price to go DOWN (bear case)
- Determines which case is stronger
- Assesses conviction level
- Suggests risk/reward ratio

**Example Output:**
```
Bull Case (Stronger):
  • Strong earnings momentum continuing
  • New product expected to drive 20% revenue growth
  • Technical breakout confirmed with volume
  • Sector rotation favorable

Bear Case:
  • Valuation elevated vs peers
  • Macro headwinds could slow growth
  • Competition intensifying

Conviction: High
Risk/Reward: 1:3 (favorable)
```

### 5. Trading Recommendation
**What it does:**
- Synthesizes all analysis into clear recommendation
- Provides: Strong Buy / Buy / Hold / Avoid
- Suggests position size (Small/Medium/Large)
- Lists key reasons, watch points, exit conditions
- Estimates time horizon

**Example Output:**
```
Recommendation: STRONG BUY
Confidence: High
Position Size: Medium

Key Reasons:
  • Multiple positive catalysts converging
  • Technical setup is ideal for breakout
  • Risk/reward heavily favors upside

Watch Points:
  • Monitor earnings date for confirmation
  • Watch sector rotation trends

Exit Conditions:
  • Take profits at 15-20% gain
  • Stop loss at 7% below entry

Time Horizon: 2-4 weeks
```

### 6. Comparative Ranking
**What it does:**
- Analyzes ALL top stocks together
- Re-ranks based on qualitative factors
- Provides reasoning for each pick
- Identifies stocks to avoid
- Gives market outlook context

**Example Output:**
```
Claude's Top 5:
#1. AAPL - Perfect setup with upcoming catalyst
#2. NVDA - Momentum + positive sector rotation
#3. MSFT - Strong fundamentals, lower risk
#4. TSLA - High risk/reward, volatile but trending
#5. AMD - Good entry point, catalyst in 2 weeks

Avoid:
  • XYZ - Red flag in earnings report
  • ABC - Regulatory risk too high

Market Outlook: Bullish with rotation into tech
```

---

## 🚀 How to Use

### Step 1: Get Claude API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Go to API Keys
4. Create new key
5. Copy the key (starts with `sk-ant-api...`)

### Step 2: Install Dependencies

```bash
pip install anthropic
```

Or update all dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Configure

Edit `config.py`:

```python
# Claude API Configuration
CLAUDE_API_KEY = "sk-ant-api-your-key-here"
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Fast and accurate
ENABLE_DEEP_ANALYSIS = True  # Enable by default
DEEP_ANALYSIS_TOP_N = 20  # Analyze top 20 stocks
```

### Step 4: Run Analysis

**Method 1: Command line flag**
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```

**Method 2: Enable in config**
Set `ENABLE_DEEP_ANALYSIS = True` in config.py, then:
```bash
python main_with_claude.py input_tickers.txt
```

### Step 5: Review Results

Three enhanced reports will be generated:
1. **CSV** - Includes Claude scores and recommendations
2. **HTML Dashboard** - Beautiful visual interface with AI insights
3. **Text Report** - Detailed analysis for each stock

---

## ⏱️ Time & Performance

### Processing Time

| Stocks | Quantitative | Claude Deep Analysis | Total |
|--------|-------------|---------------------|-------|
| 50 | 2-4 min | - | 2-4 min |
| 50 + Top 10 | 2-4 min | 3-5 min | 5-9 min |
| 50 + Top 20 | 2-4 min | 6-10 min | 8-14 min |

**Note:** Claude analysis runs sequentially (one stock at a time) to ensure quality.

### API Calls

**Per stock analyzed:**
- 5 Claude API calls (sentiment, catalysts, risks, thesis, recommendation)
- ~2,000-3,000 tokens per stock
- 1 final call for comparative ranking

**Top 20 stocks:**
- 100 Claude API calls (20 × 5)
- Plus 1 comparative call
- Total: ~50,000-70,000 tokens

---

## 💰 Cost Analysis

### Claude API Pricing (as of 2024)

**Claude Sonnet 4 (Recommended):**
- Input: $3 per million tokens
- Output: $15 per million tokens

**Claude Opus 4 (Most Thorough):**
- Input: $15 per million tokens
- Output: $75 per million tokens

### Cost Per Analysis

**Using Claude Sonnet 4:**

| Analysis | Tokens | Cost |
|----------|--------|------|
| Single stock deep analysis | ~5,000 | ~$0.06 |
| Top 10 stocks | ~50,000 | ~$0.60 |
| Top 20 stocks | ~100,000 | ~$1.20 |
| Comparative ranking | ~10,000 | ~$0.15 |

**Daily Usage (analyzing 50 stocks + top 20 deep):**
- Quantitative: FMP API costs (separate)
- Deep Analysis: ~$1.35 per day
- Monthly: ~$40 (20 trading days)

**Using Claude Opus 4 (more thorough but expensive):**
- Top 20 stocks: ~$6.00 per run
- Monthly: ~$120 (20 trading days)

### Cost-Saving Tips

1. **Analyze fewer stocks deeply** (Top 10 instead of 20)
2. **Use Sonnet instead of Opus** (5x cheaper, still excellent)
3. **Run only on promising days** (when your screener has good candidates)
4. **Batch weekly** (do deep analysis once a week, not daily)

---

## 🎨 Models Comparison

### Claude Sonnet 4 (Recommended)
**Best for:** Daily trading, cost-conscious users

✅ Fast (30-40 seconds per stock)  
✅ Affordable (~$1.35 for top 20)  
✅ Excellent quality (95% as good as Opus)  
✅ Great for most use cases  

**Cons:**
❌ Slightly less nuanced than Opus
❌ May occasionally miss subtle implications

### Claude Opus 4 (Premium)
**Best for:** Critical decisions, wealth management

✅ Best quality (most thorough)  
✅ Catches subtle nuances  
✅ More creative insights  
✅ Better at complex analysis  

**Cons:**
❌ 5x more expensive
❌ Slower (60-90 seconds per stock)
❌ Overkill for most trading

**Recommendation:** Start with Sonnet. Upgrade to Opus only if:
- Trading large positions (>$100K)
- Need maximum confidence
- Managing client money
- Cost is not a concern

---

## 🔧 Configuration Options

### In config.py

```python
# Model Selection
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Fast & affordable
# CLAUDE_MODEL = "claude-opus-4-20250514"  # Best quality

# How many stocks to analyze deeply
DEEP_ANALYSIS_TOP_N = 20  # Options: 5, 10, 15, 20

# Enable by default (vs command line flag)
ENABLE_DEEP_ANALYSIS = False  # True = always on
```

### Command Line Options

```bash
# Basic quantitative only
python main_with_claude.py input.txt

# With deep analysis
python main_with_claude.py input.txt --deep-analysis

# Alternative: use main.py (no Claude option)
python main.py input.txt
```

---

## 📈 Output Examples

### CSV Output (Enhanced)

Additional columns with Claude analysis:
- `sentiment_score` (0-10)
- `sentiment_label` (Very Positive, Positive, etc.)
- `catalyst_score_claude` (0-10)
- `risk_score` (0-10)
- `risk_label` (Very Low, Low, Moderate, High, Very High)
- `recommendation` (Strong Buy, Buy, Hold, Avoid)
- `confidence` (High, Medium, Low)
- `position_size` (Small, Medium, Large)
- `stronger_case` (bull, bear, neutral)
- `time_horizon` (days/weeks)

### HTML Dashboard (Enhanced)

Features Claude's insights:
- 🤖 AI-Enhanced badge
- Sentiment emoji indicators
- Bull/Bear case side-by-side
- Risk level indicators
- Trading recommendations with confidence
- Key catalysts highlighted
- Red flags prominently displayed
- Market outlook section
- Claude's top pick summary

### Text Report (Enhanced)

Detailed narrative format including:
- Market outlook
- Top pick summary from Claude
- Individual stock deep dives:
  - Recommendation with reasoning
  - Sentiment analysis
  - Bull case (3-5 reasons)
  - Bear case (3-5 reasons)
  - Catalysts
  - Risks and red flags
  - Key reasons to buy/avoid
  - Watch points
  - Exit conditions

---

## 💡 Best Practices

### When to Use Deep Analysis

✅ **Use Claude when:**
- Making significant trades (>$10K)
- High conviction required
- Confused between multiple picks
- News-heavy stocks
- Catalyst-driven trades
- Risk assessment critical

❌ **Skip Claude when:**
- Just scanning for ideas
- Very small positions
- Pure technical plays
- Low conviction day trades
- Want to save on API costs

### How to Interpret Results

**High Confidence + Strong Buy:**
- Consider larger position
- Fast entry
- Watch catalysts closely

**Medium Confidence + Buy:**
- Standard position size
- Wait for better entry
- Monitor closely

**Low Confidence:**
- Small position or skip
- More research needed
- Paper trade first

**Conflicting Signals:**
- Quantitative says buy, Claude says avoid → Investigate why
- Sentiment positive but risks high → Assess risk tolerance
- Technical strong but thesis weak → May be short-term only

### Combining Quantitative + Qualitative

**Best Setup:**
1. High quantitative score (>7.5)
2. Positive sentiment (>6)
3. Strong bull case
4. Low-moderate risk
5. Near-term catalyst
6. High confidence recommendation

**Red Flags:**
1. Quantitative and Claude disagree significantly
2. High risk score with red flags
3. Bear case is stronger than bull case
4. Low confidence recommendation
5. Multiple competing catalysts

---

## 🐛 Troubleshooting

### "anthropic package not installed"
```bash
pip install anthropic
```

### "Invalid API key"
- Check your key in config.py
- Verify it starts with `sk-ant-api...`
- Ensure no extra spaces
- Generate new key if needed

### "Rate limit exceeded"
- Claude has generous rate limits (50 requests/min)
- Usually not an issue
- If hit, script will handle automatically

### "JSON parsing error"
- Rare - Claude response not valid JSON
- Script handles gracefully
- Affected stock shows "Unable to analyze"
- Other stocks continue normally

### Analysis taking too long
- Normal: 30-60 seconds per stock
- Top 20 = 10-20 minutes total
- Use Sonnet instead of Opus
- Reduce DEEP_ANALYSIS_TOP_N

### Costs higher than expected
- Check which model you're using
- Verify DEEP_ANALYSIS_TOP_N setting
- Review actual token usage in console
- Consider analyzing fewer stocks

---

## 🎓 Advanced Usage

### Custom Analysis Prompts

Edit `claude_analyzer.py` to customize what Claude analyzes. For example, add earnings analysis:

```python
def _analyze_earnings(self, context, financial_data):
    prompt = f"""Analyze the earnings quality and guidance for this stock...
    {context}
    """
    # Claude analysis here
```

### Filtering Based on Claude

In your workflow, you could:

```python
# Only keep stocks with Strong Buy or Buy
strong_picks = [s for s in stocks 
                if s['claude_analysis']['recommendation']['recommendation'] 
                in ['Strong Buy', 'Buy']]

# Only high confidence picks
high_conf = [s for s in stocks 
             if s['claude_analysis']['recommendation']['confidence'] == 'High']

# Filter out high risk
safe_picks = [s for s in stocks 
              if s['claude_analysis']['risks']['overall_risk_score'] >= 6]
```

### Automated Decision Making

```python
def should_trade(stock):
    """Automated decision logic combining quant + qual"""
    quant_score = stock['total_score']
    claude = stock['claude_analysis']
    
    rec = claude['recommendation']
    risks = claude['risks']
    
    # Strong buy conditions
    if (quant_score >= 8.0 and 
        rec['recommendation'] == 'Strong Buy' and
        rec['confidence'] == 'High' and
        risks['overall_risk_score'] >= 6):
        return 'STRONG_BUY'
    
    # Avoid conditions
    if (risks['red_flags'] or
        risks['overall_risk_score'] < 4 or
        rec['recommendation'] == 'Avoid'):
        return 'AVOID'
    
    return 'CONSIDER'
```

---

## 📊 Example Complete Workflow

### Morning Routine with Claude

```bash
# 1. Run your screener (external tool) → export to input.txt

# 2. Run quantitative analysis (2-4 minutes)
python main_with_claude.py input.txt --deep-analysis

# 3. Coffee break while Claude works (10-15 minutes)

# 4. Open dashboard_deep_*.html in browser

# 5. Review Claude's top picks:
   - Check sentiment is positive
   - Verify catalysts make sense
   - Assess risk level acceptable
   - Note time horizon matches your plan

# 6. Deep dive on top 3:
   - Read full bull/bear case
   - Review watch points
   - Check exit conditions
   - Look at actual news articles

# 7. Make trading decisions:
   - Enter positions with clear plan
   - Set stops based on exit conditions
   - Monitor watch points during day

# 8. Track results:
   - Note which picks worked
   - Identify patterns in Claude's recs
   - Refine your process
```

---

## 🎯 Summary: Why Use Claude?

**The Problem:**
- Quantitative systems miss context
- Keyword sentiment is superficial  
- Hard to code "red flag" detection
- Can't assess complex catalysts
- No nuanced risk assessment

**The Solution:**
- Claude reads news like a human
- Understands implications and context
- Identifies subtle catalysts
- Assesses multifaceted risks
- Provides reasoned recommendations

**The Result:**
- Better stock selection
- Fewer false positives
- Earlier risk identification
- More confident decisions
- Higher win rate

**Cost:** ~$1.35/day for professional-grade analysis that would take hours manually

**Bottom Line:** If you're serious about short-term trading, Claude's insights are worth far more than the cost. It's like having an expert analyst reviewing every pick before you trade.

---

## 🚀 Getting Started Checklist

- [ ] Get Claude API key from console.anthropic.com
- [ ] Add key to config.py
- [ ] Install anthropic package
- [ ] Run test with --deep-analysis flag
- [ ] Review one of the enhanced reports
- [ ] Compare Claude's picks vs quantitative ranking
- [ ] Make a small trade based on recommendation
- [ ] Track the result
- [ ] Decide if Claude's insights are valuable for your trading

**Start today and see the difference AI-enhanced analysis makes!**
