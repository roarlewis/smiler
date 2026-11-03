import cv2 as cv
def create_mouth_rectangle(coords):
    low_x = 100000
    low_y = 100000
    high_x = -100000
    high_y = -100000
    for i in range(48, 68):
        if coords[i][0] < low_x:
            low_x = coords[i][0]
        if coords[i][0] > high_x:
            high_x = coords[i][0]
        if coords[i][1] < low_y:
            low_y = coords[i][1]
        if coords[i][1] > high_y:
            high_y = coords[i][1]
    return low_x, low_y, high_x, high_y


def create_lefteye_rectangle(coords):
    low_x = 100000
    low_y = 100000
    high_x = -100000
    high_y = -100000
    for i in range(36, 41):
        if coords[i][0] < low_x:
            low_x = coords[i][0]
        if coords[i][0] > high_x:
            high_x = coords[i][0]
        if coords[i][1] < low_y:
            low_y = coords[i][1]
        if coords[i][1] > high_y:
            high_y = coords[i][1]
    return low_x, low_y, high_x, high_y

def create_righteye_rectangle(coords):
    low_x = 100000
    low_y = 100000
    high_x = -100000
    high_y = -100000
    for i in range(42, 47):
        if coords[i][0] < low_x:
            low_x = coords[i][0]
        if coords[i][0] > high_x:
            high_x = coords[i][0]
        if coords[i][1] < low_y:
            low_y = coords[i][1]
        if coords[i][1] > high_y:
            high_y = coords[i][1]
    return low_x, low_y, high_x, high_y

def extract_left_eye(coords):
    left_eye_points = coords[36, 41]
    