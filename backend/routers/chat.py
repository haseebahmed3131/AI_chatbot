from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ChatRequest, TraceResponse, TraceCreate
from llm_service import generate_chatbot_response
from routers.traces import create_trace

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=TraceResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Handle chat message:
    1. Generate bot response using LLM
    2. Create trace (which triggers classification)
    3. Return complete trace with classification
    """
    try:
        # Generate chatbot response
        bot_response, response_time_ms = generate_chatbot_response(request.message)
        
        # Create trace (this will classify and save)
        trace_data = TraceCreate(
            user_message=request.message,
            bot_response=bot_response,
            response_time_ms=response_time_ms
        )
        
        trace = create_trace(trace_data, db)
        return trace
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
