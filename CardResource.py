class RemoteCardResource:
    def __init__(self):
        self.identifier = None
        self.display_name = None
        self.image_url = None

class StagedCardResource:
    def __init__(self):
        self.local_card_resource = None
        self.production_file_name = None

class LocalCardResource:
    def __init__(self):
        self.image_path = None
        self.image_preview_path = None
        self.file_name = None
        self.display_name = None