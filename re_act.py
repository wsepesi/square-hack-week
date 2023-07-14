from gpt4all import GPT4All
from run_agent import get_relevant_documents
from type_utils import ProcessedData
from typing import List

model_name = "nous-hermes-13b.ggmlv3.q4_0.bin"
model = GPT4All(model_name)

def BASE(prompt: str) -> str:
    return f"""### Instruction:
    You are an intelligent question answering agent. You answer questions politely, concisely, and factually, using the resources available to you. You operate through a series of actions, which determine how you proceed through your problem solving process. These are:
    - THINK: Reflect on the current information you have and decide what to do next.
    - SEARCH: Search for relevant information in your knowledge base. Takes an input of a query string and returns a list of the text of relevant documents. Followed by an END keyword which signals the end of the input.
    - STUDY: Study the information you have found and formulate an intermediate answer.
    - ANSWER: Answer the user's question.

    You will proceed as follows: You will be provided with an input, and then you can take one of the above ACTIONs. Depending on the action, you may then need to provide an input. You will then be provided with a response, and then you can take another ACTION. You will continue this process until you are confident you have answered the user's question. 

    ### Input:
    Let's think step by step. Who is Leo DiCaprio's girlfriend? What is her age times 2? 

    ### Response:
    ACTION THINK: I need to find out who Leo DiCaprio's girlfriend is.
    ACTION SEARCH: "Leo DiCaprio girlfriend" END
    RESULT: In 1999, DiCaprio met Brazilian model Gisele Bündchen, whom he dated until 2005.[316] He was romantically involved with Israeli model Bar Refaeli from 2005 to 2011. He later dated German fashion model Toni Garrn from 2013 to 2014 and later in 2017.[317] DiCaprio is in a relationship with American model and actress Camila Morrone from c. 2017.[318]
    ACTION STUDY: Camila Morrone is Leo DiCaprio's girlfriend.
    ACTION THINK: I need to find out Camila Morrone's age.
    ACTION SEARCH: "Camila Morrone age" END
    RESULT: Camila Rebeca Morrone Polak[3] (born June 16, 1997)[4] is an American model and actress. She is the daughter of actors Maximo Morrone and Lucila Polak; and was also raised by actor Al Pacino (who served as a parental figure during his long-term partnership with Polak).[5][6] She began her career as a model in the Victoria's Secret lookbook, and later walked the runway for Moschino.[7] 
    ACTION STUDY: 26 years
    ACTION THINK: I need to calculate 26 times 2.
    OBSERVATION: 52
    ACTION THINK: I now know the final answer.
    ACTION ANSWER: Camila Morrone is Leo DiCaprio's girlfriend and her current age times 2 is 52.
    
    ### Input:
    Let's think step by step. {prompt}
    """

def REACT(prompt: str) -> str:
    first_prompt = f"""{BASE(prompt)}

    ### Response:
    """

    cur_prompt = first_prompt
    while True:
        res = call_model_until_END(cur_prompt)
        action, meta = parse_last_action(res)

        if action == "ANSWER":
            return meta
        elif action == "SEARCH":
            docs: List[ProcessedData] = get_relevant_documents(meta)
            new_prompt = f"""{prompt}

            ### Response:
            {res}
            RESULT: {" ".join([doc.text for doc in docs])}
            """

            cur_prompt = new_prompt
        else:
            raise Exception("action not supported")

def get_END_tokens(text: str) -> int:
    # get the number of times " END" occurs in the text
    return text.lower().count(" END".lower())

def call_model_until_END(prompt: str) -> str:
    expected_num_END = get_END_tokens(prompt)
    cur_num_END = 0
    tokens = []
    for token in model.generate(prompt, streaming=True):
        if token == " END":
            if cur_num_END == expected_num_END:
                return ''.join(tokens)
            else:
                cur_num_END += 1
        tokens.append(token)

    raise Exception("end tokens didnt line up")

def parse_last_action(result: str):
    # get the last line of the result
    last_line = result.split("\n")[-1]

    # check if it is an action
    if last_line.startswith("ACTION"):
        # parse the action
        action = last_line.split("ACTION ")[1].split(":")[0]

        # if it is a search action, get the query
        if action == "SEARCH":
            query = last_line.split(": ")[1].split(" END")[0]
            return action, query
        
        # if it is a ANSWER action, get the answer
        elif action == "ANSWER":
            answer = last_line.split(": ")[1]
            return action, answer
        
        # otherwise, error
        else:
            raise Exception("action not supported")
        
    # otherwise, error
    else:
        raise Exception("last line not an action")