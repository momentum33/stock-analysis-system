# Stock Analysis System for Short-Term Trading

A comprehensive Python-based system that analyzes stocks from your daily screener and identifies the top 10 candidates for short-term trading (< 2 months). The system uses the Financial Modeling Prep (FMP) API to fetch real-time data and calculates multiple technical and fundamental metrics to rank stocks.

## Features

- **Multi-factor Scoring System**: Analyzes 7 key dimensions
  - Momentum (price trends and acceleration)
  - Volume (activity and spikes)
  - Technical indicators (RSI, moving averages, breakouts)
  - Volatility (sweet spot for short-term trading)
  - Relative strength (vs market)
  - Catalysts (news and events)
  - Liquidity (volume and spreads)

- **Multiple Output Formats**:
  - CSV file with detailed metrics
  - Interactive HTML dashboard
  - Text report with analysis

- **Smart Rate Limiting**: Respects FMP API limits (300 requests/minute)
- **Customizable**: Easy-to-adjust parameters in config.py

## Prerequisites

1. **Python 3.7+** installed
2. **FMP API Key** - Get free tier at https://financialmodelingprep.com/developer/docs/
   - Free tier: 250 requests/day, 5 requests/second
   - Paid tiers: Higher limits

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install requests numpy
   ```

3. **Configure your API key**:
   Edit `config.py` and replace `YOUR_FMP_API_KEY_HERE` with your actual FMP API key:
   ```python
   FMP_API_KEY = "your_actual_api_key_here"
   ```

## Usage

### Basic Usage

1. **Prepare your input file** with ticker symbols (one per line):
   ```
   AAPL
   TSLA
   NVDA
   MSFT
   ```

2. **Run the analysis**:
   ```bash
   python main.py input_tickers.txt
   ```

3. **View results** in the `output/` directory:
   - `stock_analysis_YYYYMMDD_HHMMSS.csv` - Detailed spreadsheet
   - `dashboard_YYYYMMDD_HHMMSS.html` - Interactive dashboard (open in browser)
   - `report_YYYYMMDD_HHMMSS.txt` - Text report

### Daily Workflow

1. Export tickers from your stock screener to a text file
2. Run: `python main.py your_screener_results.txt`
3. Open the HTML dashboard to review the top 10 picks
4. Use the CSV for further analysis in Excel/Google Sheets

## Configuration

Edit `config.py` to customize the analysis:

### Key Parameters

```python
# API Configuration
FMP_API_KEY = "your_key_here"
API_RATE_LIMIT = 300  # requests per minute

# Analysis Parameters
ANALYSIS_CONFIG = {
    'short_period': 10,      # days for short-term momentum
    'medium_period': 20,     # days for medium-term trend
    'long_period': 50,       # days for context
    
    # Scoring weights (must sum to 1.0)
    'weights': {
        'momentum_score': 0.25,
        'volume_score': 0.15,
        'technical_score': 0.20,
        'volatility_score': 0.10,
        'relative_strength_score': 0.15,
        'catalyst_score': 0.10,
        'liquidity_score': 0.05,
    },
    
    # Filters
    'min_avg_volume': 100000,    # Minimum average daily volume
    'min_price': 2.0,            # Minimum stock price
    'max_price': 10000,          # Maximum stock price
}

