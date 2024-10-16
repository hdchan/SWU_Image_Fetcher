from typing import Optional

class LocalCardResource:
    
    def __init__(self, 
                 image_path: str,
                 image_preview_path: str,
                 file_name: str,
                 display_name: str,
                 file_extension: str,
                 remote_image_url: Optional[str] = None):
        self.image_path = image_path
        self.image_preview_path = image_preview_path
        self.file_name = file_name
        self.display_name = display_name
        self.remote_image_url = remote_image_url
        self.file_extension = file_extension
        self.is_ready = False
    
class StagedCardResource:
    # TODO: might want to use trading card instead of local card resource
    def __init__(self, local_card_resource: LocalCardResource, production_file_name: str):
        self.local_card_resource = local_card_resource
        self.production_file_name = production_file_name