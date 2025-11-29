from flask import Flask, request, jsonify
from flask_cors import CORS
from bias_detection_api.few_shot_prompting_functions import remove_text_bias

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route("/remove-bias", methods=["POST"])
def remove_bias():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "invalid request"}), 400
    
    text = data.get("text")
    if text is None:
        return jsonify({"error": "no text"}), 400

    res = remove_text_bias(text)

    return jsonify({
        "result": res}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
