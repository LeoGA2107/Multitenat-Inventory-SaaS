from fastapi import FastAPI

app = FastAPI(title="Multitenant SaaS")

@app.get("/")
async def root():
    return {"message":"Hello world"}
