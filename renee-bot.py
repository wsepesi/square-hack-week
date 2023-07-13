import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier
from slack_bolt import App

# Create an instance of the Slack app
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Create an event listener for incoming messages
@app.event("message")
def handle_message(event, say):
    try:
        # Check if the event is a user message and not from a bot or itself
        if (
            event["type"] == "message"
            and "bot_id" not in event
            and event["user"] != app.client.auth_test()["user_id"]
        ):
            # Reply to the message with "Hi"
            say("Hi")
    except SlackApiError as e:
        print(f"Error responding to message: {e.response['error']}")

# Verify the request signature for incoming events
def verify_signature():
    signing_secret = os.environ.get("SIGNING_SECRET")

    def verify_request(request, response, next):
        verifier = SignatureVerifier(signing_secret)
        verifier.is_valid_request(request)
        next()

    return verify_request

if __name__ == "__main__":
    # Start the app and listen for incoming events
    app.start(port=int(os.environ.get("PORT", 3000)))


# import slack
# import os
# from pathlib import Path 
# from dotenv import load_dotenv
# from flask import Flask
# from slackeventsapi import SlackEventAdapter

# import os
# from slack import RTMClient

# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)
# app = Flask(__name__)
# slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)


# client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
# client.chat_postMessage(channel='#general', text="pineapples")

# if __name__ == '__main__':
#     app.run(debug=True)

#     # @RTMClient.run_on(event="message")
#     # def say_hello(**payload):
#     #     data = payload['data']
#     #     web_client = payload['web_client']

#     #     if 'Hello' in data['text']:
#     #         channel_id = data['channel']
#     #         thread_ts = data['ts']
#     #         user = data['user'] # This is not username but user ID (the format is either U*** or W***)

#     #         web_client.chat_postMessage(
#     #         channel=channel_id,
#     #         text=f"Hi <@{user}>!",
#     #         thread_ts=thread_ts
#     #         )

#     # slack_token = os.environ["SLACK_API_TOKEN"]
#     # rtm_client = RTMClient(token=slack_token)
#     # rtm_client.start()
