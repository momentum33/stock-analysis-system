# 🚀 QUICK START GUIDE

## Step 1: Install Dependencies (30 seconds)

```bash
pip install requests numpy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 minute)

1. Get FREE API key: https://financialmodelingprep.com/developer/docs/
2. Open `config.py`
3. Replace this line:
   ```python
   FMP_API_KEY = "YOUR_FMP_API_KEY_HERE"
   ```
   With your actual key:
   ```python
   FMP_API_KEY = "abc123xyz789"  # Your actual key
   ```
4. Save the file

## Step 3: Test Setup (10 seconds)

```bash
python setup.py
```

Should show all green checkmarks ✓

## Step 4: Run Your First Analysis (2-5 minutes)

```bash
python main.py input_tickers.txt
```

The sample file includes 10 popular stocks (AAPL, TSLA, etc.)

## Step 5: View Results

Open `output/dashboard_YYYYMMDD_HHMMSS.html` in your browser!

---

## For Daily Use

1. **Export your screener results** to a text file (one ticker per line)
2. **Run analysis**:
   ```bash
   python main.py your_screener_file.txt
   ```
3. **Open the HTML dashboard** in your browser
4. **Review the top 10** ranked stocks

---

## Example Input File Format

Create a file called `my_stocks.txt`:
```
AAPL
TSLA
NVDA
MSFT
AMD
```

Then run:
```bash
python main.py my_stocks.txt
```

---

## Customize Scoring Weights

Edit `config.py` to adjust what matters most:

```python
'weights': {
    'momentum_score': 0.25,         # Price trends
    'volume_score': 0.15,           # Trading activity
    'technical_score': 0.20,        # Indicators (RSI, MA)
    'volatility_score': 0.10,       # Movement potential
    'relative_strength_score': 0.15,# vs Market
    'catalyst_score': 0.10,         # News/events
    'liquidity_score': 0.05,        # Ease of trading
}
```

Weights must sum to 1.0!

---

## Common Adjustments

### For Momentum Trading
```python
'momentum_score': 0.35,  # Increase
'volume_score': 0.25,    # Increase
'technical_score': 0.20,
'catalyst_score': 0.15,  # Increase
```

### For Technical Trading
```python
'technical_score': 0.35,  # Increase
'volatility_score': 0.20, # Increase
'momentum_score': 0.25,
```

---

## Troubleshooting

**"API key error"**
- Check config.py has your actual key
- Verify key works at financialmodelingprep.com

**"Rate limit exceeded"**
- Free tier: 250 requests/day
- Limit your input to ~50 stocks
- Or upgrade to paid tier

**"No stocks passed filters"**
- Lower min_avg_volume in config.py
- Adjust price range filters
- Check input tickers are valid

---

## Output Files Explained

1. **CSV file** - Import to Excel/Sheets for analysis
2. **HTML dashboard** - Quick visual overview (BEST FOR DAILY USE)
3. **Text report** - Detailed breakdown

---

## Pro Tips

✅ Run analysis before market open  
✅ Focus on top 3-5 picks for deep dive  
✅ Combine with your own technical analysis  
✅ Track your picks to refine scoring weights  
✅ Check news on high catalyst-score stocks  

---

Need help? Check README.md for full documentation!
