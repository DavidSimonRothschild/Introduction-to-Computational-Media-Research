# 🔧 Issue: Code Not Running on All Team Machines

## Problem
Currently, the code has hardcoded paths and assumptions that make it difficult to run on different team members' machines. This needs to be fixed to ensure everyone can run the scripts without errors.

## Issues Found

### 1. Inconsistent Path Resolution
Different scripts use different numbers of `.parent` calls when calculating `PROJECT_ROOT`, causing path errors.

**Current State:**
- `datacleaner_instagram.py` (line 103): Uses `.parent.parent.parent` ✅
- `datacleaner_tiktok.py` (line 37): Uses `.parent.parent` ❌
- `caption_sentiment_analysis.py` (line 7): Uses `.parent.parent` ❌

**Impact:** Scripts fail with "File not found" errors when trying to access data folders.

### 2. Hardcoded Relative Path
In `sentiment_analysis.py` (line 8):
```python
datafolder = Path("data/")
```

**Impact:** This assumes `data/` exists in the current working directory, which varies depending on where the script is run from.

### 3. Incomplete Dependencies
`requirements.txt` only lists:
```
germansentiment
```

**Impact:** Team members get import errors for `pandas`, `ndjson`, and `nltk`.

### 4. No Python Version Documentation
No specification of which Python version to use.

**Impact:** Potential compatibility issues across different Python versions.

## Proposed Solutions

### Solution 1: Standardize Path Resolution
Each script should calculate `PROJECT_ROOT` based on its depth in the folder structure:

- Scripts in `1_Processing/1_Data_cleaning/`: Need **3** `.parent` calls
- Scripts in `1_Processing/2_Analysis/1_Caption_Sentiment/`: Need **4** `.parent` calls

**Files to fix:**
- [ ] `datacleaner_tiktok.py` line 37: Change to `.parent.parent.parent`
- [ ] `caption_sentiment_analysis.py` line 7: Change to `.parent.parent.parent.parent`

### Solution 2: Fix sentiment_analysis.py Path
Replace line 8 with:
```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
datafolder = PROJECT_ROOT / "1_Processing" / "2_Analysis" / "1_Caption_Sentiment" / "data"
```

### Solution 3: Complete requirements.txt
Update to include all dependencies:
```txt
germansentiment
pandas
ndjson
nltk
```

### Solution 4: Document Setup Process
Update `README.md` with:
- Required Python version (e.g., Python 3.9+)
- Virtual environment setup instructions
- Installation command: `pip install -r requirements.txt`
- Expected folder structure

## Action Items

- [ ] Fix path calculations in all scripts
- [ ] Update `requirements.txt` with complete dependencies
- [ ] Update `README.md` with setup instructions
- [ ] Test all scripts on at least 2 different machines
- [ ] Document expected data folder structure

## Discussion Points

1. Should we add a `setup.py` or `pyproject.toml` for better dependency management?
2. Should we include a `.python-version` file to specify Python version?
3. Should we add a script to verify the environment setup before running?

---

**Assign to:** [Team member names]
**Priority:** High
**Labels:** bug, setup, portability
