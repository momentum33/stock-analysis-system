# SYSTEM ARCHITECTURE & WORKFLOW

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     STOCK ANALYSIS SYSTEM                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   INPUT      │
│  TICKERS     │──────┐
│  (TXT FILE)  │      │
└──────────────┘      │
                      │
                      ▼
            ┌─────────────────┐
            │   MAIN.PY       │
            │  (Orchestrator) │
            └─────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ FMP_CLIENT   │ │  ANALYZER    │ │  REPORTER    │
│  API Calls   │ │  Scoring     │ │  Outputs     │
│  Rate Limit  │ │  Logic       │ │  Generation  │
└──────────────┘ └──────────────┘ └──────────────┘
        │             │             │
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
            ┌─────────────────┐
            │  OUTPUT FILES   │
            ├─────────────────┤
            │ • CSV           │
            │ • HTML          │
            │ • TXT Report    │
            └─────────────────┘
```

## 🔄 Data Flow

```
[User's Screener]
      │
      │ Exports 50-150 tickers
      ▼
[input_tickers.txt]
      │
      │ Read by main.py
      ▼
[FMP API Client]
      │
      │ Fetches for each ticker:
      │ • Real-time quote
      │ • 90 days historical prices
      │ • Company profile
      │ • Recent news
      │
      ▼
[Stock Analyzer]
      │
      │ Calculates 7 scores:
      │ 1. Momentum (25%)
      │ 2. Volume (15%)
      │ 3. Technical (20%)
      │ 4. Volatility (10%)
      │ 5. Relative Strength (15%)
      │ 6. Catalyst (10%)
      │ 7. Liquidity (5%)
      │
      │ Composite Score = Weighted Avg
      │
      ▼
[Filtering & Ranking]
      │
      │ • Remove low volume stocks
      │ • Remove extreme prices
      │ • Sort by composite score
      │ • Select top 10
      │
      ▼
[Report Generator]
      │
      ├──> CSV (spreadsheet)
      ├──> HTML (dashboard)
      └──> TXT (report)
      │
      ▼
[User Analysis]
```

## 📊 Scoring Pipeline

```
For each stock:

┌─────────────────────────────────────────────────────────────┐
│ 1. DATA COLLECTION (via FMP API)                            │
└─────────────────────────────────────────────────────────────┘
  • Current price & volume
  • 90 days historical data
  • Company info & sector
  • Recent news (5 articles)
  
           ▼

┌─────────────────────────────────────────────────────────────┐
│ 2. QUALITY FILTERS                                           │
└─────────────────────────────────────────────────────────────┘
  ✓ Has 50+ days of data?
  ✓ Volume > 100,000/day?
  ✓ Price between $2-$10,000?
  
  ✗ FAIL → Skip this stock
  ✓ PASS → Continue to scoring
  
           ▼

┌─────────────────────────────────────────────────────────────┐
│ 3. CALCULATE INDIVIDUAL SCORES (0-10 each)                  │
└─────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────┐
  │ MOMENTUM SCORE (25% weight)                   │
  ├───────────────────────────────────────────────┤
  │ • 10-day return                               │
  │ • 20-day return                               │
  │ • Acceleration                                │
  └───────────────────────────────────────────────┘
  
  ┌───────────────────────────────────────────────┐
  │ VOLUME SCORE (15% weight)                     │
  ├───────────────────────────────────────────────┤
  │ • Current vs average volume                   │
  │ • Volume trend (recent vs past)               │
  └───────────────────────────────────────────────┘
  
  ┌───────────────────────────────────────────────┐
  │ TECHNICAL SCORE (20% weight)                  │
  ├───────────────────────────────────────────────┤
  │ • RSI (14-day)                                │
  │ • Price vs SMA (10, 20, 50)                   │
  │ • Breakout detection                          │
  └───────────────────────────────────────────────┘
  
  ┌───────────────────────────────────────────────┐
  │ VOLATILITY SCORE (10% weight)                 │
  ├───────────────────────────────────────────────┤
  │ • Standard deviation of returns               │
  │ • Sweet spot: 2-4% daily                      │
  └───────────────────────────────────────────────┘
  
  ┌───────────────────────────────────────────────┐
  │ RELATIVE STRENGTH SCORE (15% weight)          │
  ├───────────────────────────────────────────────┤
  │ • Stock return vs SPY return                  │
  │ • 20-day comparison                           │
  └───────────────────────────────────────────────┘
  
  ┌───────────────────────────────────────────────┐
  │ CATALYST SCORE (10% weight)                   │
  ├───────────────────────────────────────────────┤
  │ • News sentiment (keyword analysis)           │
  │ • News volume                                 │
  │ • Price confirmation                          │
  └───────────────────────────────────────────────┘
  
  ┌───────────────────────────────────────────────┐
  │ LIQUIDITY SCORE (5% weight)                   │
  ├───────────────────────────────────────────────┤
  │ • Average volume                              │
  │ • Bid-ask spread                              │
  └───────────────────────────────────────────────┘
  
           ▼

┌─────────────────────────────────────────────────────────────┐
│ 4. CALCULATE COMPOSITE SCORE                                 │
└─────────────────────────────────────────────────────────────┘

  Composite = (Momentum × 0.25) + 
              (Volume × 0.15) + 
              (Technical × 0.20) + 
              (Volatility × 0.10) + 
              (Rel.Strength × 0.15) + 
              (Catalyst × 0.10) + 
              (Liquidity × 0.05)
  
  Result: Score from 0-10
  
           ▼

┌─────────────────────────────────────────────────────────────┐
│ 5. RANK ALL STOCKS                                           │
└─────────────────────────────────────────────────────────────┘
  Sort by composite score (highest first)
  Select top 10
```

## 🎯 Execution Workflow

```
DAY 1: Setup (One-time, 5 minutes)
══════════════════════════════════
1. pip install requests numpy
2. Get FMP API key
3. Edit config.py with API key
4. python setup.py (verify)

DAILY: Analysis Workflow (2-5 minutes)
══════════════════════════════════════
1. Export screener → input_tickers.txt
2. python main.py input_tickers.txt
3. Wait 2-5 minutes (automatic)
4. Open output/dashboard_*.html
5. Review top 10 picks
6. Deep dive on top 3-5
7. Make trading decisions

WEEKLY: Optimization (15 minutes)
═════════════════════════════════
1. Review week's results
2. Track which scores were high on winners
3. Adjust weights in config.py
4. Test new weights on historical data

MONTHLY: Strategy Review (30 minutes)
═════════════════════════════════════
1. Calculate win rate & profit factor
2. Identify which sectors performed best
3. Refine filtering criteria
4. Update scoring logic if needed
```

## 🔌 API Integration Flow

```
┌────────────────────────────────────────┐
│  FMP API Rate Limiting Strategy        │
└────────────────────────────────────────┘

For each ticker:
  
  Request 1: GET /quote/{ticker}
    └─> Real-time price, volume, change
    
  Request 2: GET /historical-price-full/{ticker}
    └─> 90 days of OHLCV data
    
  Request 3: GET /profile/{ticker}
    └─> Company info, sector, market cap
    
  Request 4: GET /stock_news?tickers={ticker}
    └─> Recent news articles
    
  Request 5: GET /key-metrics/{ticker}
    └─> Financial metrics (optional)

Total: ~5 requests per ticker
Rate Limit: 300 requests/minute
           = 60 tickers/minute
           = ~3-5 seconds per ticker

Free Tier: 250 requests/day
          = ~50 tickers/day
          
Wait between requests: 0.21 seconds
Auto-reset: Every 60 seconds
```

## 📈 Score Calculation Examples

### Example 1: High Momentum Stock
```
TICKER: XYZ
Price: $50.00
10-day return: +15%
20-day return: +25%
Volume: 2.5M (2x average)
RSI: 65

SCORES:
• Momentum:    9.5/10  (strong uptrend + acceleration)
• Volume:      8.0/10  (high volume spike)
• Technical:   7.0/10  (RSI neutral, price > MAs)
• Volatility:  6.0/10  (bit high at 5% daily)
• Rel.Str:     8.5/10  (beating market)
• Catalyst:    7.0/10  (positive news)
• Liquidity:   9.0/10  (excellent volume)

COMPOSITE: 8.1/10 → Strong Buy Signal
```

### Example 2: Consolidating Stock
```
TICKER: ABC
Price: $25.00
10-day return: +2%
20-day return: 0%
Volume: 500K (avg)
RSI: 45

SCORES:
• Momentum:    4.0/10  (weak momentum)
• Volume:      5.0/10  (average)
• Technical:   6.5/10  (neutral RSI, near support)
• Volatility:  8.0/10  (perfect range)
• Rel.Str:     5.0/10  (matching market)
• Catalyst:    3.0/10  (no recent news)
• Liquidity:   7.0/10  (adequate)

COMPOSITE: 5.2/10 → Watch/Avoid
```

## 🛠️ Component Details

### config.py
```
• API credentials
• Analysis parameters
• Scoring weights
• Filter thresholds
• Output settings
→ Single source of truth
```

### fmp_client.py
```
• HTTP request handling
• Rate limiting logic
• Error handling & retries
• Data parsing
• Batch operations
→ Clean API abstraction
```

### analyzer.py
```
• Score calculation methods
• Technical indicator math
• News sentiment parsing
• Filter application
• Metric aggregation
→ Pure business logic
```

### report_generator.py
```
• CSV formatting
• HTML generation
• Text report writing
• Data visualization
• File management
→ Multiple output formats
```

### main.py
```
• Workflow orchestration
• Progress tracking
• Error handling
• User interface
• File I/O
→ User-facing script
```

## 🔍 Code Quality Features

✅ **Modular Design**
   - Each component has single responsibility
   - Easy to test and maintain

✅ **Error Handling**
   - API failures handled gracefully
   - Invalid tickers skipped
   - Informative error messages

✅ **Rate Limiting**
   - Automatic throttling
   - Respects API limits
   - No manual intervention needed

✅ **Configurability**
   - All parameters in one place
   - Easy to customize
   - No code changes needed

✅ **Documentation**
   - Inline comments
   - README & guides
   - Example files

✅ **Scalability**
   - Handles 50-150+ tickers
   - Parallel processing ready
   - Database integration ready

## 🚀 Future Enhancement Possibilities

1. **Database Integration**
   - Store historical analyses
   - Track performance over time
   - Identify patterns

2. **Machine Learning**
   - Train on winning picks
   - Auto-adjust weights
   - Predict probabilities

3. **Real-time Alerts**
   - Email/SMS notifications
   - Trigger on score thresholds
   - Intraday monitoring

4. **Advanced Analytics**
   - Sector rotation analysis
   - Correlation matrices
   - Portfolio optimization

5. **Backtesting**
   - Historical simulation
   - Performance metrics
   - Strategy validation

---

**This is a professional, extensible system ready for serious trading!**
