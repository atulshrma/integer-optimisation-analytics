from fastapi import FastAPI
from simulations.router import sim_router

app = FastAPI()
app.include_router(sim_router)


@app.get("/")
async def root():
    return {"message": "Integer Optimisation Analytics. Visit http://127.0.0.1:8000/docs for API documentation"}
