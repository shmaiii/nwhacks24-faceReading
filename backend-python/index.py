from flask import Flask, request, jsonify
import json

app = Flask(__name__)

with open("db.json", "r") as file:
    db = json.load(file)

@app.route("/app/get_prophecy", methods=["GET"])
def get_prophecy():
    # if not request.is_json:
    #     return jsonify({"error": "Invalid request. Please provide a JSON request."}), 400
    
    req = request.get_json()

    attributes = list(req.keys())

    descriptions = []

    for attribute in attributes:
        value = req[attribute]
        attribute_descriptions = find_attribute_description(attribute, value, descriptions)

    concatenated_string = " ".join(descriptions)
    return f'"{concatenated_string}"'

def find_attribute_description(attribute, value, descriptions):
    if attribute in db:
        attribute_dict = db[attribute]

        if isinstance(value, list):
            # Handle attributes with more than one key (e.g., eyebrows)
            for item in value:
                descriptions.extend([obj[item] for obj in attribute_dict if item in obj])
        else:
            # Handle attributes that take in a single key (e.g., face_shape)
            descriptions.extend([obj[value] for obj in attribute_dict if value in obj])

        return descriptions

    return []

if __name__ == "__main__":
    app.run(debug=True)