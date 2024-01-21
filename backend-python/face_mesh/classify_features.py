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

jaw_left_index = 132
jaw_right_index = 361

cheekbone_left_index = 123
cheekbone_right_index = 352

eye_cornerL_index = 243
eye_cornerR_index = 463

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
    eye_distance = m['distance_between_eyes']
    upper_lip_h = m['upper_lip_height']
    lower_lip_h = m['lower_lip_height']
    mouth_w = m['mouth_width']

    # Classify
    features['face_shape'] = classify_face_shape(face_w, face_l, forehead_l, jaw_w, cheekbone_w)
    features['forehead'] = classify_forehead_shape(forehead_w, face_w, forehead_l, face_l)
    features['eyebrows'] = 'straight' # hard-coded
    features['eyes'] = classify_eye_set(eye_distance, face_w, forehead_w)
    features['cheeks'] = classify_cheeks(cheekbone_w, jaw_w, 0.5) # hard-coded
    features['lips'] = classify_lips(upper_lip_h, lower_lip_h, mouth_w, face_w)

    return features

def create_measurements_dict(points):
    measurements_dict = {}

    measurements_dict['face_width'] = calculate_distance(points, face_left_index, face_right_index)
    measurements_dict['face_length'] = calculate_distance(points, face_top_index, face_bottom_index)

    measurements_dict['forehead_width'] = calculate_distance(points, forehead_left_index, forehead_right_index)
    measurements_dict['forehead_height'] = calculate_distance(points, forehead_top_index, forehead_bottom_index)

    measurements_dict['jaw_width'] = calculate_distance(points, jaw_left_index, jaw_right_index)
    measurements_dict['cheekbone_width'] = calculate_distance(points, cheekbone_left_index, cheekbone_right_index)

    measurements_dict['distance_between_eyes'] = calculate_distance(points, eye_cornerL_index, eye_cornerR_index)

    # measurements_dict['cheek_height'] # see if possible
    # measurements_dict['face_height'] # see if possible

    measurements_dict['upper_lip_height'] = calculate_distance(points, upper_lip_top, upper_lip_bottom)
    measurements_dict['lower_lip_height'] = calculate_distance(points, lower_lip_top, lower_lip_bottom)
    measurements_dict['mouth_width'] = calculate_distance(points, mouth_cornerL, mouth_cornerR)

    return measurements_dict

def calculate_distance(points, first, second):
    pointA = points[first]
    pointB = points[second]
    return math.sqrt((pointA.x - pointB.x)**2 + (pointA.y - pointB.y)**2)

# Function takes in array of points and return face shape
def classify_face_shape(face_w, face_l, forehead_l, jaw_w, cheekbone_w):
    # Define face shape classification thresholds
    round_threshold = 0.95
    oblong_threshold = 1.1
    triangle_threshold = 0.8
    square_threshold = 1.0
    rectangle_threshold = 1.2

    # Calculate relevant ratios
    width_to_length_ratio = face_w / face_l
    forehead_to_chin_ratio = forehead_l / face_l
    jaw_to_forehead_ratio = jaw_w / forehead_l
    cheekbone_to_jaw_ratio = cheekbone_w / jaw_w

    # Classify face shape based on ratios
    if width_to_length_ratio >= round_threshold:
        return "round"
    elif width_to_length_ratio > oblong_threshold and forehead_to_chin_ratio > 0.5:
        return "oblong"
    elif jaw_to_forehead_ratio < triangle_threshold and cheekbone_to_jaw_ratio < 0.9:
        return "triangle"
    elif jaw_to_forehead_ratio > square_threshold:
        return "square"
    elif width_to_length_ratio > rectangle_threshold and forehead_to_chin_ratio > 0.5:
        return "rectangle"
    else:
        return "oval"
    

def classify_forehead_shape(forehead_w, face_w, forehead_l, face_l):
    """
    Classify forehead shapes based on width and height ratios.

    Parameters:
    - forehead_width_ratio: Ratio of forehead width to face width.
    - forehead_height_ratio: Ratio of forehead height to face height.

    Returns:
    - A string representing the classified forehead shape.
    """
    low_and_wide_threshold = 0.35
    high_and_wide_threshold = 0.35
    square_threshold = 0.45
    narrow_threshold = 0.25

    # Calculate ratios
    forehead_width_ratio = forehead_w / face_w
    forehead_height_ratio = forehead_l / face_l

    if forehead_width_ratio < narrow_threshold:
        return "narrow"
    elif forehead_width_ratio >= high_and_wide_threshold and forehead_height_ratio >= high_and_wide_threshold:
        return "high_and_wide"
    elif forehead_width_ratio >= square_threshold:
        return "square"
    elif forehead_width_ratio >= low_and_wide_threshold:
        return "low_and_wide"
    else:
        return None


