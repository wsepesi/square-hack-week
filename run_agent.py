from prompts import *
from vlite import VLite

PROMPT = ""
VERBOSE = False
DB_PATH = "demo.npz"

db = VLite(collection=DB_PATH)

def run_agent(prompt: str = PROMPT) -> str | None:
    print("Entering agent loop...")

    print("Checking relevancy of prompt...")

    if not is_relevant(prompt):
        print("Prompt is not relevant. Exiting...")
        return
    
    print("Prompt is relevant. Analyzing...")
    summary = SUMMARIZE(prompt)
    print(f"Summary: {summary}")

    keywords = GET_KEYWORDS(prompt)
    summary_keywords = GET_KEYWORDS(summary)

    print(f"Keywords: {keywords}")
    print(f"Summary Keywords: {summary_keywords}")

    print("Retrieving relevant documents...")
    prompt_docs: List[ProcessedData] = get_relevant_documents(prompt)
    # keywords_docs: List[ProcessedData] = get_relevant_documents(keywords)
    # summary_docs: List[ProcessedData] = get_relevant_documents(summary)

    print(f"Prompt docs: {_to_string(prompt_docs)}")
    # print(f"Keywords docs: {_to_string(keywords_docs)}")
    # print(f"Summary docs: {_to_string(summary_docs)}")

    answer = get_answer(prompt, prompt_docs)
    print(f"Answer: {answer}")

    print("Exiting agent loop...")

    return answer

def get_answer(prompt: str, sources: List[ProcessedData]) -> str:
    return GET_ANSWER(prompt, sources)

def _to_string(data: List[ProcessedData]) -> List[str]:
    return [doc.text for doc in data]

def get_relevant_documents(query_string: str) -> List[ProcessedData]:
    docs: List[ProcessedData] = db.remember(query_string)

    return docs

def with_stop_sequence(text: str, stop_seq: str = "\n"):
    return text.split(stop_seq)[0]

def is_relevant(prompt: str) -> bool:
    from_ai = RELEVANCY(prompt)
    if VERBOSE:
        print(from_ai)

    if from_ai == "Yes":
        return True
    elif from_ai == "No":
        return False
    else:
        raise ValueError("AI did not respond with 'Yes' or 'No'") # TODO: maybe just chop off the first word from the response and use it


if __name__ == '__main__':
    run_agent()