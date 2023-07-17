import slack
import dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from run_agent import run_agent

ENV_PATH = ".env"
EVENTS_PATH = "/slack/events"
CHANNEL_ID = dotenv.get_key(ENV_PATH, "CHANNEL_ID")
SLACK_TOKEN = dotenv.get_key(ENV_PATH, "SLACK_TOKEN")
SIGNING_SECRET = dotenv.get_key(ENV_PATH, "SIGNING_SECRET")

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, EVENTS_PATH, app)


client = slack.WebClient(token=SLACK_TOKEN)
# client.chat_postMessage(channel='#general', text="pineapples")

while True:
    result = client.conversations_history(channel=CHANNEL_ID, limit=1)
    msg = result['messages'][0]['text']
    if 'client_msg_id' in result['messages'][0]:
        res = run_agent()
        client.chat_postMessage(channel='#random', text=res)

