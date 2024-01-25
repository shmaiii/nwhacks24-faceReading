import json
from openai import OpenAI

with open("db.json", "r") as file:
    db = json.load(file)

# set up client key
openai_client = OpenAI(api_key='OPENAI_API_KEY')

def generate_prophecy(input):
    print(input)
    attributes = list(input.keys())

    descriptions = []

    for attribute in input.keys():
        value = input[attribute]
        attribute_descriptions = find_attribute_description(attribute, value, descriptions)
    
    concatenated_strings = ''.join(descriptions)
    
    user_message = f"Following the facial features and correlated attributes determined for this user based on physiognomy, similar to tarot reading and palm reading, draw predictions about their future health, wealth, relationships love life, and career: {concatenated_strings}"
 
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": user_message},
        ]
    )
    print(response.choices[0].message.content)
 
    return response.choices[0].message.content

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