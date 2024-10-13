import random
from urllib.parse import urlparse

import requests
from PIL import Image, ImageDraw, ImageFont

from ..ImageFetcherProtocol import *


class MockImageFetcher(ImageFetcherProtocol):
    def fetch(self, image_url: str) ->Image.Image:
        parsed_url = urlparse(image_url)
        file_name = parsed_url.path.split('/')[-1]
        color_palette = [
            (255, 179, 186),
            (255, 223, 186),
            (255, 255, 186),
            (186, 255, 201),
            (186, 255, 255)
        ]
        selected_color = random.choice(color_palette)
        if '-b.png' in file_name:
            img = Image.new("RGB", (300, 200), selected_color)
        else:
            img = Image.new("RGB", (200, 300), selected_color)
        I1 = ImageDraw.Draw(img)
 
        # Add Text to an image
        myFont = ImageFont.truetype('arial.ttf', 20)
        I1.text((0, 100), file_name, font=myFont, fill=(0, 0, 0))
        return img

class RemoteImageFetcher(ImageFetcherProtocol):
    def fetch(self, image_url: str) -> Image.Image:
        # TODO: retry if failed, and delete from cache
        img_data = requests.get(image_url, stream=True).raw
        img = Image.open(img_data)
        return img