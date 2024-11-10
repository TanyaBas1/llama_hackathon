"""FASTAPI APP"""

from fastapi import FastAPI, Form
from utils import send_message
from dotenv import load_dotenv


app = FastAPI()
whatsapp_number = load_dotenv("CLIENT_NUMBER")
whatsapp_number = "+923481158655"


@app.get("/status")
async def index():
    return {"msg": "up & running"}


@app.post("/message")
async def reply(Body: str = Form()) -> str:
    # Call GenAI service to generate response
    # dummy response
    chat_response = "Yo grandma, how can I help you?"

    # Call Twilio service to send message
    send_message(whatsapp_number, chat_response)
    return ""
