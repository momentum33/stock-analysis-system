# Options Data Integration Guide

This guide will help you integrate your chosen options data provider into the stock analysis system.

## 🎯 Overview

The system is designed with placeholders for options data. Once you choose a provider, you'll need to:
1. Install the provider's SDK/library
2. Update the `FinancialDataService` class methods
3. Format the data for Claude analysis
4. Test the integration

## 📊 Recommended Providers Comparison

| Provider | Best For | Pricing | Data Coverage | Ease of Use |
|----------|----------|---------|---------------|-------------|
| **Polygon.io** | General use | $29+/mo | Excellent | ⭐⭐⭐⭐⭐ |
| **TradierAPI** | Real-time | $10+/mo | Very Good | ⭐⭐⭐⭐ |
| **ThetaData** | Historical | $30/mo | Excellent | ⭐⭐⭐⭐ |
| **Market Data** | Simplicity | $19+/mo | Good | ⭐⭐⭐⭐⭐ |
| **CBOE** | Enterprise | Custom | Comprehensive | ⭐⭐⭐ |

## 🔧 Integration Steps

### Step 1: Choose and Install Provider

#### For Polygon.io:
```bash
pip install polygon-api-client
```

#### For TradierAPI:
```bash
pip install requests  # Use requests library
```

#### For ThetaData:
```bash
pip install thetadata
```

#### For Market Data API:
```bash
pip install requests  # Use requests library
```

### Step 2: Update FinancialDataService

Open `financial_data_service.py` and update the options methods:

#### Example: Polygon.io Integration

```python
from polygon import RESTClient

class FinancialDataService:
    def __init__(self, fmp_api_key: str, options_api_key: Optional[str] = None):
        self.fmp_api_key = fmp_api_key
        self.options_api_key = options_api_key
        self.fmp_base_url = "https://financialmodelingprep.com/api/v3"
        
        # Initialize Polygon client
        if options_api_key:
            self.polygon_client = RESTClient(api_key=options_api_key)
    
    def get_options_chain(self, symbol: str, expiration: str = None) -> Optional[Dict]:
        """Get options chain from Polygon"""
        if not self.options_api_key:
            return None
        
        try:
            # Get all available contracts
            contracts = self.polygon_client.list_options_contracts(
                underlying_ticker=symbol,
                limit=1000
            )
            
            calls = []
            puts = []
            
            for contract in contracts:
                option_data = {
                    "strike": contract.strike_price,
                    "expiration": contract.expiration_date,
                    "bid": getattr(contract, 'bid', None),
                    "ask": getattr(contract, 'ask', None),
                    "volume": getattr(contract, 'volume', None),
                    "open_interest": getattr(contract, 'open_interest', None),
                    "implied_volatility": getattr(contract, 'implied_volatility', None)
                }
                
                if contract.contract_type == "call":
                    calls.append(option_data)
                else:
                    puts.append(option_data)
            
            return {
                "symbol": symbol,
                "calls": calls,
                "puts": puts,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching options chain: {e}")
            return None
    
    def get_implied_volatility(self, symbol: str) -> Optional[Dict]:
        """Get IV metrics from Polygon"""
        if not self.options_api_key:
            return None
        
        try:
            # Get recent options data to calculate IV metrics
            options_data = self.get_options_chain(symbol)
            if not options_data:
                return None
            
            # Extract IV from ATM options
            all_ivs = []
            for option in options_data['calls'] + options_data['puts']:
                if option.get('implied_volatility'):
                    all_ivs.append(option['implied_volatility'])
            
            if not all_ivs:
                return None
            
            current_iv = sum(all_ivs) / len(all_ivs)
            
            return {
                "symbol": symbol,
                "current_iv": current_iv,
                "iv_rank": None,  # Calculate if you have historical IV data
                "iv_percentile": None,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching IV: {e}")
            return None
```

#### Example: TradierAPI Integration

