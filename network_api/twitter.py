import tweepy
from tweepy import OAuthHandler
import json
import io
import requests
import random
import time
import datetime


class Twitter:

    @staticmethod
    def get_image_urls(twitter_handle, consumer_key, consumer_secret, access_token, access_secret):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name=twitter_handle,
                                   count=100, include_rts=False,
                                   exclude_replies=True)
        media_files = set()
        for status in tweets:
            media = status.entities.get('media', [])
            if (len(media) > 0):
                media_files.add(media[0]['media_url'])

        return list(media_files)