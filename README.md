# Recognizing the Unseen: A Multimodal, Trauma-Informed AI Framework for Crisis Detection and Clinical Assessment

> Graduate independent study exploring interpretable AI for trauma-aware emotional-state recognition and clinical augmentation.

---

## 📘 Project Summary

This research explores a **trauma-informed, multimodal AI framework** that detects affective patterns such as emotional shutdown, dissociation, or depressive flat affect in high-stakes environments.  
The goal is to **support — not replace — human decision-making** in clinical and crisis-response contexts.

This first phase leverages the **DAIC-WOZ**, **CASME II**, and **SMIC** datasets to prototype an emotionally-aware, ethically-guided ML system with a strong emphasis on **transparency**, **interpretability**, and **real-world safety**.

---

## 💡 Why It Matters

Traditional AI systems often misinterpret trauma responses — mistaking withdrawal, flat affect, or dissociation for resistance or non-compliance.  
This work contributes to the growing movement toward **compassion-centered**, **bias-mitigated**, and **interpretable** machine-learning solutions.

> “Where symbolic logic fails to decide, human context must remain present.”  
> — *M.L. George*, [*The Haunting Problem*](docs/theory_haunting_problem.md)

---

## 🔐 Practitioner Disclosure

While I am not a licensed psychologist or clinical behaviorist, I bring a unique qualification to trauma-aware systems engineering through extensive experience in real-world behavioral observation.

In past roles as a Federal Air Marshal, Flight Attendant, and First Responder, I was trained to detect behavioral anomalies in high-pressure environments. I observed patterns of dissociation, emotional masking, and shutdown long before I had a vocabulary for them — and I now translate those lived patterns into computational logic.

This framework is not built on speculation; it is grounded in **field-based observation and real-time safety decisions**.  
It sits at the intersection of operational vigilance and symbolic verification — where lived experience meets logic models designed to do no harm.

---

## 🔒 Data Access & Privacy

No raw datasets are stored or shared in this repository.  
All sensitive material (**DAIC-WOZ**, **CASME II**, **SMIC**) remains local under `data/raw/` on the author’s secured device.

Only **derived metadata** (e.g., `.csv`, `.parquet`, `.json`, and model outputs) are versioned for reproducibility.

To reproduce experiments:
1. Request dataset access directly from the original providers (see [REPRODUCIBILITY.md](REPRODUCIBILITY.md)).
2. Place the approved datasets locally under:
   ```
   data/raw/
   ```
3. Run notebooks as described below; processed outputs will generate under:
   ```
   data/processed/   and   outputs/
   ```

> ⚠️  None of the raw data are pushed to GitHub. All file paths remain relative and local-only.

---

## 📚 Datasets Used

| Dataset | Full Name | Source | Status | Notes |
|----------|------------|---------|---------|--------|
| **DAIC-WOZ** | Distress Analysis Interview Corpus – Wizard of Oz | USC-ICT | ✅ Approved / Downloaded | Clinical interviews (audio, video, transcripts, PHQ-8 labels) |
| **CASME II** | Chinese Academy of Sciences Micro-Expression II | Chinese Academy of Sciences | ✅ Approved / Downloaded | High-frame-rate facial videos with emotion labels and Action Units |
| **SMIC** | Spontaneous Micro-Expression Corpus | University of Oulu | ✅ Approved / Downloaded | Spontaneous micro-expressions in VIS, NIR, and HS formats |

> ⚠️  Datasets are not publicly distributable.  
> Researchers must **request access directly** and comply with all license agreements.

---

## 🖥️ Environment Setup — macOS (Apple Silicon)

This framework was developed on a **Mac Studio (2023)** running **macOS Tahoe 26.0.1**, equipped with an **Apple M2 Max chip (12-core CPU / 30-core GPU)** and **32 GB unified memory**, paired with a **27-inch Apple Studio Display (5120×2880)**.

This configuration supports TensorFlow Metal acceleration and provides stable runtime for DeepFace, Z3, and Jupyter-based multimodal experiments.

### Base Environment (Python 3.12)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### DeepFace Environment (Python 3.10)

Used for emotion-inference and facial modeling tasks requiring TensorFlow 2.13 compatibility.

```bash
python3.10 -m venv deepface_env
source deepface_env/bin/activate
pip install tensorflow-macos tensorflow-metal deepface opencv-python pandas tf-keras
brew install ffmpeg
```

| Package | Purpose |
|----------|----------|
| `tensorflow-macos` | TensorFlow core optimized for Apple Silicon |
| `tensorflow-metal` | GPU acceleration via Metal API |
| `deepface` | Emotion detection / facial-affect analysis |
| `opencv-python` | Frame extraction / video processing |
| `pandas` | Structured-data handling / saving results |
| `tf-keras` | Compatibility layer for TensorFlow 2.13 |
| `ffmpeg` | Frame extraction utility for SMIC videos |

