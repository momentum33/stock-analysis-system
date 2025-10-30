# ⚡ WINDOWS ENCODING FIX

## Error You're Seeing:

```
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f4c8'
```

## What It Means:

Windows defaults to cp1252 encoding, which doesn't support emojis (📈, 🤖, etc.) used in the reports.

## 5-Second Fix:

### Option 1: Download Fixed Version (Recommended)

[Download Updated System](computer:///mnt/user-data/outputs/stock-analysis-system.zip)

Replace these two files:
- `report_generator.py`
- `claude_report_generator.py`

**What was fixed:** Added `encoding='utf-8'` to all file writes.

### Option 2: Manual Fix

Edit **both** files and add `encoding='utf-8'`:

**In `claude_report_generator.py`:**

Line ~432:
```python
# OLD
with open(filepath, 'w') as f:

# NEW
with open(filepath, 'w', encoding='utf-8') as f:
```

Line ~449:
```python
# OLD
with open(filepath, 'w') as f:

# NEW  
with open(filepath, 'w', encoding='utf-8') as f:
```

**In `report_generator.py`:**

Line ~516:
```python
# OLD
with open(filepath, 'w') as f:

# NEW
with open(filepath, 'w', encoding='utf-8') as f:
```

Line ~527:
```python
# OLD
with open(filepath, 'w') as f:

# NEW
with open(filepath, 'w', encoding='utf-8') as f:
```

### Option 3: Use PowerShell

Run in PowerShell (not cmd):
```powershell
chcp 65001
python main_with_claude.py input_tickers.txt --deep-analysis
```

---

## After Fixing:

Re-run your analysis:
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```

Reports will generate successfully!

---

## Why This Happens:

- **Mac/Linux:** Default UTF-8 encoding (supports emojis)
- **Windows:** Default cp1252 encoding (no emoji support)
- **Solution:** Explicitly specify UTF-8

---

## Good News:

Your CSV file **already generated successfully!** 

Check:
```
output\stock_analysis_deep_20251027_094414.csv
```

Only the HTML and text reports had the encoding issue.

---

## Test It Works:

After applying the fix:
```bash
python main_with_claude.py input_tickers.txt --deep-analysis
```

You should see:
```
✅ ANALYSIS COMPLETE!

Reports generated in: output/
  • CSV:       stock_analysis_deep_YYYYMMDD_HHMMSS.csv
  • Dashboard: dashboard_deep_YYYYMMDD_HHMMSS.html  ← Will work now!
  • Report:    report_deep_YYYYMMDD_HHMMSS.txt       ← Will work now!
```

---

## Future Windows Users:

This fix is now in the latest version. All Windows users should download the updated zip file to avoid this issue.

---

**Windows-specific issues are now resolved! Download the latest version and re-run.** 🚀
