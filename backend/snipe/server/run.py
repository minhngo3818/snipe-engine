from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/")
def run_init():
    message = "Init Atouch Search Engine Server!"
    return JSONResponse(content=message)

@app.get("/search")
async def search():
    return "Search engine"
