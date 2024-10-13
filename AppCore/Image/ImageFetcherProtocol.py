from PIL import Image


class ImageFetcherProtocol:
    def fetch(self, image_url: str) -> Image.Image:
        raise Exception()