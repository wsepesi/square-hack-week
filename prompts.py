from typing import List
from type_utils import ProcessedData

SERVICES = [
    "ledger",
]

def RELEVANCY(prompt: str) -> str:
    return f"""### Instruction:
    Determine if the following prompt is relevant with regards to one of the following criteria: 
    - The message is a technical question
    - The message is specific to one of the following services: {SERVICES}
    - The message is NOT related to staging / canary / production checks or a roll
    Answer with "Yes" or "No"
    
    ### Input:
    Hey how is everyone?

    ### Response:
    No

    ### Input:
    hello there, is there a way to extend a hold on a user applied via regulator "create user hold" ? for more context, credit risk ops team applied a hold on a seller(convene) but the duration is defaulted to 90 days which is not sufficient for this use case.

    ### Response:
    Yes

    ### Input:
    {prompt}

    ### Response:
    """

def SUMMARIZE(prompt: str) -> str:
    return f"""### Instructions:
    Summarize the following query in one precise sentence evaluating what the user is trying to achieve. Eliminate extraneous information and focus on the core of the question.

    ### Input:
    hello there, is there a way to extend a hold on a user applied via regulator "create user hold" ? for more context, credit risk ops team applied a hold on a seller(convene) but the duration is defaulted to 90 days which is not sufficient for this use case. without an option to extend to a custom time, ops team is waiting for the existing hold to expire and then apply a new hold for the next 90 days using reminders which is tedious and error prone. just wanted to check if there is any override that can be done in the backend to extend the hold. thanks  :pray:

    ### Response:
    User wants to know if there's a way to extend a hold on a user applied via regulator "create user hold" beyond the default 90 days.

    ### Input:
    {prompt}

    ### Response:
    """

def GET_KEYWORDS(prompt: str) -> str:
    return f"""### Instructions:
    List the keywords that are most relevant to the following prompt. Keywords should be separated by spaces.

    ### Input:
    User wants to know if there's a way to extend a hold on a user applied via regulator "create user hold" beyond the default 90 days.

    ### Response:
    extend hold create user hold regulator

    ### Input:
    {prompt}

    ### Response:
    """

def CHOOSE_SOURCES(prompt: str, sources: List[ProcessedData]) -> str:
    source_string = "" + "\n".join([f"{idx}: {source.text}" for idx, source in enumerate(sources)])
    return f"""### Instructions:
    You will be provided with 5 factual sources, labeled below. Choose up to 5 sources that you think are most relevant to the prompt. Give your answer in a list of numbers, for example "1, 3, 5".

    ### Input:
    Prompt: {prompt}
    Sources: {source_string}

    ### Response:
    """

def GET_ANSWER(prompt: str, sources: List[ProcessedData]) -> str:
    source_string = "" + "\n".join([f"{idx}: {source.text}" for idx, source in enumerate(sources)])
    return f"""### Instructions:
    You are a helpful question answering chatbot. You answer questions politely, concisely, and factually, using the resources available to you. 

    Provided below are 5 factual sources that you can use to answer questions. You will be asked to answer a prompt, pulling data from the sources to back up your response. In addition to your answer, provide a list of sources that you used to answer the question, in the format "1, 3, 5".

    Sources: 
    {source_string}

    ### Input:
    {prompt}

    ### Response:
    """