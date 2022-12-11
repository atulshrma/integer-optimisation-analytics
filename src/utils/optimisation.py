from enum import Enum
from src.config import MAX_K
from typing import List, Callable, Optional, Tuple


class OptType(str, Enum):
    naive = "naive"
    efficient = "efficient"


def naive(lists: List[List[int]], m: int, f: Callable) -> int:
    """
    :param lists: List of lists with values to choose from.
    :param m: Quotient of modulo operator.
    :param f: Function to map x to f.
    :return: Maximum
    """
    f_res = [[] for i in range(len(lists))]

    for i, sub_list in enumerate(lists):
        for j in range(len(sub_list)):
            if i == 0:
                f_res[i].append(f(sub_list[j]) % m)
            else:
                for k in range(len(f_res[i - 1])):
                    value = f_res[i - 1][k] + f(sub_list[j])
                    f_res[i].append(value % m)
    return max(f_res[-1])


def efficient(lists: List[List[int]], m: int, f: Callable) -> int:
    """
    :param lists: List of lists with values to choose from.
    :param m: Quotient of modulo operator.
    :param f: Function to map x to f.
    :return: Maximum
    """
    pass
