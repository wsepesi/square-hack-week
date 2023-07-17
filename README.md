# Square Scout

Supercharge your service's Slack channel with an AI-assistant. Field external and internal questions asynchronously with factually-grounded and thought-out responses building on your team's documentation and past Slack conversations, supported by entirely local privacy-first models.

## Getting Started

1. Set up your conda env using `env.yaml`
2. Either onboard your data using `ingest_data.py` (changing data directories to your own)
3. Run either `run_agent.py` or `run_slackbot.py` to conduct inference. Make sure to change your vector DB path and prompt in the scripts
   1. To run the Slackbot, fill out the requisite tokens in your .env file

## Credits

`/` @wsepesi \
`/experiments` @wsepesi \
`/inference_utils` @wsepesi \
`/onboarding_utils/docs_parser` @anthonyzhang-square \
`/onboarding_utils/slackparser` @rtsng \
`/slack_bot_utils` @jacob-tamor @reneenee03
