# 📋 QUICK REFERENCE - One Page Setup

## 🔑 API Keys (config.py)

```python
# Line 6 - Required
FMP_API_KEY = "your_fmp_key"  

# Line 14 - Required for Options (YOU HAVE THIS!)
POLYGON_API_KEY = "your_polygon_starter_key"

# Line 20 - Verify this
POLYGON_RATE_LIMIT = 100  # ✓ Starter plan

# Line 24 - Optional
CLAUDE_API_KEY = "your_claude_key"  # Only if using AI mode
```

---

## 🚀 Quick Commands

```bash
# Install
pip install -r requirements.txt

# Run Standard Mode (fast, includes options)
python main.py input_tickers.txt

# Run AI Mode (slow, expensive, comprehensive)
python main_with_claude.py input_tickers.txt --deep-analysis
```

---

## 📊 Scoring Breakdown

| Component | Weight | What It Measures |
|-----------|--------|------------------|
| Momentum | 18% | Price trends |
| Volume | 11% | Volume spikes |
| Technical | 17% | RSI, MAs, breakouts |
| Volatility | 7% | Optimal volatility |
| Rel. Strength | 11% | vs SPY |
| Catalyst | 7% | News sentiment |
| Liquidity | 4% | Trading ease |
| **Fundamental** | **10%** | **Business quality** ✨ |
| **Short Interest** | **4%** | **Squeeze potential** ✨ |
| **Growth** | **4%** | **Revenue/EPS growth** ✨ |
| **Options** | **7%** | **P/C ratio, liquidity** ✨ |
| **Total** | **100%** | |

---

## 🎯 Score Interpretation

- **8.0-10.0** = Strong Buy (high conviction)
- **6.5-7.9** = Buy (moderate conviction)
- **5.0-6.4** = Hold/Watch (low conviction)
- **0-4.9** = Avoid (red flags)

---

## 📁 Input File Format

```
# input_tickers.txt
AAPL
MSFT
GOOGL
TSLA
NVDA
```

---

## 📤 Output Location

```
output/
  ├── stock_analysis_report_2025-10-27.html  ← Open this
  └── stock_analysis_data_2025-10-27.csv
```

---

## 🔍 What Options Analysis Shows

```
Options Score: 9.2/10
  • P/C Ratio: 0.68 (Very Bullish)
  • Liquidity: Excellent (150 contracts)
  • Sentiment: Strongly bullish
```

**P/C Ratio Guide:**
- < 0.7 = Very bullish (more calls than puts)
- 0.7-1.0 = Bullish
- 1.0-1.3 = Neutral
- > 1.3 = Bearish (more puts than calls)

---

## 💰 Costs

- **FMP**: $0-99/month (Starter: $14.99 recommended)
- **Polygon**: $29/month (your Starter plan) ✓
- **Claude**: ~$6 per AI analysis session (optional)

**Total: ~$44/month** (without Claude)

---

## 🐛 Common Issues

**"Invalid API key"**
→ Check spelling in config.py

**"Rate limit"**
→ Wait 60 seconds or lower rate limits in config

**"No options data"**
→ Normal for small caps; system handles it

**"Module not found"**
→ `pip install -r requirements.txt`

---

## 📚 Full Docs

- **SETUP_GUIDE.md** ← Read this for complete setup
- **POLYGON_INSTALLATION.md** ← Options details
- **CONFIGURATION_GUIDE.md** ← Advanced config
- **README.md** ← System overview

---

## ✅ Pre-Flight Check

- [ ] API keys in config.py
- [ ] `POLYGON_RATE_LIMIT = 100`
- [ ] Created input_tickers.txt
- [ ] Ran: `pip install -r requirements.txt`
- [ ] Ran: `python main.py input_tickers.txt`
- [ ] Checked `output/` folder for report

**All done? Start analyzing!** 🚀

---

## 💡 Quick Tips

1. **Start with 3-5 stocks** to test
2. **Review HTML report** for easy reading
3. **Focus on scores >7.5** for high conviction
4. **Options data adds 7%** to total score
5. **System works without Claude** (standard mode only)
6. **50 stocks** ≈ **3-5 minutes** to analyze

---

**Need more help?** Open SETUP_GUIDE.md for full instructions.
