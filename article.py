class Article(object):
    def __init__(self):
        self.title = None
        self.name = None
        self.raw_text = None
        self.processed_text = None

    def set_title(self, title):
        self.title = title
    
    def set_name(self, name):
        self.name = name

    def set_raw_text(self, raw):
        self.raw_text = raw

    def set_processed_text(self, processed):
        self.processed_text = processed


