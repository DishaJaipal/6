import os
from flask import Flask,request, jsonify, render_template
from dotenv import load_dotenv
import tempfile
from rag_bot import process_pdf, get_answer

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
app = Flask(__name__,static_folder='static',template_folder='templates')


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file and file.filename.endswith('.pdf'):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                file.save(tmp.name)
                msg = process_pdf(tmp.name)  # This may raise error — it's okay
            return jsonify({"message": msg}), 200

        return jsonify({"error": "Invalid file type"}), 400

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500



@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    result = get_answer(question, GROQ_API_KEY)

    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    return jsonify({"answer": result["answer"]}), 200

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8008)))
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Flask app running on http://0.0.0.0:{port}") 
    app.run(debug=True, host="0.0.0.0", port=port)


