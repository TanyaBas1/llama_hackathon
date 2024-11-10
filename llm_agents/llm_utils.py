"this modele contains the helper functions for LLM agents"
from together import Together
from dotenv import load_dotenv
import os
import json


def call_togather(client,model, system_prompt, user_prompt):
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


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("TOGETHER_API_KEY")
    client = Together(api_key=api_key)
    model = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
    system_prompt = "You are a llama farmer and you are trying to figure out how to increase your profits. You have a llama named Carl who is very smart and can help you with your business. You ask Carl for advice on how to increase your profits."
    user_prompt = "Carl, how can I increase my profits?"
    response = call_togather(client,model, system_prompt, user_prompt)
    print(response)
