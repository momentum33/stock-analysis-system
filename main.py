#!/usr/bin/env python3
"""
Stock Analysis System - Main Script
Analyzes stocks from your screener and produces ranked reports

Usage:
    python main.py input_tickers.txt
    
Input file format: One ticker per line (e.g., AAPL, TSLA, NVDA)
"""

import sys
import os
from datetime import datetime
from typing import List
import config
from fmp_client import FMPClient
from analyzer import StockAnalyzer
from report_generator import ReportGenerator


def read_tickers_from_file(filepath: str) -> List[str]:
    """Read ticker symbols from input file"""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found")
        return []
    
    tickers = []
    with open(filepath, 'r') as f:
        for line in f:
            ticker = line.strip().upper()
            if ticker and not ticker.startswith('#'):  # Skip empty lines and comments
                tickers.append(ticker)
    
    return tickers


def main():
    """Main execution function"""
    print("=" * 80)
    print("STOCK ANALYSIS SYSTEM - SHORT TERM TRADING")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check for API key
    if config.FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
        print("❌ ERROR: Please set your FMP API key in config.py")
        print("   Edit config.py and replace 'YOUR_FMP_API_KEY_HERE' with your actual API key")
        return
    
    # Get input file
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        print("\nInput file should contain one ticker symbol per line")
        print("Example input_tickers.txt:")
        print("  AAPL")
        print("  TSLA")
        print("  NVDA")
        
        # Check for default input file
        default_file = "input_tickers.txt"
        if os.path.exists(default_file):
            print(f"\n✓ Found {default_file}, using that as input")
            input_file = default_file
        else:
            return
    else:
        input_file = sys.argv[1]
    
    # Read tickers
    print(f"Reading tickers from: {input_file}")
    tickers = read_tickers_from_file(input_file)
    
    if not tickers:
        print("❌ No valid tickers found in input file")
        return
    
    print(f"✓ Found {len(tickers)} tickers to analyze\n")
    
    # Initialize components
    print("Initializing FMP API client...")
    client = FMPClient(config.FMP_API_KEY)
    
    # Initialize Polygon client if API key is set
    polygon_client = None
    if hasattr(config, 'POLYGON_API_KEY') and config.POLYGON_API_KEY != "YOUR_POLYGON_API_KEY_HERE":
        print("Initializing Polygon.io API client for options and short interest...")
        from polygon_client import PolygonClient
        polygon_client = PolygonClient(config.POLYGON_API_KEY)
        print("✓ Polygon.io client initialized (Options & Short Interest enabled)")
    else:
        print("⚠️ Polygon API key not set - skipping options and enhanced short interest")
        print("   Set POLYGON_API_KEY in config.py to enable these features")
    
    print("Initializing stock analyzer...")
    analyzer = StockAnalyzer(client, polygon_client)
    
    print("Fetching market baseline (SPY)...")
    if not analyzer.fetch_market_baseline():
        print("⚠ Warning: Could not fetch market baseline, relative strength scores will be neutral")
    else:
        print("✓ Market baseline loaded\n")
    
    # Analyze stocks
    print("=" * 80)
    print("ANALYZING STOCKS")
    print("=" * 80)
    
    results = []
    for i, ticker in enumerate(tickers, 1):
        print(f"\n[{i}/{len(tickers)}] {ticker}")
        analysis = analyzer.analyze_stock(ticker)
        if analysis:
            results.append(analysis)
    
    print("\n" + "=" * 80)
    print(f"ANALYSIS COMPLETE: {len(results)}/{len(tickers)} stocks passed filters")
    print("=" * 80 + "\n")
    
    if not results:
        print("❌ No stocks passed the analysis filters")
        print("   Try adjusting filter thresholds in config.py")
        return
    
    # Sort by total score
    results.sort(key=lambda x: x['total_score'], reverse=True)
    
    # Get top N
    top_stocks = results[:config.TOP_N_STOCKS]
    
    print(f"Top {len(top_stocks)} stocks selected:")
    for i, stock in enumerate(top_stocks, 1):
        print(f"  {i}. {stock['symbol']:6} - Score: {stock['total_score']:.2f} - ${stock['price']:.2f}")
    
    # Generate reports
    print("\n" + "=" * 80)
    print("GENERATING REPORTS")
    print("=" * 80 + "\n")
    
    report_gen = ReportGenerator()
    report_paths = report_gen.generate_all_reports(top_stocks, len(tickers))
    
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nReports generated in: {report_gen.output_dir}/")
    print(f"  • CSV:       {os.path.basename(report_paths['csv'])}")
    print(f"  • Dashboard: {os.path.basename(report_paths['html'])}")
    print(f"  • Report:    {os.path.basename(report_paths['pdf'])}")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Quick summary
    print("\n" + "=" * 80)
    print("QUICK SUMMARY")
    print("=" * 80)
    
    if len(top_stocks) > 0:
        top_pick = top_stocks[0]
        print(f"\n🏆 TOP PICK: {top_pick['symbol']} ({top_pick['company_name']})")
        print(f"   Score: {top_pick['total_score']:.2f}/10")
        print(f"   Price: ${top_pick['price']:.2f} ({top_pick['metrics']['day_change_pct']:+.2f}%)")
        print(f"   Sector: {top_pick['sector']}")
        print(f"   Key Strengths:")
        
        # Highlight top 3 scores
        scores = [
            ('Momentum', top_pick['momentum_score']),
            ('Volume', top_pick['volume_score']),
            ('Technical', top_pick['technical_score']),
            ('Volatility', top_pick['volatility_score']),
            ('Rel. Strength', top_pick['relative_strength_score']),
            ('Catalyst', top_pick['catalyst_score']),
            ('Liquidity', top_pick['liquidity_score']),
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        
        for name, score in scores[:3]:
            print(f"     • {name}: {score:.1f}/10")
    
    print("\n✨ Ready for your trading day!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
