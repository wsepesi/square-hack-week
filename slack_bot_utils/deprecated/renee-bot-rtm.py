import slack
import os
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask
import os
from slack import RTMClient

# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)
# app = Flask(__name__)
# slack_event_adapter = SlackEventAdapter(, '/slack/events', app)

# client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
# client.chat_postMessage(channel='#general', text="anthony zhang bang gang")

@RTMClient.run_on(event="message")
def say_hello(**payload):
    data = payload['data']
    web_client = payload['web_client']

    if 'Hello' in data['text']:
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user'] # This is not username but user ID (the format is either U*** or W***)

        web_client.chat_postMessage(
        channel=channel_id,
        text=f"Hi <@{user}>!",
        thread_ts=thread_ts
        )

slack_token = os.environ["SLACK_TOKEN"]
rtm_client = RTMClient(token=slack_token)
rtm_client.start()