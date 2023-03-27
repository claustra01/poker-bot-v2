import math
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

def exist_check(db:list[Player], key:str) -> bool:
    is_exist:bool = False
    for i in range(len(db)):
        if db[i].get_key() == key:
            is_exist = True
    return is_exist

def calc_win(winner:int, loser:int) -> float:
    return 1 / (1 + pow(10, (loser-winner)/400))

def calc_lose(winner:int, loser:int) -> float:
    return 1 / (1 + pow(10, (winner-loser)/400))

def calc_rate_adds(stack:int, winner:int, loser:int) -> float:
    return 4 * calc_lose(winner, loser) * pow(math.log(stack, 100), 1.5)