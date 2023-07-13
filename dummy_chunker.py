from typing import List
import tiktoken
import re

encoding = tiktoken.get_encoding("cl100k_base")

def _count_tokens(text: str) -> int:
    """
    Count the number of tokens in a string.
    """
    return len(encoding.encode(text))

def replace_whitespace_with_space(string):
    # Use regular expression to replace multiple whitespace characters with a single space
    processed_string = re.sub(r'\s+', ' ', string)
    return processed_string

def naive_chunking(text: str) -> List[str]:
    """
    Naive chunking of text into 256 token chunks. 
    
    Implementation:
    Clean the string by replacing all white spaces and newlines, etc with a single space.
    Create a list of chunks, initialized to be empty.
    Create a current chunk string, initialized to be empty.
    Iterate over the words in the string, adding 25 words to the current chunk as long as it doesn't exceed 256 tokens.
    """

    text = replace_whitespace_with_space(text)
    chunks = []
    current_chunk = ""
    words: List[str] = text.split()

    for i in range(0, len(words), 25):
        if _count_tokens(current_chunk) + _count_tokens(" ".join(words[i:i+25])) < 256:
            current_chunk += " ".join(words[i:i+25]) + " "
        else:
            chunks.append(current_chunk)
            current_chunk = "" + " ".join(words[i:i+25]) + " "

    chunks.append(current_chunk)
    return chunks