from pydantic_settings import BaseSettings
from pydantic import BaseModel

class Scrolling(BaseModel):
    pixels: int = 1
    interval: float = 0.02

class Vertretungsplan(BaseModel):
    schulnummer: int = 10000000
    benutzer: str = "schueler"
    passwort: str = "password"

class Config(BaseSettings):
    vertretungsplan: Vertretungsplan = Vertretungsplan()
    scrolling: Scrolling = Scrolling()
    ticker: list[str] = ["Ticker sind Nachrichten die angezeigt werden", "Zeile 2"]
    dev: bool = False