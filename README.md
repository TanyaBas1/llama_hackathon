# BabAI - AI-Powered WhatsApp Bot for Social Security Information

![babAI-new-version](https://github.com/user-attachments/assets/58548f85-2911-4c74-9891-1aed26163713)


🚀 **Project Overview**

BabAI is a WhatsApp chatbot that provides users with accurate, up-to-date information on social security and pension regulations in Bulgaria. It leverages AI to retrieve information directly from official sources and ensure high-quality, reliable responses. Built with convenience, accuracy, and safety in mind, BabAI empowers users to access critical information anytime, anywhere.

🎯 **Key Features**

- Seamless WhatsApp Integration: Available on a platform familiar to most Bulgarians, with a 90% adoption rate.

- Real-Time Accurate Information: Fetches and presents information from National Social Security Institute documents.

- Guardrails for Safety: Ensures responses are ethical, accurate, and compliant with legal guidelines.


🛠️**Tech Stack**

Backend: FastAPI (Webhooks), Uvicorn, Ngrok () Twilio API (for WhatsApp integration)
Database: PostgreSQL
AI Frameworks: OpenAI API for language processing
DevOps: Docker, GitHub Actions for CI/CD
Other Tools: Python (Poetry for dependency management), ipyleaflet for maps
🏗️ Project Architecture
User Input: Users send questions about pensions or social security via WhatsApp.
API Gateway: Twilio API captures and forwards user queries to BabAI's backend.
Information Retrieval: Backend retrieves accurate, context-specific data from official documents.
Response Generation: The AI model generates responses, filtered by guardrails for quality and safety.
Output: The user receives a comprehensive, user-friendly answer directly on WhatsApp.
🚀 Quick Start
Prerequisites
Python 3.9+ installed
Docker for containerized deployment
Twilio Account for WhatsApp API integration
API keys and environment variables stored in .env file (example provided below)
Installation
Clone this repository:
bash
Copy code
git clone https://github.com/username/babai.git
cd babai
Install dependencies:
bash
Copy code
poetry install
Set up environment variables:
bash
Copy code
cp .env.example .env
Run the server locally:
bash
Copy code
uvicorn app.main:app --reload
Access BabAI on WhatsApp by connecting your Twilio number.
📝 Environment Variables
Create a .env file in the root directory with the following variables:

makefile
Copy code
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_database_url
🖼️ Screenshots
Feature	Screenshot
User Interaction on WhatsApp	
🤖 How It Works
User asks a question (e.g., "What is my pension if I have worked 40 years?").
API processes the query, retrieves data, and applies guardrails.
Response is generated and sent back on WhatsApp.
🧩 Challenges We Faced
Data Accuracy: Ensuring the information retrieved is always up-to-date and verified.
WhatsApp Integration: Setting up a seamless API with reliable message delivery.
Guardrails for AI: Preventing any misinformation or inaccurate advice.
🚀 Future Improvements
Multilingual Support: Expanding to other languages for wider accessibility.
Enhanced Accuracy: Integrate official updates in real-time.
User Personalization: Tailoring responses based on user-specific data or history.
📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙌**Team** (listed in alphabetic order)
- Gabriela Tsvetkova
- Saad Asad
- Miray Özcan
- Tetiana Bass
- Hackathon Mentor from Meta

🗣**Acknowledgements**

Thanks to [Hack for Social Impact](https://www.hackforsocialimpact.com/) and all team members who helped make BabAI a reality! Thanks mom for giving us domain expertise on this complex topic 💗










# Set up 

To run this you will have to go into the poetry shell 

```bash
poetry shell
```

```bash
poetry install
```


after that you have to load environmental variables 
- create .env
- copy the content of .env.example 
- instert the api key



## Local dev
start fastapi server:
```bash
uvicorn main:app --reload
```
Setup ngrok, this is a forward proxy since we want to send messages to a public url
from here: https://ngrok.com/docs/getting-started/

When the fastapi server is running on local, start ngrok:
```bash
ngrok http http://localhost:<port-number>
```
