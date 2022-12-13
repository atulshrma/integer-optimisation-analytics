import asyncio, concurrent
from fastapi import APIRouter
from simulations.models import (
    OptType,
    OptimizeRequestModel,
    OptimizeResponseModel,
    BenchmarkRequestModel,
    BenchmarkResponseModel,
    CompareStatsModel,
    CompareResponseModel,
)
from simulations.utils import benchmark_simulation
from optimisation.modulo_maximisation import naive, efficient

sim_router = APIRouter()


@sim_router.post("/benchmark/{opt_type}", response_model=BenchmarkResponseModel)
async def benchmark_algo(opt_type: OptType, params: BenchmarkRequestModel):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, benchmark_simulation, opt_type, params.replication, params.num_lists, params.num_elements
        )
    return result


@sim_router.post("/optimize/{opt_type}", response_model=OptimizeResponseModel)
async def run_algo(opt_type: OptType, params: OptimizeRequestModel):
    if opt_type == OptType.naive:
        max_sum = naive(params.lists, params.m, params.f)
    else:
        max_sum = efficient(params.lists, params.m, params.f)
    return OptimizeResponseModel(**{"max": max_sum})


@sim_router.post("/compare_algo", response_model=CompareResponseModel)
async def compare_algo():
    """This route generates and returns stats for the two optimisation algorithms, that can be used to plot the differences in performance between the two algorithms as a function of `num_lists`
    Ideally something like this would not run the algorithms everytime, but for the purpose of demonstration it runs the same benchmark simulation for a case, one that best shows the difference
    between the two algorithms, every time the API is invoked.
    """
    loop = asyncio.get_event_loop()
    result = {"data": []}
    seed = "TEST_SEED"
    for k in range(4, 9):
        stats_for_k = []
        params = BenchmarkRequestModel(replication=3, num_elements=10, num_lists=k)
        with concurrent.futures.ProcessPoolExecutor() as pool:
            stats_for_k.append(
                loop.run_in_executor(
                    pool,
                    benchmark_simulation,
                    OptType.naive,
                    params.replication,
                    params.num_lists,
                    params.num_elements,
                    seed,
                )
            )
            stats_for_k.append(
                loop.run_in_executor(
                    pool,
                    benchmark_simulation,
                    OptType.efficient,
                    params.replication,
                    params.num_lists,
                    params.num_elements,
                    seed,
                )
            )

            stats_data = CompareStatsModel(**{"x": k, "y": []})
            for stats in await asyncio.gather(*stats_for_k):
                stats_data.y.append(stats)
            result["data"].append(stats_data)
    return CompareResponseModel(**result)
