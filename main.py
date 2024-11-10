from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    # Access an environment variable
    secret_message = os.getenv('SECRET_MESSAGE', 'No secret message set.')
    return f'Hello, World! {secret_message}'

if __name__ == '__main__':
    app.run(debug=True)