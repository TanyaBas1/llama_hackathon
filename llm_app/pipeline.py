from llm_app.system_prompts import AMBIGUITY_DETECTION
from llm_app.llm_utils import client, call_togather, retry_json_request, search_pinecone, check_response_appropriateness, generate_response
import json

# Initialize Pinecone
#pinecone_api_key = os.getenv("PINECONE_API_KEY")
#pinecone_environment = os.getenv("PINECONE_ENVIRONMENT")
#pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

#pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)
#index = pinecone.Index(pinecone_index_name)

@retry_json_request(max_retries=3)
def get_ambiguity_detection_response(client, user_prompt):
    model = "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"
    response = call_togather(client, model, AMBIGUITY_DETECTION, user_prompt)
    # Parse the JSON response from the LLM
    response_json = json.loads(response)
    return response_json


def runner(query, previous_queries=None):
    if previous_queries is None:
        previous_queries = []

    guardrail = get_ambiguity_detection_response(client, query)
    if guardrail.get('relevant') == "no":
        return "Нерелевантен въпрос"
    elif guardrail.get('ambiguous') == "yes":
        return "Необходима е допълнителна информация"
    elif guardrail.get('needs_pension_documents') == "yes":
        queries_summary = ""
        max_attempts = 3
        for attempt in range(max_attempts):
            search_results = search_pinecone(query)
            generated_response = generate_response(search_results, query)
            
            previous_queries.append({
                "query": query,
                "response": generated_response[:500]
            })

            queries_summary = "\n".join(
                [f"Query {i + 1}: {item['query']}\nResponse: {item['response']}" for i, item in enumerate(previous_queries)]
            )

            if check_response_appropriateness(generated_response).result == "yes":
                return generated_response, queries_summary
            else:
                continue
        
        return "Неуспешно генериране на отговор", queries_summary
    else:
        return "Няма наличен отговор", None

if __name__ == "__main__":
    user_prompt = "How to get pension in Bulgaria?"
    try:
        response = runner(user_prompt)
        print(response)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error: Unable to parse JSON response after retries. {e}")