from pydantic_settings import BaseSettings
from pydantic import BaseModel, ConfigDict
from pathlib import Path
import yaml

class Config(BaseSettings):
    model_config = ConfigDict(
        extra="ignore",
    )

    class Vertretungsplan(BaseModel):
        schulnummer: int = 10000000
        benutzer: str = "schueler"
        passwort: str = "password"

    class Content(BaseModel):
        ticker: list[str] = ["Alternative für die VpMobil24 App jetzt auf vertretungsapp.de!"]
        klassen: list[str] = ["5a", "5b", "5c", "6a", "6b", "6c", "7a", "7b", "7c", "8a", "8b", "8c", "9a", "9b", "9c", "10a", "10b", "10c"]
        klassendetailiert: list[str] = ["11", "12"]
        nuränderungen: bool = False
        scrollspeed: float = 0.02
        sidebar: bool = True

    vermächtnis: str | None = None
    dev: bool = False
    content: Content = Content()
    vertretungsplan: Vertretungsplan = Vertretungsplan()
    updatecycle: float = 1

def update_config_recursively(target, source_dict):
    """Recursively update config, handling nested BaseModels."""
    for param, value in source_dict.items():
        if hasattr(target, param):
            target_attr = getattr(target, param)
            if hasattr(target_attr, "model_dump") and isinstance(value, dict):
                update_config_recursively(target_attr, value)
            else:
                setattr(target, param, value)
        else:
            setattr(target, param, value)

def load_yaml(path: Path):
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def resolve_inheritance(name: str, configs: dict[str, Config]) -> Config:
    chain = []
    seen = set()
    current = name

    while current is not None:
        if current in seen:
            raise Exception(f"Zirkuläre Vererbung erkannt bei '{current}'.")

        seen.add(current)

        if current not in configs:
            raise Exception(f"Vermächtnis '{current}' nicht gefunden.")

        cfg_part = configs[current]
        chain.append((current, cfg_part))
        current = cfg_part.vermächtnis

    resolved = Config()

    for name, part in reversed(chain):
        print(f"Konfiguration wird von '{name}' geerbt.")
        update_config_recursively(resolved, part.model_dump(exclude_unset=True))

    return resolved
