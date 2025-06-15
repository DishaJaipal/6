##  🤖 Upload.Ask.Learn – Ask Your PDF Anything (Groq + LangChain)

**Upload.Ask.Learn** is a smart chatbot that lets you upload a PDF (like a book, research paper, or notes) and then *talk to it* using natural language. It understands your questions and answers based on what's inside the file — powered by **Groq's blazing-fast LLMs** like **Mixtral** and **LLaMA 3**.

Built using:
- 🧠 [LangChain](https://www.langchain.com/) for AI logic
- ⚡ [Groq](https://console.groq.com/) for real-time, high-performance responses
- 🧮 [FAISS](https://github.com/facebookresearch/faiss) to search the right parts of your PDF
- 🧾 Flask + HTML for a simple, clean web interface

---

## 🌟 What Can It Do?

- 📎 Upload any PDF (notes, textbook, paper, etc.)
- ❓ Ask questions in plain English
- 💬 Get accurate answers based on that exact document
- 🧠 Uses "RAG" — Retrieval-Augmented Generation — to answer better
- 💡 No need to read the whole PDF yourself!

---

## 🛠️ How to Use It (For Devs)


## 🔧 1. Clone the Project



## 🌐 2. Install the Required Libraries

bash

python -m venv venv

source venv/bin/activate  # (Windows: venv\Scripts\activate)

pip install -r requirements.txt

----------
## 🔑 3. Add Your Groq API Key
- Create a file named .env in the root folder:
env
GROQ_API_KEY=your_groq_api_key_here
Get your key at 👉 https://console.groq.com/keys
---
## ▶️ 4. Start the Chatbot
bash

python app.py

Then open hhtp://localhost:500 in your broser

-----
## 🧠 How It Works (Behind the Scenes)

📂 You upload a PDF.
📄 The file is split into chunks using LangChain.
🔍 These chunks are turned into vectors and stored in a FAISS index.
💬 When you ask something, the app finds the most relevant parts.
⚡ It sends those parts (plus your question) to Groq’s LLM.
🤯 You get an answer that actually knows your document!

---
## 🗂️ Project Structure

- chatmypdf/
- ├── app.py                # Flask backend
- ├── templates/
- │   └── index.html        # Web UI
- ├── static/
- │   └── script.js         # JS logic for uploading + chatting
- ├── .env                  # Groq API key
- ├── requirements.txt      # All dependencies
- ├── vectorstore/          # Saved FAISS vector DB
- └── temp/                 # Uploaded PDF files

## 🌍 Want to Deploy?

🧪 Local	Just run python app.py and go

free deployment is not possible for this project due to the large 

---
## 🚀 Future Ideas 

Streamed responses	Use Groq's streaming API in Flask

File history	Save vectors per file in separate folders

User login	Add Firebase or Flask-Login for sessions

UI polish	Add Tailwind, Bootstrap, or React frontend

Multiple files	Combine vectors across docs

## 👩‍💻 Team Roles

- Prakruthi U:  www.linkedin.com/in/prakruthi-u-180463296 | www.github.com/PRAKRUTHI77
  Frontend development (UI/UX), Firebase integration, GitHub repository setup  
- Sindhushree N H: www.linkedin.com/in/sindhushree-nh-38a748332 | www.github.com/SindhushreeNH
  Chat UI styling, frontend Flask endpoint connection, GitHub repository management  
- Bhuvanashree: www.linkedin.com/in/bhuvanashree-s-5525a9258 | www.github.com/Bhuvanashree13
  LangChain + Groq integration for RAG chatbot, vector DB setup, embeddings and retrieval  
- Disha Jaipal: www.linkedin.com/in/disha-jaipal-25318a247 | www.github.com/DishaJaipal
  Flask backend (`main.py`), file handling, system setup, Flask–LangChain–frontend glue logic

## 👩‍💻 End Results

ppt link:https://drive.google.com/file/d/1oDF4mBhw8lEuQqwgev1caMb66ocr2R9Z/view?usp=sharing

working video link:https://drive.google.com/file/d/1sI-zmGYBSDWqvEgUguAru9vxKRslXNkG/view?usp=sharing



## 📄 License

MIT License © 2025 [PiXeLs]

## 🙌 Acknowledgements

Groq API

LangChain

FAISS by Meta

PyPDF
