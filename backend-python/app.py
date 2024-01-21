from flask import Flask, request
import requests
from face_mesh.face_mesh_main import landmarks_detect
from face_mesh.classify_features import get_facial_features

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/get_prophecy")
def get_coordinates():

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
    final_prophecy = ''

    #get the new image

    #return the image and final prophecy in a json object to send to the front-end

    return "<p>WTF</p>"

def download_image(url, destination):
    try:
        response = requests.get(url)
        response.raise_for_status() # check errors

        with open(destination, 'wb') as file:
            file.write(response.content)
        
        print(f"Image downloaded successfully to {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
