from slack_bubbler_upper import bubbler_upper
from slack_chunker import time_based_chunker
from slack_parser import parse_slack_message_file_ryan_new_version
import tiktoken

def tokenLength(input):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(input))

def get_slack_data():
    source_directory = 'slackmessages'
    destination_directory = 'slackmessages2'
    chunksize = 5


    json_files = bubbler_upper(source_directory, destination_directory)
    full_chunked_data = []

    for jfile in json_files:
        parsed_data = parse_slack_message_file_ryan_new_version("slackmessages2/" + jfile) #list of dict

        chunks = time_based_chunker(chunksize, parsed_data) #number + list of dict becomesm list of pair (list of dict, string)
        if len(chunks) == 0:
            continue
        full_chunked_data.append(chunks)

    return full_chunked_data

data = get_slack_data()

# print((data))
# print(len(data[0]))
# print((data[0][0]))
# print((data[0][0][1]))

for i in data:
    for a in i:
        print(tokenLength(a[1]), a[1])