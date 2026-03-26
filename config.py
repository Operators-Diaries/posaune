from pydantic_settings import BaseSettings
from pydantic import BaseModel

class Config(BaseSettings):

    class Vertretungsplan(BaseModel):
        schulnummer: int = 10000000
        benutzer: str = "schueler"
        passwort: str = "password"

    class Content(BaseModel):
        class Scrolling(BaseModel):
            pixels: int = 1
            interval: float = 0.02

        ticker: list[str] = ["Alternative für die VpMobil24 App jetzt auf vertretungsapp.de!"]
        klassen: list[str] = ["5a", "5b", "5c", "6a", "6b", "6c", "7a", "7b", "7c", "8a", "8b", "8c", "9a", "9b", "9c", "10a", "10b", "10c"]
        klassendetailiert: list[str] = ["11", "12"]
        scrolling: Scrolling = Scrolling()
        sidebar: bool = True

    dev: bool = False
    content: Content = Content()
    vertretungsplan: Vertretungsplan = Vertretungsplan()
    updatecycle: float = 5