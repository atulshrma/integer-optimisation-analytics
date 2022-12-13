import random, time
from enum import Enum
from pydantic import BaseModel, Field
from statistics import fmean
from typing import Callable, List, Tuple
from utils.modulo_maximisation import naive, efficient


class OptType(str, Enum):
    naive = "naive"
    efficient = "efficient"


def default_function(x):
    return x**2


class BenchmarkRequestModel(BaseModel):
    replication: int = Field(description="No. of iterations the simulation should run")
    num_lists: int = Field(description="No. of lists contained in the set")
    num_elements: int = Field(description="Max. size of a list present in the set")
    f: Callable = Field(const=True, default=lambda x: x**2)

    class Config:
        use_enum_values = True


class OptimizeRequestModel(BaseModel):
    lists: List[List[int]] = Field(description="A Set of lists of integers")
    m: int = Field(description="Value of the modulo variable")
    f: Callable = Field(const=True, default=lambda x: x**2)


def get_sim_data(num_lists: int, num_elements: int) -> Tuple[List[List[int]], int]:
    M = random.randint(1, 100)
    lists = []
    lists.append(random.sample(range(1, 10**9), num_elements))
    while len(lists) <= num_lists:
        lists.append(random.sample(range(1, 10**9), random.randint(1, num_elements)))
    return list(lists), M


def benchmark_simulation(opt_type: OptType, replication: int, num_lists: int, num_elements: int):
    execution_times = []
    sim_start = time.time()
    for _ in range(replication):
        lists, m = get_sim_data(num_lists, num_elements)
        run_start = time.time()
        if opt_type == OptType.naive:
            _ = naive(lists, m, default_function)
        else:
            _ = efficient(lists, m, default_function)
        run_end = time.time()
        execution_times.append(run_end - run_start)
    sim_end = time.time()
    return {"mean_wall_time": fmean(execution_times), "total_sim_time": sim_end - sim_start}
