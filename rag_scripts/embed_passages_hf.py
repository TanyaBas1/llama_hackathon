import os
import json
from transformers import AutoTokenizer, AutoModel
import torch
from dotenv import load_dotenv

def split_text_into_passages(file_path, chunk_size=200):
    """Split raw text into smaller passages."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split text into chunks
    words = text.split()
    passages = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    return passages

def save_passages_to_json(passages, output_file):
    """Save passages to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(passages, json_file, ensure_ascii=False, indent=4)

def generate_embeddings(passages, tokenizer, model):
    """Generate embeddings for each passage."""
    embeddings = {}
    for i, passage in enumerate(passages):
        # Tokenize and encode the passage
        inputs = tokenizer(passage, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            embedding = model(**inputs).last_hidden_state.mean(dim=1)  # Mean pooling
        embeddings[f"passage_{i}"] = {"text": passage, "embedding": embedding[0].tolist()}
    return embeddings

def save_embeddings_to_file(embeddings, output_file):
    """Save embeddings to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(embeddings, json_file, ensure_ascii=False, indent=4)

# Load environment variables (if needed for other purposes)
load_dotenv()

# Initialize Hugging Face model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Paths to input and output files
raw_text_file = "data/processed_data/extracted_cleaned_text.txt"  # Updated to use the cleaned text
output_dir = "data/processed_data"  # Directory for output files

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define output file paths
passages_file = os.path.join(output_dir, "split_passages.json")
embeddings_file = os.path.join(output_dir, "embeddings.json")

# Split text into passages
passages = split_text_into_passages(raw_text_file)

# Save passages to JSON
save_passages_to_json(passages, passages_file)

# Generate embeddings
embeddings = generate_embeddings(passages, tokenizer, model)

# Save embeddings to JSON
save_embeddings_to_file(embeddings, embeddings_file)

print(f"Passages saved to '{passages_file}'.")
print(f"Embeddings saved to '{embeddings_file}'.")