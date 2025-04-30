import datetime
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request
from slack_bolt import App
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter

import constants as constants
from src.agent import salesforce_agent
from src.messageblocks import user_acceptance_block

load_dotenv()

processed_message_ids = set()

user_question = ""
app = Flask(__name__, static_folder="assets")
app.secret_key = os.environ.get("SLACK_SIGNING_TOKEN")

slack_event_adapter = SlackEventAdapter(
    os.environ.get("SLACK_SIGNING_TOKEN"), "/slack/events", app
)
client = WebClient(token=os.environ.get("SLACK_TOKEN"))
BOT_ID = client.api_call("auth.test")["user_id"]

# processed_message_ids = set()
processed_reaction_ts = set()


@slack_event_adapter.on("message")
def message(payload):
    print(f"[{datetime.datetime.now()}] Message Payload\n", payload)

    event = payload.get("event", {})
    message_id = event.get("client_msg_id")

    if message_id not in processed_message_ids:
        processed_message_ids.add(message_id)
        channel_id = event.get("channel")
        user_id = event.get("user")
        event_ts = event.get("ts")

        # Ensure thread_ts exists; default to event_ts if it's a new message
        thread_ts = event.get("thread_ts") or event_ts

        if BOT_ID != user_id:
            try:
                query = event.get("text", "")

                # Add eyes reaction to indicate processing
                client.reactions_add(
                    channel=channel_id, name="eyes", timestamp=event_ts
                )

                # Fetch previous messages in the thread for conversation context
                conversation_history = []
                if thread_ts != event_ts:  # Check if it's a thread reply
                    response = client.conversations_replies(
                        channel=channel_id, ts=thread_ts
                    )
                    messages = response.get("messages", [])

                    conversation_history.extend(
                        [
                            {
                                "author": (
                                    "USER" if msg.get("user") == user_id else "GLEAN_AI"
                                ),
                                "messageType": "CONTENT",
                                "fragments": [{"text": msg["text"]}],
                            }
                            for msg in reversed(messages)
                            if "text" in msg
                        ]
                    )

                # Add the new user query to the history
                if thread_ts == event_ts:
                    conversation_history.append(
                        {
                            "author": "USER",
                            "messageType": "CONTENT",
                            "fragments": [{"text": query}],
                        }
                    )

                user_info = client.users_info(user=user_id)
                user_email = user_info["user"]["profile"].get(
                    "email", "ea.chatbot@zoominfo.com"
                )

                user_question = conversation_history

                message_blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": constants.REQEUST_CREATE_QUOTE,
                        },
                    },
                    *(user_acceptance_block),
                ]

                slack_answer = client.chat_postMessage(
                    channel=channel_id,
                    user=user_id,
                    text="",  # Required but acts as a fallback
                    blocks=message_blocks,
                    thread_ts=event.get("ts"),
                )

            except Exception as e:
                print(
                    f"[{datetime.datetime.now()}, Exception occurred while handling the message",
                    e,
                )
                client.chat_postEphemeral(
                    channel=channel_id,
                    user=user_id,
                    text=constants.EXCEPTION_MESSAGE,
                    thread_ts=event.get("ts"),
                )


@app.route("/slack/blockactions", methods=["POST"])
def handle_button_click():
    try:
        payload = request.form.to_dict()
        value = payload["payload"]
        payload = json.loads(value)

        print(f"[{datetime.datetime.now()}, Button action payload\n")
        print(payload)

        channel_id = payload["container"]["channel_id"]
        user_id = payload["user"]["id"]  # Get user ID to send ephemeral message
        thread_ts = payload["container"]["thread_ts"]
        actionID = payload["actions"][0]["action_id"]

        if actionID == "positive-feedback":

            client.chat_postMessage(
                channel=channel_id,
                user=user_id,  # Make message only visible to the user
                text="That's great! I'll share the quote with you in just a moment here",
                thread_ts=thread_ts,
            )
            agent_response = salesforce_agent(user_question)
            client.chat_postMessage(
                channel=channel_id,
                user=user_id,  # Make message only visible to the user
                text=agent_response,
                thread_ts=thread_ts,
            )

        elif actionID == "negative-feedback":

            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="Reachout us if anything else is required",
                thread_ts=thread_ts,
            )

        return "", 200

    except Exception as e:
        print(
            f"[{datetime.datetime.now()}, Exception occurred while handling the button",
            e,
        )

        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,  # Ensure only the user sees this error
            text=constants.EXCEPTION_MESSAGE,
            thread_ts=thread_ts,
        )
        return "", 500
