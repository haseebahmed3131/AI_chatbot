# SupportLens - Customer Support Chatbot Observability Platform

A lightweight observability platform for monitoring customer support chatbot conversations with automatic trace classification.

> 👋 **New Here?**: Start with [START_HERE.md](START_HERE.md) for a guided introduction.
>
> 🚀 **Quick Start**: See [QUICKSTART.md](QUICKSTART.md) for the fastest way to get running (3 steps, 2 minutes).
> 
> 📋 **Ready to Submit?**: See [FINAL_CHECKLIST.txt](FINAL_CHECKLIST.txt) for a printable submission checklist.
>
> 📚 **All Documentation**: See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for complete guide to all docs.

## Features

- Simple support chatbot with LLM-powered responses
- Automatic conversation classification into 5 categories
- Real-time observability dashboard with analytics
- Pre-seeded with 20 sample traces

## Tech Stack

- **Backend**: Python FastAPI
- **Frontend**: React + Vite
- **Database**: SQLite
- **LLM**: OpenAI API

## Prerequisites

- Docker & Docker Compose (recommended) OR
- Python 3.9+ and Node.js 18+
- OpenAI API key

## Setup Instructions

### Quick Start (Recommended)

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set: `OPENAI_API_KEY=your_key_here`

3. Run with Docker:
   ```bash
   docker-compose up
   ```

4. Open http://localhost:5173 in your browser

### Manual Setup (Alternative)

If you prefer to run without Docker:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here  # or set OPENAI_API_KEY=your_key_here on Windows
python seed_data.py
uvicorn main:app --reload --port 8000
```

**Frontend (in a new terminal):**
```bash
cd frontend
npm install
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Endpoints

- `POST /traces` - Create and classify a new trace
- `GET /traces` - List all traces (optional ?category= filter)
- `GET /analytics` - Get aggregate statistics

## Architecture

- FastAPI backend handles LLM calls and trace storage
- SQLite database for persistence
- React frontend with real-time dashboard
- Two-stage LLM flow: response generation + classification

## Project Structure

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for detailed architecture.

## Sample Pull Request

This repository includes a sample feature branch for demonstration:

**Feature**: CSV Export for Traces
- Branch: `feature/export-traces`
- See [FEATURE_BRANCH_GUIDE.md](FEATURE_BRANCH_GUIDE.md) for details
- Feature files in `feature-branch-files/` directory

To create the sample PR:
1. Commit main branch
2. Create feature branch: `git checkout -b feature/export-traces`
3. Apply changes from `feature-branch-files/`
4. Push and create PR on GitHub

## Key Features Demonstrated

✅ LLM-powered chatbot with custom system prompt  
✅ Automatic conversation classification (5 categories)  
✅ Real-time observability dashboard  
✅ Aggregate analytics with category breakdown  
✅ Trace filtering and detail expansion  
✅ Pre-seeded with 20 realistic traces  
✅ Clean API design with proper error handling  
✅ Responsive UI with color-coded categories  
✅ Docker support for easy deployment  

## Classification Prompt Quality

The classification prompt in `backend/llm_service.py` handles:
- Clear category definitions with examples
- Edge case handling (multi-topic messages)
- Priority rules (cancellation > billing)
- Distinction between similar categories (refund vs billing)
- Validation and normalization of LLM output

## Video Walkthrough

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for what to include in the Loom video.

## Documentation

This repository includes comprehensive documentation:
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete guide to all docs
- **[QUICKSTART.md](QUICKSTART.md)** - Fastest way to get started
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - How to test everything
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and fixes
- **[SUBMISSION_CHECKLIST.md](SUBMISSION_CHECKLIST.md)** - Pre-submission checklist
- **[LOOM_VIDEO_SCRIPT.md](LOOM_VIDEO_SCRIPT.md)** - Video recording guide

See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for the complete list.
