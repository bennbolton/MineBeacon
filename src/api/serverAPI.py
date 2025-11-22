from mcrcon import MCRcon
from .config import *
import psutil as psu

class ServerAPI:
    def __init__(self):
        self.ip = MINECRAFT_SERVER_IP
        self.port = MINECRAFT_RCON_PORT
        self.password = MINECRAFT_RCON_PASSWORD
        self.connection = None

    def connect(self):
        self.connection = MCRcon(self.ip, self.password, port=self.port)
        self.connection.connect()

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()

    def cmd(self, cmd: str) -> str:
        if not self.connection:
            self.connect()
        return self.connection.command(cmd)
    
    def get_online_players(self) -> list:
        resp = self.cmd("list")
        try:
            player_list = resp.split(": ")[1].split(", ")
            if player_list == [""]:
                return []
            return [Player(player, self) for player in player_list]
        except Exception:
            return []
        
    def get_sys_stats(self) -> dict:
        return {
            "cpu": psu.cpu_percent(),
            "ram": psu.virtual_memory().percent,
            "disk": psu.disk_usage("/").percent
        }
    


class Player:
    def __init__(self, name: str, server: ServerAPI):
        self.server = server
        self.name = name

    @property
    def pos(self):
        resp = self.server.cmd(f"data get entity {self.name} Pos")
        start = resp.index("[") + 1
        end = resp.index("]")
        inside = resp[start:end]
        nums = inside.split(", ")
        position = tuple([round(float(num[:-1]), 1) for num in nums])
        return position