```python
def get_options_chain(self, symbol: str) -> Optional[Dict]:
    """Get options chain from Tradier"""
    if not self.options_api_key:
        return None
    
    headers = {
        'Authorization': f'Bearer {self.options_api_key}',
        'Accept': 'application/json'
    }
    
    # Get expirations
    exp_url = 'https://api.tradier.com/v1/markets/options/expirations'
    exp_response = requests.get(exp_url, params={'symbol': symbol}, headers=headers)
    expirations = exp_response.json().get('expirations', {}).get('date', [])
    
    if not expirations:
        return None
    
    # Get chain for nearest expiration
    chain_url = 'https://api.tradier.com/v1/markets/options/chains'
    params = {
        'symbol': symbol,
        'expiration': expirations[0],
        'greeks': 'true'
    }
    
    response = requests.get(chain_url, params=params, headers=headers)
    data = response.json()
    
    # Format the response
    calls = []
    puts = []
    
    for option in data.get('options', {}).get('option', []):
        option_data = {
            "strike": option['strike'],
            "expiration": option['expiration_date'],
            "bid": option['bid'],
            "ask": option['ask'],
            "volume": option['volume'],
            "open_interest": option['open_interest'],
            "implied_volatility": option.get('greeks', {}).get('mid_iv'),
            "delta": option.get('greeks', {}).get('delta'),
            "gamma": option.get('greeks', {}).get('gamma'),
            "theta": option.get('greeks', {}).get('theta'),
            "vega": option.get('greeks', {}).get('vega')
        }
        
        if option['option_type'] == 'call':
            calls.append(option_data)
        else:
            puts.append(option_data)
    
    return {
        "symbol": symbol,
        "calls": calls,
        "puts": puts,
        "expirations": expirations,
        "timestamp": datetime.now().isoformat()
    }
```

### Step 3: Update Claude Analysis

Update `claude_financial_analyzer.py` to include options analysis:

```python
def _format_data_for_claude(self, data: Dict[str, Any]) -> str:
    """Enhanced with options data formatting"""
    parts = []
    
    # ... existing code ...
    
    # OPTIONS DATA (if available)
    if data['options']['chain']:
        parts.append("\n\n📊 OPTIONS DATA")
        parts.append("-" * 80)
        
        chain = data['options']['chain']
        
        # Analyze options activity
        total_call_volume = sum(opt.get('volume', 0) for opt in chain['calls'])
        total_put_volume = sum(opt.get('volume', 0) for opt in chain['puts'])
        put_call_ratio = total_put_volume / total_call_volume if total_call_volume > 0 else 0
        
        parts.append(f"Put/Call Volume Ratio: {put_call_ratio:.2f}")
        parts.append(f"Total Call Volume: {total_call_volume:,}")
        parts.append(f"Total Put Volume: {total_put_volume:,}")
        
        # ATM options
        # Find near-the-money options for current price analysis
        # ... add your ATM analysis logic ...
    
    if data['options']['implied_volatility']:
        iv_data = data['options']['implied_volatility']
        parts.append(f"\nImplied Volatility: {iv_data.get('current_iv', 'N/A')}")
        if iv_data.get('iv_rank'):
            parts.append(f"IV Rank: {iv_data['iv_rank']}")
    
    return "\n".join(parts)
```

### Step 4: Add Options-Specific Analysis

Add new analysis method in `claude_financial_analyzer.py`:

```python
def get_options_strategy_recommendation(self, symbol: str, bias: str = "neutral") -> str:
    """
    Get Claude's options strategy recommendation
    
    Args:
        symbol: Stock ticker
        bias: "bullish", "bearish", or "neutral"
    """
    data = self.financial_service.get_comprehensive_analysis_data(symbol)
    
    if not data['options']['chain']:
        return "Options data not available"
    
    formatted_data = self._format_data_for_claude(data)
    
    prompt = f"""{formatted_data}

Given the options data and your bias of '{bias}', recommend specific options strategies for {symbol}:

1. **Optimal Strategy**: What options strategy fits best? (e.g., covered call, bull put spread, iron condor)
2. **Strike Selection**: Which strikes should be targeted?
3. **Expiration**: What expiration timeframe is optimal?
4. **Risk/Reward**: Expected profit/loss and probability of success
5. **Entry/Exit**: When to enter and exit criteria
6. **Position Sizing**: Recommended contract quantity relative to portfolio size

Be specific with strikes and expirations. Consider current IV levels."""
    
    message = self.client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text
```

