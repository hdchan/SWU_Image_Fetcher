from typing import Optional

from .TradingCard import TradingCard
class LocalCardResource:
    
    def __init__(self, image_path: str, 
                 image_preview_path: str, 
                 file_name: str, 
                 display_name: str, 
                 remote_image_url: Optional[str] = None):
        self.image_path = image_path
        self.image_preview_path = image_preview_path
        self.file_name = file_name
        self.display_name = display_name
        self.remote_image_url = remote_image_url
        self.is_ready = False
        
    @classmethod
    def from_trading_card(cls,
                          trading_card: TradingCard,
                          image_path: str, 
                          image_preview_path: str):
        obj = cls.__new__(cls)
        super(LocalCardResource, obj).__init__()
        obj.image_path = image_path
        obj.image_preview_path = image_preview_path
        obj.file_name = trading_card.unique_identifier
        obj.display_name = trading_card.friendly_display_name
        obj.remote_image_url = trading_card.image_url
        return obj
    
class StagedCardResource:
    def __init__(self, local_card_resource: LocalCardResource, production_file_name: str):
        self.local_card_resource = local_card_resource
        self.production_file_name = production_file_name