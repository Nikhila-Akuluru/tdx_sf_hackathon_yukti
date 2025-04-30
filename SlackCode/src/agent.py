import os

import requests


def salesforce_agent(data=None):
    url = "https://orgfarm-37428621d3.my.salesforce.com/services/apexrest/api/Slack"

    headers = {
        "Authorization": f"Bearer {os.environ.get("SALESFORCE_BEARER_TOKEN")}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()  # Assuming response is JSON
    except requests.exceptions.RequestException as e:
        print(f"SFDC API call failed: {e}")
        if e.response is not None:
            print("Response:", e.response.text)
        return None
