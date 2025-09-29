# Recognizing the Unseen: A Multimodal, Trauma-Informed AI Framework for Crisis Detection and Clinical Assessment

> Graduate independent study exploring interpretable AI for trauma-aware emotional state recognition and clinical augmentation.

---

## 📌 Project Summary

This research explores a trauma-informed, multimodal AI framework that detects affective patterns such as emotional shutdown, dissociation, or depressive flat affect in high-stakes environments. The goal is to support-not replace-human decision-making in clinical and crisis response contexts.

This first phase leverages the **DAIC-WOZ dataset** to prototype an emotionally-aware, ethically guided ML system with a strong emphasis on transparency and real-world clinical relevance.

---

## 🧠 Why It Matters

Traditional AI systems often misinterpret trauma responses-mistaking withdrawal, flat affect, or dissociation for resistance or noncompliance. This work contributes to the growing movement toward **compassion-centered**, **bias-mitigated**, and **interpretable** machine learning solutions.

---

## 📚 Dataset Used

| Dataset     | Source                     | Status              | Notes                                                                 |
|-------------|----------------------------|---------------------|-----------------------------------------------------------------------|
| DAIC-WOZ    | USC-ICT                    | ✅ Approved/downloaded | Depression & anxiety interviews with rich multimodal cues             |
| CASME II    | Chinese Academy of Sciences | ✅ Approved          | Micro-expressions; access granted upon request                        |
| SMIC        | University of Oulu         | Pending            | Micro-expression dataset; license agreement required before download  |

> ⚠️ **Data Access Notice:**  
> These datasets are not publicly distributable.  
> To reproduce experiments, researchers must **request access directly from the dataset providers** and comply with their usage agreements.

---


## ⚡ Getting Started

Clone the repo and create a virtual environment (recommended: `.venv`):

```bash
git clone <your-repo-url>
cd trauma-informed-ai-framework
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

- **Base only** (minimal, reproducible env):
  ```bash
  make dev
  ```

- **Extras only** (embeddings, audio, widgets, etc.):
  ```bash
  make extras
  ```

- **All dependencies** (base + extras in one go):
  ```bash
  make all-deps
  ```

### Workflow Commands

- **Run tests** (validate pipeline with pytest):
  ```bash
  make test
  ```

- **Clean caches** (remove Python/pytest caches):
  ```bash
  make clean
  ```

- **Launch JupyterLab** for exploration:
  ```bash
  make notebook
  ```

- **Run a single notebook** (machine-check reproducibility):
  ```bash
  make run-nb NB=notebooks/01_import_clean_eda.ipynb
  ```

- **Run all notebooks** (end-to-end reproducibility check):
  ```bash
  make run-all
  ```

- **Strip notebook outputs** (privacy + clean diffs):
  ```bash
  make strip
  ```

- **Freeze environment** (save exact versions to lock file):
  ```bash
  make freeze
  ```

---

## 🧼 Reproducibility & Hygiene

This project follows strict hygiene practices to ensure clean, reproducible notebooks and code.  
- Non-ASCII characters are stripped or normalized.  
- Notebooks are checked and cleaned automatically.  
- All steps are automated with `make` targets.

For full reproducibility and hygiene practices, see [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

---

## 🛠️ Tools & Libraries

- Python 3.12
- OpenFace, OpenSMILE for facial and audio features
- HuggingFace Transformers (BERT / DistilBERT)
- SHAP or LIME for explainability
- Jupyter Notebook / JupyterLab
- `.venv` (virtual environment)

---

## 🧪 Technical Focus

- **Modalities**: Facial cues, vocal tone, and linguistic sentiment
- **Modeling**: Multimodal fusion + affective state classification
- **Explainability**: SHAP/LIME outputs with clinical interpretability
- **Ethics**: Transparent bias handling + human-centered model framing

---

## 📦 Project Structure

- trauma-informed-ai-framework/
  - data/ - Preprocessed DAIC-WOZ data
  - notebooks/ - Exploratory modeling & EDA
  - models/ - Saved model artifacts
  - utils/ - Custom feature extraction scripts
  - README.md - You're here
  - article_draft.md - Research article draft for publication

---

---

## 🌱 Elle-isms in This Project

This project is technical at its core, but it also carries my personality.  
I believe data science should be **human, memorable, and compassionate** - not just rows and columns.

One Elle-ism you'll see throughout the notebooks is the **"Spider Check" 🕷️**.

### What's a Spider Check?
When you're camping or staying in a cabin, before you crawl into bed you pull back the covers to make sure there are no critters - or spiders - hiding there. That little ritual gives you peace of mind before you rest.

In my workflow, a *Spider Check* is the same idea:  
- A quick `head(2)` peek or shape check  
- Confirming the data looks as expected  
- Making sure no hidden "critters" (errors, empty frames, wrong encodings) are lurking  

It's a peace-of-mind step before building further.  
Because good data science isn't just about seeing what's obvious -  
> **it's about seeing the unseen.**

👉 You'll see Spider Checks sprinkled across the notebooks (Audio, Text, TF-IDF, PHQ-8, and Multimodal Merge).  
Each one is a quick peace-of-mind peek tailored to its modality.

---


## 🔭 Upcoming Milestones

- [ ] Complete full EDA on DAIC-WOZ  
- [ ] Prototype initial multimodal classification model  
- [ ] Integrate SHAP explainability outputs  
- [ ] Draft publication-ready article  
- [ ] Prepare visuals and dashboard for final submission/presentation  

---

## 🧾 License

This work is covered under the [MIT License](https://opensource.org/licenses/MIT).

---

For questions, collaborations, or media inquiries, contact:  
**Michelle (Elle) Lynn George**  
[Michelle.L.George@vanderbilt.edu](mailto:Michelle.L.George@vanderbilt.edu)  
[https://ellelynn.netlify.app](https://ellelynn.netlify.app)

---

> ✨ This project is part of an independent study at Vanderbilt University, with the goal of contributing a publishable, reproducible, and human-centered AI model to support trauma-informed care.
