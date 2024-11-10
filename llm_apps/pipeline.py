from llm_agents.system_prompts import AMBIGUITY_DETECTION
from llm_agents.llm_utils import call_togather, retry_json_request
from together import Together
from dotenv import load_dotenv
import os
import json

@retry_json_request(max_retries=3)
def get_ambiguity_detection_response(client, user_prompt):
    model = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
    response = call_togather(client, model, AMBIGUITY_DETECTION, user_prompt)
    return response

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("TOGETHER_API_KEY")
    client = Together(api_key=api_key)
    user_prompt = "How to get pension in Bulgaria?"
    try:
        response = get_ambiguity_detection_response(client, user_prompt)
        
        if response.get("question_ambiguous") == "yes":
            print(response["clarification"])
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: Unable to parse JSON response after retries. {e}")
    # response = get_ambiguity_detection_response(client, user_prompt)
    # # print(response)

    # if isinstance(response, str):
    #     response = json.loads(response)

    # if response["question_ambiguous"] == "yes":
    #     print(response["clarification"])
    
    