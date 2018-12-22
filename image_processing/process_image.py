
import json
import io
import requests
from PIL import Image
import random
import time
import cv2
import os
import sys



def find_faces(imagePath):
    cascPath = "haarcascade_frontalface_default.xml"

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    pil_image = Image.open(imagePath).convert("RGBA")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 50),
    )

    print("Found {} faces!".format(len(faces)))

    # cropping faces
    faceimages = []
    for image_num, (x, y, w, h) in enumerate(faces):
        facedict = {}
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        faceimage = pil_image.crop(box=((x, y, x + w, y + h)))
        facedict['image'] = faceimage
        facedict['coords'] = (x, y, w, h)
        facedict['size'] = faceimage.size
        facedict['image_num'] = image_num
        faceimage.save("some_{}.jpg".format(image_num))
        os.remove("some_{}.jpg".format(image_num))
        faceimages.append(facedict)

    return faceimages, pil_image




def swap_faces(faces, base_image):
    for face in faces:
        face_index = faces.index(face)
        last_index = len(faces) - 1
        paste_index = face_index + 1 if face_index != last_index else 0
        source_image = face['image']
        #source_image.save("{}.jpg".format(face['image_num']))
        target_face = faces[paste_index]
        target_coords = target_face['coords']
        target_size = target_face['size']
        resized_image = source_image.resize((target_size[0], target_size[1]))
        base_image.paste(resized_image, (target_coords[0], target_coords[1]))

    return base_image


def process_image(image_filepath):
    faces, base_image = find_faces(image_filepath)
    if len(faces) > 1:
        new_image = swap_faces(faces, base_image)
        new_image.save("swapped_{}".format(image_filepath))
    else:
        print ("not enough faces found")




