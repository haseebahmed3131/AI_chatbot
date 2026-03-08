from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from database import get_db, Trace
from models import TraceCreate, TraceResponse
from llm_service import classify_conversation

router = APIRouter(prefix="/traces", tags=["traces"])

@router.post("", response_model=TraceResponse)
def create_trace(trace: TraceCreate, db: Session = Depends(get_db)):
    """
    Create a new trace with automatic LLM classification.
    
    Flow:
    1. Receive user_message and bot_response
    2. Classify conversation using LLM
    3. Save trace with classification
    4. Return complete trace
    """
    try:
        # Classify the conversation
        category = classify_conversation(trace.user_message, trace.bot_response)
        
        # Create trace record
        trace_id = str(uuid.uuid4())
        db_trace = Trace(
            id=trace_id,
            user_message=trace.user_message,
            bot_response=trace.bot_response,
            category=category,
            response_time_ms=trace.response_time_ms
        )
        
        db.add(db_trace)
        db.commit()
        db.refresh(db_trace)
        
        return db_trace
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create trace: {str(e)}")

@router.get("", response_model=List[TraceResponse])
def get_traces(category: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all traces, optionally filtered by category.
    Returns traces in reverse chronological order (most recent first).
    """
    query = db.query(Trace)
    
    if category:
        query = query.filter(Trace.category == category)
    
    traces = query.order_by(Trace.timestamp.desc()).all()
    return traces
