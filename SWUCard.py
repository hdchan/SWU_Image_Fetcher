
class SWUCard():
    def __init__(self):
        self.name = None
        self.set = None
        self.type = None
        self.front_art = None
        self.number = None
        self.back_art = None
        self.show_front = True

    @classmethod
    def from_json(cls, json):
        obj = cls.__new__(cls)
        super(SWUCard, obj).__init__()
        obj = SWUCard()
        obj.name = json['Name']
        obj.set = json['Set']
        obj.type = json['Type']
        obj.front_art = json['FrontArt']
        obj.number = json['Number']
        if 'BackArt' in json:
            obj.back_art = json['BackArt']
        return obj
    
    def card_art(self):
        if self.show_front:
            return self.front_art
        else:
            return self.back_art

    def unique_identifier(self):
        if self.show_front:
            return self.set + self.number
        else:
            return self.set + self.number + '-back'

    def friendly_display_name(self):
        if self.show_front:
            return f'[{self.set+self.number}] {self.name} - {self.type}'
        else:
            return f'[{self.set+self.number}] {self.name} - {self.type} (portrait)'
    
    def is_flippable(self):
        return self.back_art is not None

    def flip(self):
        self.show_front = not self.show_front
    
