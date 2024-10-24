import json
import os
from pathlib import Path

from ..cog_helpers.server_containers import ServerContainer

here = os.path.dirname(__file__)
history = Path(here, "history.json")
if history.exists():
    with history.open(mode="r") as f:
        history_data = json.load(f)
    servers = ServerContainer.from_history(history_data)
else:
    servers = ServerContainer()

# path to dispatch to other bots
RESOURCE_PATH = Path(here)
