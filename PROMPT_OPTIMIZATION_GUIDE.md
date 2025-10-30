# 🎯 OPTIMIZED PROMPTS FOR CLAUDE OPUS 4

## What's Been Improved

I've created an **optimized version** of the Claude analyzer specifically tuned for **Opus 4** and **short-term trading** (<2 months).

**File:** `claude_analyzer_optimized.py`

---

## 🚀 Key Improvements

### 1. **Short-Term Trading Focus**
**Before:** Generic analysis suitable for any timeframe
**After:** Laser-focused on 2-8 week trades

Every prompt now explicitly emphasizes:
- "Focus on the NEXT 2-8 WEEKS"
- "Near-term price impact, not long-term fundamentals"
- "Imminent catalysts with specific dates"

### 2. **Specific, Actionable Guidance**
**Before:** Broad recommendations
**After:** Tactical trading instructions

Now provides:
- Exact entry timing ("now" vs "wait for pullback" vs "on breakout")
- Specific price levels when possible
- Clear exit strategies with conditions
- Position sizing recommendations

### 3. **Catalyst Timing Emphasis**
**Before:** "Upcoming earnings"
**After:** "Q4 earnings October 28 - guidance raise expected"

Prompts now demand:
- SPECIFIC DATES for all catalysts
- Probability estimates when available
- Surprise potential assessment
- Convergence detection (multiple catalysts aligning)

### 4. **Red Flag Detection**
**Before:** General risk assessment
**After:** Specific red flag hunting

Now explicitly looks for:
- Insider selling spikes
- Accounting irregularities
- Regulatory investigations
- Management departures
- Guidance cuts
- Technical breakdowns

### 5. **Risk/Reward Ratios**
**Before:** Qualitative risk discussion
**After:** Quantified risk/reward (e.g., "1:3")

Helps you quickly assess if setup is worth it.

### 6. **Conviction Levels**
**Before:** Implicit confidence
**After:** Explicit High/Medium/Low conviction

Allows you to filter for only high-conviction trades.

### 7. **Position Sizing Guidance**
**Before:** No sizing recommendation
**After:** Large/Medium/Small/None with portfolio %

- Large: 5-10% (highest conviction, lowest risk)
- Medium: 3-5% (standard good setup)
- Small: 1-2% (speculative)
- None: 0% (avoid)

### 8. **Watch Points & Exit Conditions**
**Before:** General thesis
**After:** Specific monitoring plan

Now provides:
- What to watch daily/weekly
- Exact profit targets
- Specific stop loss levels
- Time-based exits
- News-based exit triggers

### 9. **Lower Temperature for Consistency**
Added `temperature=0.3` to all API calls for more consistent, focused responses (less creative variance).

### 10. **Streamlined Prompts**
**Before:** Very detailed but verbose
**After:** Concise critical instructions + examples

Opus 4 is smart enough that we can be more concise, letting it focus on analysis rather than parsing long prompts.

---

## 📊 Prompt Structure Comparison

### BEFORE (Generic):
```
Analyze the sentiment of recent news for this stock.

Provide:
1. Overall sentiment score (0-10)
2. Sentiment label
3. Brief summary
4. Key themes
```

### AFTER (Optimized for Short-Term Trading):
```
You are an expert short-term trader (<2 months) analyzing news sentiment.

Focus on NEAR-TERM price impact (next 2-8 weeks), not fundamentals.
Weight recent news heavily. Look for sentiment SHIFTS and ACCELERATION.
Consider if sentiment is priced in or has momentum.

Provide:
1. Sentiment Score (0-10): [specific ranges with meanings]
2. Label: Very Negative | Negative | Neutral | Positive | Very Positive
3. Summary: 2-3 sentences on narrative, direction, and short-term opportunity
4. Key Themes: 3-5 dominant topics
5. Sentiment Momentum: [specific options]

[Explicit JSON format with examples]
```

---

## 🔄 How to Use the Optimized Version

### Option 1: Replace Existing File (Recommended)

1. **Backup current version:**
```bash
copy claude_analyzer.py claude_analyzer_backup.py
```

2. **Replace with optimized:**
```bash
copy claude_analyzer_optimized.py claude_analyzer.py
```

3. **Run normally:**
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```

### Option 2: Test Side-by-Side

Keep both versions and compare:

**Run with original:**
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```
*(outputs to output/dashboard_deep_TIMESTAMP.html)*

**Edit main_with_claude.py temporarily:**
```python
# Line ~32, change:
from claude_analyzer import ClaudeAnalyzer
# To:
from claude_analyzer_optimized import ClaudeAnalyzer
```

**Run with optimized:**
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```
*(outputs to new timestamp file)*

**Compare the two HTML dashboards** to see the difference!

---

## 💡 What to Expect

### Better Recommendations

**Before:**
```
Recommendation: Buy
Confidence: Medium
Summary: Stock has good momentum and positive news.
```

**After:**
```
Recommendation: Strong Buy
Confidence: High
Position Size: Medium (3-5%)
Time Horizon: 2-4 weeks

Key Reasons:
• Q4 earnings Oct 28 expected to beat by 15% based on channel checks
• Technical breakout confirmed with 2.5x average volume
• RSI at 62 (not overbought), room to run to $310 resistance
• Sector rotation into tech creating tailwinds

