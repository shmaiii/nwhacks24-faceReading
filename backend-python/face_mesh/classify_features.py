import calculate_measurements

def get_facial_features(points):
    features = {}

    # Get measurements
    m = calculate_measurements.create_measurements_dict(points)
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
def classify_eyebrows(forehead_to_eyebrows_ratio, eyes_to_eyebrows_ratio):
    """
    Classify eyebrows based on facial ratios.

    Parameters:
    - forehead_to_eyebrows_ratio: Ratio of forehead height to eyebrows height.
    - eyes_to_eyebrows_ratio: Ratio of eyes height to eyebrows height.

    Returns:
    - A string representing the classified eyebrow type.
    """
    straight_threshold = 0.2  # Adjust based on your observations
    arched_threshold = 0.4    # Adjust based on your observations
    high_threshold = 0.5      # Adjust based on your observations
    low_threshold = 0.3       # Adjust based on your observations
    bushy_threshold = 0.4     # Adjust based on your observations
    thin_threshold = 0.2      # Adjust based on your observations

    if forehead_to_eyebrows_ratio >= high_threshold and eyes_to_eyebrows_ratio >= high_threshold:
        return "High and Arched Eyebrows"
    elif forehead_to_eyebrows_ratio >= high_threshold:
        return "High Eyebrows"
    elif eyes_to_eyebrows_ratio >= high_threshold:
        return "Arched Eyebrows"
    elif forehead_to_eyebrows_ratio <= low_threshold and eyes_to_eyebrows_ratio <= low_threshold:
        return "Low and Straight Eyebrows"
    elif forehead_to_eyebrows_ratio <= low_threshold:
        return "Low Eyebrows"
    elif eyes_to_eyebrows_ratio <= low_threshold:
        return "Straight Eyebrows"
    elif forehead_to_eyebrows_ratio >= bushy_threshold or eyes_to_eyebrows_ratio >= bushy_threshold:
        return "Bushy Eyebrows"
    elif forehead_to_eyebrows_ratio <= thin_threshold or eyes_to_eyebrows_ratio <= thin_threshold:
        return "Thin Eyebrows"
    else:
        return None


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

