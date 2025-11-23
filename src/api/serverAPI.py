from mcrcon import MCRcon
from .config import *
import psutil as psu
from datetime import datetime
import time, os, subprocess

class ServerAPI:
    MAX_BACKUPS = 10
    def __init__(self):
        self.ip = MINECRAFT_SERVER_IP
        self.port = MINECRAFT_RCON_PORT
        self.password = MINECRAFT_RCON_PASSWORD
        self.dir = os.path.expanduser(SERVER_DIR)
        self.backupDir = os.path.join(self.dir, "backups")
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
            return player_list
        except Exception:
            return []
        
    def get_sys_stats(self) -> dict:
        return {
            "cpu": psu.cpu_percent(),
            "ram": psu.virtual_memory().percent,
            "disk": psu.disk_usage("/").percent
        }
    
    def make_backup(self):
        ts = datetime.now().strftime("%F_%H-%M-%S")
        dest = os.path.join(self.backupDir, f'backup_{ts}.tar.gz')
        os.makedirs(self.backupDir, exist_ok=True)
        self.cmd("say Attemping to backup server")
        self.cmd("save-off")
        self.cmd("save-all flush")

        time.sleep(1)

        subprocess.run(
            [
                "tar", "-czf", dest,
                "-C", self.dir,
                "world",
                "server.properties", "ops.json",
                "banned-players.json", "banned-ips.json",
                "mods", "config", "dashboard", "eula.txt", "startServer.sh"
            ]
        )

        self.cmd("save-on")
        self.cmd("say Backup Complete")

        files = os.listdir(self.backupDir)
        backups = [f for f in files if f.endswith(".tar.gz")]
        backups.sort()

        while len(backups) > self.MAX_BACKUPS:
            oldest = backups.pop(0)
            os.remove(os.path.join(self.backupDir, oldest))

    def get_latest_backup_datetime(self) -> datetime:
        backups = sorted(os.listdir(self.backupDir))
        latest = backups[-1][7:-7]
        return datetime.strptime(latest, "%Y-%m-%d_%H-%M-%S")