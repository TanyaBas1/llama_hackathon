import re
import json 


def split_into_passages(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        document = file.read()

    # Define a regular expression to detect a pattern indicating the start of a new passage
    # For example, assuming passages are separated by "Page X" or "Chapter X" or any clear separator
    passage_pattern = re.compile(r'(Page \d+|Chapter \d+|[0-9]+\. [A-Za-zА-Яа-я]+)', re.IGNORECASE)

    # Split the document into passages based on the pattern
    passages = re.split(passage_pattern, document)
    
    # Clean up and filter out empty strings that might appear after splitting
    passages = [passage.strip() for passage in passages if passage.strip()]

    def handle_passage_length(passage):
        words = passage.split()
        num_words = len(words)
        
        if num_words < 50:
            return None  # Mark as short passage to be merged with the next
        elif num_words > 400: # Split the passage into two if it's too long
            midpoint = num_words // 2
            part1 = " ".join(words[:midpoint])
            part2 = " ".join(words[midpoint:])
            return [part1, part2]  
        else:
            return [passage]  # Return as is if it's of an acceptable length

    final_passages = []
    temp_passage = None

    for passage in passages:
        # If the passage is short, append it to the temp_passage
        if temp_passage is None:
            temp_passage = passage
        else:
            temp_passage += ' ' + passage

        processed_passages = handle_passage_length(temp_passage)
        
        if processed_passages is None:
            # do not add short passage separately
            continue
        else:
            final_passages.extend(processed_passages)
            temp_passage = None

    # addressing leftover passages
    if temp_passage:
        final_passages.append(temp_passage)

    return final_passages


if __name__ == "__main__":
    file_path = '/Users/tetianabas/llama_hackathon/llama_hackathon/rag/extracted_text.txt'
    passages = split_into_passages(file_path)

    # Printing the first few passages to verify
    for i, passage in enumerate(passages[:5]):
        print('------------NEW PASSAGE------------')
        print(f"Passage {i + 1}:\n{passage}\n{'-'*50}")

    output_file = '/Users/tetianabas/llama_hackathon/llama_hackathon/rag/passages.json'
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(passages, json_file, ensure_ascii=False, indent=4)

    print(f"\nPassages have been saved to {output_file}")

