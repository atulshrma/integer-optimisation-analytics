from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Integer Optimisation Analytics. Visit http://127.0.0.1:8000/redoc for API documentation"}
