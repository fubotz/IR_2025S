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
IR_2025STest/
├── data/
│   ├── raw/                             
│   └── processed/
│       └── data/
│           ├── boolean_index.db          
│           ├── dataset.json              
│           ├── dataset.jsonl             
│           ├── dataset_preprocessed.json 
│           ├── eval_data.json            
│           ├── harry_dense_index.faiss 
│           └── harry_dense_index.pkl    
│
├── lecture/                         
│
├── pipeline/                           
│   ├── 01_extract_data.py
│   ├── 02_preprocess_data.py
│   ├── 03_build_boolean_index.py
│   ├── 04_query_bm25.py
│   ├── 05_load_index.py
│   ├── 06_dense_index.py
│   ├── 07_dense_query.py
│   ├── 08_hybrid.py
│   ├── 09_evaluate_pipeline.py
│   ├── denseindex.ipynb                  
│   └── QueryRetrievalfromFAISS.ipynb     
│
├── src/
│   └── IR_2025S/
│       ├── __init__.py
│       ├── dataset_utils.py             
│       ├── dense_retriever.py            
│       ├── hybrid_retriever.py          
│       ├── indexer.py                    
│       ├── load_books.py                 
│       ├── preprocessing.py              
│       └── retriever.py                  

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
   python pipeline/08_hybrid.py "harry potter godfather"
   python pipeline/09_evaluate_pipeline.py data/processed/eval_data.json --topk 5 (for alpha value)
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

🔎 Query: harry potter godfather  (Top 5 results)
🔍 Hybrid Query: harry potter godfather
⚖️ Alpha (dense weight): 0.5
📊 Top 5 results

1. Chapter 3_22
   🔗 Combined Score: 0.5844
   📚 BM25 Score: 4.1967
   🤖 Dense Score: 0.5911
   📖 BM25 Snippet: ‘Harry!’ Hermione was tugging at his sleeve, staring at her watch. ‘We’ve got exactly ten minutes to get back down to the hospital wing without anybody seeing us – before Dumbledore locks the door –’ ‘OK,’ said Harry, wrenching his gaze from the sky, ‘let’s go …’ They slipped through the doorway beh
   🧠 Dense Snippet: I, Sirius Black, Harry Potter’s godfather, hereby give him permission to visit Hogsmeade at weekends. ‘That’ll be good enough for Dumbledore!’ said Harry happily.

2. Chapter 7_25
   🔗 Combined Score: 0.5472
   📚 BM25 Score: 3.7416
   🤖 Dense Score: 0.6192
   📖 BM25 Snippet: Bill and Fleur's cottage stood alone on a cliff overlooking the sea, its walls embedded with shells and whitewashed. It was a lonely and beautiful place. Wherever Harry went inside the tiny cottage or its garden, he could hear the constant ebb and flow of the sea, like the breathing of some great, s
   🧠 Dense Snippet: “Godfather, Harry!” said Bill as they walked into the kitchen together, helping clear the table.

3. Chapter 3_10
   🔗 Combined Score: 0.5000
   📚 BM25 Score: 0.0000
   🤖 Dense Score: 0.6473
   📖 BM25 Snippet: 
   🧠 Dense Snippet: Then they named him godfather to Harry.

4. Chapter 5_38
   🔗 Combined Score: 0.2356
   📚 BM25 Score: 3.7052
   🤖 Dense Score: 0.0000
   📖 BM25 Snippet: HE WHO MUST NOT BE NAMED RETURNS. `In a brief statement on Friday night, Minister for Magic Cornelius Fudge confirmed that He Who Must Not Be Named has returned to this country and is once more active. “`It is with great regret that I must confirm that the wizard styling himself Lord - well, you kno
   🧠 Dense Snippet: 

5. Chapter 5_24
   🔗 Combined Score: 0.2092
   📚 BM25 Score: 3.6561
   🤖 Dense Score: 0.0000
   📖 BM25 Snippet: Kreacher, it transpired, had been lurking in the attic. Sirius said he had found him up there, covered in dust, no doubt looking for more relics of the Black family to hide in his cupboard. Though Sirius seemed satisfied with this story, it made Harry uneasy. Kreacher seemed to be in a better mood o
   🧠 Dense Snippet: 

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
