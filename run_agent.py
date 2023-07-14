from prompts import *
from vlite import VLite
from gpt4all import GPT4All

PROMPT = 'hello there, is there a way to extend a hold on a user applied via regulator "create user hold" ? for more context, credit risk ops team applied a hold on a seller(convene) but the duration is defaulted to 90 days which is not sufficient for this use case. without an option to extend to a custom time, ops team is waiting for the existing hold to expire and then apply a new hold for the next 90 days using reminders which is tedious and error prone. just wanted to check if there is any override that can be done in the backend to extend the hold. thanks  :pray:'
VERBOSE = True
DB_PATH = "v1.npz"

model_name = "nous-hermes-13b.ggmlv3.q4_0.bin"
model = GPT4All(model_name)

db = VLite(collection=DB_PATH)

def run_agent(prompt: str = PROMPT) -> str | None:
    print("Entering agent loop...")

    print("Checking relevancy of prompt...")

    # if not is_relevant(prompt):
    #     print("Prompt is not relevant. Exiting...")
    #     return
    
    print("Prompt is relevant. Analyzing...")
    summary = call_model(SUMMARIZE(prompt))
    print(f"Summary: {summary}")

    keywords = call_model(GET_KEYWORDS(prompt))
    summary_keywords = call_model(GET_KEYWORDS(summary))

    print(f"Keywords: {keywords}")
    print(f"Summary Keywords: {summary_keywords}")

    print("Retrieving relevant documents...")
    prompt_docs: List[ProcessedData] = get_relevant_documents(prompt)
    # keywords_docs: List[ProcessedData] = get_relevant_documents(keywords)
    # summary_docs: List[ProcessedData] = get_relevant_documents(summary)

    print(f"Prompt docs: {_to_string(prompt_docs)}")
    # print(f"Keywords docs: {_to_string(keywords_docs)}")
    # print(f"Summary docs: {_to_string(summary_docs)}")

    answer = get_answer(prompt, prompt_docs[0:2])
    print(f"{answer}")

    print("Exiting agent loop...")

    return answer

def get_answer(prompt: str, sources: List[ProcessedData]) -> str:
    return call_model(GET_ANSWER(prompt, sources))

def _to_string(data: List[ProcessedData]) -> List[str]:
    return [doc.text for doc in data]

def get_relevant_documents(query_string: str) -> List[ProcessedData]:
    docs: List[ProcessedData] = db.remember(query_string)

    return docs

def with_stop_sequence(text: str, stop_seq: str = "\n"):
    return text.split(stop_seq)[0]

def call_model(prompt: str) -> str:
    return model.generate(prompt)

def is_relevant(prompt: str) -> bool:
    # call model and remove whitespace
    from_ai = call_model(RELEVANCY(prompt)).strip()
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