#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from typing import List
from fmp_client import DataClient
from analyzer import StockAnalyzer
from report_generator import ReportGenerator
from pre_screener import PreScreener
from data_collector import DataCollector
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
    
    # Core data
    historical = client.get_historical_prices(ticker, days=250)
    profile = client.get_company_profile(ticker)
    news = client.get_news(ticker, limit=10)
    ratios = client.get_financial_ratios(ticker)
    spy_data = client.get_historical_prices('SPY', days=250)
    
    # Get current price for options calculations
    current_price = historical[-1]['close'] if historical else 0
    
    # Polygon options data
    options_analysis = None
    if current_price > 0 and config.ANALYSIS_CONFIG.get('options', {}).get('enabled', False):
        try:
            put_call = client.get_put_call_ratio(ticker)
            atm_iv = client.get_atm_iv(ticker, current_price)
            options_agg = client.get_options_aggregate(ticker, days=30)
            
            if options_agg:
                options_analysis = {
                    'put_call_ratio': put_call,
                    'atm_implied_volatility': atm_iv,
                    'total_call_volume': options_agg.get('call_volume', 0),
                    'total_put_volume': options_agg.get('put_volume', 0),
                    'total_contracts': options_agg.get('total_contracts', 0),
                    'net_delta': options_agg.get('net_delta', 0),
                    'near_term_expirations': options_agg.get('expirations', [])[:5]
                }
        except Exception as e:
            pass
    
    # Short interest
    short_interest = client.get_short_interest_fmp(ticker)
    
    # Growth metrics
    growth = client.get_financial_growth(ticker)
    if growth and isinstance(growth, list):
        growth = growth[0]
    
    return {
        'symbol': ticker,
        'historical': historical or [],
        'profile': profile if isinstance(profile, dict) else (profile[0] if profile else {}),
        'news': news or [],
        'spy_data': spy_data or [],
        'financials': ratios if isinstance(ratios, dict) else (ratios[0] if ratios else {}),
        'options_analysis': options_analysis,
        'short_interest_data': short_interest,
        'growth_metrics': growth
    }

