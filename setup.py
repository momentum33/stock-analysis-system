#!/usr/bin/env python3
"""
Quick Setup Script for Stock Analysis System
"""

import os
import sys


def main():
    print("=" * 80)
    print("STOCK ANALYSIS SYSTEM - QUICK SETUP")
    print("=" * 80)
    print()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Your version: {sys.version}")
        return
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check if config.py exists
    if not os.path.exists('config.py'):
        print("❌ Error: config.py not found")
        return
    print("✓ Configuration file found")
    
    # Check API key
    import config
    if config.FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
        print("\n⚠ WARNING: API key not configured!")
        print("   Please follow these steps:")
        print("   1. Get a free API key from: https://financialmodelingprep.com/developer/docs/")
        print("   2. Open config.py in a text editor")
        print("   3. Replace 'YOUR_FMP_API_KEY_HERE' with your actual API key")
        print("   4. Save the file and run this setup again")
        return
    print("✓ API key configured")
    
    # Check dependencies
    print("\nChecking dependencies...")
    missing = []
    
    try:
        import requests
        print("✓ requests module installed")
    except ImportError:
        missing.append("requests")
        print("✗ requests module NOT installed")
    
    try:
        import numpy
        print("✓ numpy module installed")
    except ImportError:
        missing.append("numpy")
        print("✗ numpy module NOT installed")
    
    if missing:
        print(f"\n⚠ Missing dependencies: {', '.join(missing)}")
        print("   Install with: pip install " + " ".join(missing))
        print("   Or: pip install -r requirements.txt")
        return
    
    # Check for input file
    print("\nChecking input file...")
    if os.path.exists('input_tickers.txt'):
        print("✓ input_tickers.txt found")
        with open('input_tickers.txt', 'r') as f:
            tickers = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"  Contains {len(tickers)} ticker symbols")
    else:
        print("⚠ input_tickers.txt not found (will need to create one)")
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    print("✓ Output directory ready")
    
    # All checks passed
    print("\n" + "=" * 80)
    print("✅ SETUP COMPLETE!")
    print("=" * 80)
    print("\nYou're ready to analyze stocks!")
    print("\nQuick start:")
    print("  1. Add ticker symbols to input_tickers.txt (one per line)")
    print("  2. Run: python main.py input_tickers.txt")
    print("  3. Check results in the output/ directory")
    print("\nFor detailed instructions, see README.md")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        import traceback
        traceback.print_exc()
