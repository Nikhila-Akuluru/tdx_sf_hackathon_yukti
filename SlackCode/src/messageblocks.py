feedback_citiation_block = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": ":+1:", "emoji": True},
                "value": "positive-feedback",
                "action_id": "positive-feedback",
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": ":-1:", "emoji": True},
                "value": "negative-feedback",
                "action_id": "negative-feedback",
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Show sources", "emoji": True},
                "value": "source",
                "action_id": "view-source",
            },
        ],
    }
]

user_acceptance_block = [
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": ":YES:"},
                "value": "positive-feedback",
                "action_id": "positive-feedback",
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "NO"},
                "value": "negative-feedback",
                "action_id": "negative-feedback",
            },
        ],
    }
]
