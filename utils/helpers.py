import re
import string

def clean_text(text: str) -> str:
    """
    Cleans the input text by removing extra whitespaces and special characters.
    """
    if not text:
        return ""
    # Remove special characters that are not needed
    text = re.sub(r'[^a-zA-Z0-9\s.,@+()-]', ' ', text)
    # Replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_email(text: str) -> str | None:
    """
    Extracts the first email found in the text.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    if match:
        return match.group()
    return None

def extract_phone(text: str) -> str | None:
    """
    Extracts the first phone number found in the text.
    Matches formats like +1-123-456-7890, (123) 456-7890, 1234567890, etc.
    """
    # Simple regex for phone numbers
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    match = re.search(phone_pattern, text)
    if match:
        return match.group()
    return None
