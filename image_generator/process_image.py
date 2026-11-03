import random
import cv2 as cv
import dlib
import imutils
from imutils import face_utils
from image_helpers import *
from pathlib import Path
from face_shapes import *

import urllib.request
from io import BytesIO

det = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

def process_image(url):

    response = urllib.request.urlopen(url)
    
    img_array = np.array( bytearray(response.read()), dtype=np.uint8 )
    img = cv.imdecode( img_array, -1)

    # img = cv.resize(img, (500, 500), interpolation=cv.INTER_LINEAR)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    face_rects = det(img_gray, 1)

    for (i, rect) in enumerate(face_rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(img_gray, rect)
        shape = face_utils.shape_to_np(shape)
        # convert dlib's rectangle to a OpenCV-style bounding box
        # [i.e., (x, y, w, h)], then draw the face bounding box
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        mouth_rect = create_mouth_rectangle(shape)
        cv.rectangle(img, (mouth_rect[0], mouth_rect[1]), (mouth_rect[2], mouth_rect[3]), (0, 255, 0), 2)

        smiles_path = Path('smiles')
        smile_files = [entry for entry in smiles_path.iterdir() if entry.is_file()]
        smile_img = random.choice(smile_files)
        crop_to_bbox(smile_img)
        smile_img = cv.imread(smile_img, cv.IMREAD_UNCHANGED)

        smile_resize = 1.8
        smile_width = (mouth_rect[2]-mouth_rect[0])
        smile_height = (mouth_rect[3]-mouth_rect[1])
        smile_img = imutils.resize(smile_img, int(smile_resize * smile_width), int(smile_resize * smile_height))

        smile_x_offset = int(-(smile_width * (smile_resize - 1))/2)
        smile_y_offset = int(-(smile_height * (smile_resize - 1))/2)
        img = overlay_transparent(img, smile_img, (mouth_rect[0] + smile_x_offset, mouth_rect[1] + smile_y_offset))

        # lefteye_rect = create_lefteye_rectangle(shape)
        # cv.rectangle(img, (lefteye_rect[0], lefteye_rect[1]), (lefteye_rect[2], lefteye_rect[3]), (0, 255, 0), 2)
        # righteye_rect = create_righteye_rectangle(shape)
        # cv.rectangle(img, (righteye_rect[0], righteye_rect[1]), (righteye_rect[2], righteye_rect[3]), (0, 255, 0), 2)

        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the face number
        # cv.putText(img, "Face #{}".format(i + 1), (x - 10, y - 10),
        #            cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        # for (x, y) in shape:
        #     cv.circle(img, (x, y), 1, (0, 0, 255), -1)

    status_code, img = cv.imencode(".jpg",img)
    
    return img
        
