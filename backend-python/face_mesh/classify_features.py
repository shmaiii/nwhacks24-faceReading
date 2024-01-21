# from calculate_measurements import create_measurements_dict
import math
import random

face_top_index = 10
face_bottom_index = 152
face_left_index = 234
face_right_index = 454

forehead_top_index = 10
forehead_bottom_index = 9
forehead_left_index = 21
forehead_right_index = 251

jaw_left_index = 172
jaw_right_index = 397
cheekbone_right_index = 50
cheekbone_left_index = 280

eye_cornerL_index = 243
eye_cornerR_index = 463
right_eye_widthL = 133
right_eye_widthR = 33
left_eye_widthR = 362
left_eye_widthL = 263

upper_lip_top = 0
upper_lip_bottom = 13
lower_lip_top = 14
lower_lip_bottom = 17
mouth_cornerL = 61
mouth_cornerR = 291

def get_facial_features(points):
    features = {}

    # Get measurements
    m = create_measurements_dict(points)
    face_w = m['face_width']
    face_l = m['face_length']
    forehead_w = m['forehead_width']
    forehead_l = m['forehead_height']
    jaw_w = m['jaw_width']
    cheekbone_w = m['cheekbone_width']
    cheekbone_l = m['cheekbone_length']
    eye_distance = m['distance_between_eyes']
    upper_lip_h = m['upper_lip_height']
    lower_lip_h = m['lower_lip_height']
    mouth_w = m['mouth_width']
    eyeball_w = m['eyeball_w']

    # Classify
    features['face_shape'] = classify_face_shape(face_w, face_l, forehead_w, jaw_w)
    features['forehead'] = classify_forehead_shape(forehead_w, face_w, forehead_l, face_l)
    features['eyebrows'] = classify_eyebrows(points)
    features['eyes'] = classify_eye_set(eye_distance, eyeball_w)
    features['cheeks'] = classify_cheeks(cheekbone_l, face_l)
    features['lips'] = classify_lips(upper_lip_h, lower_lip_h, mouth_w)

    return features

def create_measurements_dict(points):
    measurements_dict = {}

    measurements_dict['face_width'] = calculate_distance(points, face_left_index, face_right_index)
    measurements_dict['face_length'] = calculate_distance(points, face_top_index, face_bottom_index) + calculate_distance(points, forehead_top_index, forehead_bottom_index) * 0.5
    measurements_dict['forehead_width'] = calculate_distance(points, forehead_left_index, forehead_right_index)
    measurements_dict['forehead_height'] = calculate_distance(points, forehead_top_index, forehead_bottom_index) * 1.75

    measurements_dict['jaw_width'] = calculate_distance(points, jaw_left_index, jaw_right_index)
    measurements_dict['cheekbone_width'] = calculate_distance(points, cheekbone_left_index, cheekbone_right_index)

    measurements_dict['distance_between_eyes'] = calculate_distance(points, eye_cornerL_index, eye_cornerR_index)

    measurements_dict['cheekbone_length'] = max(calculate_distance(points, cheekbone_right_index, 24), calculate_distance(points, cheekbone_left_index, 254))

    measurements_dict['eyeball_w'] = min(calculate_distance(points, left_eye_widthL, left_eye_widthR), calculate_distance(points, right_eye_widthL, right_eye_widthR))

    measurements_dict['upper_lip_height'] = calculate_distance(points, upper_lip_top, upper_lip_bottom)
    measurements_dict['lower_lip_height'] = calculate_distance(points, lower_lip_top, lower_lip_bottom)
    measurements_dict['mouth_width'] = calculate_distance(points, mouth_cornerL, mouth_cornerR)

    return measurements_dict

def calculate_distance(points, first, second):
    pointA = points[first]
    pointB = points[second]
    return math.sqrt((pointA.x - pointB.x)**2 + (pointA.y - pointB.y)**2)

