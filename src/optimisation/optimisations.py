from typing import Callable, List, Tuple


def slightly_efficient(lists: List[List[int]], m: int, f: Callable):
    """
    This function has a complexity of O(n ^ k), where `k` is the number of lists and `n` is the sum of sizes of lists.
    The function computes the maximum value of the modulo function during each iteration, by leveraging the
    distributive property of the modulo function `(a + b) mod n = [(a mod n) + (b mod n)] mod n`.
    This function also has a smaller memory footprint than the `naive` solution.

            Parameters:
                    lists (List[List[int]]):List of lists with values to choose from
                    m (int): Quotient of modulo operator
                    f (Callable): Function to map x to f

            Returns:
                    max_sum (int): Maximised value of the `∑(f(x)) % m` where x is one value from each nested list in lists
    """
    prev = []
    current = []
    max_sum = 0
    for i, sub_list in enumerate(lists):
        current = []
        for j in range(len(sub_list)):
            if i == 0:
                local_max = f(sub_list[j]) % m
                current.append(local_max)
                if local_max > max_sum:
                    max_sum = local_max
            else:
                for k in range(len(prev)):
                    local_max = (prev[k] + f(sub_list[j]) % m) % m
                    current.append(local_max)
                    if local_max > max_sum:
                        max_sum = local_max
        prev = current
    return max_sum, current
