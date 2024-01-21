from flask import Flask, request, jsonify
import requests
from face_mesh.face_mesh_main import landmarks_detect
from face_mesh.classify_features import get_facial_features
from flask_cors import CORS
from generate_prophecy import generate_prophecy
import base64
from PIL import Image
from imgur import upload_imgur

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/api/convertIMG', methods=['POST'])
def convert_img():
    try:
        data = request.get_json()
        b64_string = data.get('imageSrc', '')
        image_code = base64.b64decode(b64_string.replace("data:image/webp;base64,", ""))
        webp_filename = 'face_mesh/image.webp'
        jpg_filename = 'face_mesh/image.jpg'
        
        with open(webp_filename, 'wb') as f:
            f.write(image_code)

        # Convert WEBP to JPG
        im = Image.open(webp_filename).convert("RGB")
        im.save(jpg_filename, "jpeg")

        final_prophecy = get_prophecy()
        new_image_link = upload_imgur()

        return jsonify({
            'description': final_prophecy,
            'url': new_image_link
        })

        #return {'message': 'Image successfully saved as WebP and converted to JPEG'}, 200

    except Exception as e:
        print(f'Error: {str(e)}')
        return {'error': 'Failed to process the image or process the image'}, 500

def get_prophecy():

    #transform the img url into jpg file
    #img_url = request.args.get('img_url')
    #img_url = "https://i.natgeofe.com/k/c491536c-f34d-4e64-ad27-8ee070dce475/monarch-butterfly-orange-flower.jpg?w=1084.125&h=609"
    #download_image(img_url, 'face_mesh/theImage.jpg')

    # get coordinates 
    coordinates = landmarks_detect()
    #get the final result 
    facial_features = get_facial_features(coordinates)
    print(facial_features)
    #get the prophecy texts
    final_prophecy = generate_prophecy(facial_features)
    print(final_prophecy)

    return final_prophecy

# def download_image(url, destination):
#     try:
#         response = requests.get(url)
#         response.raise_for_status() # check errors

#         with open(destination, 'wb') as file:
#             file.write(response.content)
        
#         print(f"Image downloaded successfully to {destination}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading image: {e}")
