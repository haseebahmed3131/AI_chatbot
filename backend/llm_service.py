import os
from openai import OpenAI
from typing import Tuple
import time

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SUPPORT_SYSTEM_PROMPT = """You are a helpful customer support agent for BillFlow, a SaaS billing platform. 
Assist customers with billing questions, refund requests, account access issues, cancellations, and general inquiries.
Be professional, concise, and helpful. Keep responses under 100 words."""

CLASSIFICATION_PROMPT = """You are a conversation classifier. Analyze the customer support conversation and classify it into EXACTLY ONE category.

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

def generate_chatbot_response(user_message: str) -> Tuple[str, int]:
    """Generate chatbot response and return (response, time_ms)"""
    start_time = time.time()
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SUPPORT_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=150
    )
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    bot_response = response.choices[0].message.content.strip()
    
    return bot_response, elapsed_ms

def classify_conversation(user_message: str, bot_response: str) -> str:
    """Classify conversation into one of five categories"""
    prompt = CLASSIFICATION_PROMPT.format(
        user_message=user_message,
        bot_response=bot_response
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=20
    )
    
    category = response.choices[0].message.content.strip()
    
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
