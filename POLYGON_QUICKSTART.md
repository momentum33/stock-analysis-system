# 🚀 Polygon.io Quick Setup

## 3-Minute Setup

### 1. Get API Key (2 minutes)
1. Go to https://polygon.io/
2. Click "Sign Up" (free tier available)
3. Verify email
4. Go to Dashboard → API Keys
5. Copy your API key

### 2. Configure (1 minute)
Edit `config.py`:
```python
POLYGON_API_KEY = "paste_your_key_here"
POLYGON_RATE_LIMIT = 5  # Free tier
```

### 3. Run (immediate)
```bash
python main.py input_tickers.txt
```

That's it! ✅

---

## What You Get

### With Free Tier ($0/mo):
✅ 5 API calls per minute
✅ All options data (Greeks, IV, volume)
✅ Official short interest data
✅ Historical data access
✅ Perfect for testing & learning

Can analyze: ~50-100 stocks per day

### Upgrade Benefits:

**Starter ($29/mo)**:
- 100 calls/min
- Analyze 500+ stocks/day
- Real-time data
- Better for daily use

**Developer ($99/mo)**:
- 500 calls/min
- Unlimited daily analysis
- Professional trading

---

## Quick Test

After setup, test with:
```bash
python main.py input_tickers.txt
```

Look for:
```
✓ Polygon.io client initialized (Options & Short Interest enabled)
  📊 Analyzing options chain for AAPL...
  ✓ AAPL: Score = 8.2/10
```

---

## Troubleshooting

### "API key not set"
→ Edit config.py, paste your key

### "Rate limit exceeded"
→ Free tier: Wait 12 seconds between calls
→ Or upgrade to paid tier

### "No options data"
→ Some stocks have no options
→ Try: AAPL, TSLA, NVDA, SPY

---

## Cost Calculator

**Free Tier**:
- 5 calls/min = 300 calls/hour
- 2-3 calls per stock (options + short interest)
- **Can analyze 50-100 stocks/day FREE**

**Your System**:
- 67 tickers in watchlist
- Free tier handles this easily!
- Takes ~10-15 minutes to analyze all

---

## Features Enabled

With Polygon you get:

1. **Options Sentiment Score** (7% of total)
   - Put/Call ratios
   - Implied volatility
   - Options volume
   - Net delta positioning

2. **Enhanced Short Interest**
   - Bi-monthly official data
   - More reliable than FMP
   - Historical trends
   - Days to cover

3. **Claude Context**
   - Options data in analysis
   - Put/Call interpretation
   - IV analysis
   - Better recommendations

---

## Compare Plans

| Feature | Free | Starter | Developer |
|---------|------|---------|-----------|
| **Cost** | $0 | $29/mo | $99/mo |
| **Calls/Min** | 5 | 100 | 500 |
| **Options Data** | ✅ | ✅ | ✅ |
| **Short Interest** | ✅ | ✅ | ✅ |
| **Real-time** | ❌ | ✅ | ✅ |
| **Best For** | Testing | Daily use | Professional |

**Recommendation**: Start free, upgrade if needed

---

## Example Output

### Before Polygon:
```
AAPL: Score = 7.8/10
- Momentum: 8.2
- Volume: 7.5
- Technical: 7.8
- Fundamentals: 8.1
```

### After Polygon:
```
AAPL: Score = 8.3/10
- Momentum: 8.2
- Volume: 7.5
- Technical: 7.8
- Fundamentals: 8.1
- Options: 8.7 ⭐ NEW
  → Put/Call: 0.65 (bullish)
  → IV: 28% (normal)
  → Volume: 15,432 (high)
```

---

## Disable If Needed

Don't want options analysis?

```python
# In config.py
ENABLE_OPTIONS_ANALYSIS = False
ENABLE_POLYGON_SHORT_INTEREST = False
```

System works fine without Polygon!

---

## Resources

- **Polygon Docs**: https://polygon.io/docs
- **Options API**: https://polygon.io/docs/rest/options
- **Python Client**: `pip install polygon-api-client`
- **Support**: support@polygon.io

---

## Next Steps

1. ✅ Set up Polygon API key
2. ✅ Run `python main.py input_tickers.txt`
3. ✅ Check options scores in output
4. ✅ Review Claude's options insights
5. ✅ Upgrade if you hit rate limits

**That's all! Ready to trade with options intelligence! 🎯**
