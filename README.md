### Prof-Fa-Cee

## Inspiration
We get healings and guidance from our spritual beliefs. But it costs at least 10$ to see a reader! With prof-fa-cee, you can get future tellings (for free) and save yourself some money for boba!! The app is based on physiognomy to read facial features for characteristics and dispositions!!

## What it does
Predict your fate and analyze your personality based on your face!

## How we built it
With our brains!
JK!
First we take a passport-style picture of the user and sends it to the server where image processing happens (with the help of Imgur API). We then use MediaPipe, an open-source framework for building pipelines to perform computer vision inference, to detect facial landmarks and coordinates of important facial features. Then we use mathematics to logic out the important traits and characteristics associated with them. These traits will be fed into a function that maps to certain characteristics and renders out a prophecy! The app runs on a Javascript React front-end along with a Python Flask backend. 

## How to run it
1. To run the front end
   `cd frontend-app`.
   Then run `npm install`.
   Then run `npm start`

3. To run the backend (in a separate terminal):
  Run `cd python-backend`
    Then run`pip install -r requirements.txt`
   Then run `flask run`
