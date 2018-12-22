import tweepy
from tweepy import OAuthHandler
import json
import io
import requests
from PIL import Image
import random
import time
import cv2
import os
import sys
import datetime
from instagram.client import InstagramAPI


# Get user supplied values

def weird_photo(imagePath):
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
        scaleFactor=1,
        minNeighbors=1,
        minSize=(30, 30),
    )

    print("Found {} faces!".format(len(faces)))
    if len(faces) > 1:
        # Draw a rectangle around the faces
        print(faces)
        faceimages = []
        for (x, y, w, h) in faces:
            facedict = {}
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            faceimage = pil_image.crop(box=((x, y, x + w, y + h)))
            facedict['image'] = faceimage
            facedict['coords'] = (x, y, w, h)
            facedict['size'] = faceimage.size
            faceimages.append(facedict)

        for face_set in faceimages:
            face_index = faceimages.index(face_set)
            lastindex = len(faceimages) - 1
            pasteindex = face_index + 1 if face_index != lastindex else 0
            sourceimage = face_set['image']
            target_set = faceimages[pasteindex]
            target_coords = target_set['coords']
            target_size = target_set['size']
            pil_image.paste(sourceimage.resize((target_size[0], target_size[1])), (target_coords[0], target_coords[1]))

        return pil_image, len(faces)
    else:
        pil_image = None
        return pil_image, len(faces)


def download_image(url):
    r = requests.get(url)
    image = Image.open(io.BytesIO(r.content))
    return image


def resize_image(image, ratio):
    current_w, current_h = image.size
    newsize = (int(current_w * ratio), int(current_h * ratio))
    newimage = image.resize(newsize)
    return newimage


def create_offset(baseimage, pasteimage):
    base_w, base_h = baseimage.size
    paste_w, paste_h = pasteimage.size
    xoffset = int(random.uniform(0, base_w - paste_w))
    yoffset = int(random.uniform(paste_h, base_h - paste_h))
    offset = (xoffset, yoffset)
    return offset


def get_picture_urls(twitter_handle):
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=twitter_handle,
                               count=200, include_rts=False,
                               exclude_replies=True)

    media_files = set()
    for status in tweets:
        media = status.entities.get('media', [])
        if (len(media) > 0):
            media_files.add(media[0]['media_url'])

    return media_files


def get_instagram_urls(instagram_name):
    url = "https://api.instagram.com/v1/tags/" + instagram_name + "/media/recent"
    params = {"access_token": "6028897716.87013fb.698e9cd3de0b4bab894668b7274515b2"}
    r = requests.get(url, params=params)
    obj = r.json()
    return obj


def get_tumblr_urls(tumblrname):
    media_files = set()
    url = "http://api.tumblr.com/v2/blog/" + tumblrname + "/posts/photo"
    params = {'api_key': 'gz3w6ATGCYRyIsijh5wPNuSkPUBSxbbCuueJx0vIAIqJhtoJjn', "limit": 100}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        obj = r.json()
        posts = obj['response']['posts']
        for tumblr_post in posts:
            photos = tumblr_post['photos']
            for phot in photos:
                media_files.add(phot['original_size']['url'])
    return media_files


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

twitterusr = sys.argv[1]
network = sys.argv[2]

if network == "twitter":
    media_files = get_picture_urls(twitterusr)
elif network == "tumblr":
    media_files = get_tumblr_urls(twitterusr)
else:
    media_files = [str(sys.argv[2])]

print(len(media_files))

target_folder = twitterusr
if os.path.exists(target_folder):
    target_folder = target_folder + "(" + datetime.datetime.now().strftime("%I:%M") + ")"
    os.mkdir(target_folder)
else:
    # os.mkdir(target_folder)
    print("none")

counter = 1
for simp in media_files:
    actual_photo = download_image(simp)
    actual_photo.save("temp.png")
    weird_image, faces = weird_photo("temp.png")
    image_filename = target_folder + "/" + str(counter) + ".png"
    image_filename_jpg = target_folder + "/" + str(counter) + ".jpg"
    if faces > 1:
        # weird_image = weird_image.quantize(20,2)
        weird_image.save(image_filename, compress_level=6)
    counter += 1
    os.remove("temp.png")
