"this modele contains the helper functions for LLM agents"
from together import Together
import json
from dotenv import load_dotenv
import os
from .system_prompts import PINECONE_REPHRASE_PROMPT, ADMINISTRATOR_LLM

# Load environment variables
load_dotenv()

# Initialize Together client
api_key = os.getenv("TOGETHER_API_KEY")
client = Together(api_key=api_key)


def call_together(system_prompt, user_prompt, model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [{"type": "text", "text": user_prompt}]}],
        max_tokens=None,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>","<|eom_id|>"],
        stream=True
    )
    # Accumulate the response content instead of printing it
    response_content = ''
    for token in response:
        if hasattr(token, 'choices') and token.choices and hasattr(token.choices[0], 'delta'):
            response_content += token.choices[0].delta.content

    # TODO 
    return response_content

def retry_json_request(max_retries=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    response = func(*args, **kwargs)
                    # Try to parse JSON response
                    return json.loads(response)  # will raise ValueError if not valid JSON
                except (json.JSONDecodeError, ValueError) as e:
                    if attempt < max_retries - 1:
                        print(f"Attempt {attempt + 1} failed: Invalid JSON. Retrying...")
                    else:
                        print(f"Attempt {attempt + 1} failed: Invalid JSON. Max retries reached.")
                        raise e
        return wrapper
    return decorator

def rephrase_query(query):
    return call_together(system_prompt=PINECONE_REPHRASE_PROMPT, user_prompt=query)

def check_response_appropriateness(query):
    return call_together(system_prompt=ADMINISTRATOR_LLM, user_prompt=query)

def search_pinecone(query):
    query_fixed = rephrase_query(query)
    return "Размерът на пенсията за осигурителен стаж и възраст се определя, като доходът, от който се изчислява пенсията, се умножи със сумата, образувана от: по 1 процент за пенсии, отпуснати с начална дата до 31.03.2009 г., по процент 1,1 на сто за пенсии, отпуснати с началната дата от 01.04.2009 г. до 31.12.2016 г., за отпуснатите от 01.01.2017 г. до 31.12.2017 г. с 1,126 на сто, за отпуснати от 01.01.2018 г. до 31.12.2018 г. с 1,169 на сто, за отпуснатите с начална дата от 01.01.2019 г. до 24.12.2021 г. включително с 1,2 на сто за всяка година осигурителен стаж и съответната пропорционална част от процента за оставащите месеци осигурителен стаж. За пенсиите отпуснати с начална дата след 24 декември 2021 г. доходът, от който се изчислява пенсията, се умножава с процент 1,35 за всяка година осигурителен стаж без превръщане и съответната пропорционална част от този процент за месеците осигурителен стаж без превръщане, и с 1,2 за всяка година осигурителен стаж и съответната пропорционална част от този процент за месеците осигурителен стаж – за осигурителния стаж, представляващ разлика между общия осигурителен стаж, зачетен на лицето, и стажа без превръщане."
