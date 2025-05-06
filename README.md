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
├── src/
│   └── IR_project/
│       ├── __init__.py
│       ├── main.py
│       ├── indexer.py
│       ├── retriever.py
│       ├── utils.py
│       └── ...
├── data/
│   └── harry_potter_books/   # cleaned raw texts or chunked documents
├── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Create and activate environment**:
   ```bash
   conda create -n IR_2025S python=3.10
   conda activate IR_2025S
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the project in editable mode** (optional):
   ```bash
   pip install -e .
   ```

---

## 🚀 How to Use

You can run a basic search query from the command line:

```bash
python -m IR_project.main --query "quidditch match"
```

Example output:

```
Top 3 matching passages:
1. "Harry caught the Snitch after an intense Quidditch match..."
2. "The crowd roared as Gryffindor secured the win..."
3. ...
```

---

## 📚 Data Source

This project uses **cleaned versions** of the 7 Harry Potter books for educational purposes only.  
The original texts are available from 
[Kaggle](https://www.kaggle.com/datasets/shubhammaindola/harry-potter-books) and have been processed 
to remove noise and irrelevant content.
---

## 📌 Goals of the Project

- Explore core IR concepts using a fun and meaningful dataset
- Build a modular system that supports experimentation (e.g. chunk size, ranking models)
- Lay the groundwork for extending into Retrieval-Augmented Generation (RAG) chatbot systems

---

## ✍️ Authors

Angelina Radovanov & Fabian Schambeck, IR_2025S — Joint Master "Multilingual Technologies"
