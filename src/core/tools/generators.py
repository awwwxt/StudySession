from config import KEYLIST, CELLLIST

from random import randint, sample

def CreateCode() -> str:
    return "".join(sample(
        KEYLIST, 
        randint(30, 45)))

def GenCellName(start_from: int) -> str:
    if start_from < len(CELLLIST):
        return CELLLIST[start_from]
    else:
        return (CELLLIST[start_from // len(CELLLIST) - 1] + CELLLIST[start_from % len(CELLLIST)])