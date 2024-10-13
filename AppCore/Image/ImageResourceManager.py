import os
import shutil
import time
from functools import partial
from pathlib import Path

from PIL import Image, ImageDraw
from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

from AppCore.Image.ImageFetcherProvider import *
from AppCore.Models import LocalCardResource, StagedCardResource
from AppCore.Models.TradingCard import *
from typing import List

PRODUCTION_FILE_PATH = './production/'
PRODUCTION_PREVIEW_FILE_PATH = PRODUCTION_FILE_PATH + 'preview/'
CACHE_FILE_PATH = './cache/'
CACHE_PREVIEW_FILE_PATH = CACHE_FILE_PATH + 'preview/'
PNG_EXTENSION = '.png'
NORMAL_CARD_HEIGHT = 468
NORMAL_CARD_WIDTH = 652
THUMBNAIL_SIZE = 256
ROUNDED_CORNERS = 25
ROUNDED_CORDERS_MULTIPLIER_RELATIVE_TO_HEIGHT = ROUNDED_CORNERS / NORMAL_CARD_HEIGHT

class ImageResourceManager:
    def __init__(self, image_fetcher_provider: ImageFetcherProvider):
        self.image_fetcher_provider = image_fetcher_provider
        self.production_resources: List[LocalCardResource] = []
        self.staged_resources: List[StagedCardResource] = []
        self.delegate = None
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(1)

        self.generate_directories_if_needed()

    def generate_directories_if_needed(self):
        Path(PRODUCTION_PREVIEW_FILE_PATH).mkdir(parents=True, exist_ok=True)
        Path(CACHE_PREVIEW_FILE_PATH).mkdir(parents=True, exist_ok=True)

    def load_production_resources(self):
        """
        Will load images from production folder
        """
        self.generate_directories_if_needed()
        local_resources: List[LocalCardResource] = []
        filelist = os.listdir('production')
        filelist.sort()
        for production_file_name in filelist[:]:
            if production_file_name.endswith(PNG_EXTENSION):
                image_path = f'{PRODUCTION_FILE_PATH}{production_file_name}'
                image_preview_path = f'{PRODUCTION_PREVIEW_FILE_PATH}{production_file_name}'
                resource = LocalCardResource(image_path, image_preview_path, production_file_name, production_file_name)
                resource.is_ready = True
                local_resources.append(resource)

                existing_preview_file = Path(f'{PRODUCTION_PREVIEW_FILE_PATH}{production_file_name}')
                if not existing_preview_file.is_file():
                    # regnerate preview file
                    large_img = Image.open(f'{PRODUCTION_FILE_PATH}{production_file_name}')
                    preview_img = self.downscale_image(large_img)
                    preview_img_path = f'{PRODUCTION_PREVIEW_FILE_PATH}{production_file_name}'
                    preview_img.save(preview_img_path)

        self.production_resources = local_resources
        self.delegate.rm_did_load_production_resources(self, local_resources)

    def generate_local_card_resource(self, trading_card: TradingCard):
        """
        Caches image, and returns a local resource
        """
        image_path = f'{CACHE_FILE_PATH}{trading_card.unique_identifier}{PNG_EXTENSION}'
        image_preview_path = f'{CACHE_PREVIEW_FILE_PATH}{trading_card.unique_identifier}{PNG_EXTENSION}'
        
        local_resource = LocalCardResource.from_trading_card(trading_card, image_path, image_preview_path)
        local_resource.is_ready = True
        
        existing_file = Path(f'{CACHE_FILE_PATH}{trading_card.unique_identifier}{PNG_EXTENSION}')
        if existing_file.is_file():
            return local_resource
        
        large_image_path = f'{CACHE_FILE_PATH}{trading_card.unique_identifier}{PNG_EXTENSION}'
        preview_img_path = f'{CACHE_PREVIEW_FILE_PATH}{trading_card.unique_identifier}{PNG_EXTENSION}'
        local_resource.image_path = large_image_path
        local_resource.image_preview_path = preview_img_path
        local_resource.is_ready = False
        return local_resource

    def stage_resource(self, local_card_resource: LocalCardResource, index: int):
        # TODO: Handle case where cache is emptied
        staged_card_resource = StagedCardResource(local_card_resource, 
                                                  self.production_resources[index].file_name)
        self.staged_resources.append(staged_card_resource)

    def unstage_resource(self, index: int):
        production_file_name = self.production_resources[index].file_name
        for i, resource in enumerate(self.staged_resources):
            if resource.production_file_name == production_file_name:
                self.staged_resources.pop(i)
                break

    def unstage_all_resources(self):
        self.staged_resources = []

    def can_publish_staged_resources(self):
        if len(self.staged_resources) == 0:
            return False
        for resource in self.staged_resources:
            if not resource.local_card_resource.is_ready:
                return False
        return True

    def publish_staged_resources(self):
        # TODO: handle case where cache is emptied
        """
        Publishes staged resources. Returns True if success.
        Otherwise returns false.
        """
        if self.can_publish_staged_resources():
            self.generate_directories_if_needed()
            for r in self.staged_resources:
                shutil.copy(r.local_card_resource.image_path, f'{PRODUCTION_FILE_PATH}{r.production_file_name}')
                shutil.copy(r.local_card_resource.image_preview_path, f'{PRODUCTION_PREVIEW_FILE_PATH}{r.production_file_name}')
            self.staged_resources = []
            return True
        else:
            return False
        
    def generate_new_file(self, file_name: str):
        self.generate_directories_if_needed()
        existing_file = Path(f'{PRODUCTION_FILE_PATH}{file_name}{PNG_EXTENSION}')
        if existing_file.is_file():
            raise Exception(f"File already exists: {file_name}{PNG_EXTENSION}")
        img = Image.new("RGB", (1, 1))
        img.save(f"{PRODUCTION_FILE_PATH}{file_name}{PNG_EXTENSION}", "PNG")

    def async_store_local_resource(self, trading_card: TradingCard, local_resource: LocalCardResource):
        if local_resource.is_ready:
             # this needs to be called only when we don't have a local resource
            return
        self.generate_directories_if_needed()
        # TODO: might need to prevent duplicate calls?
        # https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
        worker = StoreImageWorker(trading_card, local_resource, self.image_fetcher_provider)
        worker.signals.finished.connect(partial(self._finish_storing_local_resource))
        self.pool.start(worker)

    def _finish_storing_local_resource(self, local_resource: LocalCardResource):
        self.delegate.rm_did_finish_storing_local_resource(self, local_resource)

    # TODO: Remove when refactored
    def downscale_image(self, original_img: Image.Image) -> Image.Image:
        size = THUMBNAIL_SIZE, THUMBNAIL_SIZE
        preview_img = original_img.copy().convert('RGB')
        preview_img.thumbnail(size, Image.Resampling.LANCZOS)
        return preview_img

