# ⚡ QUICK FIX: JSON Parsing Errors

## You're seeing this error:
```
⚠ Sentiment analysis error: Expecting value: line 1 column 1 (char 0)
```

## What it means:
Claude API is responding, but not in the expected JSON format. This is usually an API key or configuration issue.

## 5-Minute Fix:

### Step 1: Check Your API Key
Open `config.py` and verify:
```python
CLAUDE_API_KEY = "sk-ant-api03-your-actual-key-here"
```

❌ **Wrong:**
```python
CLAUDE_API_KEY = "YOUR_CLAUDE_API_KEY_HERE"  # Not replaced!
```

✅ **Correct:**
```python
CLAUDE_API_KEY = "sk-ant-api03-abcdefgh123456..."  # Actual key
```

### Step 2: Get a Valid API Key

1. Go to https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-api`)
4. Paste into `config.py`

### Step 3: Update the Code

**The fixed version handles JSON parsing better!**

[Download Updated System](computer:///mnt/user-data/outputs/stock-analysis-system.zip)

Replace your `claude_analyzer.py` with the updated version from the zip.

### Step 4: Re-run

```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```

---

## Still Not Working?

### Quick Diagnostics:

**Test your API key:**
```bash
python -c "
import anthropic
client = anthropic.Anthropic(api_key='YOUR_KEY_HERE')
response = client.messages.create(
    model='claude-sonnet-4-20250514',
    max_tokens=50,
    messages=[{'role': 'user', 'content': 'Say hi'}]
)
print('API Key works!', response.content[0].text)
"
```

Replace `YOUR_KEY_HERE` with your actual key.

**Expected:** Should print "API Key works! Hi there!"

**If error:** Your API key is invalid or expired.

---

## Alternative: Use Standard Mode

While you fix the Claude integration, you can still use the quantitative analysis:

```bash
python main.py input_tickers.txt
```

This works without Claude API and still gives you great results!

---

## What's Happening Behind the Scenes

The system makes 5 Claude API calls per stock:
1. Sentiment analysis
2. Catalyst identification  
3. Risk assessment
4. Bull/Bear thesis
5. Trading recommendation

If any call fails, it uses neutral defaults (score 5.0, Hold, Low confidence).

**This is by design** - you'll still get results even if Claude has issues.

---

## Expected Behavior

### ✅ Working Correctly:
```
[1/20] AAPL
  🤖 Claude analyzing AAPL...
  ✓ Sentiment: Very Positive (8.5/10)
  ✓ Recommendation: Strong Buy (Confidence: High)
```

### ⚠️ API Key Issue:
```
[1/20] AAPL
  🤖 Claude analyzing AAPL...
    ⚠ Sentiment analysis error: Expecting value...
  ✓ Sentiment: Neutral (5.0/10)
  ✓ Recommendation: Hold (Confidence: Low)
```

---

## Most Common Causes

| Issue | Fix |
|-------|-----|
| API key not set | Edit config.py with your actual key |
| API key invalid | Generate new key at console.anthropic.com |
| Wrong model name | Use `claude-sonnet-4-20250514` |
| anthropic not installed | `pip install anthropic` |
| Old version of analyzer | Download updated zip file |

---

## Need More Help?

See **CLAUDE_TROUBLESHOOTING.md** for detailed solutions to all issues.

---

**Don't let this stop you!** The quantitative system works great on its own with `python main.py`. Claude adds insights but isn't required for good stock picks.