def classify_lips(upper_lip_h, lower_lip_h, mouth_w):
    # Calculate ratios
    upper_lip_to_lower_lip_ratio = upper_lip_h / lower_lip_h
    lip_to_mouth_ratio = (upper_lip_h + lower_lip_h) / mouth_w

    if upper_lip_to_lower_lip_ratio >= 0.55 and lip_to_mouth_ratio >= 0.31:
        return "thick"
    else: 
        return "thin"
  
def classify_cheeks(cheekbone_l, face_l):
    # Calculate ratios
    cheekbone_to_face_ratio = cheekbone_l / face_l

    if cheekbone_to_face_ratio <= 0.15:
        return "high_cheekbones"
    else:
        return "full"

def classify_eye_set(eye_distance, eyeball_w):
    if eye_distance >= eyeball_w:
        return "wide_set"
    else:
        return "close_set"

def classify_eyebrows(points):
    res = ["High and Arched Eyebrows", "High Eyebrows", "Arched Eyebrows", "Low and Straight Eyebrows", "Low Eyebrows", "Straight Eyebrows", "Bushy Eyebrows", "Thin Eyebrows"]
    eyes_height = calculate_distance(points, 159, 145)
    #eyebrwo_height means height to eyebrow starting from eyes
    eyebrow_height = calculate_distance(points, 52, 27)
    eyes_to_eyebrows_ratio =  eyebrow_height / eyes_height
    eyebrows_slope = (points[105].y - points[70].y) / (points[105].x - points[70].y)
    eyebrows_height_height = calculate_distance(points, 105, 52)
    eye_brow_part_height = calculate_distance(points, 105, 27)

    if eyebrows_height_height / eye_brow_part_height >= 0.46:
        return "bushy"
    if eyebrows_height_height / eye_brow_part_height <= 0.33:
        return "thin"
    
    if eyebrows_slope >= 0.35 :
        if eyes_to_eyebrows_ratio > 1.2 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) > 1.5:
            return "Hight and Arched Eyebrows"
        return "arched"
    if eyebrows_slope <= 0.15:
        if eyes_to_eyebrows_ratio < 0.8 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) < 0.5 :
            return "low"
        return "straight"
    
    if eyes_to_eyebrows_ratio > 1.2 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) > 1.5:
        return "high"
    if eyes_to_eyebrows_ratio < 0.8 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) < 0.5 :
        return "low"
    else:
        random_num = random.randint(0, len(res) - 1)
        return res[random_num]

# Function takes in array of points and return face shape
def classify_forehead_shape(forehead_w, face_w, forehead_l, face_l):
    # Calculate ratios
    forehead_width_ratio = forehead_w / face_w
    forehead_height_ratio = forehead_l / face_l

    if forehead_width_ratio < 0.75:
        return "narrow"
    elif forehead_width_ratio >= 0.75 and forehead_height_ratio >= 0.3:
        return "high_and_wide"
    elif forehead_width_ratio >= 0.75 and forehead_w / forehead_l <= 0.6:
        return "square"
    elif forehead_width_ratio >= 0.35:
        return "low_and_wide"
    else:
        return None

def classify_face_shape(face_w, face_l, forehead_w, jaw_w):
    # Calculate relevant ratios
    width_to_length_ratio = face_w / face_l
    jaw_to_width_ratio = jaw_w / face_w
    jaw_to_forehead_ratio = jaw_w / forehead_w

    if width_to_length_ratio >= 0.90:
        return "round"
    elif width_to_length_ratio >= jaw_to_forehead_ratio and width_to_length_ratio <= jaw_to_forehead_ratio:
        return "oblong"
    elif face_l / face_w >= 0.5 and forehead_w <= face_w - 0.1:
        return "oval"
    elif jaw_to_forehead_ratio >= 0.85 and jaw_to_width_ratio >= 0.8:
        if (random.randint(1, 2) == 1):
          return "rectangle"
        else:
          return "square"
    elif max(face_w, face_l, forehead_w, jaw_w) == face_l and max(face_w, forehead_w, jaw_w) == face_w:
        return "triangle"
    else:
        return "diamond"