Entry Strategy: Enter now at $285-290, strong support at $280
Exit Strategy: 
  • Profit target: $310 (+8-10% gain)
  • Stop loss: $275 (-5%)
  • Exit before earnings if no momentum by Oct 25

Watch Points:
• Monitor volume - need sustained >1M shares daily
• Watch sector ETF (XLK) - should remain above 50-day MA
• Track options flow for institutional positioning
```

### More Specific Catalysts

**Before:**
```
Upcoming Catalysts:
• Earnings report expected soon
• Potential product launch
```

**After:**
```
Upcoming Catalysts:
• Q4 Earnings: October 28, 4:00 PM ET
  - Impact: High (could move 10-15%)
  - Expected: EPS $2.15 vs consensus $2.05 (beat likely)
  - Surprise potential: High (whisper number $2.20)
  - Guidance expected to raise Q1 outlook
  
• FDA Decision: November 15 (or before)
  - Impact: Very High (could move 20%+)
  - Probability: 70% approval based on advisory committee vote
  - Timeline: "By November 15" means could be any day
  
Catalyst Convergence: Earnings + FDA decision within 3 weeks = compounded impact if both positive
```

### Clearer Risk Assessment

**Before:**
```
Risks:
• Competition increasing
• Regulatory concerns
Overall Risk: Moderate
```

**After:**
```
Risks:
• Patent Expiration (Medium Severity, High Likelihood)
  - Core patent expires March 2026
  - Generics could launch immediately
  - Timeframe: 16 months out, but market may front-run
  - Mitigation: Company developing next-gen product
  
• Competitor Product Launch (High Severity, Medium Likelihood)
  - ACME Corp launching competing product Q1 2025
  - Could capture 20% market share
  - Timeframe: 2-3 months
  - Mitigation: Price competition unlikely due to differentiation

Overall Risk Score: 6/10 (Moderate Risk)
Risk vs Reward: Favorable - 1:2.5 ratio

RED FLAGS: None identified
```

---

## 🎯 Optimization Rationale

### Why These Changes for Opus 4?

1. **Opus excels with clear directives** - Give it specific mission
2. **Opus understands context deeply** - Don't over-explain, focus critical points
3. **Opus handles complexity** - Can process multi-part requests efficiently
4. **Opus benefits from examples** - Showing desired output format helps
5. **Lower temperature** - Opus is creative by default; dial it down for trading

### Why Short-Term Focus?

Your goal is <2 month trades, so:
- Long-term fundamentals matter less
- Catalyst timing matters more
- Technical setup matters more
- Entry/exit precision matters more
- Position sizing matters more

---

## 📈 Expected Results

With optimized prompts, you should see:

✅ **More actionable recommendations**  
✅ **Specific entry/exit levels**  
✅ **Clear position sizing guidance**  
✅ **Explicit catalyst dates and probabilities**  
✅ **Tactical watch points**  
✅ **Higher conviction on good setups**  
✅ **More willingness to say "Avoid" on poor setups**  

---

## 🔧 Further Customization

### If You Want Even More Detail

In `claude_analyzer_optimized.py`, increase max_tokens:

```python
# Current
max_tokens=1800

# For more detailed analysis
max_tokens=2500
```

**Trade-off:** Slightly longer processing time, slightly higher cost

### If You Want Faster Responses

Reduce max_tokens:

```python
# For quicker analysis
max_tokens=1200
```

**Trade-off:** Less detailed recommendations

### If You Trade Different Timeframe

Edit all prompts, change:
```python
"<2 months"  # To your preferred timeframe
"2-8 weeks"  # To your preferred range
```

### If You Want More Conservative

In recommendation prompt, adjust thresholds:
```python
# Make "Strong Buy" harder to get
"Strong Buy: All factors align AND risk/reward >1:3 (instead of >1:2)"
```

---

## 💰 Cost Impact

The optimized prompts are actually **slightly cheaper** because:
- More concise prompts = fewer input tokens
- More structured output = fewer output tokens
- More consistent JSON = less retries

**Estimate:** ~5-10% token reduction per stock

---

## 🎓 Testing Your Results

### Before/After Comparison

1. Run 5-10 stocks with original analyzer
2. Run same stocks with optimized analyzer
3. Compare:
   - Specificity of recommendations
   - Actionability of guidance
   - Confidence in decisions
   - Win rate over time

### Track These Metrics

- **Recommendation accuracy** - Did "Strong Buy" outperform?
- **Entry timing** - Did "enter now" vs "wait" calls work?
- **Exit accuracy** - Did profit targets get hit?
- **Risk management** - Did stop losses save you?

---

## ✅ Quick Start

**Want the optimized version? Here's the 30-second setup:**

```bash
# 1. Backup original
copy claude_analyzer.py claude_analyzer_backup.py

# 2. Use optimized version
copy claude_analyzer_optimized.py claude_analyzer.py

# 3. Run your analysis
python main_with_claude.py input_tickers.txt --deep-analysis

# 4. Check results in HTML dashboard
# Compare quality to your previous runs!
```

---

## 🎯 Bottom Line

The **optimized prompts extract maximum value from Opus 4** by:
1. Being crystal clear about what you need
2. Focusing on short-term trading specifics
3. Demanding actionable, tactical guidance
4. Providing structure for consistent output

**Your $6/day gets you much better insights with these prompts!**

---

**Ready to try it? Replace your claude_analyzer.py with the optimized version and see the difference!** 🚀