# TODO1
def classify_eyebrows(forehead_to_eyebrows_ratio, eyes_to_eyebrows_ratio, points):
    """
    Classify eyebrows based on facial ratios.

    Parameters:
    - forehead_to_eyebrows_ratio: Ratio of forehead height to eyebrows height.
    - eyes_to_eyebrows_ratio: Ratio of eyes height to eyebrows height.

    Returns:
    - A string representing the classified eyebrow type.
    """

    res = ["High and Arched Eyebrows", "High Eyebrows", "Arched Eyebrows", "Low and Straight Eyebrows", "Low Eyebrows", "Straight Eyebrows", "Bushy Eyebrows", "Thin Eyebrows"]
    eyes_height = calculate_distance(points, 159, 145)
    #eyebrwo_height means height to eyebrow starting from eyes
    eyebrow_height = calculate_distance(points, 52, 27)
    eyes_to_eyebrows_ratio =  eyebrow_height / eyes_height
    eyebrows_slope = (points[105].y - points[70].y) / (points[105].x - points[70].y)
    eyebrows_height_height = calculate_distance(points, 105, 52)
    eye_brow_part_height = calculate_distance(points, 105, 27)

    if eyebrows_height_height / eye_brow_part_height >= 0.46:
        return "Bushy Eyebrows"
    if eyebrows_height_height / eye_brow_part_height <= 0.33:
        return "Thin Eyebrows"
    
    if eyebrows_slope >= 0.35 :
        if eyes_to_eyebrows_ratio > 1.2 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) > 1.5:
            return "Hight and Arched Eyebrows"
        return "Arched Eyebrows"
    if eyebrows_slope <= 0.15:
        if eyes_to_eyebrows_ratio < 0.8 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) < 0.5 :
            return "Low and Straight Eyebrows"
        return "Straight Eyebrows"
    
    if eyes_to_eyebrows_ratio > 1.2 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) > 1.5:
        return "High Eyebrows"
    if eyes_to_eyebrows_ratio < 0.8 or calculate_distance(points, 65, 45) / (eyebrow_height + eyes_height) < 0.5 :
        return "Low Eyebrows"
    else:
        random_num = random.randint(0, len(res) - 1)
        return res[random_num]


def classify_eye_set(eye_distance, face_w, forehead_w):
    """
    Classify eyes as wide-set or close-set based on facial ratios.

    Parameters:
    - distance_between_eyes_ratio: Ratio of the distance between eyes to face width.
    - forehead_width_ratio: Ratio of forehead width to face width.

    Returns:
    - A string representing the classified eye set type.
    """
    wide_set_threshold = 0.4  # Adjust based on your observations
    close_set_threshold = 0.2  # Adjust based on your observations

    # Calculate ratios
    distance_between_eyes_ratio = eye_distance / face_w
    print(distance_between_eyes_ratio)
    forehead_width_ratio = forehead_w / face_w

    if distance_between_eyes_ratio >= wide_set_threshold:
        return "wide-set"
    elif distance_between_eyes_ratio <= close_set_threshold:
        return "close-set"
    elif forehead_width_ratio <= close_set_threshold:
        return "close-set"
    else:
        return None


def classify_cheeks(cheekbone_w, jaw_w, temp):
    """
    Classify cheeks as high-cheekbones, sunken, or full based on facial ratios.

    Parameters:
    - cheekbone_to_jaw_ratio: Ratio of cheekbone width to jaw width.
    - cheek_height_ratio: Ratio of cheek height to face height.

    Returns:
    - A string representing the classified cheek type.
    """
    high_cheekbones_threshold = 0.6  # Adjust based on your observations
    sunken_cheeks_threshold = 0.4    # Adjust based on your observations
    full_cheeks_threshold = 0.5      # Adjust based on your observations

    # Calculate ratios
    cheekbone_to_jaw_ratio = cheekbone_w / jaw_w
    cheek_height_ratio = temp # TODO2

    if cheekbone_to_jaw_ratio >= high_cheekbones_threshold:
        return "high_cheekbones"
    elif cheek_height_ratio <= sunken_cheeks_threshold:
        return "sunken"
    elif cheek_height_ratio >= full_cheeks_threshold:
        return "full"
    else:
        return None


def classify_lips(upper_lip_h, lower_lip_h, mouth_w, face_w):
    """
    Classify lips as thick or thin based on facial ratios.

    Parameters:
    - upper_lip_to_lower_lip_ratio: Ratio of the upper lip height to lower lip height.
    - mouth_width_ratio: Ratio of mouth width to face width.

    Returns:
    - A string representing the classified lip type.
    """
    thick_lips_threshold = 0.5  # Adjust based on your observations
    thin_lips_threshold = 0.2   # Adjust based on your observations

    # Calculate ratios
    upper_lip_to_lower_lip_ratio = upper_lip_h / lower_lip_h
    mouth_width_ratio = mouth_w /face_w

    if upper_lip_to_lower_lip_ratio >= thick_lips_threshold and mouth_width_ratio >= thick_lips_threshold:
        return "thick"
    elif upper_lip_to_lower_lip_ratio <= thin_lips_threshold and mouth_width_ratio <= thin_lips_threshold:
        return "thin"
    else:
        return None

