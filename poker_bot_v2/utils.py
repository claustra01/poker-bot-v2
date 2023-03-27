from player import Player
from medals import Medals

def id_to_key(db:list[Player], id_or_key:str) -> str:
    for i in range(len(db)):
        if db[i].get_id() == id_or_key:
            return db[i].get_key()
    return id_or_key

def key_to_player(db:list[Player], key:str) -> Player:
    for i in range(len(db)):
        if db[i].get_key() == key:
            return db[i]
    return None
