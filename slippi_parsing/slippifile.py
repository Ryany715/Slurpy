class SlippiFile:
    """A slippi file"""


    def __init__(self, filename, lcancel, datetime=""):
        self.filename = filename
        self.lcancel = lcancel
        self.datetime = datetime

    def __repr__(self):
        return "Slippi('{}','{}')".format(self.filename, self.lcancel)

