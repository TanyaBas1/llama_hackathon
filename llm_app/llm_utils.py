"this modele contains the helper functions for LLM agents"
from together import Together
import json
from dotenv import load_dotenv
import os
from .system_prompts import AMBIGUITY_DETECTION, PINECONE_REPHRASE_PROMPT, ADMINISTRATOR_LLM, FINAL_SUMMARIZER
from ..pinecone.query_pinecone_index import query_pinecone_index

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


#@retry_json_request(max_retries=3)
def get_ambiguity_detection_response(user_prompt):
    response = call_together(system_prompt=AMBIGUITY_DETECTION, user_prompt=user_prompt)
    # Parse the JSON response from the LLM
    response_json = json.loads(response)
    return response_json

def rephrase_query(query, context=""):
    return call_together(system_prompt=PINECONE_REPHRASE_PROMPT.format(context), user_prompt=query)

def check_response_appropriateness(query, responses):
    user_prompt = f"Query: {query} ; Responses: {responses}"

    response = call_together(system_prompt=ADMINISTRATOR_LLM, user_prompt=user_prompt)
    
    response_json = json.loads(response)
    
    result = response_json.get("result")
    feedback = response_json.get("feedback")

    return result, feedback


def search_pinecone(query, context=""):
    query_fixed = rephrase_query(query, context)
    search_results = query_pinecone_index(query_text=query)
    return query_fixed, search_results

def generate_response(query, sources):
    response = call_together(system_prompt=FINAL_SUMMARIZER, user_prompt=f"Query: {query} ; Sources: {sources}")
    return response
