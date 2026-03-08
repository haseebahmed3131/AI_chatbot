from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db, Trace
from models import AnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("", response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)):
    """
    Get aggregate statistics:
    - Total traces
    - Breakdown by category (count and percentage)
    - Average response time
    """
    # Total traces
    total_traces = db.query(Trace).count()
    
    if total_traces == 0:
        return AnalyticsResponse(
            total_traces=0,
            category_breakdown={},
            average_response_time=0.0
        )
    
    # Category breakdown
    category_counts = db.query(
        Trace.category,
        func.count(Trace.id).label('count')
    ).group_by(Trace.category).all()
    
    category_breakdown = {}
    for category, count in category_counts:
        percentage = (count / total_traces) * 100
        category_breakdown[category] = {
            "count": count,
            "percentage": round(percentage, 1)
        }
    
    # Average response time
    avg_response_time = db.query(
        func.avg(Trace.response_time_ms)
    ).scalar() or 0.0
    
    return AnalyticsResponse(
        total_traces=total_traces,
        category_breakdown=category_breakdown,
        average_response_time=round(avg_response_time, 2)
    )
