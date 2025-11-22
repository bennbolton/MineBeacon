import json
import os

class playerDB:
    def __init__(self, path='data/players.json'):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            self.data = {"players": {}}
            self._save()
        else:
            self._load()

    def _load(self):
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    def record_login(self, player):
        pass