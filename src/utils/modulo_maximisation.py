from typing import List, Callable


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
    f_res = [[] for i in range(len(lists))]
    max_sum = 0
    for i, sub_list in enumerate(lists):
        for j in range(len(sub_list)):
            if i == 0:
                cur_sum = f(sub_list[j]) % m
                f_res[i].append(cur_sum)
                if cur_sum > max_sum:
                    max_sum = cur_sum
            else:
                for k in range(len(f_res[i - 1])):
                    value = f_res[i - 1][k] + f(sub_list[j])
                    cur_sum = value % m
                    f_res[i].append(cur_sum)
                    if cur_sum > max_sum:
                        max_sum = cur_sum
    return max_sum
