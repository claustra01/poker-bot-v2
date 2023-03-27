from player import Player
from medals import Medals

def key_to_player(db:list[Player], key:str) -> Player:
    for i in range(len(db)):
        if db[i].get_key() == key:
            return db[i]
    return None