# Output Configuration
TOP_N_STOCKS = 10
```

### Customizing Weights

Adjust the scoring weights based on your trading style:
- **Momentum trader**: Increase `momentum_score` and `volume_score`
- **Technical trader**: Increase `technical_score` and `volatility_score`
- **News trader**: Increase `catalyst_score`

## Understanding the Scores

### Individual Scores (0-10 scale)

1. **Momentum Score**: Measures recent price trends
   - Short-term gains (10 days)
   - Medium-term gains (20 days)
   - Acceleration (momentum increasing)

2. **Volume Score**: Measures trading activity
   - Volume spikes vs average
   - Increasing volume trend
   - Institutional interest

3. **Technical Score**: Technical indicators
   - RSI (oversold/neutral zones best)
   - Price vs moving averages
   - Breakouts from resistance

4. **Volatility Score**: Movement potential
   - Sweet spot: 2-4% daily volatility
   - Too low = not enough movement
   - Too high = too risky

5. **Relative Strength Score**: Performance vs market (SPY)
   - Outperforming market = higher score
   - Shows sector/stock strength

6. **Catalyst Score**: News and events
   - Recent positive news
   - News volume
   - Price confirmation

7. **Liquidity Score**: Ease of trading
   - Average volume
   - Bid-ask spread
   - Slippage risk

### Composite Score

The final score is a weighted average of all individual scores:
```
Composite Score = Σ (Individual Score × Weight)
```

Higher composite scores indicate better short-term trading candidates.

## Output Formats

### CSV File
Detailed spreadsheet with all metrics:
- Rank, symbol, company name
- All individual scores
- Technical metrics (RSI, SMAs, etc.)
- Volume data
- Price changes (day, week, month)

### HTML Dashboard
Beautiful, interactive dashboard featuring:
- Visual score bars
- Key metrics at a glance
- Recent news headlines
- Color-coded performance indicators
- Responsive design (mobile-friendly)

### Text Report
Comprehensive text report with:
- Executive summary
- Detailed breakdown for each stock
- Score explanations
- Recent news

## Tips for Best Results

1. **Input Quality**: Use a quality stock screener first
   - Pre-filter for basic criteria (price range, volume, sector)
   - Feed 50-150 tickers for best selection

2. **Daily Routine**:
   - Run analysis before market open
   - Review HTML dashboard quickly
   - Deep dive on top 3-5 picks
   - Check news and catalysts

3. **Combine with Your Analysis**:
   - Use scores as a starting point
   - Verify with your own chart analysis
   - Consider sector rotation
   - Check overall market conditions

4. **API Usage**:
   - Free tier: ~50 stocks per run (5 requests each)
   - Paid tier: 250-300 stocks per run
   - Run once daily to stay within limits

5. **Adjust Weights**:
   - Track your winning trades
   - Notice which scores were high on winners
   - Adjust weights accordingly

## Troubleshooting

### "API key error"
- Make sure you've set your FMP API key in `config.py`
- Verify your API key is active at financialmodelingprep.com

### "Rate limit error"
- Free tier has 250 requests/day limit
- Reduce number of input tickers
- Wait 24 hours for limit reset
- Consider upgrading to paid tier

### "No stocks passed filters"
- Check your input tickers are valid
- Adjust filter thresholds in `config.py`:
  - Lower `min_avg_volume`
  - Adjust `min_price` and `max_price`

### "Insufficient data for [TICKER]"
- Some stocks may not have enough historical data
- Penny stocks often have data issues
- Newly IPO'd stocks won't have 50+ days of data

## File Structure

```
stock-analysis-system/
├── main.py                 # Main execution script
├── config.py              # Configuration parameters
├── fmp_client.py          # FMP API client
├── analyzer.py            # Stock analysis engine
├── report_generator.py    # Report generation
├── requirements.txt       # Python dependencies
├── input_tickers.txt      # Sample input file
├── README.md             # This file
└── output/               # Generated reports (created automatically)
    ├── stock_analysis_*.csv
    ├── dashboard_*.html
    └── report_*.txt
```

## Advanced Usage

### Batch Processing
Create multiple input files for different strategies:
```bash
python main.py momentum_stocks.txt
python main.py tech_stocks.txt
python main.py small_caps.txt
```

### Automation
Add to cron (Linux/Mac) or Task Scheduler (Windows):
```bash
# Run every weekday at 8:00 AM
0 8 * * 1-5 cd /path/to/stock-analysis && python main.py input_tickers.txt
```

### Integration with Other Tools
- Export CSV to your trading journal
- Import to Excel for deeper analysis
- Connect to trading platform APIs for auto-execution

## Performance Notes

- Analysis speed: ~2-5 seconds per stock (with rate limiting)
- 50 stocks: ~2-4 minutes
- 100 stocks: ~5-8 minutes
- 150 stocks: ~8-12 minutes

## Disclaimer

**This tool is for educational and informational purposes only.**

- Not financial advice
- Past performance doesn't guarantee future results
- Always do your own research
- Never invest more than you can afford to lose
- Consider consulting a financial advisor

Trading stocks involves risk, including potential loss of principal.

## Support

For issues or questions:
1. Check this README first
2. Review the configuration in `config.py`
3. Verify your FMP API key is valid
4. Check FMP API documentation: https://financialmodelingprep.com/developer/docs/

## License

Free to use and modify for personal trading purposes.

## Version History

- **v1.0** (2024) - Initial release
  - Multi-factor scoring system
  - CSV, HTML, and text reports
  - FMP API integration
  - Rate limiting and error handling

---

Happy Trading! 📈🚀
