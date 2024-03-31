from ..cog_helpers.server_containers import ServerContainer
from pathlib import Path
import os
import json
here = os.path.dirname(__file__)

history = Path(here, "history.json")
if history.exists():
    with history.open(mode="r") as f:
        history_data = json.load(f)
    servers = ServerContainer.from_history(history_data)
else:
    servers = ServerContainer()
