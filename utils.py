"""Utils for sending messages through Twilio API"""

import logging
from loguru import logger

# Third-party imports
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# env variables
account_sid = load_dotenv("TWILIO_ACCOUNT_SID")
auth_token = load_dotenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)
twillio_number = load_dotenv("TWILIO_NUMBER")
twillio_number = "+14155238886"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Twilio Messaging API initialized")


# Sending message logic through Twilio Messaging API
def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twillio_number}",
            body=body_text,
            to = f"whatsapp:{to_number}",
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")
