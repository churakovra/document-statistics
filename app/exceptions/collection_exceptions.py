class BaseCollectionNotFoundException(Exception):
    def __init__(self):
        self.message = f"Base collection  were not found"
