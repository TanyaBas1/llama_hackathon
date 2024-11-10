"""Disclaimer: this is not debugged (imports issues), just a general logic, there are many ways to do emdedding itself, if it will be hard to
figure out togather ai imports I can easity do it with huggingface. it is just that togather is prefereable since they sponsor """

from togetherai import Together
from llama_index import ServiceContext, VectorStore
from llama_index import GPTSimpleVectorIndex
import json 

def load_passages(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        passages = json.load(json_file)
    return passages

# change the path, this is global path on my machine
passages = load_passages('/Users/tetianabas/llama_hackathon/llama_hackathon/rag/extracted_text.json')

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

together = Together(api_key=api_key)
model = together.get_model("meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo")

text = "За осигурените лица за инвалидност, поради общо заболяване, за старост и за смърт се внасят осигурителните вноски в размерите, определени за фонд"
embeddings = model.encode(text)

print(embeddings)