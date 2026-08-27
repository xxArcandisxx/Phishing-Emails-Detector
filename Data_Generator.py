import pandas as pd
import random
from faker import Faker

# Initialize Faker and set seeds for reproducibility 
fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_phishing_dataset(num_samples=1000):
    dataset = []
    
    # Expanded common phishing trigger words to prepend to subjects
    phishing_triggers = [
        # Urgency & Warnings
        "URGENT: ", "Immediate Action Required: ", "Final Notice: ", 
        "Warning: ", "Attention: ", "Last Chance: ",
        
        # Security & Accounts
        "Security Alert: ", "Account Suspended: ", "Unauthorized Access: ",
        "Password Expiry: ", "Verify Your Identity: ", "Unusual Login Activity: ",
        "Action needed: ", "Account Disabled: ",
        
        # Financial & Billing
        "Invoice Overdue: ", "Payment Failed: ", "Tax Refund: ", 
        "Receipt for your Order: ", "Billing Issue: ", "Payment Confirmation: ",
        
        # Workplace & Document Sharing
        "Important HR Update: ", "DocuSign: ", "Shared Document: ", 
        "Confidential: ", "New Voicemail: ",
        
        # Prizes & Packages
        "Win a Prize: ", "Delivery Failed: ", "Package Undeliverable: ",
        "Claim Your Reward: "
    ]
    
    for _ in range(num_samples):
        # Randomly assign as legitimate (0) or phishing (1)
        is_phishing = random.choice([True, False])
        
        sender_name = fake.name()
        
        if is_phishing:
            # Phishing traits: free emails, urgent subjects, URLs in a short body
            sender_email = fake.free_email()
            subject = random.choice(phishing_triggers) + fake.catch_phrase()
            body = f"Dear Customer,\n\n{fake.paragraph(nb_sentences=2)} Please verify your account by clicking here: {fake.url()}\n\nRegards,\n{sender_name}"
            contains_url = True
            
        else:
            # Legitimate traits: corporate emails, standard subjects, normal paragraphs
            sender_email = fake.company_email()
            subject = fake.sentence(nb_words=6)
            contains_url = random.choice([True, False])
            
            body = f"Hi,\n\n{fake.paragraph(nb_sentences=4)}\n\nBest,\n{sender_name}"
            if contains_url:
                body += f"\n\nReference link: {fake.url()}"
                
        # Append the generated row to our dataset
        dataset.append({
            "sender_name": sender_name,
            "sender_email": sender_email,
            "subject": subject,
            "body": body.replace("\n", " "),
            "contains_url": contains_url,
            "is_phishing": is_phishing
        })
        
    return pd.DataFrame(dataset)

# Generate 500 rows of synthetic email data
df_emails = generate_phishing_dataset(10000)

# Save the dataset to a CSV file for machine learning models
df_emails.to_csv("phishing_dataset.csv", index=False)

print("Dataset created successfully! Here is a preview:")
print(df_emails.head())