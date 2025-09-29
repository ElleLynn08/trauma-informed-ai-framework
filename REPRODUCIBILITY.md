# Reproducibility & Hygiene Guide

This project is designed for **reproducible research** and strict hygiene.  
Every notebook, dataset, and environment step is documented here so that others (and my future self!) can reproduce the results exactly.

---

## 📚 Dataset Access

⚠️ **Important Disclaimer:**  
All datasets used in this project are available **for research and non-commercial use only**.  
You must request access directly from the dataset providers and agree to their license terms and consent forms.  
These datasets cannot be redistributed in this repository.

- **DAIC-WOZ** (Distress Analysis Interview Corpus – Wizard of Oz)  
  - Request form: [USC ICT](https://dcapswoz.ict.usc.edu/)  
  - Contains audio, video, and transcripts of clinical interviews.  

- **CASME II** (Chinese Academy of Sciences Micro-Expressions II)  
  - Request form: [CASME II Dataset](http://casme.psych.ac.cn/casme/e2)  
  - Contains high-resolution micro-expression sequences.  

- **SMIC** (Spontaneous Micro-expression Corpus, University of Oulu)  
  - Contact: [University of Oulu – Center for Machine Vision and Signal Analysis](https://www.oulu.fi/en/university/faculties-and-units/faculty-information-technology-and-electrical-engineering/center-for-machine-vision-and-signal-analysis)  
  - Access requires contacting the research group and signing agreements.  

👉 Once you obtain the datasets, place them under:
```
data/raw/
```

---

## 🖥️ Environment Setup

1. Clone the repo:
   ```bash
   git clone <your-repo-url>
   cd trauma_informed_ai_framework
   ```

2. Create a virtual environment (recommended `.venv`):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   make dev        # base requirements
   make extras     # optional extras (audio/embeddings/widgets)
   make all-deps   # both in one go
   ```

4. Verify environment:
   ```bash
   make env
   ```
   This prints Python version, OS info, and confirms required packages are available.

---

## 🧼 Hygiene Tools

This repo uses automated tools to keep notebooks and code clean, consistent, and reproducible.

### 1. ASCII Spider Check 🕷️

Scans code and docs for hidden non-ASCII characters (curly quotes, em dashes, ellipses, etc.).

This ties into my **Spider Check philosophy**:  
a Spider Check is my shorthand for a quick peace-of-mind sanity step — like pulling back the covers in a cabin to make sure no critters are hiding before you rest.  
In this project, it means confirming files look as expected and are free of hidden characters before building further.  

It’s light, a little quirky, and part of my personality woven into the workflow — because good data science isn’t just about what’s obvious, it’s about *seeing the unseen*.

```bash
make ascii-check
```

Alias:
```bash
make spider-check
```

Output should be:
```
✅ No non-ASCII issues detected (aside from allowed symbols).
```

> Symbols like ✅, 🕷️, and README emojis are whitelisted intentionally.

---

### 2. Notebook Cleaner
Notebooks often pick up curly quotes, em dashes, or ellipses when you paste text.  
To normalize them:

- **Fix in place:**
  ```bash
  make nb-fix
  ```

- **Check only (dry run):**
  ```bash
  make nb-check
  ```

Expected clean output:
```
all notebooks clean.
```

---

### 3. Full Sanity Sweep
Runs environment check, ASCII spider check, and notebook check in one step:

```bash
make sanity
```

Expected clean run:
```
✅ No non-ASCII issues detected (aside from allowed symbols).
all notebooks clean.
```

---

## 📓 Reproducing Experiments

1. **Prepare datasets**  
   - Ensure you’ve downloaded and placed them in `data/raw/` as described above.  
   - Run any preprocessing notebooks as directed (these will generate files in `data/processed/`).

2. **Run one notebook at a time**  
   ```bash
   make run-nb NB=notebooks/01_import_clean_eda.ipynb
   ```

3. **Run all notebooks sequentially**  
   ```bash
   make run-all
   ```

   Logs are saved to:
   ```
   logs/notebook_runs/
   ```

---

## ✅ Pre-Push Checklist

Before committing or pushing, always run:

```bash
make nb-fix       # normalize notebooks
make ascii-check  # ensure code/docs clean
make sanity       # full hygiene sweep
make run-all      # verify reproducibility
```

Commit only when everything passes.

---

## 🔍 Notes & Troubleshooting

- **Smart punctuation** sneaks in when copying from PDFs, Word, or websites.  
  Solution: `make nb-fix`.

- **ASCII Spider Check** flags dataset names correctly once normalized.  
  Emojis are whitelisted — no action needed unless you add new ones.

- **Dataset access** must be obtained manually; links and contacts are provided above.  
  Do **not** push raw or processed dataset files into the repo.

---

For quick start, see [README.md](README.md).  
For full hygiene practices, use this document.

---
