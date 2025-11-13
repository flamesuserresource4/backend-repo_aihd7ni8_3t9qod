import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Restaurant, Post

app = FastAPI(title="Additive Food Social Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Additive Food Social Platform API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Helper to parse ObjectId strings safely
class IdModel(BaseModel):
    id: str

# Restaurant endpoints
@app.post("/api/restaurants")
def create_restaurant(payload: Restaurant):
    try:
        inserted_id = create_document("restaurant", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/restaurants")
def list_restaurants():
    try:
        docs = get_documents("restaurant")
        # Convert ObjectId to string
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Posts endpoints
@app.post("/api/posts")
def create_post(payload: Post):
    try:
        inserted_id = create_document("post", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts")
def list_posts(restaurant_id: Optional[str] = None):
    try:
        filter_dict = {}
        if restaurant_id:
            filter_dict["restaurant_id"] = restaurant_id
        docs = get_documents("post", filter_dict=filter_dict)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
