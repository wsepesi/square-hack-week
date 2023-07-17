from inference_utils.type_utils import ProcessedData
from typing import List, Tuple
from vlite import VLite
from uuid import uuid4
from onboarding_utils.docs_parser.preprocessor import chunker
from onboarding_utils.slackparser.ledgertextscraper import get_slack_data

DB_PATH = "v1.npz" # specify your database path here. further functions either create or use this database
db = VLite(collection = DB_PATH)
DOCS_SOURCE = "Ledger/" # change to your data folder containing Google Docs exported as HTML files
SLACK_DATA_PATH = "ledger.txt" # change to your data folder containing Slack data exported as a text file


def ingest():
    chunked_data = chunker(DOCS_SOURCE)
    docs_data = process_docs_data(chunked_data)

    slack_chunked_data = get_slack_data(SLACK_DATA_PATH) # use get_slack_data_from_structured() if you have structured slack data
    slack_data = process_slack_data(slack_chunked_data)

    data = docs_data + slack_data
    print("ingesting data....")
    db.memorize(data)
    print("done")


def process_docs_data(chunked_data) -> List[ProcessedData]:
    docs_data: List[ProcessedData] = []
    for key in chunked_data:
        for item in chunked_data[key]:
            docs_data.append(ProcessedData(id = str(uuid4()), text = item, metadata = {"key": key}))
    return docs_data

def process_slack_data(slack_data) -> List[ProcessedData]:
    return [ProcessedData(id = str(uuid4()), text = item, metadata = {"key": "slack"}) for item in slack_data]


if __name__ == "__main__":
    ingest()