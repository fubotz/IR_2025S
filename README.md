# Harry Potter Information Retrieval System ⚯ ͛

This project implements an Information Retrieval system based on the **Harry Potter** book series (Books 1–7). 
It is designed as part of the *VU Information Extraction and Retrieval for Multilingual Natural Language Data (FHCW) 
2025S* course project.

---

## 🔍 Features

- Indexing of all 7 Harry Potter books (cleaned, structured)
- Text preprocessing (tokenization, normalization, etc.)
- Query-based document/passage retrieval
- Support for different retrieval models (e.g. BM25, dense embeddings)
- Integration with a Retrieval-Augmented Generation (RAG) chatbot

---

## 🗂️ Project Structure

```
IR_2025S/
├── data/
│   ├── processed/
│   │   ├── boolean_index.db
│   │   ├── dataset.json
│   │   ├── dataset.jsonl
│   │   └── dataset_preprocessed.json
│   └── raw/
├── lecture/
├── pipeline/
│   ├── 01_extract_data.py
│   ├── 02_preprocess_data.py
│   ├── 03_build_boolean_index.py
│   └── 04_query_bm25.py
├── src/
│   └── IR_2025S/
│       ├── __init__.py
│       ├── dataset_utils.py
│       ├── indexer.py
│       ├── load_books.py
│       ├── preprocessing.py
│       └── retriever.py
├── tests/
│   └── main.py
├── .gitignore
├── environment.yml
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Create and activate a conda environment from .yml file**:
   ```bash
   conda env create -f environment.yml
   conda activate IR_2025S
   ```

2. **Download the required spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Install the project in editable mode** (optional):
   ```bash
   pip install -e .
   ```
---

## 🚀 How to Use

You can run a basic search query from the command line:

   ```bash
   python pipeline/04_query_bm25.py "dobby sock" --topk 3
   ```

Example output:

```
🔎 Query: dobby sock  (Top 3 results)

1. 📘 HP 2 - Harry Potter and The Chamber of Secrets — DOBBY’S REWARD (2_18)
   For a moment there was silence as Harry, Ron, Ginny, and Lockhart stood in the doorway,...
2. 📘 HP 4 - Harry Potter and The Goblet of Fire — THE HOUSE-ELF LIBERATION FRONT (4_21)
   Harry, Ron, and Hermione went up to the Owlery that evening to find Pigwidgeon,...
3. 📘 HP 4 - Harry Potter and The Goblet of Fire — THE YULE BALL (4_23)
   Despite the very heavy load of homework that the fourth years had been given...
```

---

## 📚 Data Source

- This project uses **cleaned versions** of the 7 Harry Potter books for educational purposes only.  
- The original texts are available from [Kaggle](https://www.kaggle.com/datasets/shubhammaindola/harry-potter-books) 
and have been processed to remove noise and irrelevant content.
---

## 📌 Goals of the Project

- Explore core IR concepts using a fun and meaningful dataset
- Build a modular system that supports experimentation (e.g. chunk size, ranking models)
- Lay the groundwork for extending into Retrieval-Augmented Generation (RAG) chatbot systems

---

## ✍️ Authors

Angelina Radovanov & Fabian Schambeck, IR_2025S — Joint Master "Multilingual Technologies"
