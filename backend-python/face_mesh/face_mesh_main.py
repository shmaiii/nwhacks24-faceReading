# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import json
import numpy as np
import matplotlib.pyplot as plt
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions
import cv2
import os

path = os.path.join(os.path.dirname(__file__), 'image.jpg')

model_path = os.path.join(os.path.dirname(__file__), 'face_landmarker.task')
#path = "./mai.jpg"

def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

  return annotated_image

def landmarks_detect():
  #path = "./mai.jpg" # img_path
  BaseOptions = mp.tasks.BaseOptions
  FaceLandmarker = mp.tasks.vision.FaceLandmarker
  FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
  VisionRunningMode = mp.tasks.vision.RunningMode

  options = FaceLandmarkerOptions(
      base_options=BaseOptions(model_asset_path=model_path),
      running_mode=VisionRunningMode.IMAGE)

  mp_image = mp.Image.create_from_file(path)
      
  with FaceLandmarker.create_from_options(options) as landmarker:
    # The landmarker is initialized. Use it here.
      detection_result = landmarker.detect(mp_image)
      res = detection_result.face_landmarks
      print(res[0][1].x)

      annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
      cv2.imwrite(os.path.join(os.path.dirname(__file__), 'annotated_image.jpg'), cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

  return res[0]

if __name__ == "__main__":
    landmarks_detect()

