import time, random
from tinder_client import TinderClient

class ChatterBot(object):

    def __init__(self, token):
        self.tinder_client = TinderClient(token)
        self.recs = self.tinder_client.get_recs()['results']
        self.matches = {}

    def choose_match(self):
        rec = self.recs.pop(0)['_id']
        handler = random.choice([self.tinder_client.like, self.tinder_client.dislike])
        handler(rec)