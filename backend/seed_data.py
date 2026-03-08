import uuid
from datetime import datetime, timedelta
import random
from database import SessionLocal, init_db, Trace

# Initialize database
init_db()

# Sample data for seeding
SEED_DATA = [
    # Billing
    ("Why was I charged twice this month?", "I apologize for the confusion. Let me check your account. It appears one charge was a pending authorization that will drop off. You'll only be charged once.", "Billing", 850),
    ("What payment methods do you accept?", "We accept all major credit cards (Visa, Mastercard, Amex), PayPal, and ACH bank transfers for annual plans.", "Billing", 720),
    ("Can I see my invoice history?", "Absolutely! You can view all past invoices in your account dashboard under Billing > Invoice History. Would you like me to email them to you as well?", "Billing", 680),
    ("How much does the Pro plan cost?", "Our Pro plan is $49/month or $470/year (save 20%). It includes unlimited users, advanced analytics, and priority support.", "Billing", 790),
    
    # Refund
    ("I want a refund for last month", "I understand. Can you tell me more about why you'd like a refund? We have a 30-day money-back guarantee and I'd be happy to process that for you.", "Refund", 920),
    ("This charge is wrong, I need my money back", "I'm sorry about that. Let me investigate this charge immediately. Can you provide the transaction date? I'll process a refund if there was an error.", "Refund", 880),
    ("How do I dispute a charge?", "To dispute a charge, I can help you right now. Please provide the charge amount and date, and I'll review it with our billing team and process a refund if warranted.", "Refund", 760),
    
    # Account Access
    ("I can't log into my account", "I'm sorry you're having trouble logging in. Let's reset your password. I'll send a reset link to your registered email address right away.", "Account Access", 650),
    ("My password reset isn't working", "That's frustrating. Let me generate a new reset link for you. Can you confirm the email address associated with your account?", "Account Access", 710),
    ("I'm locked out after too many attempts", "I see your account was temporarily locked for security. I've unlocked it now. Please try logging in again and let me know if you need help.", "Account Access", 820),
    ("How do I enable two-factor authentication?", "Great security question! Go to Settings > Security > Two-Factor Authentication. You can use an authenticator app or SMS. I recommend an app like Google Authenticator.", "Account Access", 740),
    
    # Cancellation
    ("I want to cancel my subscription", "I'm sorry to see you go. I can help you cancel. May I ask what prompted this decision? We might have a solution that works better for you.", "Cancellation", 890),
    ("How do I downgrade my plan?", "I can help you downgrade. Which plan would you like to switch to? Note that you'll keep your current plan benefits until the end of your billing cycle.", "Cancellation", 770),
    ("Cancel my account immediately", "I understand. I can process your cancellation right away. Your access will continue until the end of your current billing period. Should I proceed?", "Cancellation", 810),
    ("What happens to my data if I cancel?", "If you cancel, your data is retained for 90 days in case you want to reactivate. After that, it's permanently deleted per our privacy policy.", "Cancellation", 730),
    
    # General Inquiry
    ("What features are in the Enterprise plan?", "Our Enterprise plan includes everything in Pro plus: custom integrations, dedicated account manager, SLA guarantees, advanced security features, and custom contracts.", "General Inquiry", 800),
    ("Do you have a mobile app?", "Yes! We have mobile apps for both iOS and Android. You can download them from the App Store or Google Play. They sync seamlessly with your web account.", "General Inquiry", 690),
    ("How do I export my data?", "You can export your data anytime from Settings > Data Export. Choose your format (CSV, JSON, or Excel) and we'll email you a download link within minutes.", "General Inquiry", 750),
    ("Is there a free trial?", "Yes! We offer a 14-day free trial with full access to all Pro features. No credit card required to start. Would you like me to help you sign up?", "General Inquiry", 670),
    ("What's new in the latest update?", "Our latest update includes a redesigned dashboard, faster report generation, new API endpoints, and improved mobile experience. Check our changelog for details!", "General Inquiry", 780),
    ("Can I integrate with Salesforce?", "Yes, we have a native Salesforce integration. You can connect it in Settings > Integrations. It syncs customer data, invoices, and payment status automatically.", "General Inquiry", 830),
]

def seed_database():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(Trace).count()
        if existing_count > 0:
            print(f"Database already has {existing_count} traces. Skipping seed.")
            return
        
        print("Seeding database with sample traces...")
        
        # Create traces with timestamps spread over the last 7 days
        base_time = datetime.utcnow()
        
        for i, (user_msg, bot_resp, category, response_time) in enumerate(SEED_DATA):
            # Spread timestamps over last 7 days
            hours_ago = random.randint(0, 168)  # 7 days = 168 hours
            timestamp = base_time - timedelta(hours=hours_ago)
            
            trace = Trace(
                id=str(uuid.uuid4()),
                user_message=user_msg,
                bot_response=bot_resp,
                category=category,
                timestamp=timestamp,
                response_time_ms=response_time + random.randint(-50, 50)
            )
            db.add(trace)
        
        db.commit()
        print(f"Successfully seeded {len(SEED_DATA)} traces!")
        
        # Print summary
        for category in ["Billing", "Refund", "Account Access", "Cancellation", "General Inquiry"]:
            count = db.query(Trace).filter(Trace.category == category).count()
            print(f"  {category}: {count} traces")
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
