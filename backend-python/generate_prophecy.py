import json

with open("db.json", "r") as file:
    db = json.load(file)

# @app.route("/app/get_prophecy", methods=["GET"])
# def get_prophecy():
#     return

def generate_prophecy(input):
    print(input)
    attributes = list(input.keys())

    descriptions = []

    for attribute in input.keys():
        value = input[attribute]
        attribute_descriptions = find_attribute_description(attribute, value, descriptions)
    
    concatenated_strings = ''.join(descriptions)
    return concatenated_strings

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