# 🧠 Personal AI Knowledge Base (Local RAG System)

A full-stack, fully local Retrieval-Augmented Generation (RAG) application. This project allows users to securely register, upload PDF documents, and chat with a local AI model about the contents of those documents. 

Built with **FastAPI**, **Ollama**, **ChromaDB**, and a lightweight **HTML/Tailwind** frontend, this app runs entirely on your own hardware—meaning zero API costs and total data privacy.

---

## ✨ Features

* **100% Local AI:** Powered by [Ollama](https://ollama.com/) (Llama 3), ensuring your data never leaves your machine.
* **Secure Authentication:** JWT-based user login and registration using modern Argon2 password hashing.
* **Document Ingestion (RAG):** Upload PDFs, extract text, and automatically generate vector embeddings stored in ChromaDB.
* **Persistent Memory:** Chat history is saved in a local SQLite database using SQLAlchemy, so the AI remembers past conversations.
* **Built-in Web UI:** A clean, ChatGPT-style interface built with HTML, JS, and Tailwind CSS, served directly by FastAPI.
* **Multi-tenant Architecture:** Users can only search and interact with the documents they have personally uploaded.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your system:
* **Python 3.10+**
* **Ollama:** Download and install from [ollama.com](https://ollama.com/)

---
<br>

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/Anuj0kumar/personal-ai-rag.git

cd personal-ai-rag
```


**2. Create a virtual environment**

```Bash
python -m venv .venv

# On Windows :
.venv\Scripts\activate

# On macOS/Linux :
source .venv/bin/activate 
```
**3. Install dependencies**
```
pip install -r requirements.txt
```
#
**4. Download the Local AI Model**

Open a separate terminal window and run:
```
ollama run llama3
```
Keep this terminal window open. This is your local AI engine.
#
<br>

## 💻 Running the Application

Once Ollama is running in the background, start the FastAPI backend:
```
uvicorn app.main:app --reload
```
The application will automatically create the required SQLite database (sql_app.db) and ChromaDB vector storage folders on the first run.

#
<br>

## 🌐 Usage

The Web Interface
Open your browser and navigate to:
```http://127.0.0.1:8000/static/index.html```

* Click Register to create a new account.

* Login with your new credentials.

* Use the Upload PDF button to add a document to your knowledge base.

Start chatting!

#
### The API Docs (Swagger UI)
For developers wanting to interact directly with the API endpoints, navigate to:
```http://127.0.0.1:8000/docs```


# 
<br>

## 📁 Project Structure

<pre>
personal-ai-rag/
│
├── app/
│   ├── api/
│   │   └── endpoints/     # API Routes (auth.py, chat.py, upload.py)
│   ├── core/              # Config, Database setup, Security (JWT/Argon2)
│   ├── models/            # SQLAlchemy Models (user.py, chat_history.py)
│   ├── schemas/           # Pydantic validation schemas
│   ├── services/          # Business logic (ai_service.py, vector_service.py)
│   └── main.py            # FastAPI application instance
│
├── static/
│   └── index.html         # Web UI
│
├── data/
│   └── chroma/            # Vector Database storage (auto-generated)
│
└── sql_app.db             # SQLite relational database (auto-generated)
</pre>



## 🛠️ Troubleshooting



* **Connection error:** Is Ollama running locally?
Make sure you have an active terminal running ollama run llama3.
<br>

* **ValueError:** password cannot be longer than 72 bytes (If using older bcrypt)
This project uses argon2 to avoid this. If you encounter password hashing errors, ensure you have deleted any old sql_app.db files from previous testing to avoid
<br>

* **Uploaded PDF returns no answers:**
Ensure the PDF contains extractable text (not just scanned images). If using a scanned document, you would need to add an OCR library like Tesseract, which is not included by default.</li>
</ul>