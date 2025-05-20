from flask import Flask, request, jsonify
from pyswip import Prolog
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'query' not in request.form:
        return jsonify({"error": "Need both 'file' and 'query'"}), 400

    file = request.files['file']
    query = request.form['query']

    if not file.filename.endswith('.pl'):
        return jsonify({"error": "Only .pl files are allowed"}), 400

    # Save the uploaded file
    filename = f"{uuid.uuid4()}.pl"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Consult and query
    prolog = Prolog()
    try:
        prolog.consult(filepath)
        results = [res for res in prolog.query(query)]
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        os.remove(filepath)  # Clean up

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
