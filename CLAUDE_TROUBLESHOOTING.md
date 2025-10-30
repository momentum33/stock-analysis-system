# 🔧 CLAUDE API TROUBLESHOOTING GUIDE

## Common Issues and Solutions

### Issue 1: JSON Parsing Errors

**Symptoms:**
```
⚠ Sentiment analysis error: Expecting value: line 1 column 1 (char 0)
⚠ Catalyst analysis error: Expecting value: line 1 column 1 (char 0)
```

**Cause:**
Claude's API response is not returning valid JSON, or the response format is unexpected.

**Solutions:**

#### Solution A: API Key Not Set
Check your `config.py`:
```python
# Must be set correctly
CLAUDE_API_KEY = "sk-ant-api03-your-actual-key-here"
```

**How to verify:**
1. Open `config.py`
2. Check that `CLAUDE_API_KEY` doesn't say "YOUR_CLAUDE_API_KEY_HERE"
3. Verify your key starts with `sk-ant-api`
4. No extra spaces or quotes

#### Solution B: API Key Invalid or Expired
1. Go to https://console.anthropic.com/settings/keys
2. Check if your key is active
3. Generate a new key if needed
4. Update `config.py` with new key

#### Solution C: Model Not Available
The model name might be incorrect. Try these:
```python
# Current recommended models
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Fast, accurate
# OR
CLAUDE_MODEL = "claude-opus-4-20250514"    # Most thorough
# OR
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # Also good
```

#### Solution D: Rate Limiting
If you're hitting rate limits:
```python
# In config.py, analyze fewer stocks
DEEP_ANALYSIS_TOP_N = 10  # Instead of 20
```

Wait a minute and try again.

---

### Issue 2: Empty or Malformed Responses

**Symptoms:**
```
✓ Sentiment: Neutral (5.0/10)
✓ Recommendation: Hold (Confidence: Low)
```
All stocks show neutral/hold with low confidence.

**Cause:**
Claude is returning responses but they're not in the expected JSON format.

**Solution:**

The updated `claude_analyzer.py` (v2) handles this automatically by:
1. Extracting JSON from markdown code blocks
2. Finding JSON in mixed responses
3. Providing detailed error messages

**To verify you have the updated version:**
```bash
grep "_extract_json" claude_analyzer.py
```
Should show the _extract_json method.

**If you don't have it:**
Download the latest version from the updated zip file.

---

### Issue 3: API Connection Errors

**Symptoms:**
```
Error: Connection timeout
Error: APIConnectionError
```

**Solutions:**

#### Check Internet Connection
```bash
ping console.anthropic.com
```

#### Firewall/Proxy Issues
If behind corporate firewall:
```python
# May need to configure proxy
import anthropic
client = anthropic.Anthropic(
    api_key="your-key",
    proxies={
        "http": "http://proxy.company.com:8080",
        "https": "http://proxy.company.com:8080"
    }
)
```

#### Anthropic Service Status
Check https://status.anthropic.com for any outages

---

### Issue 4: Slow Performance

**Symptoms:**
Each stock takes > 60 seconds to analyze.

**Solutions:**

#### Use Faster Model
```python
# Faster
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # 30-40 sec per stock

# Slower but more thorough
# CLAUDE_MODEL = "claude-opus-4-20250514"  # 60-90 sec per stock
```

#### Reduce Number of Stocks
```python
DEEP_ANALYSIS_TOP_N = 10  # Instead of 20
```

#### Check API Response Times
Normal: 30-60 seconds per stock (5 API calls)
Slow: > 90 seconds per stock

If consistently slow, check:
- Your internet speed
- Anthropic's service status
- Time of day (peak hours may be slower)

---

### Issue 5: Import Errors

**Symptoms:**
```
ImportError: No module named 'anthropic'
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
```bash
pip install anthropic

# Or upgrade if already installed
pip install --upgrade anthropic

# Verify installation
python -c "import anthropic; print(anthropic.__version__)"
```

Expected: Should print version number like `0.39.0`

---

### Issue 6: High Costs

**Symptoms:**
Your Claude API bills are higher than expected.

**Solutions:**

#### Check Token Usage
Add to `claude_analyzer.py` after each API call:
```python
print(f"  Tokens used: {response.usage.input_tokens + response.usage.output_tokens}")
```

#### Reduce Analyzed Stocks
```python
# Analyze fewer stocks
DEEP_ANALYSIS_TOP_N = 10  # ~$0.70 per run instead of $1.35
```

#### Use Cheaper Model
```python
# Sonnet is 5x cheaper than Opus
CLAUDE_MODEL = "claude-sonnet-4-20250514"
```

#### Analyze Less Frequently
Instead of daily:
- 3x per week: ~$12/month
- 1x per week: ~$6/month
- On-demand only: Variable

---

### Issue 7: Inconsistent Results

**Symptoms:**
Same stock analyzed twice gives different recommendations.

**Cause:**
This is normal - Claude uses some randomness for natural language.

**To Get More Consistent Results:**

1. **Use temperature parameter** (not currently exposed, but could be added):
```python
response = self.client.messages.create(
    model=self.model,
    max_tokens=1000,
    temperature=0.3,  # Lower = more deterministic (0.0 to 1.0)
    messages=[{"role": "user", "content": prompt}]
)
```

2. **Focus on high-confidence recommendations**
Only act on recommendations with "High" confidence level.

3. **Look for agreement**
If quantitative score AND Claude both agree, higher confidence.

---

### Issue 8: All Analyses Timing Out

**Symptoms:**
Script hangs or times out during Claude analysis phase.

**Solutions:**

#### Increase Timeout
In `claude_analyzer.py`, modify the client initialization:
```python
self.client = anthropic.Anthropic(
    api_key=api_key,
    timeout=120.0  # 2 minutes instead of default
)
```

#### Add Retry Logic
```python
import time

