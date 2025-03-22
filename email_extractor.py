import re

def extract_emails(text):
    """Extract email addresses from the given text."""
    if not text:
        return []
    
    # Regular expression pattern for email extraction
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
    # Find all matches
    emails = re.findall(pattern, text)
    
    # Remove duplicates while preserving order
    unique_emails = []
    for email in emails:
        if email not in unique_emails:
            unique_emails.append(email)
    
    return unique_emails
