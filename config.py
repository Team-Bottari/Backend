from settings import VERSION
from pathlib import Path
import os


MAIN_DIR = str(Path(__file__).parent)
MAIN_URL = "/api"+f"/{VERSION}"

MEMBER_URL = MAIN_DIR+"/member"


