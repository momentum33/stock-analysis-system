import sys
from fmp_client import DataClient
import config

print("="*80)
print("SIMPLE API TEST")
print("="*80)

print("\n1. Testing API Key Loading...")
print(f"   FMP Key: {config.FMP_API_KEY[:10]}...")
if config.FMP_API_KEY == "YOUR_FMP_API_KEY_HERE":
    print("   ERROR: API key not loaded!")
    sys.exit(1)
else:
    print("   API key loaded from .env")

print("\n2. Initializing FMP Client...")
try:
    client = DataClient()
    print("   Client initialized")
except Exception as e:
    print(f"   ERROR: {e}")
    sys.exit(1)

print("\n3. Fetching AAPL quote...")
try:
    quote = client.get_quote("AAPL")
    if quote:
        print(f"   AAPL Price: $" + str(quote[0].get('price', 'N/A')))
    else:
        print("   No data returned")
except Exception as e:
    print(f"   ERROR: {e}")

print("\nTEST COMPLETE!")
