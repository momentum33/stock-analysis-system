#!/usr/bin/env python3
"""
Stock Analysis System with Claude Deep Analysis - Main Script
Now with Data Collection

Usage:
    python main_with_claude_enhanced.py input_tickers.txt
    python main_with_claude_enhanced.py input_tickers.txt --deep-analysis
"""

import sys
import os
from datetime import datetime
from typing import List
import config
from fmp_client import DataClient
from analyzer import StockAnalyzer
from report_generator import ReportGenerator
from data_collector import DataCollector


def read_tickers_from_file(filepath: str) -> List[str]:
    """Read ticker symbols from input file"""
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


def main():
    """Main execution function"""
    print("=" * 80)
    print("STOCK ANALYSIS SYSTEM - SHORT TERM TRADING")
    print("With Data Collection & Claude AI Analysis")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check for API key
    if config.FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
        print("âŒ ERROR: Please set your FMP API key in config.py")
        return
    
    # Initialize data collector
    print("ðŸ“Š Initializing data collection system...")
    data_collector = DataCollector()
    
    # Check for deep analysis flag
    enable_deep_analysis = "--deep-analysis" in sys.argv or config.ENABLE_DEEP_ANALYSIS
    
    if enable_deep_analysis:
        print("ðŸ¤– DEEP ANALYSIS MODE ENABLED (Using Claude API)")
        
        if config.CLAUDE_API_KEY == "YOUR_CLAUDE_API_KEY_HERE":
            print("âŒ ERROR: Please set your Claude API key in config.py for deep analysis")
            print("   Get your API key from: https://console.anthropic.com/")
            return
        
        # Import Claude analyzer (only if needed)
        try:
            from claude_analyzer_enhanced import ClaudeAnalyzer  # Use enhanced version
            claude_analyzer = ClaudeAnalyzer(
                api_key=config.CLAUDE_API_KEY,
                model=config.CLAUDE_MODEL
            )
            print(f"âœ… Claude API initialized (Model: {config.CLAUDE_MODEL})")
            print(f"âœ… Will analyze top stocks deeply with options strategies\n")
        except ImportError:
            print("âŒ ERROR: anthropic package not installed")
            print("   Install with: pip install anthropic")
            return
        except Exception as e:
            print(f"âŒ ERROR initializing Claude API: {e}")
            return
    
    # Get input file
    input_files = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    
    if len(input_files) < 1:
        print("Usage: python main_with_claude.py <input_file> [--deep-analysis]")
        print("\nOptions:")
        print("  --deep-analysis   Enable Claude API deep analysis on top stocks")
        print("\nInput file should contain one ticker symbol per line")
        
        default_file = "input_tickers.txt"
        if os.path.exists(default_file):
            print(f"\nâœ… Found {default_file}, using that as input")
            input_file = default_file
        else:
            return
    else:
        input_file = input_files[0]
    
    # Read tickers
    print(f"Reading tickers from: {input_file}")
    tickers = read_tickers_from_file(input_file)
    
    if not tickers:
        print("âŒ No valid tickers found in input file")
        return
    
    print(f"âœ… Found {len(tickers)} tickers to analyze\n")
    
    # Initialize components
    print("Initializing FMP API client...")
    client = DataClient()
    
    # Initialize Polygon client if API key is set
    polygon_client = None
    if hasattr(config, 'POLYGON_API_KEY') and config.POLYGON_API_KEY != "YOUR_POLYGON_API_KEY_HERE":
        print("Initializing Polygon.io API client for options and short interest...")
        from polygon_client import PolygonClient
        polygon_client = PolygonClient(config.POLYGON_API_KEY)
        print("âœ… Polygon.io client initialized (Options & Short Interest enabled)")
    else:
        print("âš ï¸ Polygon API key not set - skipping options and enhanced short interest")
    
    print("Initializing stock analyzer...")
    analyzer = StockAnalyzer()
    
    print("Fetching market baseline (SPY)...")
    spy_data = analyzer.fetch_market_baseline()
    if not spy_data:
        print("âš  Warning: Could not fetch market baseline")
        spy_price = None
        spy_change = None
    else:
        print("âœ… Market baseline loaded")
        spy_price = spy_data.get('price')
        spy_change = spy_data.get('metrics', {}).get('day_change_pct')
        print(f"   SPY: ${spy_price:.2f} ({spy_change:+.2f}%)\n")
    
    # Start data collection run
    run_id = data_collector.start_analysis_run(
        total_tickers=len(tickers),
        deep_analysis=enable_deep_analysis,
        spy_price=spy_price,
        spy_change=spy_change,
        notes=f"Analysis from {input_file}"
    )
    print(f"ðŸ“ Started data collection run #{run_id}\n")
    
    # Analyze stocks
    print("=" * 80)
    print("PHASE 1: QUANTITATIVE ANALYSIS")
    print("=" * 80)
    
    results = []
    for i, ticker in enumerate(tickers, 1):
        print(f"\n[{i}/{len(tickers)}] {ticker}")
        analysis = analyzer.analyze_stock(ticker)
        if analysis:
            results.append(analysis)
            # Log to database
            analysis_id = data_collector.log_stock_analysis(run_id, analysis)
            analysis['analysis_id'] = analysis_id  # Store for later use
    
    print("\n" + "=" * 80)
    print(f"PHASE 1 COMPLETE: {len(results)}/{len(tickers)} stocks passed filters")
    print("=" * 80 + "\n")
    
    if not results:
        print("âŒ No stocks passed the analysis filters")
        return
    
    # Update run with passed count
    data_collector.update_run_passed_filters(run_id, len(results))
    
    # Sort by total score
    results.sort(key=lambda x: x['total_score'], reverse=True)
    
    # Get top N for reporting
    top_stocks = results[:config.TOP_N_STOCKS]
    
    print(f"Top {len(top_stocks)} stocks by quantitative score:")
    for i, stock in enumerate(top_stocks, 1):
        print(f"  {i}. {stock['symbol']:6} - Score: {stock['total_score']:.2f} - ${stock['price']:.2f}")
    
    # Deep analysis with Claude
    if enable_deep_analysis:
        print("\n" + "=" * 80)
        print("PHASE 2: QUALITATIVE DEEP ANALYSIS (Claude API)")
        print("=" * 80)
        
        # Use top N stocks directly (your screener already filtered them)
        deep_analysis_stocks = results[:config.DEEP_ANALYSIS_TOP_N]
        
        print(f"\nAnalyzing top {len(deep_analysis_stocks)} stocks with Claude...")
        print("This may take a few minutes...\n")
        
        for i, stock in enumerate(deep_analysis_stocks, 1):
            print(f"[{i}/{len(deep_analysis_stocks)}] {stock['symbol']}")
            
            # Get full news for Claude
            news = client.get_stock_news(stock['symbol'], limit=10)
            
            # Perform deep analysis
            claude_analysis = claude_analyzer.analyze_stock_deep(stock, news or [])
            
            # Add Claude's analysis to stock data
            stock['claude_analysis'] = claude_analysis
            
            # Log Claude analysis to database
            data_collector.log_claude_analysis(stock['analysis_id'], claude_analysis)
            
            # Print quick summary
            sentiment = claude_analysis.get('sentiment', {})
            recommendation = claude_analysis.get('recommendation', {})
            options = claude_analysis.get('options_strategies', {})
            
            print(f"  âœ… Sentiment: {sentiment.get('label', 'Unknown')} ({sentiment.get('score', 0):.1f}/10)")
            print(f"  âœ… Recommendation: {recommendation.get('recommendation', 'Unknown')} (Confidence: {recommendation.get('confidence', 'Unknown')})")
            if options and options.get('strategies'):
                print(f"  ðŸ“ˆ Options Strategies: {len(options['strategies'])} strategies generated")
            print()
        
        # Comparative ranking
        print("=" * 80)
        print("PHASE 4: COMPARATIVE ANALYSIS")
        print("=" * 80)
        
        comparative_analysis = claude_analyzer.comparative_ranking(deep_analysis_stocks)
        
        print("\nðŸ† Claude's Top Picks:")
        for pick in comparative_analysis.get('top_5', [])[:5]:
            print(f"\n#{pick['rank']}. {pick['symbol']}")
            print(f"   Reason: {pick['reason']}")
            if 'key_edge' in pick:
                print(f"   Edge: {pick['key_edge']}")
            if 'entry_timing' in pick:
                print(f"   Entry: {pick['entry_timing']}")
        
        if comparative_analysis.get('avoid'):
            print("\nâš ï¸ Stocks to Avoid:")
            for stock in comparative_analysis.get('avoid', []):
                print(f"   â€¢ {stock['symbol']}: {stock['reason']}")
        
        print(f"\nðŸ“Š Market Outlook: {comparative_analysis.get('market_outlook', 'N/A')}")
        
        # Store comparative analysis
        for stock in deep_analysis_stocks:
            stock['comparative_analysis'] = comparative_analysis
    
    # Generate reports
    print("\n" + "=" * 80)
    print("GENERATING REPORTS")
    print("=" * 80 + "\n")
    
    report_gen = ReportGenerator()
    
    if enable_deep_analysis:
        # Use enhanced report generator for deep analysis
        try:
            from claude_report_generator import ClaudeReportGenerator
            claude_report_gen = ClaudeReportGenerator()
            
            report_paths = claude_report_gen.generate_all_reports(
                deep_analysis_stocks,
                len(tickers),
                comparative_analysis
            )
        except ImportError:
            print("âš  Using standard reports (claude_report_generator not found)")
            report_paths = report_gen.generate_all_reports(top_stocks, len(tickers))
    else:
        report_paths = report_gen.generate_all_reports(top_stocks, len(tickers))
    
    # Summary
    print("\n" + "=" * 80)
    print("âœ… ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\nReports generated in: {report_gen.output_dir}/")
    print(f"  â€¢ CSV:       {os.path.basename(report_paths['csv'])}")
    print(f"  â€¢ Dashboard: {os.path.basename(report_paths['html'])}")
    print(f"  â€¢ Report:    {os.path.basename(report_paths['pdf'])}")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Data collection summary
    print("\n" + "=" * 80)
    print("ðŸ“Š DATA COLLECTION SUMMARY")
    print("=" * 80)
    print(f"Run ID: #{run_id}")
    print(f"Stocks Analyzed: {len(results)}")
    if enable_deep_analysis:
        print(f"Deep Analysis: {len(deep_analysis_stocks)} stocks")
    print(f"Database: {data_collector.db_path}")
    
    # Show historical stats
    stats = data_collector.get_summary_stats(days_back=30)
    print(f"\nLast 30 Days Statistics:")
    print(f"  Total Runs: {stats['total_runs']}")
    print(f"  Total Stocks: {stats['total_stocks_analyzed']}")
    print(f"  Avg Score: {stats['average_score']}")
    if stats['trades']['total'] > 0:
        print(f"\nTrade Performance:")
        print(f"  Total Trades: {stats['trades']['total']}")
        print(f"  Closed: {stats['trades']['closed']}")
        print(f"  Win Rate: {stats['trades']['win_rate']}%")
        print(f"  Avg P&L: {stats['trades']['avg_pnl_pct']}%")
    
    # Enhanced summary with Claude
    if enable_deep_analysis and comparative_analysis.get('top_pick_summary'):
        print("\n" + "=" * 80)
        print("ðŸ¤– CLAUDE'S RECOMMENDATION")
        print("=" * 80)
        print(f"\n{comparative_analysis['top_pick_summary']}")
    
    print("\nâœ¨ Ready for your trading day!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nâš  Analysis interrupted by user")
    except Exception as e:
        print(f"\nâŒ Error: {e}")
        import traceback
        traceback.print_exc()
