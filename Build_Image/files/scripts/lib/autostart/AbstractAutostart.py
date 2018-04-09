import threading


class AbstractAutostart(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(AbstractAutostart, self).__init__(*args, **kwargs)

    def run(self):
        pass
