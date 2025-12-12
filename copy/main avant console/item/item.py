class Item:
    def __init__(self, name, description, image_path):
        self.name = name
        self.description = description
        self.image_path = image_path

    def getName(self):
        return self.name

    def getImagePath(self):
        return self.image_path
    
    def onUse(self):
        pass

    def getDescription(self):
        return self.description