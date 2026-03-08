from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TraceCreate(BaseModel):
    user_message: str
    bot_response: str
    response_time_ms: int

class TraceResponse(BaseModel):
    id: str
    user_message: str
    bot_response: str
    category: str
    timestamp: datetime
    response_time_ms: int

    class Config:
        from_attributes = True

class AnalyticsResponse(BaseModel):
    total_traces: int
    category_breakdown: dict
    average_response_time: float

class ChatRequest(BaseModel):
    message: str
