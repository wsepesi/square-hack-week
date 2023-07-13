import slack
import os
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

import os
from slack import RTMClient

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)


client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
# client.chat_postMessage(channel='#general', text="pineapples")

while True:
    result = client.conversations_history(channel="C05GJJJPA94", limit=1)
    msg = result['messages'][0]['text']
    if 'client_msg_id' in result['messages'][0]:
        client.chat_postMessage(channel='#general', text=msg + " ur mom")

