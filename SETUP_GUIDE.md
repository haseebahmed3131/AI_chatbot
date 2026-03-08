# SupportLens Setup Guide

## Video Walkthrough

For a complete walkthrough, watch the Loom video: [Link to be added]

## What You'll See

1. **Dashboard Tab**: 
   - Analytics overview with total traces and average response time
   - Category breakdown showing distribution across 5 categories
   - Trace list with all conversations
   - Click any trace to expand and see full details
   - Filter traces by category

2. **Chatbot Tab**:
   - Simple chat interface
   - Type a message and get an AI-powered response
   - Each conversation is automatically classified
   - New traces appear immediately on the dashboard

## Pre-seeded Data

The application comes with 20 sample traces covering all categories:
- Billing: 4 traces
- Refund: 3 traces
- Account Access: 4 traces
- Cancellation: 4 traces
- General Inquiry: 5 traces

## Testing the Live Flow

1. Go to the Chatbot tab
2. Type a message like "I want a refund"
3. Wait for the bot response
4. Switch to Dashboard tab
5. See your new trace at the top of the list with its classification

## Classification Logic

The system uses a two-stage LLM approach:

1. **Response Generation**: GPT-3.5-turbo generates the support response
2. **Classification**: A second LLM call analyzes both the user message and bot response to assign one of five categories

The classification prompt handles edge cases:
- Multi-topic messages (chooses primary intent)
- Cancellation takes priority over billing
- Refunds are distinct from general billing questions

## Architecture Highlights

- **Backend**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite for simplicity (easily swappable)
- **LLM Integration**: OpenAI API with structured prompts
- **Frontend**: React with clean component structure
- **API Design**: RESTful with clear separation of concerns

## Troubleshooting

**Issue**: "OpenAI API key not found"
- Solution: Make sure you've set the OPENAI_API_KEY environment variable

**Issue**: Frontend can't connect to backend
- Solution: Ensure backend is running on port 8000

**Issue**: Database not seeding
- Solution: Delete `backend/supportlens.db` and restart
