"""
Simple FinViz Elite Screener Ticker Fetcher
Uses FinViz's built-in CSV export API
"""

import requests
import csv
from io import StringIO

def fetch_finviz_tickers(screener_url: str, api_token: str) -> list:
    """
    Fetch tickers from FinViz Elite screener using CSV export
    
    Args:
        screener_url: Your FinViz screener URL
        api_token: Your FinViz API token (from the export page)
        
    Returns:
        List of ticker symbols
    """
    # Convert screener URL to export URL
    export_url = screener_url.replace('screener.ashx', 'export.ashx')
    
    # Add authentication token
    if '&auth=' not in export_url:
        export_url += f'&auth={api_token}'
    
    print(f"📥 Fetching tickers from FinViz...")
    
    try:
        # Download CSV
        response = requests.get(export_url, timeout=10)
        response.raise_for_status()
        
        # Parse CSV
        csv_data = StringIO(response.text)
        reader = csv.DictReader(csv_data)
        
        # Extract tickers (first column is usually 'Ticker')
        tickers = []
        for row in reader:
            ticker = row.get('Ticker') or row.get('ticker') or list(row.values())[0]
            if ticker:
                tickers.append(ticker.strip())
        
        print(f"✅ Found {len(tickers)} tickers")
        return tickers
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def save_tickers(tickers: list, output_file: str = "input_tickers.txt"):
    """Save tickers to text file"""
    with open(output_file, 'w') as f:
        f.write("# FinViz Screener Tickers\n")
        for ticker in tickers:
            f.write(f"{ticker}\n")
    print(f"💾 Saved to {output_file}")


if __name__ == "__main__":
    import sys
    
    # YOUR CONFIGURATION
    SCREENER_URL = "https://elite.finviz.com/screener.ashx?v=141&f=cap_microover,fa_debteq_u1,fa_epsyoy_pos,fa_epsyoy1_pos,fa_roe_o10,geo_usa,sh_avgvol_o500,sh_price_o5,ta_beta_o1,ta_sma20_sa50,ta_sma50_pa&ft=4&o=-relativevolume"
    
    # Get your API token from: https://elite.finviz.com/export.ashx
    # Click "Regenerate Token" if needed
    API_TOKEN = "6a8f4866-8965-4c9e-b941-f56c97379554"  # Replace with your actual token
    
    # Allow command line arguments for flexibility
    # Usage: python finviz_scraper.py [custom_url] [output_file]
    if len(sys.argv) > 1:
        SCREENER_URL = sys.argv[1]
    
    output_file = "input_tickers.txt"
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    # Fetch tickers
    tickers = fetch_finviz_tickers(SCREENER_URL, API_TOKEN)
    
    if tickers:
        save_tickers(tickers, output_file)
        print(f"\n✅ Ready to analyze! Run: python main.py {output_file}")
    else:
        print("\n❌ No tickers found. Check your token and URL.")
        print("\n💡 Make sure to:")
        print("   1. Set your API_TOKEN in the script")
        print("   2. Verify your screener URL is correct")
        print("   3. Check you're logged into FinViz Elite")
    