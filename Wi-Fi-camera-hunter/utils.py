import os
import subprocess
import logging
from colorama import init, Fore, Style

init(autoreset=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_root():
    if os.geteuid() != 0:
        logger.error("Program requires root privileges!")
        exit(1)

def check_monitor_support(iface):
    try:
        out = subprocess.check_output(
            ["iw", "list"],
            stderr=subprocess.STDOUT
        ).decode(errors="ignore")

        return "* monitor" in out

    except Exception:
        return False
        
def create_temp_dir():
    os.makedirs("temp", exist_ok=True)
