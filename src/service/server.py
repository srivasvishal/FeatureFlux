from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from src.models import model_loader

app = FastAPI(
    title="FeatureFlux ML Serving API", 
    version="0.1.0",
    openapi_url=None,   # Disables the /openapi.json endpoint
    docs_url=None,      # Disables Swagger UI
    redoc_url=None      # Disables ReDoc
)

# Connect to Redis (using default host/port from docker-compose)
redis_client = redis.Redis(host="redis", port=6379)

class PredictRequest(BaseModel):
    model_name: str
    data: dict
    entity_id: str = None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: PredictRequest):
    features = {}
    if request.entity_id:
        raw = redis_client.hgetall(f"features:{request.entity_id}")
        features = {k.decode('utf-8'): float(v.decode('utf-8')) for k, v in raw.items()} if raw else {}
    try:
        result = model_loader.predict(request.model_name, request.data, features)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"model": request.model_name, "entity_id": request.entity_id, "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)