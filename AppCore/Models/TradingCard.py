from typing import Optional


class TradingCard:
    def __init__(self, 
                 name: str, 
                 set: str, 
                 type: str, 
                 front_art: str, 
                 number: str, 
                 back_art: Optional[str] = None):
        super().__init__()
        self.name: str = name
        self.set: str = set
        self.type: str = type
        self.front_art: str = front_art
        self.number: str = number
        self.back_art: Optional[str] = back_art
        self.show_front: bool = True

    @property
    def image_url(self) -> str:
        if self.show_front:
            return self.front_art
        else:
            if self.back_art is None:
                return self.front_art
            else:
                return self.back_art

    @property
    def unique_identifier(self) -> str:
        if self.show_front:
            return self.set + self.number
        else:
            return self.set + self.number + '-back'

    @property
    def friendly_display_name(self) -> str:
        if self.show_front:
            return f'[{self.set+self.number}] {self.name} - {self.type}'
        else:
            return f'[{self.set+self.number}] {self.name} - {self.type} (back)'
    
    @property
    def is_flippable(self) -> bool:
        return self.back_art is not None

    def flip(self):
        self.show_front = not self.show_front
    
