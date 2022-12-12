from fastapi import APIRouter
from simulations.models import OptType, OptimizeRequestModel, BenchmarkRequestModel, Benchmark
from utils.modulo_maximisation import naive, efficient

sim_router = APIRouter()


@sim_router.post("/benchmark/{type}")
async def benchmark_algo(type: OptType, params: BenchmarkRequestModel):
    return Benchmark.benchmark_simulation(type, params)


@sim_router.post("/optimize/{type}")
async def run_algo(type: OptType, params: OptimizeRequestModel):
    if type == OptType.naive:
        max_sum = naive(params.lists, params.m, params.f)
    else:
        max_sum = efficient(params.lists, params.m, params.f)
    return {"max": max_sum}
