import os
import shutil
import subprocess
from datetime import datetime

from tqdm import tqdm

SOURCE = os.path.expanduser("~/.config")
DEST_BASE = "/Volumes/ARCH/config-backups"
folders_to_backup = ["ghostty", "zsh"]
exclude_map = {
    "zsh": [
        ".git",
        "plugins",
        ".zcompcache",
        ".zsh_sessions",
    ],  # Do not copy 'cache' in 'nvim'
    # 'alacritty': ['some_subdir'],  # Add more as needed
}
max_versions = 5


def limit_backups(base_dir, max_versions=5):
    backups = [d for d in os.listdir(base_dir) if d.startswith("backup_")]
    backups.sort()
    while len(backups) >= max_versions:
        oldest = backups.pop(0)
        shutil.rmtree(os.path.join(base_dir, oldest))


os.makedirs(DEST_BASE, exist_ok=True)
limit_backups(DEST_BASE, max_versions)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
DEST = os.path.join(DEST_BASE, f"backup_{timestamp}")
os.makedirs(DEST, exist_ok=True)


def backup_folder(folder):
    src_path = os.path.join(SOURCE, folder)
    dest_path = os.path.join(DEST, folder)
    cmd = ["rsync", "-arv", "--delete"]
    for subfolder in exclude_map.get(folder, []):
        cmd.append(f"--exclude={subfolder}/")
    cmd += [f"{src_path}/", dest_path]
    subprocess.run(cmd, check=True)


# Progress bar for folders
with tqdm(
    total=len(folders_to_backup), desc="Backing up folders", unit="folder"
) as pbar:
    for folder in folders_to_backup:
        backup_folder(folder)
        pbar.update(1)

print(f"Backup completed: {DEST}")
