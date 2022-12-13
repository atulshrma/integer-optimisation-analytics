import asyncio, concurrent
from fastapi import APIRouter
from simulations.models import OptType, OptimizeRequestModel, BenchmarkRequestModel, benchmark_simulation
from utils.modulo_maximisation import naive, efficient

sim_router = APIRouter()


@sim_router.post("/benchmark/{opt_type}")
async def benchmark_algo(opt_type: OptType, params: BenchmarkRequestModel):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, benchmark_simulation, opt_type, params.replication, params.num_lists, params.num_elements
        )
    return result


@sim_router.post("/optimize/{opt_type}")
async def run_algo(opt_type: OptType, params: OptimizeRequestModel):
    if opt_type == OptType.naive:
        max_sum = naive(params.lists, params.m, params.f)
    else:
        max_sum = efficient(params.lists, params.m, params.f)
    return {"max": max_sum}
