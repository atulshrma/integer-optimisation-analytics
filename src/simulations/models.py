import random, time
from enum import Enum
from pydantic import BaseModel, Field
from statistics import fmean
from typing import Callable, List, Tuple
from utils.modulo_maximisation import naive, efficient


class OptType(str, Enum):
    naive = "naive"
    efficient = "efficient"


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


class Benchmark:
    @staticmethod
    def get_sim_data(params: BenchmarkRequestModel) -> Tuple[List[List[int]], int]:
        M = random.randint(0, 100)
        lists = []
        lists.append(random.sample(range(1, 10**9), params.num_elements))
        while len(lists) <= params.num_lists:
            lists.append(random.sample(range(1, 10**9), random.randint(1, params.num_elements)))
        return list(lists), M

    @staticmethod
    def benchmark_simulation(opt_type: OptType, params: BenchmarkRequestModel):
        execution_times = []
        for _ in range(params.replication):
            lists, m = Benchmark.get_sim_data(params)
            print(lists, m)
            start = time.time()
            if opt_type == OptType.naive:
                _ = naive(lists, m, params.f)
            else:
                _ = efficient(lists, m, params.f)
            end = time.time()
            execution_times.append(end - start)

        return {"mean_wall_time": fmean(execution_times)}