## 📝 Data Structures

### Standard Options Contract Format

Use this format for consistency:

```python
{
    "strike": 150.0,
    "expiration": "2024-12-20",
    "contract_type": "call",  # or "put"
    "bid": 5.20,
    "ask": 5.40,
    "last": 5.30,
    "volume": 1250,
    "open_interest": 5430,
    "implied_volatility": 0.28,  # 28%
    "delta": 0.65,
    "gamma": 0.03,
    "theta": -0.05,
    "vega": 0.15,
    "rho": 0.08
}
```

## 🧪 Testing Your Integration

Create `test_options.py`:

```python
from financial_data_service import FinancialDataService
import os
from dotenv import load_dotenv

load_dotenv()

service = FinancialDataService(
    fmp_api_key=os.getenv('FMP_API_KEY'),
    options_api_key=os.getenv('OPTIONS_API_KEY')
)

# Test options chain
print("Testing options chain...")
chain = service.get_options_chain("AAPL")
if chain:
    print(f"✓ Got {len(chain['calls'])} calls and {len(chain['puts'])} puts")
else:
    print("✗ Failed to get options chain")

# Test IV
print("\nTesting implied volatility...")
iv = service.get_implied_volatility("AAPL")
if iv:
    print(f"✓ Current IV: {iv['current_iv']}")
else:
    print("✗ Failed to get IV data")
```

Run: `python test_options.py`

## 💡 Advanced Features to Add

Once basic integration works, consider adding:

### 1. Options Flow Detection
```python
def detect_unusual_options_activity(self, symbol: str) -> List[Dict]:
    """Detect large or unusual options trades"""
    # Compare current volume to average
    # Flag trades with volume > 2x average
    # Identify sweep orders
```

### 2. Options Greeks Analysis
```python
def analyze_greeks(self, symbol: str) -> Dict:
    """Analyze portfolio Greeks and risk"""
    # Calculate portfolio delta, gamma, theta, vega
    # Risk metrics and hedge recommendations
```

### 3. IV Surface Visualization
```python
def get_iv_surface(self, symbol: str) -> Dict:
    """Get IV across strikes and expirations"""
    # Create IV surface data
    # Identify skew and term structure
```

### 4. Options Probability Calculator
```python
def calculate_option_probability(self, strike: float, current_price: float, 
                                 days: int, iv: float) -> float:
    """Calculate probability of option expiring ITM"""
    # Use Black-Scholes or similar model
```

## 🔍 Troubleshooting

### Issue: "No options data returned"
- Check API key is valid
- Verify symbol has options available (not all stocks do)
- Check rate limits on your plan
- Look at API response for error messages

### Issue: "IV data missing"
- Not all providers include Greeks/IV
- May need to calculate IV from option prices
- Check if stock has sufficient options volume

### Issue: "Rate limit exceeded"
- Implement caching for options data
- Add delays between requests
- Upgrade to higher tier plan

## 📚 Resources

### Polygon.io
- Docs: https://polygon.io/docs/options/getting-started
- Python SDK: https://github.com/polygon-io/client-python

### TradierAPI
- Docs: https://documentation.tradier.com/brokerage-api
- Options Endpoints: https://documentation.tradier.com/brokerage-api/markets/get-options-chains

### ThetaData
- Docs: https://http-docs.thetadata.us/docs/theta-data-rest-api-v2
- Python SDK: https://github.com/ThetaData-API/ThetaData-API-Python

### Market Data API
- Docs: https://www.marketdata.app/docs/api/options
- Getting Started: https://www.marketdata.app/docs/getting-started

## ✅ Completion Checklist

- [ ] Chose options data provider
- [ ] Installed provider SDK/library
- [ ] Updated `get_options_chain()` method
- [ ] Updated `get_implied_volatility()` method
- [ ] Updated `get_options_flow()` method (if applicable)
- [ ] Added options data to Claude analysis formatting
- [ ] Tested with real API calls
- [ ] Added error handling
- [ ] Implemented rate limiting
- [ ] Added caching (optional)
- [ ] Created options-specific analysis methods
- [ ] Updated documentation

Once complete, uncomment the options examples in `example_usage.py` to test full functionality!
