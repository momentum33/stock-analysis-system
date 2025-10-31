"""
FMP + Polygon API Client v4.0
Integrated client for financial data (FMP) and options data (Polygon)
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import config

class DataClient:
    """
    Unified client for FMP (fundamentals, prices, news) and Polygon (options)
    """
    
    def __init__(self):
        # FMP Configuration
        self.fmp_api_key = config.FMP_API_KEY
        self.fmp_base_url = "https://financialmodelingprep.com/api/v3"
        self.fmp_rate_limit = config.FMP_RATE_LIMIT
        self.fmp_last_request = 0
        
        # Polygon Configuration
        self.polygon_api_key = config.POLYGON_API_KEY
        self.polygon_base_url = "https://api.polygon.io"
        self.polygon_rate_limit = config.POLYGON_RATE_LIMIT
        self.polygon_last_request = 0
        
        # Options configuration
        self.options_enabled = config.ANALYSIS_CONFIG['options']['enabled']
    
    # ========================================================================
    # RATE LIMITING
    # ========================================================================
    
    def _fmp_rate_limit(self):
        """Enforce FMP rate limiting"""
        elapsed = time.time() - self.fmp_last_request
        if elapsed < self.fmp_rate_limit['delay_between_requests']:
            time.sleep(self.fmp_rate_limit['delay_between_requests'] - elapsed)
        self.fmp_last_request = time.time()
    
    def _polygon_rate_limit(self):
        """Enforce Polygon rate limiting"""
        elapsed = time.time() - self.polygon_last_request
        if elapsed < self.polygon_rate_limit['delay_between_requests']:
            time.sleep(self.polygon_rate_limit['delay_between_requests'] - elapsed)
        self.polygon_last_request = time.time()
    
    # ========================================================================
    # REQUEST HELPERS
    # ========================================================================
    
    def _make_fmp_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make FMP API request with rate limiting and error handling"""
        self._fmp_rate_limit()
        
        if params is None:
            params = {}
        params['apikey'] = self.fmp_api_key
        
        url = f"{self.fmp_base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  FMP error ({endpoint}): {e}")
            return None
    
    def _make_polygon_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make Polygon API request with rate limiting and error handling"""
        if not self.polygon_api_key or self.polygon_api_key == "YOUR_POLYGON_API_KEY_HERE":
            return None
        
        self._polygon_rate_limit()
        
        if params is None:
            params = {}
        params['apiKey'] = self.polygon_api_key
        
        url = f"{self.polygon_base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"  Polygon error ({endpoint}): {e}")
            return None
    
    # ========================================================================
    # FMP API METHODS - Stock Data
    # ========================================================================
    
    def get_quote(self, symbol: str) -> Optional[Dict]:
        """Get real-time quote from FMP"""
        data = self._make_fmp_request(f"quote/{symbol}")
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_historical_prices(self, symbol: str, days: int = 250) -> Optional[List[Dict]]:
        """Get historical price data from FMP"""
        data = self._make_fmp_request(f"historical-price-full/{symbol}", 
                                      params={'timeseries': days})
        if data and 'historical' in data:
            return data['historical']
        return None
    
    def get_company_profile(self, symbol: str) -> Optional[Dict]:
        """Get company profile from FMP"""
        data = self._make_fmp_request(f"profile/{symbol}")
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_news(self, symbol: str, limit: int = 5) -> Optional[List[Dict]]:
        """Get recent news from FMP"""
        data = self._make_fmp_request("news/stock", 
                              params={'symbols': symbol, 'limit': limit})
        return data if data and isinstance(data, list) else []
    
    # ========================================================================
    # FMP API METHODS - Fundamental Data
    # ========================================================================
    
    def get_financial_ratios(self, symbol: str) -> Optional[Dict]:
        """Get financial ratios (ROIC, ROE, etc.) from FMP"""
        data = self._make_fmp_request(f"ratios/{symbol}", params={'limit': 1})
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_key_metrics(self, symbol: str) -> Optional[Dict]:
        """Get key metrics (market cap, P/E, etc.) from FMP"""
        data = self._make_fmp_request(f"key-metrics/{symbol}", params={'limit': 1})
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_income_statement(self, symbol: str) -> Optional[Dict]:
        """Get income statement from FMP"""
        data = self._make_fmp_request(f"income-statement/{symbol}", params={'limit': 1})
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_balance_sheet(self, symbol: str) -> Optional[Dict]:
        """Get balance sheet from FMP"""
        data = self._make_fmp_request(f"balance-sheet-statement/{symbol}", params={'limit': 1})
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_cash_flow(self, symbol: str) -> Optional[Dict]:
        """Get cash flow statement from FMP"""
        data = self._make_fmp_request(f"cash-flow-statement/{symbol}", params={'limit': 1})
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    def get_financial_growth(self, symbol: str) -> Optional[Dict]:
        """Get growth metrics from FMP"""
        data = self._make_fmp_request(f"financial-growth/{symbol}", params={'limit': 1})
        return data[0] if data and isinstance(data, list) and len(data) > 0 else None
    
    # ========================================================================
    # FMP API METHODS - Short Interest (if available in your plan)
    # ========================================================================
    
    def get_short_interest_fmp(self, symbol: str) -> Optional[Dict]:
        """
        Get short interest from FMP (if available in your plan)
        Note: This endpoint may not be in free tier
        """
        # FMP doesn't have a dedicated short interest endpoint in free tier
        # This is a placeholder - you may need to use a different source
        return None
    
    # ========================================================================
    # POLYGON API METHODS - Options Data
    # ========================================================================
    
    def get_options_chain(self, symbol: str, expiry_date: str = None) -> Optional[Dict]:
        """
        Get options chain from Polygon
        
        Args:
            symbol: Stock ticker
            expiry_date: Expiration date in YYYY-MM-DD format (optional)
        """
        if not self.options_enabled:
            return None
        
        # If no expiry specified, get next monthly expiry
        if not expiry_date:
            expiry_date = self._get_next_monthly_expiry()
        
        endpoint = f"v3/reference/options/contracts"
        params = {
            'underlying_ticker': symbol,
            'expiration_date': expiry_date,
            'limit': 250
        }
        
        return self._make_polygon_request(endpoint, params)
    
    def get_options_snapshot(self, ticker: str, option_contract: str) -> Optional[Dict]:
        """
        Get options snapshot (current greeks, IV, etc.)
        
        Args:
            ticker: Underlying stock ticker
            option_contract: Full options contract identifier (e.g., O:AAPL230616C00150000)
        """
        if not self.options_enabled:
            return None
        
        endpoint = f"v3/snapshot/options/{ticker}/{option_contract}"
        return self._make_polygon_request(endpoint)
    
    def get_options_aggregate(self, symbol: str, days: int = 30) -> Optional[Dict]:
        """
        Get aggregated options data (P/C ratio, volume, open interest)
        
        Args:
            symbol: Stock ticker
            days: Days of history to aggregate
        """
        if not self.options_enabled:
            return None
        
        # Get recent options trades to calculate P/C ratio
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        endpoint = f"v2/aggs/ticker/O:{symbol}/range/1/day/{from_date}/{to_date}"
        return self._make_polygon_request(endpoint)
    
    def get_put_call_ratio(self, symbol: str) -> Optional[float]:
        """
        Calculate Put/Call ratio from options snapshot
        
        Based on TradeMamba's approach: Use snapshot endpoint with TODAY's volume
        Source: https://medium.com/@trademamba/put-call-ratio-of-tsla-vs-nvda-in-python-739668ae3460
        
        P/C Ratio = Total Put Volume / Total Call Volume
        
        IMPORTANT: Must use limit=100 to get both puts AND calls
        (Default limit=10 often returns only one type)
        
        Interpretation:
        - < 0.7: Bullish (heavy call buying)
        - 0.7-1.0: Neutral to bullish
        - 1.0-1.5: Neutral to bearish
        - > 1.5: Bearish (heavy put buying)
        
        Returns None if data unavailable
        """
        if not self.options_enabled:
            return None
        
        try:
            # Use snapshot endpoint with limit=100 to get both puts and calls
            url = f"v3/snapshot/options/{symbol}"
            params = {'limit': 100}  # CRITICAL: Need limit to get adequate sample
            
            # Make request with params
            data = self._make_polygon_request(url, params)
            
            if not data or 'results' not in data:
                return None
            
            results = data['results']
            if not results:
                return None
            
            put_volume = 0
            call_volume = 0
            
            # Sum volumes by contract type
            for contract in results:
                # Get contract details
                details = contract.get('details', {})
                contract_type = details.get('contract_type', '').lower()
                
                # Get today's volume from 'day' object
                day = contract.get('day', {})
                volume = day.get('volume', 0)
                
                # Accumulate by type
                if contract_type == 'put' and volume:
                    put_volume += volume
                elif contract_type == 'call' and volume:
                    call_volume += volume
            
            # Calculate ratio
            if call_volume == 0:
                return None
            
            ratio = put_volume / call_volume
            return round(ratio, 4)
            
        except Exception as e:
            print(f"  Error calculating P/C ratio: {e}")
            return None
    
    def get_atm_iv(self, symbol: str, current_price: float) -> Optional[float]:
        """
        Get at-the-money implied volatility
        
        Args:
            symbol: Stock ticker
            current_price: Current stock price
        """
        if not self.options_enabled:
            return None
        
        try:
            chain = self.get_options_chain(symbol)
            if not chain or 'results' not in chain:
                return None
            
            # Find ATM call option (closest to current price)
            atm_contract = None
            min_diff = float('inf')
            
            for contract in chain['results']:
                if contract.get('contract_type') != 'call':
                    continue
                
                strike = contract.get('strike_price', 0)
                diff = abs(strike - current_price)
                
                if diff < min_diff:
                    min_diff = diff
                    atm_contract = contract
            
            if not atm_contract:
                return None
            
            # Get detailed snapshot for IV
            contract_ticker = atm_contract.get('ticker')
            snapshot = self.get_options_snapshot(symbol, contract_ticker)
            
            if snapshot and 'results' in snapshot:
                iv = snapshot['results'].get('implied_volatility')
                return iv * 100 if iv else None  # Convert to percentage
            
            return None
            
        except Exception as e:
            print(f"  Error getting ATM IV: {e}")
            return None
    
    def get_options_greeks(self, symbol: str, current_price: float) -> Optional[Dict]:
        """
        Get options greeks for ATM contracts
        
        Returns dict with: delta, gamma, theta, vega
        """
        if not self.options_enabled:
            return None
        
        try:
            chain = self.get_options_chain(symbol)
            if not chain or 'results' not in chain:
                return None
            
            # Find ATM call option
            atm_contract = None
            min_diff = float('inf')
            
            for contract in chain['results']:
                if contract.get('contract_type') != 'call':
                    continue
                
                strike = contract.get('strike_price', 0)
                diff = abs(strike - current_price)
                
                if diff < min_diff:
                    min_diff = diff
                    atm_contract = contract
            
            if not atm_contract:
                return None
            
            # Get detailed snapshot
            contract_ticker = atm_contract.get('ticker')
            snapshot = self.get_options_snapshot(symbol, contract_ticker)
            
            if snapshot and 'results' in snapshot:
                greeks = snapshot['results'].get('greeks', {})
                return {
                    'delta': greeks.get('delta'),
                    'gamma': greeks.get('gamma'),
                    'theta': greeks.get('theta'),
                    'vega': greeks.get('vega')
                }
            
            return None
            
        except Exception as e:
            print(f"  Error getting greeks: {e}")
            return None
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _get_next_monthly_expiry(self) -> str:
        """Get next monthly options expiration (3rd Friday of next month)"""
        today = datetime.now()
        
        # Start with first day of next month
        if today.month == 12:
            next_month = datetime(today.year + 1, 1, 1)
        else:
            next_month = datetime(today.year, today.month + 1, 1)
        
        # Find first Friday
        days_until_friday = (4 - next_month.weekday()) % 7
        first_friday = next_month + timedelta(days=days_until_friday)
        
        # Third Friday is 14 days after first Friday
        third_friday = first_friday + timedelta(days=14)
        
        return third_friday.strftime('%Y-%m-%d')
    
    # ========================================================================
    # COMPREHENSIVE DATA FETCH
    # ========================================================================
    
    def fetch_complete_data(self, symbol: str) -> Dict:
        """
        Fetch all available data for a stock
        
        Returns dict with:
        - quote: Current price data
        - historical: Historical prices
        - profile: Company info
        - news: Recent news
        - financials: Financial ratios and metrics
        - short_interest: Short interest data (if available)
        - growth_metrics: Growth data
        - options: Options data (P/C ratio, IV, greeks) if enabled
        """
        print(f"\n📊 Fetching data for {symbol}...")
        
        data = {
            'symbol': symbol,
            'quote': None,
            'historical': None,
            'profile': None,
            'news': None,
            'financials': {},
            'short_interest': {},
            'growth_metrics': {},
            'options': {}
        }
        
        # FMP Data
        print("  └─ Quote...", end=" ")
        data['quote'] = self.get_quote(symbol)
        print("✓" if data['quote'] else "✗")
        
        print("  └─ Historical prices...", end=" ")
        data['historical'] = self.get_historical_prices(symbol)
        print("✓" if data['historical'] else "✗")
        
        print("  └─ Company profile...", end=" ")
        data['profile'] = self.get_company_profile(symbol)
        print("✓" if data['profile'] else "✗")
        
        print("  └─ News...", end=" ")
        data['news'] = self.get_news(symbol)
        print("✓" if data['news'] else "✗")
        
        print("  └─ Financial ratios...", end=" ")
        ratios = self.get_financial_ratios(symbol)
        if ratios:
            data['financials']['roic'] = ratios.get('returnOnCapitalEmployed', 0) * 100
            data['financials']['debt_to_equity'] = ratios.get('debtEquityRatio', 0)
        print("✓" if ratios else "✗")
        
        print("  └─ Key metrics...", end=" ")
        metrics = self.get_key_metrics(symbol)
        if metrics:
            data['financials']['fcf_yield'] = metrics.get('freeCashFlowYield', 0) * 100
        print("✓" if metrics else "✗")
        
        print("  └─ Growth metrics...", end=" ")
        growth = self.get_financial_growth(symbol)
        if growth:
            data['growth_metrics']['revenue_growth_1y'] = growth.get('revenueGrowth', 0) * 100
            data['growth_metrics']['eps_growth_1y'] = growth.get('epsgrowth', 0) * 100
        print("✓" if growth else "✗")
        
        # Options Data (Polygon)
        if self.options_enabled and data['quote']:
            current_price = data['quote'].get('price', 0)
            
            print("  └─ Options P/C ratio...", end=" ")
            pc_ratio = self.get_put_call_ratio(symbol)
            if pc_ratio:
                data['options']['pc_ratio'] = pc_ratio
            print("✓" if pc_ratio else "✗")
            
            print("  └─ ATM IV...", end=" ")
            atm_iv = self.get_atm_iv(symbol, current_price)
            if atm_iv:
                data['options']['atm_iv'] = atm_iv
            print("✓" if atm_iv else "✗")
            
            print("  └─ Greeks...", end=" ")
            greeks = self.get_options_greeks(symbol, current_price)
            if greeks:
                data['options']['greeks'] = greeks
            print("✓" if greeks else "✗")
        
        return data

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("Data Client v4.0 - FMP + Polygon Integration")
    print("=" * 70)
    
    # Test initialization
    try:
        client = DataClient()
        print("✅ Client initialized successfully")
        
        if client.options_enabled:
            print("✅ Options data enabled (Polygon)")
        else:
            print("⚠️  Options data disabled")
        
        # Test with a sample stock
        print("\n" + "=" * 70)
        print("Testing with AAPL...")
        data = client.fetch_complete_data("AAPL")
        
        print("\n" + "=" * 70)
        print("Data Summary:")
        print(f"  Quote: {'✓' if data['quote'] else '✗'}")
        print(f"  Historical: {'✓' if data['historical'] else '✗'}")
        print(f"  Profile: {'✓' if data['profile'] else '✗'}")
        print(f"  News: {'✓' if data['news'] else '✗'}")
        print(f"  Financials: {'✓' if data['financials'] else '✗'}")
        print(f"  Options: {'✓' if data['options'] else '✗'}")
        
        if data['options']:
            print(f"\n  Options Data:")
            print(f"    P/C Ratio: {data['options'].get('pc_ratio', 'N/A')}")
            print(f"    ATM IV: {data['options'].get('atm_iv', 'N/A')}%")
            greeks = data['options'].get('greeks', {})
            if greeks:
                print(f"    Delta: {greeks.get('delta', 'N/A')}")
                print(f"    Gamma: {greeks.get('gamma', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
