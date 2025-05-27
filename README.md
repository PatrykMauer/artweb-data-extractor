# 🖼️ Dataset Extractor for AI-Powered Art Discovery

## Overview
This repository contains a **lightweight webcrawler and metadata extractor** built to collect structured data for training a machine learning model. The end goal is to power a separate, AI-enhanced smart webcrawler that can autonomously discover websites containing artworks.

This project **only covers dataset creation**. The actual AI crawler using the trained model will be part of a future, separate repository.

---

## 🧱 Project Structure

### Phase 1: Lightweight Extractor (Baseline)

#### 🎯 Goal:
Collect structured data from 5000 websites for model training.

#### ✅ Features:
- Extracts metadata from given URLs
- Gathers key features for art detection
- Stores data in CSV

#### 🔍 Data Columns:
| Column | Description |
|--------|-------------|
| `url` | Page URL |
| `page_title` | Page <title> tag |
| `meta_description` | Meta description tag |
| `meta_keywords` | Meta keywords tag |
| `image_count` | Number of <img> tags |
| `alt_tags` | Combined alt text of all images |
| `link_texts` | Text content from <a> tags |
| `has_gallery` | Boolean if gallery/carousel terms found |
| `artist_names` | Detected artist names (simple list) |
| `context_keywords` | Detected art-related terms |
| `contains_artwork` | Manual label for classifier |

#### 📦 Output:
- `art_dataset.csv` containing 5000 rows

---

### Phase 2: Manual Labeling

Label `contains_artwork` column for supervised model training.
- True = page contains genuine artwork
- False = page is not art-related

---

### Phase 3: AI Model Training

#### 🎯 Goal:
Train a binary classification model to predict presence of artwork.

#### 🧠 Model:
- Random Forest or SVM
- Inputs: All columns from Phase 1
- Output: 0 = No Artwork, 1 = Contains Artwork

#### 📊 Target Accuracy:
≥ 80% on a 100-row test set

---

### Phase 4: NLP-Enriched Version (Optional Enhancement)

#### 🎯 Goal:
Improve precision by using NLP tools like spaCy or transformers.

#### 🔬 Enrichment Targets:
| Column | NLP Enhancement |
|--------|-----------------|
| `artist_names` | Named Entity Recognition (NER) for unknown artist detection |
| `context_keywords` | Context-aware phrase extraction, dependency parsing |
| `meta_description`, `page_title`, `link_texts` | Art-related classification or semantic similarity |
| `art_score` (new) | Computed signal score based on all NLP signals |

#### 🧰 Tools:
- `spaCy` for NER and POS tagging
- `transformers` for text similarity or classification
- Optional: CLIP for image analysis

---

## 🚀 Getting Started
1. Clone this repo
2. Run the lightweight extractor on seed URLs
3. Manually label `contains_artwork`
4. Train classifier model
5. Optionally enrich dataset with NLP
6. Use the dataset in a smart crawler (separate project)

---

## 📁 Folder Structure

art-dataset-extractor/
├── data/
│ └── art_dataset.csv
├── scripts/
│ ├── extract_lightweight.py
│ ├── enrich_with_nlp.py
│ └── train_classifier.py
├── models/
│ └── art_classifier.pkl
└── README.md


## 🧩 Future Integration
The output of this project will be used in a separate repository:
- **Smart Webcrawler** using the trained model
- Real-time classification of crawled pages
- Ongoing data enrichment and retraining

---

## 🤝 License
MIT License — free to use, modify, and share.