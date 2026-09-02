# 📚 PDF RAG Study

A simple **Retrieval-Augmented Generation (RAG)** system that allows users to ask questions about PDF documents and receive answers based only on the information retrieved from those documents.

This project was built as a learning project to understand the basic workflow of a RAG application using **Python, ChromaDB, embeddings, and Groq LLMs**.

---

## 🚀 What is RAG?

**RAG (Retrieval-Augmented Generation)** combines document retrieval with a Large Language Model (LLM).

Instead of asking the LLM to answer completely from its own knowledge, the system:

```text
PDF
 ↓
Extract Text
 ↓
Split into Chunks
 ↓
Generate Embeddings
 ↓
Store in ChromaDB
 ↓
User Question
 ↓
Similarity Search
 ↓
Relevant Context
 ↓
Groq LLM
 ↓
Answer
```

This helps the model answer questions based on the provided PDF content.

---

## 🛠️ Technologies Used

* **Python 3.12**
* **ChromaDB** — vector database for storing document embeddings
* **Sentence Transformers** — generates text embeddings
* **Groq API** — provides the LLM for answer generation
* **PyMuPDF** — extracts text from PDF files
* **python-dotenv** — manages environment variables

---

## 📁 Project Structure

```text
pdf-rag-study/
│
├── data/
│   └── Week3_Bash_Scripting_Organized.pdf
│
├── src/
│   ├── read_pdf.py
│   ├── chunk_pdf.py
│   ├── store_embeddings.py
│   ├── search_pdf.py
│   └── rag_answer.py
│
├── .gitignore
└── README.md
```

### File Description

| File                  | Purpose                                                    |
| --------------------- | ---------------------------------------------------------- |
| `read_pdf.py`         | Extracts text from the PDF                                 |
| `chunk_pdf.py`        | Splits extracted text into smaller chunks                  |
| `store_embeddings.py` | Generates embeddings and stores them in ChromaDB           |
| `search_pdf.py`       | Searches the vector database for relevant chunks           |
| `rag_answer.py`       | Sends retrieved context to the LLM and generates an answer |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Hawk-Out/pdf-rag-study.git
cd pdf-rag-study
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure the Groq API Key

The project uses the Groq API to generate answers.

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_api_key_here
```

**Never commit your actual API key to GitHub.**

The `.env` file is already included in `.gitignore`.

---

## ▶️ Running the Project

First, make sure your virtual environment is active:

```bash
source .venv/bin/activate
```

### Step 1 — Process the PDF

Run:

```bash
python src/read_pdf.py
```

### Step 2 — Create document chunks

```bash
python src/chunk_pdf.py
```

### Step 3 — Store embeddings

```bash
python src/store_embeddings.py
```

This creates the local ChromaDB vector database.

### Step 4 — Search the PDF

```bash
python src/search_pdf.py
```

### Step 5 — Ask questions using RAG

```bash
python src/rag_answer.py
```

You can then ask questions such as:

```text
What is a shell script?
```

or:

```text
What is the difference between a shell and a shell script?
```

The system retrieves relevant information from the PDF and uses that context to generate the answer.

---

## 🧠 How the RAG Pipeline Works

### 1. PDF Text Extraction

The PDF is processed and its text is extracted using PyMuPDF.

### 2. Chunking

The extracted text is divided into smaller pieces called **chunks**.

Chunking makes it easier to search for specific information.

### 3. Embeddings

Each chunk is converted into a numerical vector called an **embedding**.

Similar pieces of text have similar vector representations.

### 4. Vector Database

The embeddings are stored in **ChromaDB**.

This allows the system to efficiently search for relevant information.

### 5. Retrieval

When the user asks a question, the question is also converted into an embedding.

The system searches ChromaDB for the most similar document chunks.

### 6. Generation

The retrieved chunks are given to the Groq LLM as context.

The LLM then generates the final answer based on that context.

---

## 💬 Example

### Question

```text
What is a shell script?
```

### Retrieved Context

The system searches the PDF and retrieves the most relevant sections.

### Generated Answer

The LLM uses those sections to generate a natural-language answer.

The current implementation can also be instructed to answer in **Banglish** (Bengali written using English/Roman characters).

---

## 🔐 Security

API keys and local generated files should not be committed to GitHub.

The following are excluded through `.gitignore`:

```text
.venv/
__pycache__/
chroma_db/
.env
```

If an API key is accidentally exposed, revoke it immediately and generate a new one.

---

## 🎯 Learning Goals

This project was created to understand:

* PDF text extraction
* Text chunking
* Embeddings
* Vector databases
* Semantic search
* Retrieval-Augmented Generation
* Prompt engineering
* LLM integration
* Environment variables
* Git and GitHub

---

## 🔮 Future Improvements

Possible improvements include:

* [ ] Support multiple PDFs
* [ ] Add a web interface
* [ ] Add conversation memory
* [ ] Improve chunking strategy
* [ ] Add metadata filtering
* [ ] Add citation support
* [ ] Add streaming responses
* [ ] Improve Banglish generation
* [ ] Add a frontend using React
* [ ] Deploy the application

---

## 👨‍💻 Author

**Shahriar Jaman Siyam**

GitHub: [Hawk-Out](https://github.com/Hawk-Out)

---

## 📄 License

This project is intended primarily as a learning and study project.
