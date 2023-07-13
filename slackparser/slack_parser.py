import json

def parse_slack_message_file_ryan_new_version(file_path):
    with open(file_path, 'r') as file:
        json_data = file.read()
    

    def parse_json(data):
        superdata = []
        for item in data:
            try: 
                superdata.append({"text": item["text"], "user": item["user"], "timestamp": item["ts"], "client_msg_id": item["client_msg_id"]})
            except:
                continue
        
        return superdata
    
    data = json.loads(json_data)
    parsed_data = parse_json(data)
    return parsed_data
    # for item in parsed_data: print(item)


# def parse_slack_message_file(file_path):
#     # Read the JSON file
#     with open(file_path, 'r') as file:
#         json_data = file.read()
    
    
    
    

#     # Recursive function to parse nested structures
#     def parse_json(data):
#         if isinstance(data, dict):
#             for key, value in data.items():
#                 parsed_data[key] = parse_json(value)
#             return parsed_data
#         elif isinstance(data, list):
#             parsed_data = []
#             for item in data:
#                 parsed_data.append(parse_json(item))
#             return parsed_data
#         else:
#             return data

    
#     # Parse the JSON data
#     try:
#         data = json.loads(json_data)
#         parsed_data = parse_json(data)
#         print("here")
#     except json.JSONDecodeError as e:
#         print(f"Error parsing JSON: {e}")
#         return None

#     # Extract relevant information from the parsed data
#     messages = parsed_data.get('messages', [])
#     parsed_messages = []


#     for message in messages:
#         # Extract necessary fields from the message object
#         timestamp = message.get('ts', '')
#         user = message.get('user', '')
#         text = message.get('text', '')

#         # Perform additional processing or analysis on the extracted data

#         # Create a dictionary to represent the parsed message
#         parsed_message = {
#             'timestamp': timestamp,
#             'user': user,
#             'text': text
#         }

#         # Append the parsed message to the list
#         parsed_messages.append(parsed_message)

#     return parsed_messages

# # Example usage
# file_path = 'slackmessages2/2023-07-12_4.json'
# parsed_messages = parse_slack_message_file_ryan_new_version(file_path)
# if parsed_messages:
#     for message in parsed_messages:
#         print(message)