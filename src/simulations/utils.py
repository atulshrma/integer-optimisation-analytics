import random, time
from .models import BenchmarkResponseModel, default_function, OptType
from statistics import fmean
from typing import List, Tuple
from utils.modulo_maximisation import naive, efficient


def get_sim_data(num_lists: int, num_elements: int, seed: int | float | str = None) -> Tuple[List[List[int]], int]:
    if seed:
        random.seed(seed)
    M = random.randint(1, 100)
    lists = []
    lists.append(random.sample(range(1, 10**9), num_elements))
    while len(lists) <= num_lists:
        lists.append(random.sample(range(1, 10**9), random.randint(1, num_elements)))
    return list(lists), M


def benchmark_simulation(
    opt_type: OptType, replication: int, num_lists: int, num_elements: int, seed: int | float | str = None
) -> BenchmarkResponseModel:
    execution_times = []
    sim_start = time.time()
    for _ in range(replication):
        lists, m = get_sim_data(num_lists, num_elements, seed=seed)
        run_start = time.time()
        if opt_type == OptType.naive:
            _ = naive(lists, m, default_function)
        else:
            _ = efficient(lists, m, default_function)
        run_end = time.time()
        execution_times.append(run_end - run_start)
    sim_end = time.time()
    return BenchmarkResponseModel(
        **{"label": opt_type, "mean_wall_time": fmean(execution_times), "total_sim_time": sim_end - sim_start}
    )
