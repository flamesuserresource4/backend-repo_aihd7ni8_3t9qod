"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Core app schemas

class Restaurant(BaseModel):
    """
    Restaurants collection schema
    Collection name: "restaurant"
    """
    name: str = Field(..., description="Restaurant name")
    cuisine: Optional[str] = Field(None, description="Cuisine type")
    description: Optional[str] = Field(None, description="Short description")
    image_url: Optional[str] = Field(None, description="Cover image URL")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    is_open: bool = Field(True, description="Open status")

class Post(BaseModel):
    """
    Social posts related to food/restaurants
    Collection name: "post"
    """
    restaurant_id: Optional[str] = Field(None, description="Related restaurant ObjectId as string")
    author: str = Field(..., description="Author display name")
    content: str = Field(..., description="Post text content")
    images: Optional[List[str]] = Field(default=None, description="Image URLs")
    rating: Optional[int] = Field(default=None, ge=1, le=5, description="Optional rating 1-5")

# Example schemas (kept for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
