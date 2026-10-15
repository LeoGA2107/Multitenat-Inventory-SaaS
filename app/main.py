from fastapi import FastAPI
from app.routers import auth, users

app = FastAPI(title="Multitenant SaaS")


app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message":"Hello world"}
