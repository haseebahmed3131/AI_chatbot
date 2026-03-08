import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from typing import Tuple
import time
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from root .env file
root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'
load_dotenv(dotenv_path=env_path)

# Get OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please set it in .env file")

# Initialize LangChain with OpenRouter
# OpenRouter uses OpenAI-compatible API, so we use ChatOpenAI with custom base_url
llm_chat = ChatOpenAI(
    model="openai/gpt-3.5-turbo",  # OpenRouter model format
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=150
)

llm_classify = ChatOpenAI(
    model="openai/gpt-3.5-turbo",  # OpenRouter model format
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
    max_tokens=20
)

SUPPORT_SYSTEM_PROMPT = """You are a helpful customer support agent for BillFlow, a SaaS billing platform. 
Assist customers with billing questions, refund requests, account access issues, cancellations, and general inquiries.
Be professional, concise, and helpful. Keep responses under 100 words."""

CLASSIFICATION_PROMPT_TEMPLATE = """You are a conversation classifier. Analyze the customer support conversation and classify it into EXACTLY ONE category.

Categories:
- Billing: Questions about invoices, charges, payment methods, pricing, or subscription fees
- Refund: Requests to return a product, get money back, dispute a charge, or process a credit
- Account Access: Issues logging in, resetting passwords, locked accounts, or MFA problems
- Cancellation: Requests to cancel a subscription, downgrade a plan, or close an account
- General Inquiry: Anything else (feature questions, product info, how-to questions, etc.)

Rules:
1. Return ONLY the category name, nothing else
2. If a message covers multiple topics, choose the PRIMARY intent
3. Cancellation intent takes priority over billing questions
4. Refund requests are distinct from general billing questions

Customer Message: {user_message}
Bot Response: {bot_response}

Category:"""

# Create LangChain prompt templates
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SUPPORT_SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template("{user_message}")
])

classification_prompt = ChatPromptTemplate.from_template(CLASSIFICATION_PROMPT_TEMPLATE)

def generate_chatbot_response(user_message: str) -> Tuple[str, int]:
    """Generate chatbot response using LangChain and return (response, time_ms)"""
    start_time = time.time()
    
    # Format the prompt with user message
    messages = chat_prompt.format_messages(user_message=user_message)
    
    # Invoke LLM through LangChain
    response = llm_chat.invoke(messages)
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    bot_response = response.content.strip()
    
    return bot_response, elapsed_ms

def classify_conversation(user_message: str, bot_response: str) -> str:
    """Classify conversation into one of five categories using LangChain"""
    # Format the classification prompt
    messages = classification_prompt.format_messages(
        user_message=user_message,
        bot_response=bot_response
    )
    
    # Invoke LLM through LangChain
    response = llm_classify.invoke(messages)
    category = response.content.strip()
    
    # Validate and normalize category
    valid_categories = {
        "Billing", "Refund", "Account Access", "Cancellation", "General Inquiry"
    }
    
    # Handle variations
    category_map = {
        "billing": "Billing",
        "refund": "Refund",
        "account access": "Account Access",
        "cancellation": "Cancellation",
        "general inquiry": "General Inquiry",
        "general": "General Inquiry"
    }
    
    normalized = category_map.get(category.lower(), category)
    
    if normalized not in valid_categories:
        return "General Inquiry"
    
    return normalized
