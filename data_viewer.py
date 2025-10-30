#!/usr/bin/env python3
"""
Data Viewer - View historical analysis data
Simple command-line tool to query your analysis history
"""

import sys
from data_collector import DataCollector
from datetime import datetime


def print_recent_analyses(collector, days=7):
    """Show recent analysis runs"""
    print(f"\n{'='*80}")
    print(f"RECENT ANALYSES (Last {days} days)")
    print(f"{'='*80}\n")
    
    data = collector.get_historical_performance(days_back=days)
    
    if not data:
        print("No analyses found in this period.")
        return
    
    current_date = None
    for row in data:
        # Print date header if changed
        if row['analysis_date'] != current_date:
            current_date = row['analysis_date']
            print(f"\n📅 {current_date}")
            print("-" * 80)
        
        # Print stock info
        print(f"  {row['ticker']:6} | Score: {row['total_score']:.2f} | ${row['price']:.2f}", end="")
        
        if row['recommendation']:
            print(f" | {row['recommendation']}", end="")
        if row['sentiment_score']:
            print(f" | Sentiment: {row['sentiment_score']:.1f}/10", end="")
        
        print()


def print_ticker_history(collector, ticker, days=30):
    """Show history for specific ticker"""
    print(f"\n{'='*80}")
    print(f"HISTORY FOR {ticker} (Last {days} days)")
    print(f"{'='*80}\n")
    
    data = collector.get_historical_performance(ticker=ticker, days_back=days)
    
    if not data:
        print(f"No analyses found for {ticker} in this period.")
        return
    
    print(f"{'Date':<12} {'Score':<7} {'Price':<10} {'Rec':<12} {'Sentiment':<10}")
    print("-" * 80)
    
    for row in data:
        print(f"{row['analysis_date']:<12} "
              f"{row['total_score']:>5.2f}  "
              f"${row['price']:>7.2f}  "
              f"{row['recommendation'] or 'N/A':<12} "
              f"{row['sentiment_score'] or 'N/A':<10}")


def print_stats(collector, days=30):
    """Show summary statistics"""
    stats = collector.get_summary_stats(days_back=days)
    
    print(f"\n{'='*80}")
    print(f"STATISTICS (Last {days} days)")
    print(f"{'='*80}\n")
    
    print(f"Total Runs: {stats['total_runs']}")
    print(f"Total Stocks Analyzed: {stats['total_stocks_analyzed']}")
    print(f"Average Score: {stats['average_score']}")
    
    if stats['recommendations']:
        print(f"\nRecommendations:")
        for rec, count in stats['recommendations'].items():
            print(f"  {rec}: {count}")
    
    if stats['trades']['total'] > 0:
        print(f"\nTrade Performance:")
        print(f"  Total Trades: {stats['trades']['total']}")
        print(f"  Closed Trades: {stats['trades']['closed']}")
        print(f"  Win Rate: {stats['trades']['win_rate']}%")
        print(f"  Average P&L: {stats['trades']['avg_pnl_pct']}%")
        print(f"  Winners: {stats['trades']['winners']}")
        print(f"  Losers: {stats['trades']['losers']}")


def log_trade_interactive(collector):
    """Interactive trade logging"""
    print(f"\n{'='*80}")
    print("LOG NEW TRADE")
    print(f"{'='*80}\n")
    
    ticker = input("Ticker: ").upper()
    entry_date = input("Entry Date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not entry_date:
        entry_date = datetime.now().strftime('%Y-%m-%d')
    
    entry_price = float(input("Entry Price: $"))
    position_size = input("Position Size (shares or $, optional): ").strip()
    position_size = float(position_size) if position_size else None
    
    strategy = input("Strategy Type (stock/options) [stock]: ").strip().lower() or 'stock'
    
    option_type = None
    strikes = None
    expiration = None
    contracts = None
    
    if strategy == 'options':
        option_type = input("Option Type (call/put/spread): ").strip().lower()
        strikes = input("Strikes (e.g., '150' or '150/155'): ").strip()
        expiration = input("Expiration (YYYY-MM-DD): ").strip()
        contracts = int(input("Contracts: "))
    
    notes = input("Notes (optional): ").strip() or None
    
    trade_id = collector.log_trade(
        ticker=ticker,
        entry_date=entry_date,
        entry_price=entry_price,
        position_size=position_size,
        strategy_type=strategy,
        option_type=option_type,
        strikes=strikes,
        expiration=expiration,
        contracts=contracts,
        notes=notes
    )
    
    print(f"\n✅ Trade logged! Trade ID: {trade_id}")


def export_data(collector, days=30):
    """Export data to CSV"""
    filename = f"analysis_export_{datetime.now().strftime('%Y%m%d')}.csv"
    collector.export_to_csv(filename, days_back=days)
    print(f"\n✅ Data exported to {filename}")


def main():
    """Main menu"""
    collector = DataCollector()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'recent':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            print_recent_analyses(collector, days)
        
        elif command == 'ticker':
            if len(sys.argv) < 3:
                print("Usage: python data_viewer.py ticker SYMBOL [days]")
                return
            ticker = sys.argv[2].upper()
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
            print_ticker_history(collector, ticker, days)
        
        elif command == 'stats':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            print_stats(collector, days)
        
        elif command == 'trade':
            log_trade_interactive(collector)
        
        elif command == 'export':
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            export_data(collector, days)
        
        else:
            print(f"Unknown command: {command}")
            print_help()
    else:
        # Interactive mode
        while True:
            print(f"\n{'='*80}")
            print("DATA VIEWER - Analysis History")
            print(f"{'='*80}\n")
            print("1. Recent Analyses (last 7 days)")
            print("2. Ticker History")
            print("3. Statistics")
            print("4. Log Trade")
            print("5. Export to CSV")
            print("6. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                print_recent_analyses(collector)
            elif choice == '2':
                ticker = input("Ticker: ").upper()
                print_ticker_history(collector, ticker)
            elif choice == '3':
                print_stats(collector)
            elif choice == '4':
                log_trade_interactive(collector)
            elif choice == '5':
                export_data(collector)
            elif choice == '6':
                break
            else:
                print("Invalid choice")


def print_help():
    """Print help"""
    print("""
Data Viewer - View historical analysis data

Usage:
    python data_viewer.py                    # Interactive mode
    python data_viewer.py recent [days]      # Show recent analyses
    python data_viewer.py ticker SYMBOL [days]  # Show ticker history
    python data_viewer.py stats [days]       # Show statistics
    python data_viewer.py trade              # Log a trade
    python data_viewer.py export [days]      # Export to CSV

Examples:
    python data_viewer.py recent 14          # Last 2 weeks
    python data_viewer.py ticker AAPL 30     # AAPL last 30 days
    python data_viewer.py stats 7            # Stats for last week
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