Each environment is isolated and activated explicitly before notebook execution for full reproducibility.

---

## ⚡ Getting Started

Clone the repo and initialize your environment:

```bash
git clone <repo-url>
cd trauma-informed-ai-framework
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
make all-deps
```

Run a single notebook:
```bash
make run-nb NB=notebooks/05_model_calibration_verification.ipynb
```

Run all notebooks:
```bash
make run-all
```

---

## 🧩 Notebook Overview

| Notebook | Dataset(s) | Focus | Outputs |
|-----------|-------------|--------|----------|
| **01 – Import + EDA** | DAIC-WOZ | Cleaning, PHQ-8 prep | `data/processed/` |
| **02 – Baselines** | DAIC-WOZ | Logistic Regression and Random Forest baselines | `outputs/models/` |
| **03 – Feature Engineering** | DAIC-WOZ | Audio, text, and video feature fusion | `data/fused/` |
| **04 – Model Training + Fairness** | DAIC-WOZ | Calibrated classification + fairness audit | `outputs/metrics/` |
| **05 – Model Calibration + Safety Verification** | DAIC-WOZ | ✅ Z3 symbolic empathy rules + calibration audit | `outputs/checks/`, `outputs/visuals/` |
| **06 – Micro-Expression Fusion** | SMIC + CASME II | AU mapping and dataset fusion | `outputs/checks/` |
| **07 – Micro-Expression Modeling** | SMIC + CASME II | Classifier benchmarks (LogReg, RF, KNN, SVC, MLP) | `outputs/visuals/` |
| **08 – Symbolic Facial Audit** | SMIC + CASME II | Z3-based symbolic facial-rule application | `data/processed/`, `outputs/visuals/` |
| **09 – Fusion Modeling + Fuzzy-Symbolic Integration** | All datasets | Hybrid fuzzy calibration + symbolic empathy weighting | `data/processed/`, `outputs/visuals/` |
| **10 – Symbolic Verification (Core)** | Derived data | ✅ Verified all 25 empathy rules (SAT) + final spider check | `data/processed/`, `outputs/visuals/` |
| **11 – Edge-Case Verification Suite** | Derived data | 🧩 Stress-tests symbolic empathy rules under contradiction, boundary, and signal-loss conditions to confirm logical stability | `outputs/edge_cases/` |
---
## 📦 Key Artifacts & Outputs
Each notebook builds on the previous stage, progressing from preprocessing
and modeling to symbolic reasoning, verification, and finally edge-case testing.

| Artifact | Type | Path | Description |
|-----------|------|------|--------------|
| **Symbolic Rule Matrix (25 Rules)** | `.parquet`, `.csv` | `data/processed/symbolic_rule_matrix.*` | ✅ Final verified empathy rule set from Notebook 10 — includes all 25 trauma-informed symbolic logic rules (Reflective → Haunting Zone) validated as satisfiable (SAT) under the Z3 solver. |
| **Symbolic Rule Activation Matrix** | `.png` | `outputs/visuals/symbolic_rule_activation_matrix.png` | Visual summary of rule-activation states. Green = Satisfied (SAT), Yellow = Unknown, Red = Unsatisfied (UNSAT). Confirms logical consistency and ethical stability of the empathy model. |
| **Empathy Fusion Data** | `.parquet` | `data/processed/empathy_rule_fusion.parquet` | Intermediate fused output combining confidence, emotion category, and fuzzy-membership weights for symbolic reasoning (source: Notebook 09 fusion + Notebook 08 audit). |
| **Fuzzy Threshold Constants** | `.json` | `data/processed/fuzzy_thresholds.json` | Hybrid quantile + fixed-range cutoffs (Low ≤ 0.60; High > 0.83) used across Notebooks 09–10 to maintain consistent symbolic calibration. |
| **Fuzzy Confidence Visualization** | `.png` | `outputs/visuals/fuzzy_confidence_distribution.png` | Histogram showing normalized confidence distribution and uncertainty zones (Low, Medium, High) — foundational to symbolic-empathy scaling. |
| **Fuzzy–Emotion Heatmap** | `.png` | `outputs/visuals/fuzzy_emotion_heatmap.png` | Cross-tab visualization of emotion class × fuzzy-confidence level. Demonstrates adaptive hesitation for ambiguous emotions (neutral / surprise). |
| **Empathy Signal Distribution Plot** | `.png` | `outputs/visuals/empathy_signal_distribution.png` | Histogram + boxplot showing reflective, cautious, and assertive reasoning tiers derived from EmpathySignal. |
| **Empathy Rule Fusion (Z3 Ready)** | `.parquet` | `data/processed/fuzzy_symbolic_ready.parquet` | Cleaned symbolic-input table aligned for Z3 integration; includes ConfidenceNorm, EmpathySignal, and rule-weight coefficients. |
| **Microexpression Feature Alignment** | `.parquet` | `data/processed/fused_visual_emotions_fuzzy.parquet` | Final merged emotion dataset from SMIC + CASME II with fuzzy-calibrated confidence; input to symbolic fusion in Notebook 09. |
| **Final Verification Notebook** | `.ipynb` | `notebooks/10_symbolic_verification.ipynb` | Complete end-to-end Z3 verification of all symbolic empathy rules — proving coherence, ethical reasoning, and absence of logical contradictions. |
| **Edge-Case Verification Suite** | `.ipynb`, `.csv`, `.png` | `notebooks/11_edge_case_suite.ipynb`, `outputs/edge_cases/` | ✅ New Notebook 11 — stress-tests symbolic empathy rules under boundary, contradiction, and signal-loss conditions. Includes `edge_case_results.csv` and `verification_surface_final.png`, confirming logical stability across all fuzzy-tier thresholds. |
| **Calibrated Model Artifact** | `.joblib` | `outputs/models/final_model_linsvc.joblib` | Final CalibratedClassifierCV model with sigmoid scaling for PHQ-8 depression classification (DAIC-WOZ baseline, Notebook 04). |
| **Microexpression Confusion Matrices** | `.png` | `outputs/visuals/07_confmat_*.png` | Class-level visualizations of model confusion (happy, sad, angry, neutral, surprise) used to evaluate SMIC + CASME II predictive stability. |

