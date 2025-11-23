from dotenv import load_dotenv
import os

load_dotenv()

MINECRAFT_SERVER_IP = os.getenv("MINECRAFT_SERVER_IP")
MINECRAFT_RCON_PORT = int(os.getenv("MINECRAFT_RCON_PORT"))
MINECRAFT_RCON_PASSWORD = os.getenv("MINECRAFT_RCON_PASSWORD")
SERVER_DIR = os.getenv("SERVER_DIR")
