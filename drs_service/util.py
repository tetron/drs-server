class DRSBackend(object):
    """Stores and retrieves options.  Intended to be inherited."""
    def __init__(self, opts):
        """Parse and store options as a list of tuples."""
        self.pairs = []
        for o in opts if opts else []:
            k, v = o.split("=", 1)
            self.pairs.append((k, v))

    def getopt(self, p, default=None):
        """Returns the first option value stored that matches p or default."""
        for k, v in self.pairs:
            if k == p:
                return v
        return default

    def getoptlist(self, p):
        """Returns all option values stored that match p as a list."""
        optlist = []
        for k, v in self.pairs:
            if k == p:
                optlist.append(v)
        return optlist
