import requests

class Tumblr:

    @staticmethod
    def get_image_urls(tumblrname, api_key):
        media_files = set()
        url = "http://api.tumblr.com/v2/blog/" + tumblrname + "/posts/photo"
        params = {'api_key': api_key, "limit": 100}
        r = requests.get(url, params=params)
        if r.status_code == 200:
            obj = r.json()
            posts = obj['response']['posts']
            for tumblr_post in posts:
                photos = tumblr_post.get('photos',[])
                for phot in photos:
                    media_files.add(phot['original_size']['url'])
        return list(media_files)