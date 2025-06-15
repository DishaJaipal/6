import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Serve the frontend
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint for PDF upload
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
        # Here you would add your PDF processing logic
        # For now, we'll just return a success message
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

# API endpoint for asking questions
@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Here you would add your RAG pipeline logic
    # For now, we'll return a dummy response
    answer = "This is a sample answer from the AI. In a real implementation, this would be the response from your RAG system."
    return jsonify({"answer": answer}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))