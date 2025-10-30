"""
Polygon.io API Client for Options and Short Interest Data
"""
import requests
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import config


class PolygonClient:
    """Client for Polygon.io API - Options and Short Interest"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io"
        self.last_request_time = 0
        self.request_count = 0
        self.minute_start = time.time()
        
    def _rate_limit(self):
        """Enforce rate limiting (5 requests per minute for free tier, more for paid)"""
        current_time = time.time()
        
        # Reset counter every minute
        if current_time - self.minute_start > 60:
            self.request_count = 0
            self.minute_start = current_time
        
        # For free tier: 5 calls/min, paid tiers have higher limits
        rate_limit = config.POLYGON_RATE_LIMIT if hasattr(config, 'POLYGON_RATE_LIMIT') else 5
        
        if self.request_count >= rate_limit - 1:
            sleep_time = 60 - (current_time - self.minute_start)
            if sleep_time > 0:
                print(f"Polygon rate limit approaching, sleeping {sleep_time:.1f}s...")
                time.sleep(sleep_time)
                self.request_count = 0
                self.minute_start = time.time()
        
        # Add buffer between requests
        elapsed = current_time - self.last_request_time
        buffer = 12 if rate_limit == 5 else 0.2  # 12s for free tier, 0.2s for paid
        if elapsed < buffer:
            time.sleep(buffer - elapsed)
        
        self.last_request_time = time.time()
        self.request_count += 1
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make API request with error handling"""
        self._rate_limit()
        
        if params is None:
            params = {}
        params['apiKey'] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Polygon API error for {endpoint}: {e}")
            return None
    
    # ==================== OPTIONS CHAIN & CONTRACTS ====================
    
    def get_options_contracts(self, 
                            underlying_ticker: str,
                            contract_type: Optional[str] = None,
                            expiration_date: Optional[str] = None,
                            strike_price: Optional[float] = None,
                            limit: int = 250) -> Optional[List[Dict]]:
        """
        Get options contracts for an underlying ticker
        
        Args:
            underlying_ticker: Stock symbol (e.g., 'AAPL')
            contract_type: 'call' or 'put' (optional)
            expiration_date: Date in YYYY-MM-DD format (optional)
            strike_price: Strike price (optional)
            limit: Max results (default 250, max 1000)
            
        Returns:
            List of contract details
        """
        params = {
            'underlying_ticker': underlying_ticker,
            'limit': limit,
            'order': 'asc',
            'sort': 'expiration_date'
        }
        
        if contract_type:
            params['contract_type'] = contract_type
        if expiration_date:
            params['expiration_date'] = expiration_date
        if strike_price:
            params['strike_price'] = strike_price
        
        data = self._make_request('v3/reference/options/contracts', params)
        return data.get('results', []) if data else None
    
    def get_options_chain_snapshot(self,
                                  underlying_ticker: str,
                                  contract_type: Optional[str] = None,
                                  expiration_date_gte: Optional[str] = None,
                                  strike_price: Optional[float] = None,
                                  limit: int = 250) -> Optional[List[Dict]]:
        """
        Get snapshot of entire options chain with Greeks, IV, quotes
        
        Args:
            underlying_ticker: Stock symbol
            contract_type: 'call' or 'put' (optional)
            expiration_date_gte: Minimum expiration date YYYY-MM-DD (optional)
            strike_price: Strike price (optional)
            limit: Max results (default 250, max 250)
            
        Returns:
            List of option chain data with Greeks, IV, quotes, open interest
        """
        endpoint = f'v3/snapshot/options/{underlying_ticker}'
        params = {'limit': limit}
        
        if contract_type:
            params['contract_type'] = contract_type
        if expiration_date_gte:
            params['expiration_date.gte'] = expiration_date_gte
        if strike_price:
            params['strike_price'] = strike_price
        
        data = self._make_request(endpoint, params)
        return data.get('results', []) if data else None
    
    def get_option_contract_snapshot(self, option_ticker: str) -> Optional[Dict]:
        """
        Get detailed snapshot for a single option contract
        
        Args:
            option_ticker: Option contract symbol (e.g., 'O:AAPL250117C00250000')
            
        Returns:
            Detailed contract data including Greeks, IV, quotes, trades
        """
        # Remove O: prefix if present, endpoint expects it
        if not option_ticker.startswith('O:'):
            option_ticker = f'O:{option_ticker}'
        
        endpoint = f'v3/snapshot/options/{option_ticker.replace("O:", "", 1)}/{option_ticker}'
        data = self._make_request(endpoint)
        return data.get('results', {}) if data else None
    
    # ==================== SHORT INTEREST ====================
    
    def get_short_interest(self, ticker: str, limit: int = 20) -> Optional[List[Dict]]:
        """
        Get bi-monthly short interest data from Polygon
        
        Per Polygon docs: https://polygon.io/docs/rest/stocks/fundamentals/short-interest
        
        Args:
            ticker: Stock symbol (optional - if not provided, returns all)
            limit: Number of records to return (default 20)
            
        Returns:
            List of short interest records with:
            - settlement_date: Date of record
            - ticker: Stock symbol
            - short_interest: Total shares sold short
            - avg_daily_volume: Average daily volume
            - days_to_cover: Short interest / average volume
        """
        # CORRECT endpoint per your testing!
        endpoint = 'stocks/v1/short-interest'
        params = {}
        
        # Add ticker filter if provided
        if ticker:
            params['ticker'] = ticker.upper()
        
        if limit:
            params['limit'] = limit
            
        data = self._make_request(endpoint, params)
        return data.get('results', []) if data else None
    
    def get_short_volume(self, 
                        ticker: str,
                        date: Optional[str] = None,
                        limit: int = 20) -> Optional[List[Dict]]:
        """
        Get daily short volume data from Polygon
        
        Per Polygon docs: https://polygon.io/docs/rest/stocks/fundamentals/short-volume
        
        Args:
            ticker: Stock symbol
            date: Specific date YYYY-MM-DD (optional)
            limit: Number of records (default 20)
            
        Returns:
            List of daily short volume records with:
            - date: Trading date
            - short_volume: Number of shares sold short
            - total_volume: Total trading volume
            - short_volume_percent: Percent of volume that was short
        """
        # Correct endpoint - use v3 not vX
        endpoint = f'v3/reference/short-volume'
        params = {
            'ticker': ticker.upper(),
            'limit': limit,
            'sort': 'date',
            'order': 'desc'
        }
        
        if date:
            params['date'] = date
        
        data = self._make_request(endpoint, params)
        return data.get('results', []) if data else None
    
    # ==================== HELPER METHODS ====================
    
    def analyze_options_chain(self, symbol: str) -> Optional[Dict]:
        """
        Analyze full options chain and extract key metrics
        
        Returns:
            Dictionary with analysis:
            - total_call_volume
            - total_put_volume
            - put_call_ratio
            - atm_iv (at-the-money implied volatility)
            - near_term_expirations
            - greeks_summary
        """
        try:
            print(f"  📊 Analyzing options chain for {symbol}...")
            
            # Get near-term options (next 60 days)
            today = datetime.now()
            min_date = (today + timedelta(days=7)).strftime('%Y-%m-%d')
            
            chain_data = self.get_options_chain_snapshot(
                underlying_ticker=symbol,
                expiration_date_gte=min_date,
                limit=250
            )
            
            if not chain_data or len(chain_data) == 0:
                print(f"  ⚠️  No options data available for {symbol}")
                return None
            
            # Separate calls and puts
            calls = [opt for opt in chain_data if opt.get('details', {}).get('contract_type') == 'call']
            puts = [opt for opt in chain_data if opt.get('details', {}).get('contract_type') == 'put']
            
            # Calculate volumes
            total_call_volume = sum(opt.get('day', {}).get('volume', 0) for opt in calls)
            total_put_volume = sum(opt.get('day', {}).get('volume', 0) for opt in puts)
            
            # Safe put/call ratio calculation
            if total_call_volume > 0:
                put_call_ratio = total_put_volume / total_call_volume
            elif total_put_volume > 0:
                put_call_ratio = 999  # Extremely bearish - only puts trading
            else:
                put_call_ratio = 1.0  # Neutral if no volume on either side
            
            # Get ATM IV (options with strikes closest to current price)
            current_price = 0
            avg_iv = None
            
            if chain_data and len(chain_data) > 0 and 'underlying_asset' in chain_data[0]:
                current_price = chain_data[0]['underlying_asset'].get('price', 0)
                
                # Only calculate ATM options if we have a valid current price
                if current_price > 0:
                    # Find ATM options (within 5% of current price)
                    atm_options = [
                        opt for opt in chain_data 
                        if 'details' in opt 
                        and 'strike_price' in opt['details']
                        and abs(opt['details']['strike_price'] - current_price) / current_price < 0.05
                        and opt.get('implied_volatility')
                    ]
                    
                    if atm_options and len(atm_options) > 0:
                        avg_iv = sum(opt['implied_volatility'] for opt in atm_options) / len(atm_options)
            
            # Get unique expiration dates
            expirations = sorted(list(set(
                opt['details']['expiration_date'] 
                for opt in chain_data 
                if 'details' in opt and 'expiration_date' in opt['details']
            )))[:5]
            
            # Aggregate Greeks
            total_delta = sum(opt.get('greeks', {}).get('delta', 0) for opt in calls)
            avg_gamma = (sum(opt.get('greeks', {}).get('gamma', 0) for opt in chain_data) / len(chain_data)) if chain_data and len(chain_data) > 0 else 0
            
            return {
                'symbol': symbol,
                'total_call_volume': total_call_volume,
                'total_put_volume': total_put_volume,
                'put_call_ratio': round(put_call_ratio, 2) if put_call_ratio < 999 else 999,
                'atm_implied_volatility': round(avg_iv, 4) if avg_iv else None,
                'near_term_expirations': expirations,
                'total_contracts': len(chain_data),
                'total_call_contracts': len(calls),
                'total_put_contracts': len(puts),
                'net_delta': round(total_delta, 2),
                'avg_gamma': round(avg_gamma, 6),
                'timestamp': datetime.now().isoformat()
            }
            
        except ZeroDivisionError as e:
            print(f"  ⚠️  Options analysis failed for {symbol}: Division by zero error")
            return None
        except Exception as e:
            print(f"  ⚠️  Options analysis failed for {symbol}: {str(e)}")
            return None
    
    def get_short_interest_summary(self, symbol: str) -> Optional[Dict]:
        """
        Get short interest summary with trend analysis
        
        Returns:
            Dictionary with:
            - latest_short_interest
            - latest_days_to_cover
            - trend (increasing/decreasing/stable)
            - change_pct
        """
        short_data = self.get_short_interest(symbol, limit=4)
        
        if not short_data or len(short_data) == 0:
            return None
        
        latest = short_data[0]
        
        # Calculate trend if we have multiple data points
        trend = "stable"
        change_pct = 0
        
        if len(short_data) >= 2:
            current_si = latest.get('short_interest', 0)
            prev_si = short_data[1].get('short_interest', 0)
            
            if prev_si > 0:
                change_pct = ((current_si - prev_si) / prev_si) * 100
                
                if change_pct > 5:
                    trend = "increasing"
                elif change_pct < -5:
                    trend = "decreasing"
        
        return {
            'symbol': symbol,
            'settlement_date': latest.get('settlement_date'),
            'short_interest': latest.get('short_interest'),
            'average_volume': latest.get('average_volume'),
            'days_to_cover': latest.get('days_to_cover'),
            'trend': trend,
            'change_pct': round(change_pct, 2),
            'data_points': len(short_data),
            'timestamp': datetime.now().isoformat()
        }
    
    def batch_options_analysis(self, symbols: List[str]) -> Dict[str, Dict]:
        """
        Analyze options for multiple symbols
        
        Args:
            symbols: List of stock symbols
            
        Returns:
            Dictionary mapping symbols to options analysis
        """
        results = {}
        
        for symbol in symbols:
            try:
                analysis = self.analyze_options_chain(symbol)
                if analysis:
                    results[symbol] = analysis
                time.sleep(1)  # Be nice to the API
            except Exception as e:
                print(f"  ✗ Error analyzing {symbol}: {e}")
                continue
        
        return results
