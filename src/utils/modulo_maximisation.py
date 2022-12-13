import itertools
import multiprocessing
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List, Callable
from .optimisations import slightly_efficient


MAX_K = int(os.getenv("MAX_K", 5))


def naive(lists: List[List[int]], m: int, f: Callable) -> int:
    """
    This function has a complexity of O(n ^ (m*k)), where `k` is the number of lists, `n` is the sum of sizes of lists and
    `m` is the factor of the total number of combinations by selecting one element from each list.
    This function computes all possible combinations of elements by selecting one value from each nested list.
    It then computes the maximum value of the modulo function from all combinations.

            Parameters:
                    lists (List[List[int]]):List of lists with values to choose from
                    m (int): Quotient of modulo operator
                    f (Callable): Function to map x to f

            Returns:
                    max_sum (int): Maximised value of the `∑(f(x)) % m` where x is one value from each nested list in lists
    """
    all_possible_combinations = itertools.product(*lists)
    max_sum = 0
    for combination in all_possible_combinations:
        local_sum = 0
        for num in combination:
            local_sum = local_sum + f(num)
        local_sum = local_sum % m
        if local_sum > max_sum:
            max_sum = local_sum
    return max_sum


def efficient(lists: List[List[int]], m: int, f: Callable) -> int:
    """
    This function has a complexity of O(n ^ k), where `k` is the number of lists and `n` is the sum of sizes of lists.
    The function computes the maximum value of the modulo function during each iteration, by leveraging the
    distributive property of the modulo function `(a + b) mod n = [(a mod n) + (b mod n)] mod n`.

    This also allows the function to be parallelised to achive better computational efficiency for higher values of `k`.

            Parameters:
                    lists (List[List[int]]):List of lists with values to choose from
                    m (int): Quotient of modulo operator
                    f (Callable): Function to map x to f

            Returns:
                    max_sum (int): Maximised value of the `∑(f(x)) % m` where x is one value from each nested list in lists
    """
    max_sum = 0

    def split(target: List):
        for i in range(0, len(target), MAX_K):
            yield target[i : i + MAX_K]

    while len(lists) > MAX_K:
        combined_batch_futures = []
        combined_batch_res = []
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count() - 2) as executor:
            for batch in split(lists):
                future = executor.submit(slightly_efficient, batch, m, f)
                combined_batch_futures.append(future)
            for res in as_completed(combined_batch_futures):
                _, subset_res = res.result()
                combined_batch_res.append(subset_res)
        lists = combined_batch_res

    max_sum, _ = slightly_efficient(lists, m, f)
    return max_sum
