# Reproducibility Guide

This document details the technical setup, environment management, and system configuration used to reproduce experiments in the **Trauma-Informed, Empathy-Aware AI Framework**.

---

## 🖥️ Hardware Specifications

| Component | Specification |
|------------|----------------|
| **Device** | Mac Studio (2023) |
| **Processor** | Apple M2 Max (12-core CPU, 30-core GPU) |
| **Memory** | 32 GB Unified Memory |
| **Operating System** | macOS Tahoe 26.0.1 |
| **Display** | Apple Studio Display (27-inch, 5120×2880 Retina) |
| **Acceleration** | TensorFlow Metal GPU backend enabled |
| **Python Environments** | Dual environments: `.venv` (3.12) and `deepface_env` (3.10) |

This configuration ensures both symbolic verification and DeepFace inference can run independently and reproducibly.

---

## ⚙️ Environment Overview

The project uses **two isolated virtual environments** to maintain reproducibility and compatibility.

### 1. `.venv` (Python 3.12)
Used for all symbolic logic, Z3 verification, and data processing notebooks.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Key libraries:**
- `z3-solver`, `pandas`, `scikit-learn`, `numpy`
- `matplotlib`, `seaborn`, `jupyterlab`, `notebook`

> TensorFlow is not included here; it is only supported via the secondary environment.

---

### 2. `deepface_env` (Python 3.10)
Used for emotion recognition, DeepFace, Mediapipe, and OpenCV pipelines.

```bash
python3.10 -m venv deepface_env
source deepface_env/bin/activate
pip install -r requirements-extras.txt
brew install ffmpeg
```

**Key libraries:**
- `tensorflow-macos`, `tensorflow-metal`, `deepface`
- `mediapipe`, `opencv-python`, `opensmile`
- `ffmpeg-python`, `moviepy`, `sentence-transformers`

This environment enables the DeepFace + TensorFlow integrations powering emotion inference from CASME II and SMIC datasets.

---

## 📦 Dependency Management

- **requirements.txt** — for reproducible symbolic verification, fairness auditing, and modeling.  
- **requirements-extras.txt** — for GPU-accelerated visual and audio inference on Apple Silicon.

Check installations:

```bash
pip list | grep tensorflow
pip list | grep deepface
```

---

## 🧩 Reproduction Steps

1. **Dataset Setup**
   - Request and download DAIC-WOZ, CASME II, and SMIC datasets.  
   - Place files in the following local directory structure:
     ```
     data/raw/
     ```

2. **Environment Initialization**
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   deactivate

   source deepface_env/bin/activate
   pip install -r requirements-extras.txt
   deactivate
   ```

3. **Run Experiments**
   ```bash
   make run-all
   ```

4. **Verify Outputs**
   - Expected artifacts should include:
     - `data/processed/symbolic_rule_matrix.parquet`
     - `outputs/visuals/symbolic_rule_activation_matrix.png`
     - `data/processed/empathy_rule_fusion.parquet`

---

## 🔍 Spider Check Verification

Before pushing or archiving results, verify all critical artifacts:

```python
from pathlib import Path
expected = [
    "data/processed/symbolic_rule_matrix.parquet",
    "data/processed/symbolic_rule_matrix.csv",
    "outputs/visuals/symbolic_rule_activation_matrix.png",
    "data/processed/empathy_rule_fusion.parquet",
    "data/processed/fuzzy_thresholds.json"
]
for f in expected:
    print("✅" if Path(f).exists() else "⚠️", f)
```

---

## 🧠 Notes on Reproducibility

- **Hardware Acceleration:** TensorFlow Metal requires macOS 12+ and M1/M2 chips.  
- **Fixed Seeds:** Randomization is controlled in all notebooks for consistent results.  
- **Version Locking:** Dependency versions are pinned to ensure long-term reproducibility.  
- **Privacy Compliance:** Raw datasets remain local and are never pushed to GitHub. Only derived `.parquet`, `.csv`, and `.png` artifacts are versioned.

---

## 📜 Citation

If using or referencing this work, please cite:

> George, M.L. (2025). *Recognizing the Unseen: A Multimodal, Trauma-Informed AI Framework for Crisis Detection and Clinical Assessment.* Vanderbilt University.

---

**Maintained by:** Michelle (Elle) Lynn George  
📧 [Michelle.L.George@vanderbilt.edu](mailto:Michelle.L.George@vanderbilt.edu)  
🌐 [https://ellelynn.netlify.app](https://ellelynn.netlify.app)
