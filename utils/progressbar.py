import sys

class ProgressBar:
    def __init__(self, size):
        self.size = size
        self.last_percentage = -1.0

    def update(self, position):
        percentage = (position + 1) / self.size
        if abs(percentage - self.last_percentage) < 0.005:
            #no visual change
            return
        self.last_percentage = percentage
        sys.stderr.write('\r')
        sys.stderr.write("[%-20s] %d%%" % ('='*int(20*percentage), 100*percentage))
        sys.stderr.flush()

    def clear(self):
        sys.stderr.write('\r' + ' '*26)
        sys.stderr.flush()

