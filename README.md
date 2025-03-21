# 📰 Autonomous News Processing with RAG & CrewAI

## Overview
This project implements a **Retrieval-Augmented Generation (RAG) pipeline** using **CrewAI** to automate news searching, classification, and storage. Given a user query, the system:
1. **Searches the web** using Tavily API.
2. **Optimizes results** using an SEO agent.
3. **Classifies & Parses news** into structured data.
4. **Embeds the news** into ChromaDB for retrieval.
5. **Retrieves relevant documents** for answering queries.
6. **Grades responses** using hallucination and answer grading agents.

## 🚀 Features
✔ **Automated Web Search** (Tavily API)  
✔ **SEO Optimization** to pick the best source  
✔ **Classifies & Summarizes News** (LLM-based)  
✔ **Embeds Data into ChromaDB** for efficient retrieval  
✔ **Retrieval-Augmented Generation (RAG)** for accurate responses  
✔ **Grading System** to reduce hallucinations  
✔ **Scalable & Modular** CrewAI-based architecture  

## 🛠️ Tech Stack
- **Python** (Backend Processing)
- **CrewAI** (Multi-agent AI System)
- **LangChain** (LLM & RAG Framework)
- **Tavily API** (Web Search)
- **ChromaDB** (Vector Database for Retrieval)
- **FastAPI** (API Endpoint for Queries)
- **Streamlit** (Frontend UI for Interaction)
- **GroqCloud (DeepSeek-Qwen-32B / Llama-3.3-70B / Mistral-70B)** (LLM)

## 📂 Project Structure
```
├── src
│   ├── agents.py          # CrewAI Agents (Search, SEO, Retriever, Graders)
│   ├── classify_parse.py  # News Classification & Parsing
│   ├── embedder.py        # ChromaDB Embedding & Retrieval
│   ├── rag_pipeline.py    # RAG Workflow Implementation
│   ├── app.py             # FastAPI Endpoints
│   ├── frontend.py        # Streamlit Frontend
│   ├── utils.py           # Helper Functions (Cleaning, Storage)
│
├── data
│   ├── news_dataset.csv   # Preprocessed News Data
│   ├── chromadb_index/    # ChromaDB Vector Store
│
├── README.md              # Project Documentation
├── requirements.txt       # Python Dependencies
├── .env                   # API Keys & Configuration
```

## 🏗️ Setup & Installation
### 1️⃣ Clone Repository
```sh
git clone https://github.com/yourusername/rag-news-pipeline.git
cd rag-news-pipeline
```

### 2️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys (Tavily, Groq, ChromaDB)
Create a `.env` file and add:
```env
TAVILY_API_KEY=your_tavily_key
GROQ_API_KEY=your_groq_key
CHROMADB_PATH=./data/chromadb_index
```

### 4️⃣ Run the FastAPI Backend
```sh
uvicorn src.app:app --reload
```

### 5️⃣ Run the Streamlit Frontend
```sh
streamlit run src/frontend.py
```

## 🏃 Usage
### 🔹 **Querying the System** (API)
Send a GET request:
```sh
curl -X GET "http://localhost:8000/query?prompt='Latest updates on AI regulation'"
```

### 🔹 **Using the Streamlit UI**
1. Open `http://localhost:8501` in your browser.
2. Enter a **news query** or **URL**.
3. View **structured results** with Type, Subtype, Summary, and Source Link.

## 🛠️ Future Improvements
- Fine-tuning LLM on domain-specific news data
- Adding **multi-modal** support (video, images)
- Expanding to more **news categories & regions**
- **Fact-checking agent** for misinformation detection

---
**📌 Contribute**: Open issues, submit PRs, and help improve this project!

🔗 **GitHub Repo**: [your-repo-link](https://github.com/yourusername/rag-news-pipeline)
