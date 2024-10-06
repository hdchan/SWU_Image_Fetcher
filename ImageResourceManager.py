from PIL import Image
from CardResource import LocalCardResource, StagedCardResource
from PIL import Image, ImageDraw
import requests
import shutil
import os
from pathlib import Path

PRODUCTION_FILE_PATH = './production/'
PRODUCTION_PREVIEW_FILE_PATH = PRODUCTION_FILE_PATH + 'preview/'
CACHE_FILE_PATH = './cache/'
CACHE_PREVIEW_FILE_PATH = CACHE_FILE_PATH + 'preview/'
PNG_EXTENSION = '.png'

class ImageResourceManager:
    def __init__(self):
        
        self.production_resources = []
        self.staged_resources = []
        self.delegate = None

        self.generate_directories_if_needed()

    def generate_directories_if_needed(self):
        Path(PRODUCTION_PREVIEW_FILE_PATH).mkdir(parents=True, exist_ok=True)
        Path(CACHE_PREVIEW_FILE_PATH).mkdir(parents=True, exist_ok=True)

    def load_production_resources(self):
        """
        Will load images from production folder
        """
        self.generate_directories_if_needed()
        production_resources = []
        filelist = os.listdir('production')
        filelist.sort()
        for production_file_name in filelist[:]:
            if production_file_name.endswith(PNG_EXTENSION):
                resource = LocalCardResource()
                resource.file_name = production_file_name
                resource.display_name = production_file_name
                resource.image_path = f'{PRODUCTION_FILE_PATH}{production_file_name}'
                resource.image_preview_path = f'{PRODUCTION_PREVIEW_FILE_PATH}{production_file_name}'
                production_resources.append(resource)

                existing_preview_file = Path(f'{PRODUCTION_PREVIEW_FILE_PATH}{production_file_name}')
                if not existing_preview_file.is_file():
                    # regnerate preview file
                    large_img = Image.open(f'{PRODUCTION_FILE_PATH}{production_file_name}')
                    preview_img = self.downscale_image(large_img)
                    preview_img_path = f'{PRODUCTION_PREVIEW_FILE_PATH}{production_file_name}'
                    preview_img.save(preview_img_path)

        self.production_resources = production_resources
        self.delegate.rm_did_load_production_resources(self, production_resources)

    def generate_local_card_resource(self, remote_card_resource):
        """
        Caches image, and returns a preview image
        """
        self.generate_directories_if_needed()
        existing_file = Path(f'{CACHE_FILE_PATH}{remote_card_resource.identifier}{PNG_EXTENSION}')
        if existing_file.is_file():
            local_resource = LocalCardResource()
            local_resource.display_name = remote_card_resource.display_name
            local_resource.file_name = remote_card_resource.identifier
            local_resource.image_path = f'{CACHE_FILE_PATH}{remote_card_resource.identifier}{PNG_EXTENSION}'
            local_resource.image_preview_path = f'{CACHE_PREVIEW_FILE_PATH}{remote_card_resource.identifier}{PNG_EXTENSION}'
            return local_resource
        
        img_data = requests.get(remote_card_resource.image_url, stream=True).raw
        # TODO: rounded rect needs to be propotional to size of image
        large_img = self.add_corners(Image.open(img_data).convert('RGB'), 25)
        preview_img = self.downscale_image(large_img)
        large_image_path = f'{CACHE_FILE_PATH}{remote_card_resource.identifier}{PNG_EXTENSION}'
        large_img.save(large_image_path)
        preview_img_path = f'{CACHE_PREVIEW_FILE_PATH}{remote_card_resource.identifier}{PNG_EXTENSION}'
        preview_img.save(preview_img_path)

        local_resource = LocalCardResource()
        local_resource.display_name = remote_card_resource.display_name
        local_resource.file_name = remote_card_resource.identifier
        local_resource.image_path = large_image_path
        local_resource.image_preview_path = preview_img_path
        
        return local_resource

    def stage_resource(self, local_card_resource, index):
        staged_card_resource = StagedCardResource()
        staged_card_resource.local_card_resource = local_card_resource
        staged_card_resource.production_file_name = self.production_resources[index].file_name
        self.staged_resources.append(staged_card_resource)

    def unstage_resource(self, index):
        production_file_name = self.production_resources[index].file_name
        for i, resource in enumerate(self.staged_resources):
            if resource.production_file_name == production_file_name:
                self.staged_resources.pop(i)
                break

    def unstage_all_resources(self):
        self.staged_resources = []

    def publish_staged_resources(self):
        self.generate_directories_if_needed()
        for r in self.staged_resources:
            shutil.copy(r.local_card_resource.image_path, f'{PRODUCTION_FILE_PATH}{r.production_file_name}')
            shutil.copy(r.local_card_resource.image_preview_path, f'{PRODUCTION_PREVIEW_FILE_PATH}{r.production_file_name}')
        self.staged_resources = []
        
    def generate_new_file(self, file_name):
        self.generate_directories_if_needed()
        existing_file = Path(f'{PRODUCTION_FILE_PATH}{file_name}{PNG_EXTENSION}')
        if existing_file.is_file():
            raise Exception(f"File already exists: {file_name}{PNG_EXTENSION}")
        img = Image.new("RGB", (1, 1))
        img.save(f"{PRODUCTION_FILE_PATH}{file_name}{PNG_EXTENSION}", "PNG")

    def downscale_image(self, original_img):
        size = 256, 256
        preview_img = original_img.copy().convert('RGB')
        preview_img.thumbnail(size, Image.Resampling.LANCZOS)
        return preview_img

    def add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    