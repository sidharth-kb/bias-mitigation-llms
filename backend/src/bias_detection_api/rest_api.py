from flask import Flask, request, jsonify
from flask_cors import CORS
#from bias_detection_api.bias_neutralisation import remove_section_bias
#from bias_detection_api.bias_detection import detect_bias

from bias_neutralisation import remove_section_bias
from bias_detection import detect_bias

from pydantic import BaseModel
from pydantic import ValidationError

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


"""
 {
    section: {
        context: ...,
        text: ...
    },
    mode: ...
 }
"""
@app.route("/remove-section-bias", methods=["POST"])
def remove_section_bias_api():

    class Section(BaseModel):
        context: str
        text: str

    class Payload(BaseModel):
        section: Section
        mode: bool

    payload : Payload | None = None

    try:
        payload = Payload(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400

    if payload is None:
        return jsonify({"error": "invalid request"}), 400

    if not payload.mode:
        return jsonify({"error": "Not implemented yet"}), 500

    neutralised_text = remove_section_bias({
        "text": payload.section.text,
        "context": payload.section.context,
    })

    return jsonify({
        "neutralised_text": neutralised_text
    }), 200



@app.route("/tag-text", methods=["POST"])
def tag_text():
    context_size = request.args.get("context_size", type=int, default=2)

    class Payload(BaseModel):
        text: str

    payload = None

    try:
        payload = Payload(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors()), 400

    if payload is None:
        return jsonify({"error": "invalid request"})

    tagged_text, parsed_text = detect_bias(payload.text, context_size)

    return jsonify({"tagged_text": tagged_text,
                    "parsed_text": parsed_text,
                    "bias": len(parsed_text) > 0}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)