# https://stackoverflow.com/questions/13909195/how-run-two-different-threads-simultaneously-in-pyqt
class WorkerSignals(QObject):
    finished = pyqtSignal(object)

class StoreImageWorker(QRunnable):
    def __init__(self, trading_card: TradingCard, local_resource: LocalCardResource, image_fetcher_provider: ImageFetcherProvider):
        super(StoreImageWorker, self).__init__()
        self.trading_card = trading_card
        self.local_resource = local_resource
        self.image_fetcher_provider = image_fetcher_provider
        self.signals = WorkerSignals()

    def run(self):
        # time.sleep(5)
        self.store_local_resource(self.trading_card, self.local_resource)

    def store_local_resource(self, trading_card: TradingCard, local_resource: LocalCardResource):
        img = self.image_fetcher_provider.provideImageFetcher().fetch(trading_card.image_url)
        img_height = min(img.height, img.width)
        rad = int(img_height * ROUNDED_CORDERS_MULTIPLIER_RELATIVE_TO_HEIGHT)
        # TODO: rounded rect needs to be propotional to size of image
        large_img = self._add_corners(img.convert('RGB'), rad)
        preview_img = self._downscale_image(large_img)
        large_img.save(local_resource.image_path)
        preview_img.save(local_resource.image_preview_path)
        local_resource.is_ready = True
        self.signals.finished.emit(local_resource)

    def _downscale_image(self, original_img: Image.Image) -> Image.Image:
        size = THUMBNAIL_SIZE, THUMBNAIL_SIZE
        preview_img = original_img.copy().convert('RGBA')
        preview_img.thumbnail(size)
        return preview_img

    def _add_corners(self, im: Image.Image, rad: int) -> Image.Image:
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
    