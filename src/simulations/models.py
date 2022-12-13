from enum import Enum
from pydantic import BaseModel, Field
from typing import Callable, List


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


class BenchmarkResponseModel(BaseModel):
    label: OptType = Field(description="Type of algo that was benchmarked")
    mean_wall_time: float = Field(description="Mean execution time for algo")
    total_sim_time: float = Field(description="Total simulation time")

    class Config:
        use_enum_values = True


class OptimizeRequestModel(BaseModel):
    lists: List[List[int]] = Field(description="A Set of lists of integers")
    m: int = Field(description="Value of the modulo variable")
    f: Callable = Field(const=True, default=lambda x: x**2)


class OptimizeResponseModel(BaseModel):
    max: int = Field(description="Max value for the modulo function")


class CompareStatsModel(BaseModel):
    x: int
    y: List[BenchmarkResponseModel]


class CompareResponseModel(BaseModel):
    data: List[CompareStatsModel]
