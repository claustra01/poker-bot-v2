import math

def calc_win(winner:int, loser:int) -> float:
    return 1 / (1 + pow(10, (loser-winner)/400))

def calc_lose(winner:int, loser:int) -> float:
    return 1 / (1 + pow(10, (winner-loser)/400))

def calc_rate_adds(stack:int, winner:int, loser:int) -> float:
    return 4 * calc_lose(winner, loser) * pow(math.log(stack, 100), 1.5)