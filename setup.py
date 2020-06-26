import os
import importlib.util
from setuptools import setup

# Boilerplate to load commonalities
spec = importlib.util.spec_from_file_location(
    "setup_common", os.path.join(os.path.dirname(__file__), "setup_common.py")
)
common = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common)

common.KWARGS["install_requires"] += ["aiohttp>=3.6.2"]
common.KWARGS["entry_points"] = {
    "dffml.operation": [
        f"usreps.or_address_to_cords = {common.IMPORT_NAME}.oregon:or_address_to_cords",
        f"usreps.or_find_reps = {common.IMPORT_NAME}.oregon:or_find_reps",
    ]
}

setup(**common.KWARGS)
