"""
server.py

A REST API server built using FastAPI.
It exposes endpoints for prediction, health check, and optionally training triggers.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import model_loader
from feature_store.store import RedisFeatureStore
import os

# Initialize FastAPI app with custom settings (disable OpenAPI docs if desired)
app = FastAPI(
    title="FeatureFlux ML Serving API",
    version="0.1.0",
    # Uncomment below to disable OpenAPI schema if needed:
    # openapi_url=None, docs_url=None, redoc_url=None
)

# Initialize Redis feature store.
# Use configuration from environment if needed.
redis_host = os.environ.get("REDIS_HOST", "redis")
store = RedisFeatureStore(host=redis_host)

class PredictRequest(BaseModel):
    model_name: str
    data: dict            # Raw input data for prediction
    entity_id: str = None # Optional entity identifier to fetch features from store

@app.get("/health")
def health_check():
    # Basic endpoint to check server status.
    return {"status": "ok"}

@app.post("/predict")
def predict(request: PredictRequest):
    try:
        # If an entity_id is provided, fetch stored features and merge with input.
        features = {}
        if request.entity_id:
            features = store.get_features(f"features:{request.entity_id}")
        # Call dynamic model loader for prediction.
        result = model_loader.predict(request.model_name, request.data, features)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"model": request.model_name, "entity_id": request.entity_id, "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)