import hiyapyco

class Utils:

    def __init__(self):
        pass

    def merge(self, paths):
        return hiyapyco.load(paths, method=hiyapyco.METHOD_MERGE, interpolate=True, failonmissingfiles=True)
