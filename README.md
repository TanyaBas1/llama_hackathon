## Set up 

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
- instert the api key (feel free to message me to ask it)


to run a module 

```bash
python path/to/your/module
```

## Useful debugging commands 

to check if the api keys are loaded 

```bash
poetry run echo $TOGETHER_API_KEY
```

## Important notes

Please create a branch with your name and work on a branch, do not push into main
also try to add comments about what you do and what are the next steps that should be done - it will make the handover easier

## Libraries that need to be installed 
- openai 
- pinecone-client 
- PyPDF2 
- pdfplumber 
- pandas 
- requests

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

Thank you!