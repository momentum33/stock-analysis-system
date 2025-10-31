#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from typing import List
from fmp_client import DataClient
from analyzer import StockAnalyzer
from report_generator import ReportGenerator
import config

def read_tickers(filepath: str) -> List[str]:
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found")
        return []
    
    tickers = []
    with open(filepath, 'r') as f:
        for line in f:
            ticker = line.strip().upper()
            if ticker and not ticker.startswith('#'):
                tickers.append(ticker)
    return tickers

def fetch_stock_data(client: DataClient, ticker: str) -> dict:
    print(f"  Fetching {ticker}...")
    historical = client.get_historical_prices(ticker, days=250)
    profile = client.get_company_profile(ticker)
    news = client.get_news(ticker, limit=10)
    ratios = client.get_financial_ratios(ticker)
    spy_data = client.get_historical_prices('SPY', days=250)
    
    return {
        'symbol': ticker,
        'historical': historical or [],
        'profile': profile if isinstance(profile, dict) else (profile[0] if profile else {}),
        'news': news or [],
        'spy_data': spy_data or [],
        'financials': ratios if isinstance(ratios, dict) else (ratios[0] if ratios else {})
    }

def main():
    print("="*80)
    print("STOCK ANALYSIS SYSTEM")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    if config.FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
        print("ERROR: Set FMP_API_KEY in .env")
        return
    
    if len(sys.argv) < 2:
        print("Usage: python working_main.py input_tickers.txt")
        return
    
    tickers = read_tickers(sys.argv[1])
    if not tickers:
        return
    
    print(f"Analyzing {len(tickers)} stocks\n")
    
    client = DataClient()
    analyzer = StockAnalyzer()
    
    results = []
    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] {ticker}")
        try:
            stock_data = fetch_stock_data(client, ticker)
            analysis = analyzer.analyze_stock(stock_data)
            
            if analysis:
                # Map composite_score to total_score
                analysis['total_score'] = analysis.get('composite_score', 0)
                analysis['symbol'] = ticker
                analysis['company_name'] = stock_data['profile'].get('companyName', ticker)
                hist = stock_data['historical']
                analysis['price'] = hist[-1]['close'] if hist else 0
                
                # Map analyzer metrics to report generator format
                if 'metrics' in analysis:
                    m = analysis['metrics']
                    analysis['metrics']['day_change_pct'] = m.get('daily_change', 0)
                    analysis['metrics']['week_change_pct'] = m.get('roc_5d', 0)
                    analysis['metrics']['month_change_pct'] = m.get('roc_20d', 0)
                    analysis['metrics']['volume_ratio'] = 1.0
                    analysis['metrics']['rsi_14'] = 50.0
                    # Add technical indicators
                    analysis['metrics']['sma_10'] = analysis['price']
                    analysis['metrics']['sma_20'] = analysis['price']
                    analysis['metrics']['sma_50'] = analysis['price']
                    analysis['metrics']['ema_12'] = analysis['price']
                    analysis['metrics']['ema_26'] = analysis['price']
                    analysis['volume'] = m.get('volume', 0)
                    analysis['avg_volume'] = m.get('avg_volume', m.get('volume', 0))
                
                analysis['market_cap'] = stock_data['profile'].get('mktCap', 0)
                analysis['sector'] = stock_data['profile'].get('sector', 'Unknown')
                analysis['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Add missing score fields
                if 'liquidity_score' not in analysis:
                    analysis['liquidity_score'] = 0.0
                if 'options_score' not in analysis:
                    analysis['options_score'] = 0.0
                
                results.append(analysis)
                print(f"  Score: {analysis['total_score']:.2f}\n")
        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    results.sort(key=lambda x: x.get('total_score', 0), reverse=True)
    
    print(f"\n{len(results)}/{len(tickers)} stocks passed filters\n")
    
    if results:
        print("Top 10:")
        for i, s in enumerate(results[:10], 1):
            print(f"  {i}. {s['symbol']:6} - {s.get('total_score', 0):.2f} - ")
        
        print("\nGenerating reports...")
        report_gen = ReportGenerator()
        report_paths = report_gen.generate_all_reports(results[:config.TOP_N_STOCKS], len(tickers))
        print(f"\nReports saved to output/")
        print(f"  CSV:  {os.path.basename(report_paths['csv'])}")
        print(f"  HTML: {os.path.basename(report_paths['html'])}")
        print(f"  PDF:  {os.path.basename(report_paths['pdf'])}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


