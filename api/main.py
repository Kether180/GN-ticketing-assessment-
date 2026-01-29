from fastapi import FastAPI
from api.routes.tickets import router as tickets_router

app = FastAPI(
    title="Ticketing API",
    description="A simple support ticketing system",
    version="1.0.0",
)

app.include_router(tickets_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}
