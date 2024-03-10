import environ
from pathlib import Path
import sys
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# This allows easy placement of apps within the interior
# apps directory.
sys.path.append(str(BASE_DIR / "apps"))
env = environ.Env()

# Fetching
if not env.bool("ENV_FOR_RENDER",False):
    env_dir = os.path.join(BASE_DIR, "envs", ".env")
else:
    env_dir = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_dir):
    environ.Env.read_env(env_dir)
