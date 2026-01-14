import pkgutil
import importlib
from pathlib import Path

def auto_import_handlers():
    package_name = __name__
    package_path = Path(__file__).parent

    for module_info in pkgutil.walk_packages(
        path=[str(package_path)],
        prefix=package_name + "."
    ):
        module_name = module_info.name

        # пропускаем __init__
        if module_name.endswith(".__init__"):
            continue

        importlib.import_module(module_name)
