# Take in array of points and return necessary measurements

import math

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