from random import randint
from env import base_folder, base_url
import cv2

def run(img_path):
    # Read the input image
    img = cv2.imread(img_path)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

    # Detect faces
    detected_faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces and crop the faces
    idx = 1
    files = []
    for (x, y, w, h) in detected_faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        detected_faces = img[y:y + h, x:x + w]
        img_id = str(randint(1, 100000))
        cv2.imwrite(base_folder+'\\face_' + img_id+ '.png', detected_faces[:])
        files.append(base_url+'/face_' + img_id + '.png')
        idx+=1
    return files