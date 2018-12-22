import requests
import io
from PIL import Image



class Utils:

    @staticmethod
    def download_image(url):
        print (url)
        r = requests.get(url)
        image = Image.open(io.BytesIO(r.content))
        image.save("temp.png")
        return "temp.png"
