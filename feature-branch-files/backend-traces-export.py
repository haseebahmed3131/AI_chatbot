# Add this to backend/routers/traces.py after the get_traces function

from fastapi.responses import StreamingResponse
import io
import csv

@router.get("/export")
def export_traces(category: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Export traces to CSV format.
    Optionally filter by category.
    """
    query = db.query(Trace)
    
    if category:
        query = query.filter(Trace.category == category)
    
    traces = query.order_by(Trace.timestamp.desc()).all()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Timestamp', 'User Message', 'Bot Response', 'Category', 'Response Time (ms)'])
    
    # Write data
    for trace in traces:
        writer.writerow([
            trace.timestamp.isoformat(),
            trace.user_message,
            trace.bot_response,
            trace.category,
            trace.response_time_ms
        ])
    
    # Prepare response
    output.seek(0)
    filename = f"supportlens_traces_{category.lower().replace(' ', '_') if category else 'all'}.csv"
    
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
