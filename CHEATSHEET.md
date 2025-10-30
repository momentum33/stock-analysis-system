# 📋 QUICK REFERENCE CHEAT SHEET

## ⚡ Quick Commands

```bash
# First time setup
pip install requests numpy

# Verify installation
python setup.py

# Run analysis
python main.py input_tickers.txt

# Run with custom file
python main.py my_stocks.txt
```

---

## 🎯 Daily Workflow

1. Export screener results to text file
2. `python main.py your_file.txt`
3. Open `output/dashboard_*.html`
4. Review top 10 picks

**Time:** 2-5 minutes

---

## ⚙️ Configuration Quick Edit

**File:** `config.py`

### Set API Key (Required!)
```python
FMP_API_KEY = "your_actual_key_here"
```

### Adjust Scoring Weights
```python
'weights': {
    'momentum_score': 0.25,      # Increase for momentum
    'volume_score': 0.15,        # Increase for volume plays
    'technical_score': 0.20,     # Increase for technical
    'volatility_score': 0.10,    # Increase for stability
    'relative_strength_score': 0.15,  # Increase for market leaders
    'catalyst_score': 0.10,      # Increase for news plays
    'liquidity_score': 0.05,     # Increase for easy fills
}
# Must sum to 1.0!
```

### Filter Stocks
```python
'min_avg_volume': 100000,    # Higher = more liquid
'min_price': 2.0,            # Higher = avoid penny stocks
'max_price': 10000,          # Lower = avoid expensive stocks
```

---

## 📊 Score Meanings (0-10 scale)

| Score | What It Measures |
|-------|------------------|
| **Momentum** | Recent price gains & acceleration |
| **Volume** | Trading activity & spikes |
| **Technical** | RSI, MAs, breakouts |
| **Volatility** | Movement range (sweet spot: 2-4%) |
| **Rel. Strength** | Performance vs market (SPY) |
| **Catalyst** | News sentiment & events |
| **Liquidity** | Volume & spread (ease of trading) |

**Composite Score:** Weighted average of all 7 scores

---

## 🎨 Pre-Built Configurations

### Momentum Trading
```python
'momentum_score': 0.35,
'volume_score': 0.25,
'technical_score': 0.15,
```

### Technical Trading
```python
'technical_score': 0.35,
'volatility_score': 0.20,
'liquidity_score': 0.15,
```

### News Trading
```python
'catalyst_score': 0.30,
'volume_score': 0.20,
'momentum_score': 0.20,
```

---

## 📁 Output Files

| File | Use For |
|------|---------|
| **CSV** | Excel analysis, tracking |
| **HTML** | Quick visual review (BEST!) |
| **TXT** | Detailed breakdown |

**Location:** `output/` directory

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| API key error | Set key in config.py |
| Rate limit | Wait 24h or upgrade tier |
| No stocks pass | Lower filters in config.py |
| Wrong scores | Adjust weights |
| Missing data | Check ticker is valid |

---

## 💡 Pro Tips

✅ Run before market open  
✅ Focus on top 3-5 stocks  
✅ Adjust weights weekly  
✅ Combine with chart analysis  
✅ Track performance to optimize  

---

## 📱 API Limits

**Free Tier:**
- 250 requests/day
- 5 requests/second
- ~50 stocks/day

**Each Stock = 5 Requests:**
- Quote
- Historical data
- Profile
- News
- Metrics

---

## 🎯 Score Targets

| Range | Signal |
|-------|--------|
| **8.0-10.0** | Strong buy |
| **6.0-7.9** | Buy |
| **4.0-5.9** | Watch |
| **0.0-3.9** | Avoid |

---

## 🔄 Common Edits

### More Aggressive
```python
'momentum_score': 0.35  # ⬆
'volume_score': 0.25    # ⬆
'volatility_score': 0.05 # ⬇
```

### More Conservative
```python
'technical_score': 0.35  # ⬆
'volatility_score': 0.20 # ⬆
'liquidity_score': 0.15  # ⬆
```

---

## 📖 Documentation Files

| File | When to Read |
|------|--------------|
| **QUICKSTART.md** | First time (5 min) |
| **README.md** | Full manual (15 min) |
| **CONFIGURATION_GUIDE.md** | Customizing (20 min) |
| **ARCHITECTURE.md** | Technical (25 min) |

---

## ⌨️ Input File Format

```
# One ticker per line
AAPL
TSLA
NVDA
# Comments start with #
```

---

## 🚀 Keyboard Shortcuts

```bash
# Save time with aliases (add to ~/.bashrc)
alias stock='python /path/to/main.py'
alias stockcheck='python /path/to/setup.py'

# Then just:
stock my_tickers.txt
```

---

## 📊 Example Results

```
#1 AAPL - Score: 8.5
   • Price: $175.50 (+2.3%)
   • Strong momentum & technical

#2 TSLA - Score: 8.2  
   • Price: $242.75 (+5.1%)
   • High volume & catalyst

#3 NVDA - Score: 7.8
   • Price: $495.20 (+1.8%)
   • Technical breakout
```

---

## 🎓 Best Practices

1. **Consistent timing** - Run same time daily
2. **Weight tracking** - Log what works
3. **Hybrid approach** - Use + your analysis
4. **Risk management** - Don't blindly follow
5. **Paper trade first** - Test your settings

---

## 📈 Success Metrics

Track these to optimize:
- Win rate on top 3 picks
- Average gain of top 10
- Days to profit
- False positive rate

---

## 🔄 Update Cycle

| Frequency | Action |
|-----------|--------|
| **Daily** | Run analysis |
| **Weekly** | Review results, adjust weights |
| **Monthly** | Optimize filters |
| **Quarterly** | Major strategy review |

---

## 🆘 Quick Help

**Setup issues?** → Run `python setup.py`  
**Need API key?** → https://financialmodelingprep.com  
**Full docs?** → See README.md  
**Customize?** → See CONFIGURATION_GUIDE.md  

---

## 💰 Cost Breakdown

**Free Tier:**
- $0/month
- 250 requests/day
- Perfect for testing

**Paid Tiers:**
- Starter: $14-29/month
- Pro: $49-99/month
- Higher limits & features

---

**Print this page for quick reference!**