def main():
    print("="*80)
    print("STOCK ANALYSIS SYSTEM - 3 STAGE WORKFLOW")
    
    # Check for deep analysis flag
    enable_deep_analysis = "--deep-analysis" in sys.argv
    claude = None
    
    if enable_deep_analysis:
        print("WITH CLAUDE AI DEEP ANALYSIS & OPTIONS STRATEGIES")
        if config.CLAUDE_API_KEY == "YOUR_CLAUDE_API_KEY_HERE":
            print("ERROR: Set CLAUDE_API_KEY in .env")
            return
        from claude_analyzer_enhanced import ClaudeAnalyzer
        claude = ClaudeAnalyzer(api_key=config.CLAUDE_API_KEY, model=config.CLAUDE_MODEL)
        print(f"Claude initialized: {config.CLAUDE_MODEL}")
    
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize data collector
    data_collector = DataCollector()
    print("Database initialized for tracking\n")
    
    if config.FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
        print("ERROR: Set FMP_API_KEY in .env")
        return
    
    if len(sys.argv) < 2:
        print("Usage: python working_main.py input_tickers.txt [--deep-analysis]")
        return
    
    input_file = [arg for arg in sys.argv[1:] if not arg.startswith('--')][0]
    tickers = read_tickers(input_file)
    if not tickers:
        return
    
    print(f"Stage 1: Analyzing {len(tickers)} stocks from FinViz\n")
    
    # Start tracking this analysis run
    run_id = data_collector.start_analysis_run(
        total_tickers=len(tickers),
        deep_analysis=enable_deep_analysis,
        notes=f"3-stage analysis from {input_file}"
    )
    print(f"Started tracking run #{run_id}\n")
    
    client = DataClient()
    analyzer = StockAnalyzer()
    
    # STAGE 1: QUANTITATIVE ANALYSIS
    print("="*80)
    print("STAGE 1: QUANTITATIVE ANALYSIS")
    print("="*80 + "\n")
    
    results = []
    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] {ticker}")
        try:
            stock_data = fetch_stock_data(client, ticker)
            analysis = analyzer.analyze_stock(stock_data)
            
            if analysis:
                analysis['total_score'] = analysis.get('composite_score', 0)
                analysis['symbol'] = ticker
                analysis['company_name'] = stock_data['profile'].get('companyName', ticker)
                hist = stock_data['historical']
                analysis['price'] = hist[-1]['close'] if hist else 0
                
                if 'metrics' in analysis:
                    m = analysis['metrics']
                    analysis['metrics']['day_change_pct'] = m.get('daily_change', 0)
                    analysis['metrics']['week_change_pct'] = m.get('roc_5d', 0)
                    analysis['metrics']['month_change_pct'] = m.get('roc_20d', 0)
                    analysis['metrics']['volume_ratio'] = 1.0
                    analysis['metrics']['rsi_14'] = 50.0
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
                analysis['options_analysis'] = stock_data.get('options_analysis')
                
                if 'liquidity_score' not in analysis:
                    analysis['liquidity_score'] = 0.0
                if 'options_score' not in analysis:
                    analysis['options_score'] = 0.0
                
                # Log to database
                analysis_id = data_collector.log_stock_analysis(run_id, analysis)
                analysis['analysis_id'] = analysis_id
                
                results.append(analysis)
                print(f"  Score: {analysis['total_score']:.2f}\n")
        except Exception as e:
            print(f"  Error: {e}\n")
    
    print(f"\nStage 1 Complete: {len(results)}/{len(tickers)} stocks passed\n")
    
    if not results:
        print("No stocks passed initial analysis")
        return
    
    # Sort by score
    results.sort(key=lambda x: x.get('total_score', 0), reverse=True)
    
    # STAGE 2: PRE-SCREENING (if deep analysis enabled)
    filtered_results = results
    if enable_deep_analysis:
        print("="*80)
        print("STAGE 2: PRE-SCREENING")
        print("="*80 + "\n")
        
        prescreener = PreScreener(client)
        
        # Just rank by quality, don't filter aggressively
        print(f"Ranking {len(results)} stocks by analysis quality...")
        filtered_results = prescreener.rank_by_quality(results)
        
        # Take top N for deep analysis
        deep_analysis_count = min(len(filtered_results), config.DEEP_ANALYSIS_TOP_N)
        filtered_results = filtered_results[:deep_analysis_count]
        
        print(f"\nSelected top {len(filtered_results)} stocks for Claude deep analysis")
        for i, s in enumerate(filtered_results, 1):
            print(f"  {i}. {s['symbol']:6} - Score: {s['total_score']:.2f} (Quality: {s.get('quality_score', 0):.1f})")
        print()
    
    # STAGE 3: CLAUDE DEEP ANALYSIS
    if enable_deep_analysis and claude and filtered_results:
        print("="*80)
        print("STAGE 3: CLAUDE DEEP ANALYSIS & OPTIONS STRATEGIES")
        print("="*80 + "\n")
        
        for i, stock in enumerate(filtered_results, 1):
            print(f"[{i}/{len(filtered_results)}] {stock['symbol']} - Score: {stock['total_score']:.2f}")
            try:
                # Find original stock data for news
                original = next((s for s in results if s['symbol'] == stock['symbol']), stock)
                
                print(f"  Running Claude AI analysis...")
                claude_result = claude.analyze_stock_deep(stock, original.get('news', []))
                stock['claude_analysis'] = claude_result
                
                # Log Claude analysis to database
                if 'analysis_id' in stock:
                    data_collector.log_claude_analysis(stock['analysis_id'], claude_result)
                
                if 'options_strategies' in claude_result:
                    strats = claude_result['options_strategies'].get('strategies', [])
                    print(f"  ✅ Generated {len(strats)} options strategies")
                    for s in strats[:3]:
                        print(f"    • {s.get('name', 'Strategy')}")
                
                print()
            except Exception as e:
                print(f"  Error in Claude analysis: {e}\n")
    
    # GENERATE REPORTS
    print("="*80)
    print("GENERATING REPORTS")
    print("="*80 + "\n")
    
    # Use all results for standard reports, filtered for deep analysis
    report_stocks = filtered_results if enable_deep_analysis else results[:config.TOP_N_STOCKS]
    
    if enable_deep_analysis and any('claude_analysis' in s for s in report_stocks):
        try:
            from claude_report_generator import ClaudeReportGenerator
            report_gen = ClaudeReportGenerator()
            print("Using enhanced reports with options strategies...")
        except ImportError:
            report_gen = ReportGenerator()
    else:
        report_gen = ReportGenerator()
    
    # Create comparative analysis if we have Claude results
    comparative = None
    if any('claude_analysis' in s for s in report_stocks):
        comparative = {
            'top_5': [{'rank': i+1, 'symbol': s['symbol'], 'reason': 'High quantitative score'} 
                     for i, s in enumerate(report_stocks[:5])],
            'market_outlook': 'See individual analyses for details'
        }
    
    report_paths = report_gen.generate_all_reports(report_stocks, len(tickers), comparative)
    
    print(f"\nReports saved to output/")
    print(f"  CSV:  {os.path.basename(report_paths['csv'])}")
    print(f"  HTML: {os.path.basename(report_paths['html'])}")
    print(f"  PDF:  {os.path.basename(report_paths['pdf'])}")
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nWorkflow Summary:")
    print(f"  Stage 1 (Quantitative): {len(results)}/{len(tickers)} passed")
    if enable_deep_analysis:
        print(f"  Stage 2 (Pre-screening): {len(filtered_results)} selected")
        print(f"  Stage 3 (Claude AI): {sum(1 for s in report_stocks if 'claude_analysis' in s)} analyzed")
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show historical stats
    print("\n" + "="*80)
    print("DATABASE TRACKING SUMMARY")
    print("="*80)
    stats = data_collector.get_summary_stats(days_back=30)
    print(f"Last 30 Days:")
    print(f"  Total Runs: {stats['total_runs']}")
    print(f"  Stocks Analyzed: {stats['total_stocks_analyzed']}")
    print(f"  Average Score: {stats['average_score']:.2f}")
    if enable_deep_analysis:
        print(f"  Deep Analysis Runs: {stats.get('deep_analysis_runs', 0)}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()



