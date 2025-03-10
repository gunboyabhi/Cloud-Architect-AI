from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Cloud Architect AI Agent", version="1.0")

# Register API routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "home!"}
