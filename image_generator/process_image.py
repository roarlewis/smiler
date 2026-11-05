import random
import cv2 as cv
import numpy as np
import dlib
import imutils
from imutils import face_utils
from image_generator.image_helpers import overlay_transparent
from pathlib import Path
from image_generator.face_shapes import create_mouth_rectangle

import urllib.request
from io import BytesIO
import threading

det = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('image_generator/data/shape_predictor_68_face_landmarks.dat')

# added by claude to fix seg faults: dlib's detector and predictor aren't
# thread-safe, so only one Flask request thread may use them at a time.
# (Flask starts a new thread per request, so per-thread copies reloaded
# the 100 MB model on every request.)
dlib_lock = threading.Lock()


# load and crop the smiles once at startup, in memory, so requests never
# rewrite the PNG files (concurrent rewrites were corrupting them)
def load_smiles():
    smiles = []
    for entry in Path('image_generator/smiles').iterdir():
        smile = cv.imread(str(entry), cv.IMREAD_UNCHANGED)
        if smile is None or smile.ndim != 3 or smile.shape[2] != 4:
            continue
        # crop away the fully transparent border
        ys, xs = np.nonzero(smile[:, :, 3])
        smiles.append(smile[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    return smiles

smile_images = load_smiles()

def process_image(url):

    request = urllib.request.Request(url, headers={'User-Agent': 'SMILR/0.1'})
    response = urllib.request.urlopen(request)
    
    img_array = np.array( bytearray(response.read()), dtype=np.uint8 )
    img = cv.imdecode( img_array, -1)

    if img is None:
        raise ValueError('could not decode image')
    if img.ndim == 2:
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    elif img.shape[2] == 4:
        img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)

    # img = cv.resize(img, (500, 500), interpolation=cv.INTER_LINEAR)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    with dlib_lock:
        face_rects = det(img_gray, 1)

    for (i, rect) in enumerate(face_rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        with dlib_lock:
            shape = predictor(img_gray, rect)
        shape = face_utils.shape_to_np(shape)
        # convert dlib's rectangle to a OpenCV-style bounding box
        # [i.e., (x, y, w, h)], then draw the face bounding box
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        mouth_rect = create_mouth_rectangle(shape)
        # cv.rectangle(img, (mouth_rect[0], mouth_rect[1]), (mouth_rect[2], mouth_rect[3]), (0, 255, 0), 2)

        smile_img = random.choice(smile_images)

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

        # cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the face number
        # cv.putText(img, "Face #{}".format(i + 1), (x - 10, y - 10),
        #            cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        # for (x, y) in shape:
        #     cv.circle(img, (x, y), 1, (0, 0, 255), -1)

    status_code, img = cv.imencode(".jpg",img)
    
    return img.tobytes()
        
