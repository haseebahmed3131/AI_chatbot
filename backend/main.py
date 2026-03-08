from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import traces, analytics, chat

# Initialize database
init_db()

app = FastAPI(title="SupportLens API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(traces.router)
app.include_router(analytics.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "SupportLens API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