def api_call_with_retry(self, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = self.client.messages.create(...)
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"    Retry {attempt + 1}/{max_retries}...")
                time.sleep(2)
            else:
                raise e
```

---

## Diagnostic Commands

### Check Setup
```bash
# 1. Verify Python packages
pip list | grep anthropic

# 2. Test API key
python -c "
import anthropic
client = anthropic.Anthropic(api_key='YOUR_KEY_HERE')
response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=100,
    messages=[{'role': 'user', 'content': 'Say hello'}]
)
print(response.content[0].text)
"

# 3. Check config
python -c "import config; print(f'FMP: {config.FMP_API_KEY[:10]}...')"
python -c "import config; print(f'Claude: {config.CLAUDE_API_KEY[:10]}...')"
```

### Test Individual Component
```bash
# Test Claude analyzer in isolation
python -c "
from claude_analyzer import ClaudeAnalyzer
import config

analyzer = ClaudeAnalyzer(config.CLAUDE_API_KEY)
print('Analyzer initialized successfully')
"
```

---

## Configuration Best Practices

### Recommended Settings for Beginners
```python
# In config.py
CLAUDE_API_KEY = "your-key-here"
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Fast & affordable
ENABLE_DEEP_ANALYSIS = False  # Use --flag when needed
DEEP_ANALYSIS_TOP_N = 10  # Start with fewer stocks
```

### Recommended Settings for Production
```python
# In config.py
CLAUDE_API_KEY = "your-key-here"
CLAUDE_MODEL = "claude-sonnet-4-20250514"
ENABLE_DEEP_ANALYSIS = True  # Always on
DEEP_ANALYSIS_TOP_N = 20  # Full analysis
```

### Recommended Settings for High Volume
```python
# In config.py
CLAUDE_API_KEY = "your-key-here"
CLAUDE_MODEL = "claude-sonnet-4-20250514"
ENABLE_DEEP_ANALYSIS = True
DEEP_ANALYSIS_TOP_N = 5  # Only top 5 for speed
```

---

## Getting Help

### Error Message Format
When reporting issues, include:
```
1. Error message (full text)
2. Which stock it occurred on
3. Python version: python --version
4. Anthropic version: pip show anthropic
5. Relevant config settings (without revealing API keys)
```

### Debug Mode
To see full API responses, add to `claude_analyzer.py`:
```python
# At top of _analyze_sentiment method
print(f"DEBUG: Prompt length: {len(prompt)}")
print(f"DEBUG: Model: {self.model}")

# After API call
print(f"DEBUG: Response preview: {response.content[0].text[:500]}")
```

---

## Quick Fixes Checklist

When you encounter errors, try these in order:

- [ ] Verify API key is set correctly in config.py
- [ ] Check internet connection
- [ ] Verify anthropic package is installed (`pip list | grep anthropic`)
- [ ] Try with fewer stocks (`DEEP_ANALYSIS_TOP_N = 5`)
- [ ] Use Sonnet model instead of Opus
- [ ] Check Anthropic service status
- [ ] Download latest claude_analyzer.py from updated zip
- [ ] Restart Python / clear cache
- [ ] Try with a fresh API key

---

## Prevention Tips

### Before Each Run:
1. Check config.py has valid API keys
2. Verify enough API credits in Anthropic console
3. Test with small sample first (5-10 stocks)
4. Monitor console output for warnings

### Regular Maintenance:
1. Update anthropic package monthly: `pip install --upgrade anthropic`
2. Check for new model versions
3. Review API usage in Anthropic console
4. Rotate API keys every 6 months

---

## Advanced Debugging

### Enable Verbose Logging
```python
# Add to top of main_with_claude.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Save API Responses
```python
# In claude_analyzer.py, after each API call:
with open(f'debug_{symbol}_sentiment.json', 'w') as f:
    f.write(response.content[0].text)
```

### Monitor Token Usage
```python
# Track total tokens
total_tokens = 0
for stock in stocks:
    # ... API call ...
    total_tokens += response.usage.input_tokens
    total_tokens += response.usage.output_tokens
    print(f"Total tokens so far: {total_tokens}")
```

---

## Still Having Issues?

If none of these solutions work:

1. **Simplify**: Try running on just 1-2 stocks manually
2. **Isolate**: Test Claude API outside the system
3. **Update**: Make sure you have the latest version
4. **Alternative**: Use standard mode without Claude temporarily

The system is designed to handle errors gracefully - even if Claude fails, you'll still get the quantitative analysis.

---

## Success Indicators

You know Claude is working correctly when you see:

```
[1/20] AAPL
  🤖 Claude analyzing AAPL...
  ✓ Sentiment: Very Positive (8.5/10)
  ✓ Recommendation: Strong Buy (Confidence: High)

[2/20] TSLA
  🤖 Claude analyzing TSLA...
  ✓ Sentiment: Positive (7.2/10)
  ✓ Recommendation: Buy (Confidence: Medium)
```

Not like this:
```
[1/20] AAPL
  🤖 Claude analyzing AAPL...
    ⚠ Sentiment analysis error: ...
    ⚠ Catalyst analysis error: ...
  ✓ Sentiment: Neutral (5.0/10)
  ✓ Recommendation: Hold (Confidence: Low)
```

---

**Remember:** The system works in two modes - if Claude isn't working, you can always fall back to `python main.py` for quantitative analysis only!
