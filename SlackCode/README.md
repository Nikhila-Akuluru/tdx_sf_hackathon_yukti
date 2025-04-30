


# 🤖 Slack-Salesforce Agent Integration

This project bridges Slack and Salesforce by embedding **AgentForce** capabilities directly into your team’s daily workflow—**inside Slack**. Instead of toggling between tools, sales reps can now interact with Salesforce data and automations from the same place they collaborate every day.

## 🚀 Why This Matters

In modern sales environments, speed and focus are everything. By bringing the agent into Slack, we eliminate the need to switch between Salesforce and Slack, empowering reps to take action faster and stay in the flow of conversation.

## ⚙️ How It Works

- Slack messages trigger a `POST` request to the Salesforce REST endpoint
 
- This endpoint is powered by **AgentForce**, which processes the request and returns a dynamic response based on Salesforce logic.
- Authorization is handled via a **Bearer token**.


