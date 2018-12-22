from image_processing import process_image
from network_api.tumblr import Tumblr
from network_api.twitter import Twitter
from Utils import Utils

import random
import os
import sys





def main(image_url = '', social_page = '', network= ''):

    #twitter credential loading
    consumer_key = os.environ['consumer_key']
    consumer_secret = os.environ['consumer_secret']
    access_token = os.environ['access_token']
    access_secret = os.environ['access_seceret']

    #tumblr credential loading
    tumblr_key = os.environ['tumblr_api_key']

    if image_url == "":
        if social_page != '':
            if network.lower() == "twitter":
                image_urls = Twitter.get_image_urls(social_page, consumer_key, consumer_secret, access_token, access_secret)
            elif network.lower() == "tumblr":
                image_urls = Tumblr.get_image_urls(social_page,tumblr_key)
            else:
                raise ValueError("{} network not supported".format(social_page))
            random.shuffle(image_urls)
            image_url =image_urls[0]

    if image_url:
        downloaded_image = Utils.download_image(image_url)
        new_image_file = process_image.process_image(downloaded_image)

    else:
        print ("no images found")



if __name__ == "__main__":
    os.environ['consumer_key'] = ''
    os.environ['consumer_secret'] = ''
    os.environ['access_token'] = ''
    os.environ['access_seceret'] =''
    os.environ['tumblr_api_key'] = ""


    image_url = sys.argv[1]
    social_page = sys.argv[2]
    network = sys.argv[3]
    main(image_url=image_url,social_page=social_page,network=network)