import requests


class Instagram:

    @staticmethod
    def get_instagram_urls(instagram_handle,access_token):
        url = "https://api.instagram.com/v1/tags/" + instagram_handle + "/media/recent"
        params = {"access_token": access_token}
        r = requests.get(url, params=params)
        obj = r.json()
        return obj