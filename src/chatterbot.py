import time, random
from threading import Timer
from tinder_client import TinderClient

class ChatterBot(object):

    def __init__(self, token):
        self.is_running = False
        self.timer = None
        self.tinder_client = TinderClient(token)
        self.recs = self.tinder_client.get_recs()
        self.matches = {}

    def choose_match(self):
        rec = self.recs.pop(0)['_id']
        handler = random.choice([self.tinder_client.like, self.tinder_client.dislike])
        handler(rec)

    def start(self):
        if not self.is_running:
            self.timer = Timer(5, self.run)
            self.timer.daemon = True
            self.timer.start()
            self.is_running = True

    def stop(self):
        self.timer.cancel()
        self.is_running = False

    def run(self):
        self.is_running = False
        self.start()
        # Refresh recs if necessary
        if not self.recs:
            self.recs = self.tinder_client.get_recs()
        self.choose_match()