---

🧭 **Interpretation Notes**
- The **EmpathySignal** (Notebook 09) and **SymbolicRuleMatrix** (Notebook 10) together form the first *formally verified emotional reasoning core* — a quantifiable proof that empathy can be represented as a consistent logical construct.
- All verification assets are self-contained and reproducible; no external data dependencies are committed.
- Each artifact contributes to a multi-layer verification chain: *data → fuzzification → fusion → rule evaluation → symbolic proof*.

---
## 🧠 Theory Integration — *The Haunting Problem*

**The Haunting Problem** introduces a new category of verification risk:  
when silence, masking, or repression produce *false confidence* in AI safety checks.

- Challenges assumptions of observability in model verification  
- Frames **absence as evidence** within trauma-aware AI  
- Informs the symbolic empathy rules used across Notebooks 05–10  

📄 Read the formal definition:  
[`docs/theory_haunting_problem.md`](docs/theory_haunting_problem.md)

---

## 🕷️ The Spider Check (An Elle-ism)

When you’re camping, you pull back the covers before crawling into bed to check for spiders — that peace of mind before resting.  
In data science, my **Spider Check** is the same ritual: a quick look under the hood to make sure nothing’s hiding.

- A `head(2)` peek at the data  
- Shape validation (`df.shape`)  
- Sanity checks for encoding, empties, or anomalies  

Because good science isn’t only about what’s visible —  
> **it’s about seeing the unseen.**

🕷️ Spider Checks are scattered throughout the notebooks — they’re part of my workflow for mindfulness and reproducibility.

---

## 🧾 Academic Integration

| Course | Deliverable |
|---------|--------------|
| **CS 6315 – Automated Verification** | Formal Z3 symbolic empathy verification engine |
| **CS 8390 – Independent Study (Trauma-Informed AI)** | Full multimodal pipeline + publication-ready theory (*The Haunting Problem*) |

Both tracks share this single verified, reproducible codebase.

---

## 🧠 Future Work

- [ ] Expand emotion taxonomy using clinical psychology sources  
- [ ] Integrate physiological data streams (EEG/EDA)  
- [ ] Draft journal article on symbolic empathy verification  
- [ ] Extend symbolic reasoning to multimodal fusion dashboard  

---

## 📜 License

© 2025 Michelle Lynn George  

**Paper & documentation** — licensed under a  
[Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)  

**Source code** — licensed under the  
[MIT License](LICENSE)

You are free to share and adapt the written material for non-commercial purposes,
provided that proper credit is given, a link to this license is included,
and any changes made are indicated.

---

### 📄 Citation

George, M. L. (2025). *The Haunting Problem: Recognizing Semantic Absence in Trauma-Aware AI (v1.0).*  
Zenodo. [https://doi.org/10.5281/zenodo.17578153](https://doi.org/10.5281/zenodo.17578153)

---

## 🤝 Collaboration & Contact

For collaboration inquiries, research discussions, or dataset access verification, please reach out via:

**Michelle (Elle) Lynn George**  
**Vanderbilt University — School of Engineering**  
📧 [Michelle.L.George@vanderbilt.edu](mailto:Michelle.L.George@vanderbilt.edu)  
📧 [Elle.Lynn.Research@icloud.com](mailto:Elle.Lynn.Research@icloud.com)  
🌐 [https://ellelynn.netlify.app](https://ellelynn.netlify.app)  

> *Open to interdisciplinary collaborations in Responsible AI, trauma-aware systems, and symbolic verification ethics.*
---

> ✨ *For the unseen. For those who felt invisible. For the ones who whispered their truth and still weren't heard — until now.*
